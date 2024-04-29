from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from Register_Login.views import login_page
from Register_Login.models import CargoTeam
from . models import *
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os

# Create your views here.

@login_required(login_url='login_page')
def admin_dashboard(request):
    return render(request,'admin_dashboard.html')



# service section views
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
        messages.success(request,'Testimonial Added')
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
        messages.success(request,'Updated')
        return redirect('testimonial_section')
    else:
        return redirect('testimonial_section')


@login_required(login_url='login_page')
def testimonial_delete(request,pk):
    data=Testimonials.objects.get(id=pk,is_active=1)
    data.delete()
    messages.success(request,'Deleted')
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
        messages.success(request,'New Opening Added')
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
        messages.success(request,'Updated')
        return redirect('career_section')
    else:
        return redirect('career_section')


@login_required(login_url='login_page')
def opening_delete(request,pk):
    data=Currentopenings.objects.get(id=pk,is_active=1)
    data.delete()
    messages.success(request,'Deleted')
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


def view_resume(request, pk):
    
    job_application = get_object_or_404(JobApplications, id=pk)
    
    
    file_path = job_application.resume.name
    
   
    if default_storage.exists(file_path):
        
        with default_storage.open(file_path, 'rb') as resume_file:
            
            resume_content = resume_file.read()
        
        
        response = HttpResponse(resume_content, content_type='application/pdf')
        return response
    else:
        return HttpResponse("Resume not found.", status=404)


def download_resume(request, pk):
    job_application = get_object_or_404(JobApplications, id=pk)
    
    file_path = os.path.join(settings.MEDIA_ROOT, str(job_application.resume))
    
    with open(file_path, 'rb') as resume_file:
        response = HttpResponse(resume_file.read(), content_type='application/pdf')
        
        # Set the Content-Disposition header to force download with the original file name
        response['Content-Disposition'] = f'attachment; filename="{job_application.resume.name}"'
        
        return response


# cargo team section views

@login_required(login_url='login_page')
def cargo_team(request):
    return render(request,'cargo-team/cargo_team.html')


@login_required(login_url='login_page')
def login_requests(request):
    data = CargoTeam.objects.filter(admin_approval=0)
    context={
        'data':data
    }
    return render(request,'cargo-team/login_requests.html',context)

@login_required(login_url='login_page')
def accept_request(request,pk):
    data = CargoTeam.objects.get(id=pk)
    data.admin_approval=1
    data.save()
    messages.success(request,'Request approved')
    return redirect('login_requests')


@login_required(login_url='login_page')
def cancel_request(request,pk):
    data = CargoTeam.objects.get(id=pk)
    data.admin_approval=2
    data.save()
    messages.success(request,'Request rejected')
    return redirect('login_requests')


@login_required(login_url='login_page')
def approved_requests(request):
    data = CargoTeam.objects.filter(admin_approval=1)
    context={
        'data':data
    }
    return render(request,'cargo-team/approved_requests.html',context)

@login_required(login_url='login_page')
def rejected_requests(request):
    data = CargoTeam.objects.filter(admin_approval=2)
    context={
        'data':data
    }
    return render(request,'cargo-team/rejected_requests.html',context)


@login_required(login_url='login_page')
def member_details(request):
    return render(request,'cargo-team/member_details.html')


@login_required(login_url='login_page')
def team_members(request):
    data = CargoTeam.objects.filter(designation='Team Member',admin_approval=1)
    context={
        'data':data
    }
    return render(request,'cargo-team/team_members.html',context)

@login_required(login_url='login_page')
def executive_members(request):
    data = CargoTeam.objects.filter(designation='Executive Member',admin_approval=1)
    context={
        'data':data
    }
    return render(request,'cargo-team/executive_members.html',context)



# Service locations section views

@login_required(login_url='login_page')
def location_hub(request):
    all_country=Country.objects.all()
    all_state=State.objects.all()
    all_city=City.objects.all()
    all_location=ServiceLocation.objects.all()
    country=Country.objects.filter(is_active=True)
    state=State.objects.filter(is_active=True)
    city=City.objects.filter(is_active=True)
    context={
        'all_country':all_country,
        'all_state':all_state,
        'all_city':all_city,
        'all_location':all_location,
        'country':country,
        'state':state,
        'city':city,
    }

    return render(request,'locations/location_hub.html',context)

@login_required(login_url='login_page')
def add_country(request):
    if request.method == 'POST':
        country=request.POST.get('name')
        
        data=Country(
            name=country,
    
        )
        
        data.save()
        messages.success(request,'Country Added')
        return redirect('location_hub')
    else:
        return redirect('location_hub')


@login_required(login_url='login_page')
def add_state(request):
    if request.method == 'POST':
        state=request.POST.get('name')
        data=State(
            name=state,
        )
        
        data.save()
        messages.success(request,'State Added')
        return redirect('location_hub')
    else:
        return redirect('location_hub')


@login_required(login_url='login_page')
def add_city(request):
    if request.method == 'POST':
        city=request.POST.get('name')
        data=City(
            name=city,
        )
        
        data.save()
        messages.success(request,'City Added')
        return redirect('location_hub')
    else:
        return redirect('location_hub')


@login_required(login_url='login_page')
def add_location(request):
    if request.method == 'POST':
        country_id=request.POST.get('country')
        state_id=request.POST.get('state')
        city_id=request.POST.get('city')

        country=Country.objects.get(id=country_id)
        state=State.objects.get(id=state_id)
        city=City.objects.get(id=city_id)

        location=request.POST.get('name')
        pincode=request.POST.get('pincode')

        data=ServiceLocation(
            country=country,state=state,city=city,
            name=location,
            postal_code=pincode
        )
        
        data.save()
        messages.success(request,'Location Added')
        return redirect('location_hub')
    else:
        return redirect('location_hub')

@login_required(login_url='login_page')
def delete_country(request,pk):
       
    data=Country.objects.get(id=pk)
    data.delete()
    messages.success(request,'Country Deleted')
    return redirect('location_hub')
    

@login_required(login_url='login_page')
def delete_state(request,pk):
       
    data=State.objects.get(id=pk)
    data.delete()
    messages.success(request,'State Deleted')
    return redirect('location_hub')


@login_required(login_url='login_page')
def delete_city(request,pk):
       
    data=City.objects.get(id=pk)
    data.delete()
    messages.success(request,'City Deleted')
    return redirect('location_hub')

@login_required(login_url='login_page')
def delete_location(request,pk):
       
    data=ServiceLocation.objects.get(id=pk)
    data.delete()
    messages.success(request,'Location Deleted')
    return redirect('location_hub')


@login_required(login_url='login_page')
def active_country(request,pk):
       
    data=Country.objects.get(id=pk)
    data.is_active=1
    data.save()
    messages.success(request,'Active')
    return redirect('location_hub')

@login_required(login_url='login_page')
def inactive_country(request,pk):
       
    data=Country.objects.get(id=pk)
    data.is_active=0
    data.save()
    messages.success(request,'Inactive')
    return redirect('location_hub')

@login_required(login_url='login_page')
def active_state(request,pk):
       
    data=State.objects.get(id=pk)
    data.is_active=1
    data.save()
    messages.success(request,'Active')
    return redirect('location_hub')

@login_required(login_url='login_page')
def inactive_state(request,pk):
       
    data=State.objects.get(id=pk)
    data.is_active=0
    data.save()
    messages.success(request,'Inactive')
    return redirect('location_hub')