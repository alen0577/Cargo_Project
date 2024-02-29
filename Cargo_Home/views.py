from django.shortcuts import render

# Create your views here.

# Landing page of cargo
def cargo_home(request):
    return render(request, 'home/cargo_home.html')


# aboutus page of cargo
def aboutus(request):
    return render(request, 'aboutus/aboutus.html')