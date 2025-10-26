from django import forms
from .models import Story, StoryNode, StoryComment

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['title', 'genre', 'initial_prompt', 'cover_image', 'is_public', 'max_contributors']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter story title...'
            }),
            'genre': forms.Select(attrs={
                'class': 'form-select'
            }),
            'initial_prompt': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write the initial prompt or premise for your story...'
            }),
            'cover_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'is_public': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'max_contributors': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 50
            })
        }
        labels = {
            'initial_prompt': 'Story Premise',
            'is_public': 'Make this story public',
            'max_contributors': 'Maximum Contributors'
        }

class StoryNodeForm(forms.ModelForm):
    class Meta:
        model = StoryNode
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Continue the story...',
                'id': 'node-content'
            })
        }
        labels = {
            'content': ''
        }

class StoryCommentForm(forms.ModelForm):
    class Meta:
        model = StoryComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Add a comment...'
            })
        }
        labels = {
            'content': ''
        }
