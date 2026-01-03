from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.views import View
import razorpay
from django.http import JsonResponse
from .models import Product,Customer,Cart,Payment,OrderPlaced,Wishlist
from django.db.models import Q
from .forms import CustomerRegistrationForms,CustomerProfileForm
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.contrib.auth.decorators import login_required #for def
from django.utils.decorators import method_decorator #class


# Create your views here.
@login_required
def home(request):
    totalitem = 0
    wishlist = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishlist = len(Wishlist.objects.filter(user=request.user))
    return render(request, "app/home.html",locals())

@login_required
def about(request):
    totalitem = 0
    wishlist = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishlist = len(Wishlist.objects.filter(user=request.user))
    return render(request, "app/about.html",locals())

@login_required
def contact(request):
    totalitem = 0
    wishlist = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishlist = len(Wishlist.objects.filter(user=request.user))
    return render(request, "app/contact.html",locals())

@method_decorator(login_required,name="dispatch")
class CategoryView(View):
    def get(self,request,val): 
        totalitem = 0
        wishlist = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishlist = len(Wishlist.objects.filter(user=request.user))
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title').annotate(total=Count('title'))
        return render(request, "app/category.html",locals())

@method_decorator(login_required,name="dispatch")
class CategoryTitle(View):
    def get(self,request,val): 
        product = get_object_or_404(Product, title=val)
        related_products = Product.objects.filter(category=product.category)
        title = related_products.values('title')
        totalitem = len(Cart.objects.filter(user=request.user))
        wishlist = len(Wishlist.objects.filter(user=request.user))
        return render(request, "app/category.html",{
            "product": related_products,
            "title": title,
            "totalitem": totalitem,
            "wishlist": wishlist,
        })    

@method_decorator(login_required,name="dispatch")
class ProductDetails(View):
    def get(self,request,pk):
        product = get_object_or_404(Product, pk=pk)
        totalitem = len(Cart.objects.filter(user=request.user))
        wishlist_count = len(Wishlist.objects.filter(user=request.user))
        in_wishlist = Wishlist.objects.filter(product=product, user=request.user).exists()
        return render(
            request,
            "app/productdetail.html",
            {
                "product": product,
                "totalitem": totalitem,
                "wishlist": wishlist_count,
                "in_wishlist": in_wishlist,
            },
        )


