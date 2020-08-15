# Generated by Django 3.0.8 on 2020-08-15 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_core', '0134_auto_add_role_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postaladdress',
            name='address',
            field=models.TextField(help_text='Department name, street/avenue, block, building, floor, door, etc.'),
        ),
    ]
