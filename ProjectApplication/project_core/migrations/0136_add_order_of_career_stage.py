# Generated by Django 3.0.8 on 2020-08-17 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_core', '0135_auto_change_help_texts'),
    ]

    operations = [
        migrations.AddField(
            model_name='careerstage',
            name='list_order',
            field=models.IntegerField(blank=True, help_text='Order that this field is displayed', null=True),
        ),
    ]
