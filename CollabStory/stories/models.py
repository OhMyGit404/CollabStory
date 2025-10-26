from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Story(models.Model):
    GENRE_CHOICES = [
        ('fantasy', 'Fantasy'),
        ('sci-fi', 'Science Fiction'),
        ('mystery', 'Mystery'),
        ('romance', 'Romance'),
        ('horror', 'Horror'),
        ('comedy', 'Comedy'),
        ('adventure', 'Adventure'),
        ('thriller', 'Thriller'),
        ('drama', 'Drama'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=100, choices=GENRE_CHOICES, default='other')
    initial_prompt = models.TextField(help_text="The starting prompt or premise for the story")
    cover_image = models.ImageField(upload_to='story_covers/', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_stories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=True)
    max_contributors = models.IntegerField(default=10)
    current_state = models.TextField(help_text="Latest story content", blank=True)
    is_completed = models.BooleanField(default=False)
    word_count = models.IntegerField(default=0)
    
    # Soft delete fields
    is_archived = models.BooleanField(default=False, help_text="Whether the story is archived (hidden from public)")
    archived_at = models.DateTimeField(null=True, blank=True, help_text="When the story was archived")
    archived_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='archived_stories', help_text="User who archived the story")
    archive_reason = models.CharField(max_length=200, blank=True, help_text="Reason for archiving")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Stories"
    
    def __str__(self):
        return self.title
    
    def get_contributors(self):
        """Get all users who have contributed to this story"""
        return User.objects.filter(
            story_nodes__story=self
        ).distinct()
    
    def get_active_writers(self):
        """Get users currently in writing sessions for this story"""
        return User.objects.filter(
            writing_sessions__story=self,
            writing_sessions__is_active=True
        ).distinct()
    
    def can_be_deleted_by(self, user):
        """Check if a user can delete this story"""
        # Only the creator can delete, and only if no other users have contributed
        if self.created_by != user:
            return False
        
        # Check if other users have contributed
        other_contributors = self.get_contributors().exclude(id=user.id)
        return not other_contributors.exists()
    
    def can_be_archived_by(self, user):
        """Check if a user can archive this story"""
        # Creator or admin can archive
        return self.created_by == user or user.is_staff
    
    def archive(self, user, reason=""):
        """Archive the story"""
        if self.can_be_archived_by(user):
            self.is_archived = True
            self.archived_at = timezone.now()
            self.archived_by = user
            self.archive_reason = reason
            self.save()
            return True
        return False
    
    def unarchive(self, user):
        """Unarchive the story"""
        if self.can_be_archived_by(user):
            self.is_archived = False
            self.archived_at = None
            self.archived_by = None
            self.archive_reason = ""
            self.save()
            return True
        return False

class StoryNode(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='nodes')
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='story_nodes')
    created_at = models.DateTimeField(auto_now_add=True)
    parent_node = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    order = models.IntegerField(default=0)
    ai_generated = models.BooleanField(default=False)
    word_count = models.IntegerField(default=0)
    is_branch_point = models.BooleanField(default=False, help_text="Whether this node allows for branching")
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.story.title} - Node {self.id}"
    
    def save(self, *args, **kwargs):
        # Calculate word count
        self.word_count = len(self.content.split())
        super().save(*args, **kwargs)
        
        # Update story word count
        self.story.word_count = sum(node.word_count for node in self.story.nodes.all())
        self.story.save(update_fields=['word_count'])

class Contribution(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contributions')
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='contributions')
    nodes_created = models.IntegerField(default=0)
    words_contributed = models.IntegerField(default=0)
    last_contribution = models.DateTimeField(auto_now=True)
    first_contribution = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'story']
    
    def __str__(self):
        return f"{self.user.username} - {self.story.title}"

class WritingSession(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='writing_sessions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='writing_sessions')
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    current_node = models.ForeignKey(StoryNode, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        unique_together = ['story', 'user']
    
    def __str__(self):
        return f"{self.user.username} writing {self.story.title}"

class AIWritingPrompt(models.Model):
    PROMPT_TYPE_CHOICES = [
        ('plot_twist', 'Plot Twist'),
        ('character', 'Character Development'),
        ('dialogue', 'Dialogue'),
        ('setting', 'Setting Description'),
        ('conflict', 'Conflict Generation'),
        ('continuation', 'Story Continuation'),
        ('description', 'Scene Description'),
    ]
    
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='ai_prompts')
    prompt_type = models.CharField(max_length=50, choices=PROMPT_TYPE_CHOICES)
    generated_text = models.TextField()
    used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    used_at = models.DateTimeField(null=True, blank=True)
    context = models.TextField(blank=True, help_text="The story context used to generate this prompt")
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.story.title} - {self.get_prompt_type_display()}"

class StoryBranch(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='branches')
    parent_node = models.ForeignKey(StoryNode, on_delete=models.CASCADE, related_name='branches')
    branch_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.story.title} - {self.branch_name}"

class StoryComment(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='comments')
    node = models.ForeignKey(StoryNode, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='story_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.story.title}"
