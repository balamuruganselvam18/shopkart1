from django.shortcuts import render ,redirect
from .models import *
from django.contrib import messages
import json
from django.http import  JsonResponse
from .form import CustomUserForm
from django.contrib.auth import authenticate,login,logout
# from .models import payment

# Create your views here.
def home(request):
  products=Product.objects.filter(trending=1)
  return render(request,"home.html",{"products":products})
 
def favviewpage(request):
  if request.user.is_authenticated:
    fav=Favourite.objects.filter(user=request.user)
    return render(request,"fav.html",{"fav":fav})
  else:
    return redirect("/")
 
def remove_fav(request,fid):
  item=Favourite.objects.get(id=fid)
  item.delete()
  return redirect("/favviewpage")
 
 
 
 
def cart_page(request):
  if request.user.is_authenticated:
    cart=Cart.objects.filter(user=request.user)
    return render(request,"cart.html",{"cart":cart})
  else:
    return redirect("/")
 
def remove_cart(request,cid):
  cartitem=Cart.objects.get(id=cid)
  cartitem.delete()
  return redirect("/cart")
 
 
 
def fav_page(request):
   if request.headers.get('x-requested-with')=='XMLHttpRequest':
    if request.user.is_authenticated:
      data=json.load(request)
      product_id=data['pid']
      product_status=Product.objects.get(id=product_id)
      if product_status:
         if Favourite.objects.filter(user=request.user.id,product_id=product_id):
          return JsonResponse({'status':'Product Already in Favourite'}, status=200)
         else:
          Favourite.objects.create(user=request.user,product_id=product_id)
          return JsonResponse({'status':'Product Added to Favourite'}, status=200)
    else:
      return JsonResponse({'status':'Login to Add Favourite'}, status=200)
   else:
    return JsonResponse({'status':'Invalid Access'}, status=200)
 
 
def add_to_cart(request):
   if request.headers.get('x-requested-with')=='XMLHttpRequest':
    if request.user.is_authenticated:
      data=json.load(request)
      product_qty=data['product_qty']
      product_id=data['pid']
      #print(request.user.id)
      product_status=Product.objects.get(id=product_id)
      if product_status:
        if Cart.objects.filter(user=request.user.id,product_id=product_id):
          return JsonResponse({'status':'Product Already in Cart'}, status=200)
        else:
          if product_status.quantity>=product_qty:
            Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
            return JsonResponse({'status':'Product Added to Cart'}, status=200)
          else:
            return JsonResponse({'status':'Product Stock Not Available'}, status=200)
    else:
      return JsonResponse({'status':'Login to Add Cart'}, status=200)
   else:
    return JsonResponse({'status':'Invalid Access'}, status=200)


 
def logout_page(request):
  if request.user.is_authenticated:
    logout(request)
    messages.success(request,"Logged out Successfully")
  return redirect("/")
 
 
def login_page(request):
  if request.user.is_authenticated:
    return redirect("/")
  else:
    if request.method=='POST':
      name=request.POST.get('username')
      pwd=request.POST.get('password')
      user=authenticate(request,username=name,password=pwd)
      if user is not None:
        login(request,user)
        messages.success(request,"Logged in Successfully")
        return redirect("/")
      else:
        messages.error(request,"Invalid User Name or Password")
        return redirect("/login")
    return render(request,"login.html")

def register(request):
  form=CustomUserForm()
  if request.method=='POST':
    form=CustomUserForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request,"Registration Success You can Login Now..!")
      return redirect('/login')
  return render(request,"register.html",{'form':form})
     

def collections(request):
    key=catagory.objects.filter(status=0)
    return render(request,'collections.html',{"catagory":key})


def collectionsview(request,name):
  if(catagory.objects.filter(name=name,status=0)):
      products=Product.objects.filter(catagory__name=name)
      return render(request,"index.html",{"products":products,"catagory_name":name})
  else:
    messages.warning(request,"No Such Catagory Found")
    return redirect('collections')
  

def product_details(request,cname,pname):
    if(catagory.objects.filter(name=cname,status=0)):
      if(Product.objects.filter(name=pname,status=0)):
        products=Product.objects.filter(name=pname,status=0).first()
        return render(request,"product_details.html",{"products":products})
      else:
        messages.error(request,"No Such Produtct Found")
        return redirect('collections')
    else:
      messages.error(request,"No Such Catagory Found")
      return redirect('collections')
   




def payment_success(request):
    return render(request, 'payment_success.html')




from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .form import PaymentForm  # Ensure you have the correct import
from django.urls import reverse

def payment_page(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Process payment here (dummy implementation)
            payment_method = form.cleaned_data['payment_method']
            if payment_method == 'ATM':
                card_number = form.cleaned_data['card_number']
                expiry_date = form.cleaned_data['expiry_date']
                cvv = form.cleaned_data['cvv']
                # Process card payment (add your payment processing logic here)
            if payment_method == 'UPI':
                upi_id = form.cleaned_data['upi_id']
                # Process UPI payment (add your payment processing logic here)
            
            # Send email after successful payment
            try:
                send_mail(
                    'Payment Confirmation',
                    'Hi Bala, your payment of ₹621 has been successfully processed.',
                    'your_email@gmail.com',  # From email
                    [request.user.email],    # To email (assuming user is logged in)
                    fail_silently=False,  # Change to False to see errors
                )
                print("Email sent successfully")
            except Exception as e:
                # Log the error or print it for debugging
                print(f"Failed to send email: {e}")
            
            return redirect(reverse('payment_success'))
    else:
        form = PaymentForm()
    
    return render(request, 'payment_page.html', {'form': form})

def payment_success(request):
    return render(request, 'payment_success.html')





# views.py

# from django.core.mail import send_mail
# from django.http import HttpResponseRedirect
# from django.shortcuts import render
# from .form import PaymentForm

# def payment_page(request):
#     if request.method == 'POST':
#         form = PaymentForm(request.POST)
#         if form.is_valid():
#             # Extract email and other information
#             email = form.cleaned_data['email']
#             payment_method = form.cleaned_data['payment_method']
#             card_number = form.cleaned_data['card_number']
#             expiry_date = form.cleaned_data['expiry_date']
#             cvv = form.cleaned_data['cvv']
#             upi_id = form.cleaned_data['upi_id']
            
#             # Send confirmation email
#             subject = 'Payment Confirmation'
#             message = 'Thank you for your payment. Your transaction was successful.'
#             from_email = 'balamuruganselvam78@gmail.com'
#             recipient_list = [email]
            
#             send_mail(subject, message, from_email, recipient_list)
            
#             return HttpResponseRedirect('/payment_success/')  # Redirect to success page

#     else:
#         form = PaymentForm()
    
#     return render(request, 'payment_page.html', {'form': form})

