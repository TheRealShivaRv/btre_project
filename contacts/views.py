from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contact
from django.core.mail import send_mail
def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        contact = Contact(listing_id=listing_id, listing=listing, name=name, email=email, phone=phone, message=message, user_id=user_id)

        if request.user.is_authenticated:
            has_enquired = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)
            if has_enquired:
                messages.error(request, 'You have already made this inquiry for this listing')
                return redirect('/listings/'+listing_id)

        contact.save()

        send_mail(
        'Property Listing Enquiry',
        'There has been an inquiry for ' + listing + 'Sign in to the admin panel for more info',
        'abc@abc.com',
        [realtor_email, 'xyz@xyz.com'],
        fail_silently=False,
        )

        messages.success(request, 'Your request has been submitted, a realtor will get in touch with you shortly')
        return redirect('/listings/'+listing_id)
# Create your views here.
