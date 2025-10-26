from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from stories.models import Story, StoryNode, Contribution

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('stories:story_list')
    else:
        form = UserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    # Get user's stories
    user_stories = Story.objects.filter(created_by=request.user).order_by('-created_at')
    
    # Get user's contributions
    user_contributions = Contribution.objects.filter(user=request.user)
    total_words = user_contributions.aggregate(total_words=Sum('words_contributed'))['total_words'] or 0
    
    # Get recent story nodes
    recent_nodes = StoryNode.objects.filter(author=request.user).order_by('-created_at')
    
    context = {
        'user_stories': user_stories,
        'user_contributions': user_contributions,
        'total_words': total_words,
        'recent_nodes': recent_nodes,
    }
    
    return render(request, 'users/profile.html', context)
