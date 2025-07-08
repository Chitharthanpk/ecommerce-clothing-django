from django.shortcuts import render , redirect
from uwapp.models import CartOrder, CartOrderItems, Category, productimage, Product, Address
from userauth.models import User
from django.http import JsonResponse
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import razorpay
from django.core.mail import send_mail
from django.http import HttpResponseBadRequest
from django.contrib import messages

def index(request): 
    products= Product.objects.filter(featured=True,product_status="published")
    context = {
        "products":products
    }
    if request.method == 'POST':
        name = request.POST.get('name', '') 
        review_text = request.POST.get('review_text', '')  
        email = request.POST.get('email', '') 
        subject = 'New Review Submitted'
        message = f'Name: {name}\nReview: {review_text}'
        from_email = {email}  
        recipient_list = ['sidhupkc@gmail.com']  
        send_mail(subject, message, from_email, recipient_list)
        messages.info(request, 'sent ! Thank you for your Review')
        return redirect('uwapp:index')

        
    return render(request,'uwapp/index.html',context)

def product(request):
    product = Product.objects.filter(product_status="published")
    context = {
        "products":product
    }
    return render(request,'uwapp/product.html',context)

def category(request):
    categories = Category.objects.all()  
    context = {
        "categories":categories
    }
    return render(request,'uwapp/category.html',context)

def category_product(request, cid):
    category = Category.objects.get(cid=cid)
    product = Product.objects.filter(product_status="published",category=category)
    context = {
        "category":category,
        "product":product
    }
    return render(request ,'uwapp/category-product.html',context )

def details(request,Pid , ): 
    product = Product.objects.get(Pid=Pid)
    p_image= product.p_images.all()
    context={
        "p":product,
        "p_image":p_image,

    }
    return render(request,'uwapp/productpage.html',context)

@login_required
def account(request):
    account = request.user
    existing_address = Address.objects.filter(user=request.user).first()
    existing_phone = existing_address.phone_num if existing_address else None
    
    if request.method == "POST":
        new_address_text = request.POST.get("address")
        new_phone_text = request.POST.get("phone")
        if existing_address:
            existing_address.Address = new_address_text
            existing_address.phone_num = new_phone_text
            existing_address.save()
        else:
            existing_address = Address(user=request.user, Address=new_address_text, phone_num=new_phone_text)
            existing_address.save()

    # You should refresh the existing_address after the update.
    existing_address = Address.objects.filter(user=request.user).first()

    context = {
        "account": account,
        "existing_address": existing_address,
        "existing_phone": existing_address.phone_num if existing_address else None,
    }
    return render(request, 'uwapp/account.html', context)


def add_to_cart(request):
    product_id = request.GET.get('id')
    product_name = request.GET.get('name')
    product_qty = request.GET.get('qty')
    product_price = request.GET.get('price')
    product_size = request.GET.get('size')
    product_image = request.GET.get('image')

    if not all([product_id, product_name, product_qty, product_price, product_size]):
        return JsonResponse({"error": "Invalid request parameters"})

    cart_data_obj = request.session.get('cart_data_obj', {})

    # Create a unique identifier for the product based on ID and size
    cart_product_id = f"{product_id}_{product_size}"

    if cart_product_id in cart_data_obj:
        # Product with the same ID and size is already in the cart
        existing_qty = cart_data_obj[cart_product_id]['qty']
        cart_data_obj[cart_product_id]['qty'] = existing_qty + int(product_qty)
    else:
        # Product with the given ID and size is not in the cart, so add it
        cart_product = {
            'name': product_name,
            'qty': int(product_qty),
            'price': float(product_price),
            'size': product_size,
            'pid': product_id,
            'image': product_image,
        }
        cart_data_obj[cart_product_id] = cart_product

    request.session['cart_data_obj'] = cart_data_obj

    response_data = {
        "data": request.session['cart_data_obj'],
        'totalcartitems': len(request.session['cart_data_obj']),
    }
    return JsonResponse(response_data)

    

def cart(request):
    cart_total_amount = 0
    cart_data_obj = request.session.get('cart_data_obj', {})  
    if cart_data_obj:
        for p_id, item in cart_data_obj.items():
            qty = int(item['qty'])
            price = float(item['price'])
            cart_total_amount += qty * price
            
        return render(request, 'uwapp/cart.html', {
            "cart_data": cart_data_obj,
            'totalcartitems': len(cart_data_obj),
            'cart_total_amount': cart_total_amount
        })
    else:
        messages.warning(request, "Your cart is empty")
        return redirect('uwapp:index')
    
