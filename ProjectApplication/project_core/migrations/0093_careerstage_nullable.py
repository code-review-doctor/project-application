# Generated by Django 2.2.6 on 2019-12-03 16:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_core', '0092_rename_call_overarching_project_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personposition',
            name='career_stage',
            field=models.ForeignKey(blank=True, help_text='Stage of the person in the career', null=True, on_delete=django.db.models.deletion.PROTECT, to='project_core.CareerStage'),
        ),
    ]
