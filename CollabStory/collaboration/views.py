from django.shortcuts import render

def collaboration_home(request):
    return render(request, 'collaboration/home.html')
