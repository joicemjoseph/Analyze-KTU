from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings

def home(request):
    """
    Home View
    """
    
    return render(request, 'index.html', {})
def about(request):
	"""
	About View
	"""
	return render(request, 'about.html', {'developers':settings.DEVELOPERS})

@login_required
def dashboard(request):
    """
    Dashboard View
    """
    return render(request, 'dashboard.html', {})
