from django.shortcuts import render

def ai_dashboard(request):
    return render(request, 'ai_assistant/dashboard.html')
