from django.contrib import admin
from uwapp.models import CartOrder, CartOrderItems, Category, productimage, Product, Address 

# Register your models here.

class ProductImagesAdmin(admin.TabularInline):
    model = productimage

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ['user', 'name', 'product_image', 'price', 'featured', 'product_status','Pid','category']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category_image']

class Addressadmin(admin.ModelAdmin):
    list_display = ['user', 'Address']  

class CartOrderItemsInline(admin.TabularInline):  
    model = CartOrderItems
    extra = 1  

class CartOrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'price', 'paid_status', 'order_date', 'product_status']
    inlines = [CartOrderItemsInline]

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartOrderItems,)
admin.site.register(Address, Addressadmin)





