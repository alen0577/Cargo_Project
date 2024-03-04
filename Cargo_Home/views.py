from django.shortcuts import render

# Create your views here.

# Landing page of cargo
def cargo_home(request):
    return render(request, 'home/cargo_home.html')


# aboutus page of cargo
def aboutus(request):
    return render(request, 'aboutus/aboutus.html')

# contactus page of cargo
def contactus(request):
    return render(request, 'contactus/contactus.html')


# service page of cargo
def services(request):
    return render(request, 'services/services.html')

# career page of cargo
def careers(request):
    return render(request, 'careers/careers.html')