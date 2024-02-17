from django.shortcuts import render

# Create your views here.

# Landing page of cargo project
def cargo_home(request):
    return render(request, 'cargo_home.html')