from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.db.models import Count, Q
from django.core.paginator import Paginator
from django.utils import timezone
import json
from .models import Story, StoryNode, WritingSession, AIWritingPrompt, Contribution, StoryComment
from .forms import StoryForm, StoryNodeForm, StoryCommentForm
from ai_assistant.ai_helpers import generate_ai_suggestion, analyze_writing_style

def story_list(request):
    """Display list of public stories"""
    stories = Story.objects.filter(is_public=True, is_archived=False).order_by('-created_at')
    
    # Filtering
    genre = request.GET.get('genre')
    if genre:
        stories = stories.filter(genre=genre)
    
    search = request.GET.get('search')
    if search:
        stories = stories.filter(
            Q(title__icontains=search) | 
            Q(initial_prompt__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(stories, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'genres': Story.GENRE_CHOICES,
        'current_genre': genre,
        'search_query': search,
    }
    return render(request, 'stories/story_list.html', context)

@login_required
def story_detail(request, story_id):
    """Display story detail and writing interface"""
    story = get_object_or_404(Story, id=story_id)
    nodes = story.nodes.all()
    
    # Get or create writing session
    writing_session, created = WritingSession.objects.get_or_create(
        story=story,
        user=request.user,
        defaults={'is_active': True}
    )
    
    # Get active writers
    active_writers = story.get_active_writers()
    
    # Get recent AI prompts
    recent_prompts = story.ai_prompts.filter(used=False)[:5]
    
    # Get story comments
    comments = story.comments.filter(is_resolved=False)[:10]
    
    context = {
        'story': story,
        'nodes': nodes,
        'writing_session': writing_session,
        'active_writers': active_writers,
        'recent_prompts': recent_prompts,
        'comments': comments,
        'node_form': StoryNodeForm(),
        'comment_form': StoryCommentForm(),
    }
    return render(request, 'stories/story_detail.html', context)

@login_required
def create_story(request):
    """Create a new story"""
    if request.method == 'POST':
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.created_by = request.user
            story.save()
            
            # Create initial contribution record
            Contribution.objects.create(
                user=request.user,
                story=story,
                nodes_created=0,
                words_contributed=0
            )
            
            messages.success(request, 'Story created successfully!')
            return redirect('stories:story_detail', story_id=story.id)
    else:
        form = StoryForm()
    
    return render(request, 'stories/create_story.html', {'form': form})

@login_required
@require_http_methods(["POST"])
def add_story_node(request, story_id):
    """Add a new node to the story"""
    story = get_object_or_404(Story, id=story_id)
    data = json.loads(request.body)
    
    content = data.get('content', '').strip()
    if not content:
        return JsonResponse({'success': False, 'error': 'Content cannot be empty'})
    
    parent_node = None
    if data.get('parent_node_id'):
        parent_node = get_object_or_404(StoryNode, id=data['parent_node_id'])
    
    # Create new node
    new_node = StoryNode.objects.create(
        story=story,
        content=content,
        author=request.user,
        parent_node=parent_node,
        ai_generated=data.get('ai_generated', False)
    )
    
    # Update or create contribution record
    contribution, created = Contribution.objects.get_or_create(
        user=request.user,
        story=story,
        defaults={'nodes_created': 0, 'words_contributed': 0}
    )
    contribution.nodes_created += 1
    contribution.words_contributed += new_node.word_count
    contribution.save()
    
    # Update writing session
    writing_session = WritingSession.objects.get(story=story, user=request.user, is_active=True)
    writing_session.current_node = new_node
    writing_session.save()
    
    # Update story current state
    story.current_state = content
    story.save(update_fields=['current_state'])
    
    return JsonResponse({
        'success': True,
        'node_id': new_node.id,
        'content': new_node.content,
        'author': new_node.author.username,
        'created_at': new_node.created_at.isoformat(),
        'word_count': new_node.word_count
    })

@login_required
def get_ai_suggestion(request, story_id):
    """Get AI writing suggestion"""
    story = get_object_or_404(Story, id=story_id)
    prompt_type = request.GET.get('type', 'continuation')
    
    # Get recent story content for context
    recent_nodes = story.nodes.order_by('-created_at')[:5]
    context = "\n".join([node.content for node in recent_nodes])
    
    if not context:
        context = story.initial_prompt
    
    suggestion = generate_ai_suggestion(context, prompt_type, story.genre)
    
    # Save the suggestion
    ai_prompt = AIWritingPrompt.objects.create(
        story=story,
        prompt_type=prompt_type,
        generated_text=suggestion,
        context=context
    )
    
    return JsonResponse({
        'suggestion': suggestion,
        'prompt_id': ai_prompt.id,
        'prompt_type': prompt_type
    })

@login_required
def use_ai_suggestion(request, prompt_id):
    """Mark an AI suggestion as used"""
    prompt = get_object_or_404(AIWritingPrompt, id=prompt_id)
    prompt.used = True
    prompt.used_at = timezone.now()
    prompt.save()
    
    return JsonResponse({'success': True})

@login_required
def analyze_text(request):
    """Analyze writing style of provided text"""
    if request.method == 'POST':
        data = json.loads(request.body)
        text = data.get('text', '')
        
        analysis = analyze_writing_style(text)
        return JsonResponse(analysis)
    
    return JsonResponse({'error': 'Invalid request method'})

@login_required
def add_comment(request, story_id):
    """Add a comment to a story"""
    story = get_object_or_404(Story, id=story_id)
    
    if request.method == 'POST':
        form = StoryCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.story = story
            comment.user = request.user
            comment.save()
            
            return JsonResponse({
                'success': True,
                'comment_id': comment.id,
                'content': comment.content,
                'author': comment.user.username,
                'created_at': comment.created_at.isoformat()
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid form data'})

@login_required
def join_writing_session(request, story_id):
    """Join a writing session for a story"""
    story = get_object_or_404(Story, id=story_id)
    
    if not story.is_public:
        return JsonResponse({'success': False, 'error': 'Story is not public'})
    
    # Check contributor limit
    if story.max_contributors and story.get_contributors().count() >= story.max_contributors:
        return JsonResponse({'success': False, 'error': 'Story has reached maximum contributors'})
    
    writing_session, created = WritingSession.objects.get_or_create(
        story=story,
        user=request.user,
        defaults={'is_active': True}
    )
    
    if not created:
        writing_session.is_active = True
        writing_session.save()
    
    return JsonResponse({'success': True, 'created': created})

@login_required
def leave_writing_session(request, story_id):
    """Leave a writing session"""
    story = get_object_or_404(Story, id=story_id)
    
    try:
        writing_session = WritingSession.objects.get(
            story=story,
            user=request.user,
            is_active=True
        )
        writing_session.is_active = False
        writing_session.save()
        
        return JsonResponse({'success': True})
    except WritingSession.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'No active writing session found'})

def story_branches(request, story_id):
    """Display story branches"""
    story = get_object_or_404(Story, id=story_id)
    branches = story.branches.filter(is_active=True)
    
    context = {
        'story': story,
        'branches': branches,
    }
    return render(request, 'stories/story_branches.html', context)

@login_required
def story_management(request):
    """Display user's story management page"""
    user_stories = Story.objects.filter(created_by=request.user).order_by('-created_at')
    
    # Pre-calculate permissions for each story
    stories_with_permissions = []
    for story in user_stories:
        story.can_delete = story.can_be_deleted_by(request.user)
        story.can_archive = story.can_be_archived_by(request.user)
        stories_with_permissions.append(story)
    
    context = {
        'user_stories': stories_with_permissions,
    }
    return render(request, 'stories/story_management.html', context)

@login_required
@require_http_methods(["POST"])
def archive_story(request, story_id):
    """Archive a story"""
    story = get_object_or_404(Story, id=story_id)
    
    if not story.can_be_archived_by(request.user):
        return JsonResponse({'success': False, 'error': 'You do not have permission to archive this story'})
    
    reason = request.POST.get('reason', '')
    if story.archive(request.user, reason):
        messages.success(request, f'Story "{story.title}" has been archived.')
        return JsonResponse({'success': True, 'message': 'Story archived successfully'})
    else:
        return JsonResponse({'success': False, 'error': 'Failed to archive story'})

@login_required
@require_http_methods(["POST"])
def unarchive_story(request, story_id):
    """Unarchive a story"""
    story = get_object_or_404(Story, id=story_id)
    
    if not story.can_be_archived_by(request.user):
        return JsonResponse({'success': False, 'error': 'You do not have permission to unarchive this story'})
    
    if story.unarchive(request.user):
        messages.success(request, f'Story "{story.title}" has been unarchived.')
        return JsonResponse({'success': True, 'message': 'Story unarchived successfully'})
    else:
        return JsonResponse({'success': False, 'error': 'Failed to unarchive story'})

@login_required
@require_http_methods(["POST"])
def delete_story(request, story_id):
    """Delete a story (only if no other contributors)"""
    story = get_object_or_404(Story, id=story_id)
    
    if not story.can_be_deleted_by(request.user):
        return JsonResponse({'success': False, 'error': 'You cannot delete this story. Either you are not the creator or other users have contributed to it.'})
    
    story_title = story.title
    story.delete()
    messages.success(request, f'Story "{story_title}" has been deleted.')
    return JsonResponse({'success': True, 'message': 'Story deleted successfully'})

@login_required
@require_http_methods(["POST"])
def transfer_ownership(request, story_id):
    """Transfer story ownership to another user"""
    story = get_object_or_404(Story, id=story_id)
    
    if story.created_by != request.user:
        return JsonResponse({'success': False, 'error': 'You can only transfer stories you created'})
    
    new_owner_username = request.POST.get('new_owner')
    if not new_owner_username:
        return JsonResponse({'success': False, 'error': 'New owner username is required'})
    
    try:
        from django.contrib.auth.models import User
        new_owner = User.objects.get(username=new_owner_username)
        story.created_by = new_owner
        story.save()
        messages.success(request, f'Story ownership transferred to {new_owner.username}')
        return JsonResponse({'success': True, 'message': f'Ownership transferred to {new_owner.username}'})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User not found'})
