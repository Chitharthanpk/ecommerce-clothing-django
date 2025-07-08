from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.translation import gettext_lazy as _
from django.db.models.fields import CharField

# Create your models here.

STATUS_CHOICE=(("processing","Processing"),("shipped","Shipped"),("delivered","Delivered"), )

STATUS=(("draft","Draft"),("disabled","Disabled"),("rejected","Rejected"),("published","published"))

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id,filename)

class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=30, prefix="cat",alphabet="abcdefghijklm12345")
    name = models.CharField(max_length=100,default="cloth") 
    image = models.ImageField(upload_to="category")

    class Meta:
        verbose_name_plural = "categories"

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' % (self.image.url))
    
    def __str__(self) :
        return self.name
    
class Product(models.Model):
    Pid = ShortUUIDField(unique=True, length=10, max_length=30, prefix="prd",alphabet="abcdefghijklm12345")    
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=100) 
    image = models.ImageField(upload_to=user_directory_path)
    description = RichTextUploadingField(null=True,blank=True,default="This is the product")
    category=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,related_name="category")
    price= models.DecimalField(max_digits=99999,decimal_places=2,default="300.00")
    product_status =  models.CharField(choices=STATUS,max_length=10,default="in_review")
    featured = models.BooleanField(default=True)
    small_in_stock = models.BooleanField(default=True)
    medium_in_stock = models.BooleanField(default=True)
    large_in_stock = models.BooleanField(default=True)
    xl_in_stock = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True,blank=True)

    class Meta:
        verbose_name_plural = "Product"

    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' % (self.image.url))
    
    def __str__(self) :
        return self.name    
    
class productimage(models.Model):
    images = models.ImageField (upload_to="product-image")
    product = models.ForeignKey(Product,related_name="p_images",on_delete=models.SET_NULL,null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "productimages"

######################################################################## cartorder #######################################################################################
######################################################################## cartitems ####################################################################################### 
 
class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mail=models.EmailField(default="")
    price= models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    Address = models.TextField(max_length=100,default="")
    Phone = models.CharField(max_length=20,default="Number")
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status =  models.CharField(choices=STATUS_CHOICE,max_length=30,default="processing")
    order_identifier = models.CharField(max_length=40,default="",null=True)
    razorpay_payment_id = models.CharField(max_length=40,default="",null=True)
    razorpay_signature = models.CharField(max_length=100,default="",null=True)

    
    class Meta:
        verbose_name_plural = "cart order"

class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    order_identifier = models.CharField(max_length=40,default="",null=True)
    invoice_no =  models.CharField(max_length=200,default="")
    item =  models.CharField(max_length=200)
    image =  models.CharField(max_length=200)
    qty = models.IntegerField(default=0)
    price= models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total= models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    size = models.CharField(max_length=10,default='N/A')
    
    class Meta:
        verbose_name_plural = "cart order items"

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' % (self.image.url))
    
    def order_image(self):
        return mark_safe('<img src="/media/%s" width="50" height="50"/>' % (self.image))
    
######################################################################## Address #####################################################################################

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Address = models.CharField(max_length=200,null=True)
    phone_num = models.CharField(max_length=15, null=True)

    class Meta:
        verbose_name_plural = "Address"






    
    