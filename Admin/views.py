from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from Register_Login.views import login_page
from . models import *
from django.contrib import messages

# Create your views here.

@login_required(login_url='login_page')
def admin_dashboard(request):
    return render(request,'admin_dashboard.html')



# Testimonial section views
@login_required(login_url='login_page')
def service_section(request):
    data=Services.objects.filter(is_active=1)
    archive=Services.objects.filter(is_active=0)
    context={
        'data':data,
        'archive':archive,
    }
    return render(request,'service-sections/service_section.html',context)


@login_required(login_url='login_page')
def service_save(request):
    if request.method == 'POST':
        title=request.POST.get('title')
        description=request.POST.get('description')
        image=request.FILES.get('picture')
        
        data=Services(title=title,description=description,image=image)
        data.save()
        messages.success(request,'Service Added')
        return redirect('service_section')
    else:
        return redirect('service_section')


@login_required(login_url='login_page')
def service_edit(request,pk):
    data=Services.objects.get(id=pk,is_active=1)
    if request.method == 'POST':
        img=request.FILES.get('image')
        data.title=request.POST.get('title')
        data.description=request.POST.get('description')
        if img:
            data.image=img
       
        data.save()
        messages.success(request,'Updated')
        return redirect('service_section')
    else:
        return redirect('service_section')


@login_required(login_url='login_page')
def service_delete(request,pk):
    data=Services.objects.get(id=pk,is_active=1)
    data.delete()
    messages.success(request,'Deleted')
    return redirect('service_section')

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
    data=Currentopenings.objects.filter(is_active=1)
    context={
        'data':data,

    }
    return render(request,'career-sections/career_section.html', context)


@login_required(login_url='login_page')
def current_opening_save(request):
    if request.method == 'POST':
        job_title=request.POST.get('title')
        job_location=request.POST.get('location')
        job_type=request.POST.get('type')
        experience=request.POST.get('experience')
        responsibilities=request.POST.get('responsibilities')
        requirements=request.POST.get('requirements')
        apply_email=request.POST.get('email')
       
        data=Currentopenings(
            job_title=job_title,job_location=job_location,job_type=job_type,
            experience=experience,responsibilities=responsibilities,requirements=requirements,
            apply_email=apply_email
        )
        
        data.save()
        return redirect('career_section')
    else:
        return redirect('career_section')


@login_required(login_url='login_page')
def opening_edit(request,pk):
    data=Currentopenings.objects.get(id=pk,is_active=1)
    if request.method == 'POST':
        data.job_title=request.POST.get('title')
        data.job_location=request.POST.get('location')
        data.job_type=request.POST.get('type')
        data.experience=request.POST.get('experience')
        data.responsibilities=request.POST.get('responsibilities')
        data.requirements=request.POST.get('requirements')
        data.apply_email=request.POST.get('email')
       
        data.save()
        return redirect('career_section')
    else:
        return redirect('career_section')


@login_required(login_url='login_page')
def opening_delete(request,pk):
    data=Currentopenings.objects.get(id=pk,is_active=1)
    data.delete()
    return redirect('career_section')



@login_required(login_url='login_page')
def application_lists(request,pk):
    job_opening=Currentopenings.objects.get(id=pk,is_active=1)
    applications=JobApplications.objects.filter(applied_for=job_opening).order_by('date','time')
    context={
        'job_opening':job_opening,
        'applications':applications

    }
    return render(request,'career-sections/application_lists.html', context)