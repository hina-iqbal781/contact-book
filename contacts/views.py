from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Contact
from .forms import ContactForm


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('signup')

        user = User.objects.create_user(
            username=username,
            password=password
        )

        login(request, user)
        return redirect('listing')

    return render(request, 'contacts/signup.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('listing')
        else:
            messages.error(request, 'Invalid username or password!')
            return redirect('login')

    return render(request, 'contacts/login.html')


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def contact_list(request):
    contacts = Contact.objects.all()

    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Contact added successfully!')
            return redirect('listing')
    else:
        form = ContactForm()

    return render(request, 'contacts/contact_list.html', {
        'contacts': contacts,
        'form': form
    })


@login_required
def listing(request):
    query = request.GET.get('q', '')

    if query:
        contacts = Contact.objects.filter(
            name__icontains=query
        ) | Contact.objects.filter(
            phone__icontains=query
        ) | Contact.objects.filter(
            email__icontains=query
        )
    else:
        contacts = Contact.objects.all()

    return render(request, 'contacts/listing.html', {
        'contacts': contacts,
        'query': query
    })


@login_required
def delete_contact(request, id):
    contact = get_object_or_404(Contact, id=id)
    contact.delete()

    messages.success(request, 'Contact deleted successfully!')

    return redirect('listing')


@login_required
def edit_contact(request, id):
    contact = get_object_or_404(Contact, id=id)

    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)

        if form.is_valid():
            form.save()

            messages.success(request, 'Contact updated successfully!')

            return redirect('listing')
    else:
        form = ContactForm(instance=contact)

    return render(request, 'contacts/edit_contact.html', {
        'form': form,
        'contact': contact
    })


@login_required
def contact_detail(request, id):
    contact = get_object_or_404(Contact, id=id)

    return render(request, 'contacts/contact_detail.html', {
        'contact': contact
    })
