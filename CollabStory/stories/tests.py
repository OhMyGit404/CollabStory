from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Story, StoryNode, Contribution
from django.utils import timezone


class StoryModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_story_creation(self):
        """Test that a story can be created"""
        story = Story.objects.create(
            title='Test Story',
            genre='fantasy',
            initial_prompt='Once upon a time...',
            created_by=self.user
        )
        self.assertEqual(story.title, 'Test Story')
        self.assertEqual(story.genre, 'fantasy')
        self.assertEqual(story.created_by, self.user)
        self.assertFalse(story.is_public)
        self.assertFalse(story.is_archived)
        
    def test_story_string_representation(self):
        """Test the string representation of Story"""
        story = Story.objects.create(
            title='Test Story',
            genre='fantasy',
            initial_prompt='Once upon a time...',
            created_by=self.user
        )
        self.assertEqual(str(story), 'Test Story')
        
    def test_story_node_creation(self):
        """Test that a story node can be created"""
        story = Story.objects.create(
            title='Test Story',
            genre='fantasy',
            initial_prompt='Once upon a time...',
            created_by=self.user
        )
        node = StoryNode.objects.create(
            story=story,
            content='This is a test node',
            author=self.user
        )
        self.assertEqual(node.story, story)
        self.assertEqual(node.content, 'This is a test node')
        self.assertEqual(node.author, self.user)


class StoryViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.story = Story.objects.create(
            title='Test Story',
            genre='fantasy',
            initial_prompt='Once upon a time...',
            created_by=self.user,
            is_public=True
        )
        
    def test_story_list_view(self):
        """Test that the story list view works"""
        response = self.client.get(reverse('stories:story_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Story')
        
    def test_story_detail_view(self):
        """Test that the story detail view works"""
        response = self.client.get(reverse('stories:story_detail', args=[self.story.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Story')
        
    def test_create_story_view_requires_login(self):
        """Test that creating a story requires login"""
        response = self.client.get(reverse('stories:create_story'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
    def test_create_story_view_with_login(self):
        """Test that creating a story works when logged in"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('stories:create_story'))
        self.assertEqual(response.status_code, 200)