def delete_item_from_cart(request):
    product_id = str(request.GET.get('id'))  
    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']
        
        if product_id in cart_data:
            del cart_data[product_id]
            request.session['cart_data_obj'] = cart_data  
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            qty = int(item['qty'])
            price = float(item['price'])
            cart_total_amount += qty * price
    context = {
        "cart_data": request.session.get('cart_data_obj', {}), 
        'totalcartitems': len(request.session.get('cart_data_obj', {})),  
        'cart_total_amount': cart_total_amount,
    }
    rendered_html = render_to_string("core/async/cart-list.html", context)
    return JsonResponse({"data": rendered_html, 'totalcartitems': len(request.session.get('cart_data_obj', {}))})

    
def orders(request):
    orders = CartOrder.objects.filter(user=request.user)
    context = {
        "orders":orders,
    }
    return render(request,'uwapp/orders.html',context)



razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
@login_required
def checkout(request):
    cart_total_amount = 0
    total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            qty = int(item['qty'])
            price = float(item['price'])
            total_amount += qty * price
        user = request.user  
        mail = request.user.email

        # user_address = Address.objects.get(user=user)

        try:
            user_address = Address.objects.get(user=user)
        except Address.DoesNotExist:
            # messages.error(request, "No address found. Please update your address in your account before checkout.")
            return redirect("uwapp:account")
        
        user_phone_number = user_address.phone_num if user_address else None
        address=user_address.Address
        Phone=user_address.phone_num if user_address else None,

        order = CartOrder.objects.create(
            user=user,
            price=total_amount,
            mail=mail,
            Address=address,
            Phone=user_address.phone_num if user_address else None,
            order_identifier=''
        )
        for p_id, item in request.session['cart_data_obj'].items():
            qty = int(item['qty'])
            price = float(item['price'])
            cart_total_amount += qty * price
            cart_order_products = CartOrderItems.objects.create(
                order=order,
                invoice_no="invoice_no-" + str(order.id),
                item=item['name'],
                image=item['image'],
                qty=qty,
                price=price,
                total=qty * price,
                size=item.get('size', ''),
                order_identifier='',
            )
        amount = int(cart_total_amount * 100)
        data = {
            'amount': amount,
            'currency': 'INR',
            'payment_capture': 1,
        }
        razorpay_order = razorpay_client.order.create(data=data)
        razorpay_order_id = razorpay_order['id']
        order.order_identifier = razorpay_order_id
        order.save()
        for cart_order_item in CartOrderItems.objects.filter(order=order):
            cart_order_item.order_identifier = razorpay_order_id
            cart_order_item.save()

        return render(request, 'uwapp/checkout.html', {
            "cart_data": request.session['cart_data_obj'],
            'totalcartitems': len(request.session['cart_data_obj']),
            'cart_total_amount': cart_total_amount,
            'AMOUNT': amount,
            'razorpay_order_id': razorpay_order_id,
            'username': request.user.username,
            'email': request.user.email,
            'id': razorpay_order_id,
            'order': razorpay_order,'phone':user_phone_number,'address':address,
        })
    else:
        return redirect('cart_empty_page')





@csrf_exempt
@login_required
def payment_completed(request):
    if request.method == 'POST':
        try:
            payment_id = request.POST.get('razorpay_payment_id')
            payment_signature = request.POST.get('razorpay_signature')
        except KeyError:
            return HttpResponseBadRequest("Missing payment information")
        order_id = request.POST.get('razorpay_order_id')
        cart_order = CartOrder.objects.filter(order_identifier=order_id).first()
        if cart_order:
            if payment_id and payment_signature:
                cart_order.paid_status = True
                cart_order.razorpay_payment_id = payment_id
                cart_order.razorpay_signature = payment_signature
                cart_order.save()
                username = request.user.username
                email = request.user.email
                try:
                    user_address = Address.objects.get(user__username=username)
                except Address.DoesNotExist:
                    user_address = None
                user_phone_number = user_address.phone_num if user_address else None
                order_date = timezone.now()
                cart_total_amount = 0
                if 'cart_data_obj' in request.session:
                    cart_data = request.session['cart_data_obj']
                    for p_id, item in cart_data.items():
                        qty = int(item['qty'])
                        price = float(item['price'])
                        cart_total_amount += qty * price

                if 'cart_data_obj' in request.session:
                    del request.session['cart_data_obj']
                    
                return render(request, 'uwapp/payment_complete.html', {
                    'cart_data': cart_data,
                    'totalcartitems': len(cart_data),
                    'cart_total_amount': cart_total_amount,
                    'username': username,
                    'email': email,
                    'order_date': order_date,
                    'user_address': user_address,
                    'user_phone_number': user_phone_number,
                })
            else:
        
                return redirect('uwapp:payment_failed')
        else:
            return HttpResponseBadRequest("Invalid order identifier")
    else:
        return HttpResponseBadRequest("Invalid HTTP method")

@login_required
def payment_failed(request):
    return render(request,'uwapp/payment_failed.html')




