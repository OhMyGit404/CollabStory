from django.contrib import admin
from .models import Story, StoryNode, Contribution, WritingSession, AIWritingPrompt, StoryBranch, StoryComment

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'genre', 'created_by', 'created_at', 'is_public', 'is_archived', 'word_count', 'is_completed']
    list_filter = ['genre', 'is_public', 'is_archived', 'is_completed', 'created_at']
    search_fields = ['title', 'initial_prompt', 'created_by__username']
    readonly_fields = ['created_at', 'updated_at', 'word_count', 'archived_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'genre', 'initial_prompt', 'cover_image', 'created_by')
        }),
        ('Settings', {
            'fields': ('is_public', 'max_contributors', 'is_completed')
        }),
        ('Archive Information', {
            'fields': ('is_archived', 'archived_at', 'archived_by', 'archive_reason'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('word_count', 'current_state'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(StoryNode)
class StoryNodeAdmin(admin.ModelAdmin):
    list_display = ['story', 'author', 'created_at', 'word_count', 'ai_generated', 'is_branch_point']
    list_filter = ['ai_generated', 'is_branch_point', 'created_at']
    search_fields = ['content', 'story__title', 'author__username']
    readonly_fields = ['created_at', 'word_count']

@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    list_display = ['user', 'story', 'nodes_created', 'words_contributed', 'last_contribution']
    list_filter = ['last_contribution', 'first_contribution']
    search_fields = ['user__username', 'story__title']

@admin.register(WritingSession)
class WritingSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'story', 'is_active', 'joined_at', 'last_activity']
    list_filter = ['is_active', 'joined_at']
    search_fields = ['user__username', 'story__title']

@admin.register(AIWritingPrompt)
class AIWritingPromptAdmin(admin.ModelAdmin):
    list_display = ['story', 'prompt_type', 'used', 'created_at']
    list_filter = ['prompt_type', 'used', 'created_at']
    search_fields = ['story__title', 'generated_text']

@admin.register(StoryBranch)
class StoryBranchAdmin(admin.ModelAdmin):
    list_display = ['story', 'branch_name', 'created_by', 'created_at', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['story__title', 'branch_name']

@admin.register(StoryComment)
class StoryCommentAdmin(admin.ModelAdmin):
    list_display = ['story', 'user', 'created_at', 'is_resolved']
    list_filter = ['is_resolved', 'created_at']
    search_fields = ['content', 'story__title', 'user__username']