class CustomerRegistrationView(View):
    def get(self, request):
        totalitem = 0
        wishlist = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishlist = len(Wishlist.objects.filter(user=request.user))
        form = CustomerRegistrationForms()
        return render(request, "app/customerregistration.html", {"form": form})
    def post(self, request):
        form = CustomerRegistrationForms(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! User registered successfully.")
            return redirect("login")  # Change to your desired success URL name
        else:
            messages.warning(request, "Invalid input data.")
        return render(request, "app/customerregistration.html", {"form": form})        

@method_decorator(login_required,name="dispatch")
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        totalitem = 0
        wishlist = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishlist = len(Wishlist.objects.filter(user=request.user))
        return render(request,"app/profile.html",locals())
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user 
            name = form.cleaned_data["name"]
            locality= form.cleaned_data["locality"]
            city = form.cleaned_data["city"]
            mobile = form.cleaned_data["mobile"]
            state = form.cleaned_data["state"]
            zipcode = form.cleaned_data["zipcode"]

            reg = Customer(user=user,name=name,locality=locality,city=city,mobile=mobile,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request, "Congratulations! Profile save successfully.")
        else:
            messages.warning(request, "invalid data.")
        return render(request,"app/profile.html",locals())
  
@login_required    
def address(request):
    add = Customer.objects.filter(user=request.user)
    totalitem = len(Cart.objects.filter(user=request.user))
    wishlist = len(Wishlist.objects.filter(user=request.user))
    return render(request, "app/address.html",locals())

@method_decorator(login_required,name="dispatch")
class UpdateAddress(View):
    def get(self,request,pk):
        add = Customer.objects.get(pk=pk)
        form =  CustomerProfileForm(instance=add)
        totalitem = 0
        wishlist = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishlist = len(Wishlist.objects.filter(user=request.user))
        return render(request,"app/updateaddress.html",locals())
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data["name"]
            add.locality = form.cleaned_data["locality"]
            add.city = form.cleaned_data["city"]
            add.mobile = form.cleaned_data["mobile"]
            add.state = form.cleaned_data["state"]
            add.zipcode = form.cleaned_data["zipcode"]
            add.save()
            messages.success(request,"Congratulation ! Profile Update Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return redirect("address")

@method_decorator(login_required,name="dispatch")        
class CustomLogoutView(auth_views.LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
    
@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get("prod_id")
    product = get_object_or_404(Product, id=product_id)
    Cart.objects.get_or_create(user=user, product=product)
    return redirect("/cart")

@login_required
def show_cart(request):
    user=request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount += value
    totalamount = amount + 40 if cart else 0
    totalitem = len(Cart.objects.filter(user=request.user))
    wishlist = len(Wishlist.objects.filter(user=request.user))
    return render(
        request,
        "app/addtocart.html",
        {
            "cart": cart,
            "amount": amount,
            "totalamount": totalamount,
            "totalitem": totalitem,
            "wishlist": wishlist,
        },
    )

@login_required
def plus_cart(request):
    if request.method == "GET":
        prod_id = request.GET["prod_id"]
        try:
            cart_item = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
            cart_item.quantity += 1
            cart_item.save()
        except Cart.DoesNotExist:
            return JsonResponse({"error": "Item not in cart"}, status=404)

        amount = sum(
            item.quantity * item.product.discounted_price
            for item in Cart.objects.filter(user=request.user)
        )
        totalamount = amount + 40 if amount else 0
        data = {
            "quantity": cart_item.quantity,
            "amount": amount,
            "totalamount": totalamount,
        }
        return JsonResponse(data)

@login_required
def minus_cart(request):
    if request.method == "GET":
        prod_id = request.GET["prod_id"]
        try:
            cart_item = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        except Cart.DoesNotExist:
            return JsonResponse({"error": "Item not in cart"}, status=404)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            quantity_value = cart_item.quantity
        else:
            quantity_value = 0
            cart_item.delete()

        amount = sum(
            item.quantity * item.product.discounted_price
            for item in Cart.objects.filter(user=request.user)
        )
        totalamount = amount + 40 if amount else 0
        data = {
            "quantity": quantity_value,
            "amount": amount,
            "totalamount": totalamount,
        }
        return JsonResponse(data)
    
@method_decorator(login_required,name="dispatch")    
class checkout(View):
    def get(self,request):
        user = request.user
        totalitem = len(Cart.objects.filter(user=user))
        wishlist = len(Wishlist.objects.filter(user=user))
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)

        famount = sum(
            item.quantity * item.product.discounted_price for item in cart_items
        )
        totalamount = famount + 40 if cart_items else 0

        payment = None
        order_id = None
        razoramount = None
        if settings.RAZOR_KEY_ID and settings.RAZOR_KEY_SECRET and cart_items:
            try:
                client = razorpay.Client(
                    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET)
                )
                data = {
                    "amount": int(totalamount * 100),
                    "currency": "INR",
                    "receipt": "order_rcptid_12",
                }
                payment_response = client.order.create(data=data)
                order_id = payment_response["id"]
                razoramount = payment_response["amount"]
                order_status = payment_response["status"]
                if order_status == "created":
                    payment = Payment.objects.create(
                        user=user,
                        amount=totalamount,
                        razorpay_order_id=order_id,
                        razorpay_payment_status=order_status,
                    )
            except Exception as exc:
                messages.error(request, f"Unable to start payment: {exc}")
        elif cart_items:
            messages.warning(
                request,
                "Payment keys are missing. Add Razorpay keys to enable checkout.",
            )

        return render(
            request,
            "app/checkout.html",
            {
                "add": add,
                "cart_items": cart_items,
                "totalamount": totalamount,
                "famount": famount,
                "totalitem": totalitem,
                "wishlist": wishlist,
                "payment": payment,
                "order_id": order_id,
                "razoramount": razoramount,
                "razor_key_id": settings.RAZOR_KEY_ID,
            },
        )

@csrf_exempt  # ✅ if this is called by Razorpay callback
@login_required
def payment_done(request):
    order_id = request.GET.get("order_id")
    payment_id = request.GET.get("payment_id")
    cust_id = request.GET.get("cust_id")

    customer = get_object_or_404(Customer, id=cust_id, user=request.user)
    payment = get_object_or_404(Payment, razorpay_order_id=order_id, user=request.user)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()

    cart_items = Cart.objects.filter(user=request.user)
    for cart_item in cart_items:
        OrderPlaced.objects.create(
            user=request.user,
            customer=customer,
            product=cart_item.product,
            quantity=cart_item.quantity,
            payment=payment,
        )
        cart_item.delete()

    return redirect("orders")

@login_required
def orders(request):
    totalitem = len(Cart.objects.filter(user=request.user))
    wishlist = len(Wishlist.objects.filter(user=request.user))
    order_Placed = OrderPlaced.objects.filter(user=request.user)
    return render(request,"app/order.html",locals())


@login_required
def remove_cart(request):
    if request.method == "GET":
        prod_id = request.GET["prod_id"]
        try:
            cart_item = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
            cart_item.delete()
        except Cart.DoesNotExist:
            return JsonResponse({"error": "Item not in cart"}, status=404)

        amount = sum(
            item.quantity * item.product.discounted_price
            for item in Cart.objects.filter(user=request.user)
        )
        totalamount = amount + 40 if amount else 0
        data={
            "amount": amount,
            "totalamount":totalamount
        }
        return JsonResponse(data)

@login_required
def show_wishlist(request):
    user=request.user
    totalitem = 0
    wishlist = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishlist = len(Wishlist.objects.filter(user=request.user))
    product = Wishlist.objects.filter(user=user)
    return render(request,"app/wishlist.html",locals())



@login_required
def add_wishlist(request):
    if request.method == "GET":
        prod_id = request.GET.get("prod_id")
        product = get_object_or_404(Product, id=prod_id)
        user = request.user

        obj, created = Wishlist.objects.get_or_create(user=user, product=product)
        if created:
            return JsonResponse({"message": "Wishlist Added Successfully"}, status=200)
        return JsonResponse({"message": "Already in Wishlist"}, status=200)


@login_required
def remove_wishlist(request):
    if request.method == "GET":
        prod_id = request.GET.get("prod_id")
        product = get_object_or_404(Product, id=prod_id)
        user = request.user

        deleted, _ = Wishlist.objects.filter(user=user, product=product).delete()
        if deleted:
            return JsonResponse({"message": "Wishlist Removed Successfully"}, status=200)
        return JsonResponse({"message": "Item not found in Wishlist"}, status=404)
    
@login_required  
def search(request):
    query = request.GET["search"]
    totalitem = 0
    wishlist = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishlist = len(Wishlist.objects.filter(user=request.user))
        products = Product.objects.filter(Q(title__icontains=query))
        return render(request,"app/search.html",locals())