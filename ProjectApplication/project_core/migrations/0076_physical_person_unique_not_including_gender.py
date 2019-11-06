# Generated by Django 2.2.6 on 2019-11-06 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_core', '0075_budgetcategory_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fundinginstrument',
            name='description',
            field=models.TextField(help_text='Description of the funding instrument that can be used to distinguish it from others'),
        ),
        migrations.AlterUniqueTogether(
            name='physicalperson',
            unique_together={('first_name', 'surname')},
        ),
    ]
