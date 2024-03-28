from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from Register_Login.views import login_page
from . models import *

# Create your views here.

@login_required(login_url='login_page')
def admin_dashboard(request):
    return render(request,'admin_dashboard.html')

@login_required(login_url='login_page')
def testimonial_section(request):
    data=Testimonials.objects.filter(is_active=1)
    archive=Testimonials.objects.filter(is_active=0)
    context={
        'data':data,
        'archive':archive,
        }
    return render(request,'testimonial-sections/testimonial_section.html',context)


@login_required(login_url='login_page')
def testimonial_save(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        position=request.POST.get('position')
        content=request.POST.get('content')
        picture=request.POST.get('picture')
        
        data=Testimonials(client_name=name,position=position,content=content,image=picture)
        data.save()
        return redirect('testimonial_section')
    else:
        return redirect('testimonial_section')