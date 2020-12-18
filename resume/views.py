from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def dashboard_view(request):
    context = {}

    return render(request, 'resume/dashboard.html', context)

@login_required(login_url='login')
def create_view(request):
    context = {}

    return render(request, 'resume/create.html', context)