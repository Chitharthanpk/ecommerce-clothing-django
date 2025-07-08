from django.urls import path,include
from uwapp.views import payment_completed,payment_failed,product,login_required,cart,category,category_product,checkout,delete_item_from_cart,details,index,account,add_to_cart,orders

app_name="uwapp"

urlpatterns = [
    path("",index,name="index"),

    path("product/",product,name="product"),

    path("category/<cid>",category_product,name="category_product"),

    path("category/",category,name="category"),

    path("details/<Pid>/",details,name="details"),

    path("add_to_cart/",add_to_cart,name="add_to_cart"),

    path("cart/",cart,name="cart"),

    path("delete-from-cart/",delete_item_from_cart,name="delete-from-cart"),

    path("account/",account,name="account"),

    path("orders/",orders,name="orders"),
    
    path("checkout/",checkout,name="checkout"),


    path('payment/success/', payment_completed, name='payment_success'),
    
    path('payment/failed/', payment_failed, name='payment_failed'),

]
