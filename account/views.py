from django.shortcuts import render

# Create your views here.
def login_view(request):
    context = {}

    return render(request, 'account/login.html', context)

def register_view(request):
    context = {}

    return render(request, 'account/register.html', context)