from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django import forms

from payment.forms import ShippingForm
from payment.models import ShippingAddress

from django.db.models import Q
import json
from cart.cart import Cart

def product(request, pk):
    product=Product.objects.get(id=pk)
    return render(request, 'product.html',{'product':product})


def category(request,foo: str):
    foo=foo.replace('-',' ')

    #grab the category from the url
    try:
        category=Category.objects.get(name=foo)
        products=Product.objects.filter(category=category)
        return render(request, 'category.html',{'products':products, 'category':category})
    except:
        messages.success(request,('That category does not exist'))
        return redirect('home')




# Create your views here.
def home(request):
    products=Product.objects.all()
    return render(request, 'home.html',{'products':products})


def about(request):
    return render(request, 'about.html', {})    


def login_user(request):
    if request.method== 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user= authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            #Shopping cart stuff
            current_user=Profile.objects.get(user__id=request.user.id)
            #Get their saved cart from database
            saved_cart=current_user.old_cart

            #Convert database string to dictionary using JSON

            if saved_cart:
                converted_cart=json.loads(saved_cart)
                #Add loaded dictionary to our session
                #Get the cart
                cart=Cart(request)
                #Loop thru the cart and add the items from dictionary
                for key,value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)


            messages.success(request,("You have been logged in Succesfully ") )
            return redirect('home')

        else:
            messages.success(request, ("There was an error. Please try again! "))
            return redirect('login')
    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out"))
    return redirect('home')


def register_user(request):
    form= SignUpForm()
    if request.method=='POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']

            #login user
            user=authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have registered your Shinra Ban account, Please Fill Out Your User Info!!")
            return redirect('update_info')
        else:
            messages.success(request, 'Oops, There seems to be a problem with the username or password. Please try again!')
            return redirect('register')


    else:

        return render(request, 'register.html', {'form': form})


def update_user(request):
    if request.user.is_authenticated:
        current_user=User.objects.get(id=request.user.id)
        user_form=UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request,current_user)
            messages.success(request, 'Profile has been Updated!')
            return redirect('home')

        return render(request, 'update_user.html', {'user_form': user_form})  
    else:
        messages.success(request, 'You Must Be Logged In To Access This Page!')
        return redirect('home')


def category_summary(request):
    categories=Category.objects.all()

    return render (request, 'category_summary.html', {'categories': categories}) 


def update_password(request):
    if request.user.is_authenticated:
        current_user=request.user

        #Did they fill out the form
        if request.method=='POST':
            form=ChangePasswordForm(current_user, request.POST)

            if form.is_valid():
                form.save()
                messages.success(request,'Your password has been updated')
                login(request, current_user)
                return redirect('update_user')

            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')

        else:
            form= ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'form': form})

    else:
        messages.success(request, "You must be logged in to view that page")
        return redirect('home')


    return render(request, 'update_password.html', {})


def update_info(request):

    if request.user.is_authenticated:
        current_user=Profile.objects.get(user__id=request.user.id)

        #Getting current user shipping info
        shipping_user=ShippingAddress.objects.get(user__id=request.user.id)
        
        #User info form
        form=UserInfoForm(request.POST or None, instance=current_user)

        #Get user shipping deets form
        shipping_form=ShippingForm(request.POST or None, instance= shipping_user)

        if form.is_valid() or shipping_form.is_valid():
            form.save()

            messages.success(request, 'Your Info has been Updated!')
            return redirect('home')

        return render(request, 'update_info.html', {'form': form, 'shipping_form': shipping_form})  
    else:
        messages.success(request, 'You Must Be Logged In To Access This Page!')
        return redirect('home')



def search(request):
    #determine if they filled out the form
    if request.method=='POST':
        searched=request.POST['searched'] 

        #Query Products DB Model 
        searched= Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))

        if not searched:
            messages.success(request, 'This product does not Exist. Please search for a product in our Store!')
            return render(request, 'search.html', {})
        else:
             return render(request, 'search.html', {'searched':searched})

    else:
        return render(request, 'search.html', {})