from django.urls import path
from . import views

app_name = 'stories'

urlpatterns = [
    # Story management
    path('', views.story_list, name='story_list'),
    path('create/', views.create_story, name='create_story'),
    path('<int:story_id>/', views.story_detail, name='story_detail'),
    path('<int:story_id>/branches/', views.story_branches, name='story_branches'),
    
    # Story nodes
    path('<int:story_id>/add_node/', views.add_story_node, name='add_story_node'),
    
    # AI assistance
    path('<int:story_id>/ai_suggestion/', views.get_ai_suggestion, name='get_ai_suggestion'),
    path('ai_suggestion/<int:prompt_id>/use/', views.use_ai_suggestion, name='use_ai_suggestion'),
    path('analyze_text/', views.analyze_text, name='analyze_text'),
    
    # Writing sessions
    path('<int:story_id>/join/', views.join_writing_session, name='join_writing_session'),
    path('<int:story_id>/leave/', views.leave_writing_session, name='leave_writing_session'),
    
    # Comments
    path('<int:story_id>/comment/', views.add_comment, name='add_comment'),
    
    # Story management
    path('manage/', views.story_management, name='story_management'),
    path('<int:story_id>/archive/', views.archive_story, name='archive_story'),
    path('<int:story_id>/unarchive/', views.unarchive_story, name='unarchive_story'),
    path('<int:story_id>/delete/', views.delete_story, name='delete_story'),
    path('<int:story_id>/transfer/', views.transfer_ownership, name='transfer_ownership'),
]
