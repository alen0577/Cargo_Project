from django.shortcuts import render,redirect
from Admin.models import *
from Customer.models import CustomerIssues
from Admin.models import ServiceLocation
from django.contrib import messages
from django.http import JsonResponse

# Create your views here.

# Landing page of cargo
def cargo_home(request):
    atestimonial = Testimonials.objects.filter(is_active=1).first()
    rtestimonials = Testimonials.objects.filter(is_active=True).exclude(id=atestimonial.id) if atestimonial else None


    context={
        'atestimonial': atestimonial,
        'rtestimonials': rtestimonials
    }
    return render(request, 'home/cargo_home.html',context)


# aboutus page of cargo
def aboutus(request):
    return render(request, 'aboutus/aboutus.html')

# contactus page of cargo
def contactus(request):
    return render(request, 'contactus/contactus.html')


def customer_issues(request):
    if request.method == 'POST':
        name=request.POST.get('fname')
        email=request.POST.get('email')
        number=request.POST.get('number')
        issue=request.POST.get('issue')
        data=CustomerIssues(full_name=name,email=email,contact_number=number,issues=issue)
        data.save()
        messages.success(request,'Issue reported, actions will take as soon...')
        return redirect('contactus')
    else:
        return redirect('contactus')



# service page of cargo
def services(request):
    services=Services.objects.filter(is_active=1)
    context={
        'services':services
    }
    return render(request, 'services/services.html', context)


# service page of cargo
def service_details(request,pk):
    service=Services.objects.get(id=pk,is_active=1)
    context={
        'service':service
    }
    return render(request, 'services/service_details.html', context)


# career page of cargo
def careers(request):
    openings=Currentopenings.objects.filter(is_active=1)
    context = {
        'openings':openings,
    }
    return render(request, 'careers/careers.html', context)

def job_apply(request):
    if request.method == "POST":
        job_id=request.POST.get('applied_for')
        applied_for=Currentopenings.objects.get(id=job_id)
        first_name=request.POST.get('fname')
        last_name=request.POST.get('lname')
        email=request.POST.get('email')
        contact_number=request.POST.get('number')
        resume=request.FILES.get('resume')

        if JobApplications.objects.filter(applied_for=applied_for,email=email).exists():
            messages.warning(request,'Already applied')
            return redirect('careers')
        else:
            application=JobApplications(applied_for=applied_for,first_name=first_name,last_name=last_name,email=email,contact_number=contact_number,resume=resume,)
            application.save()
            messages.success(request,'Job Applied')
            return redirect('careers')
    else:
         return redirect('careers')



# available locations page of cargo
def available_locations(request):
    return render(request, 'available locations/available_locations.html')

def check_service_availability(request):
    if request.method == 'POST':
        search_query = request.POST.get('query')
        if search_query.isdigit():
            locations = ServiceLocation.objects.filter(postal_code=search_query,is_active=True)
        else:
            locations = ServiceLocation.objects.filter(city__name__icontains=search_query,is_active=True)
        
        print(locations.values)
        if locations.exists():
            data = {
                'available': True,
                'count': locations.count(),
                'query': search_query,
                'locations': list(locations.values('city__name', 'postal_code', 'name')),
            }
        else:
            data = {
                'available': False,
                'message': 'Service not available in this location.',
            }
        return JsonResponse(data)
    return JsonResponse({'error': 'Invalid request'}, status=400)