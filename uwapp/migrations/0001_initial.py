# Generated by Django 5.0.4 on 2025-04-06 16:34

import ckeditor_uploader.fields
import django.db.models.deletion
import shortuuid.django_fields
import uwapp.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cid', shortuuid.django_fields.ShortUUIDField(alphabet='abcdefghijklm12345', length=10, max_length=30, prefix='cat', unique=True)),
                ('name', models.CharField(default='cloth', max_length=100)),
                ('image', models.ImageField(upload_to='category')),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Address', models.CharField(max_length=200, null=True)),
                ('phone_num', models.CharField(max_length=15, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Address',
            },
        ),
        migrations.CreateModel(
            name='CartOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mail', models.EmailField(default='', max_length=254)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('Address', models.TextField(default='', max_length=100)),
                ('Phone', models.CharField(default='Number', max_length=20)),
                ('paid_status', models.BooleanField(default=False)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('product_status', models.CharField(choices=[('processing', 'Processing'), ('shipped', 'Shipped'), ('delivered', 'Delivered')], default='processing', max_length=30)),
                ('order_identifier', models.CharField(default='', max_length=40, null=True)),
                ('razorpay_payment_id', models.CharField(default='', max_length=40, null=True)),
                ('razorpay_signature', models.CharField(default='', max_length=100, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'cart order',
            },
        ),
        migrations.CreateModel(
            name='CartOrderItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_identifier', models.CharField(default='', max_length=40, null=True)),
                ('invoice_no', models.CharField(default='', max_length=200)),
                ('item', models.CharField(max_length=200)),
                ('image', models.CharField(max_length=200)),
                ('qty', models.IntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('size', models.CharField(default='N/A', max_length=10)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uwapp.cartorder')),
            ],
            options={
                'verbose_name_plural': 'cart order items',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Pid', shortuuid.django_fields.ShortUUIDField(alphabet='abcdefghijklm12345', length=10, max_length=30, prefix='prd', unique=True)),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to=uwapp.models.user_directory_path)),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='This is the product', null=True)),
                ('price', models.DecimalField(decimal_places=2, default='300.00', max_digits=99999)),
                ('product_status', models.CharField(choices=[('draft', 'Draft'), ('disabled', 'Disabled'), ('rejected', 'Rejected'), ('published', 'published')], default='in_review', max_length=10)),
                ('featured', models.BooleanField(default=True)),
                ('small_in_stock', models.BooleanField(default=True)),
                ('medium_in_stock', models.BooleanField(default=True)),
                ('large_in_stock', models.BooleanField(default=True)),
                ('xl_in_stock', models.BooleanField(default=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(blank=True, null=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category', to='uwapp.category')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Product',
            },
        ),
        migrations.CreateModel(
            name='productimage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.ImageField(upload_to='product-image')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='p_images', to='uwapp.product')),
            ],
            options={
                'verbose_name_plural': 'productimages',
            },
        ),
    ]
