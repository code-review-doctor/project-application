# Generated by Django 3.0.8 on 2020-08-20 08:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_core', '0136_add_order_of_career_stage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalproposal',
            name='head_of_research_unit',
        ),
        migrations.RemoveField(
            model_name='proposal',
            name='head_of_research_unit',
        ),
    ]
