# Generated by Django 4.1.3 on 2022-11-26 15:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0004_foodproduct_product_polymorphic_ctype_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AlcoholSaleTransaction',
        ),
    ]