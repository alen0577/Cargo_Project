from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from Register_Login.views import login_page
from . models import *

# Create your views here.

@login_required(login_url='login_page')
def admin_dashboard(request):
    return render(request,'admin_dashboard.html')

# Testimonial section views
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
        picture=request.FILES.get('picture')
        
        data=Testimonials(client_name=name,position=position,content=content,image=picture)
        data.save()
        return redirect('testimonial_section')
    else:
        return redirect('testimonial_section')


@login_required(login_url='login_page')
def testimonial_edit(request,pk):
    data=Testimonials.objects.get(id=pk,is_active=1)
    if request.method == 'POST':
        img=request.FILES.get('image')
        data.client_name=request.POST.get('name')
        data.position=request.POST.get('position')
        data.content=request.POST.get('content')
        if img:
            data.image=img
        print(img)
        data.save()
        return redirect('testimonial_section')
    else:
        return redirect('testimonial_section')


@login_required(login_url='login_page')
def testimonial_delete(request,pk):
    data=Testimonials.objects.get(id=pk,is_active=1)
    data.delete()
    return redirect('testimonial_section')



# career section views
@login_required(login_url='login_page')
def career_section(request):
    # data=Testimonials.objects.filter(is_active=1)
    # archive=Testimonials.objects.filter(is_active=0)
    # context={
    #     'data':data,
    #     'archive':archive,
    # }
    return render(request,'career-sections/career_section.html',)

