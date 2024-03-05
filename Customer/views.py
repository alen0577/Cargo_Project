from django.shortcuts import render

# Create your views here.


# booking request page
def booking_request(request):
    return render(request, 'booking_request.html')