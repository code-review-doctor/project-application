# Generated by Django 3.0.5 on 2020-05-19 09:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project_core', '0118_calls_need_to_be_part_of_a_funding_instrument'),
        ('grant_management', '0043_grant_management_model_help_texts'),
    ]

    operations = [
        migrations.CreateModel(
            name='MilestoneCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, help_text='Date and time at which the entry was created')),
                ('modified_on', models.DateTimeField(auto_now=True, help_text='Date and time at which the entry was modified', null=True)),
                ('name', models.CharField(max_length=20)),
                ('created_by', models.ForeignKey(help_text='User that created the category', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Milestone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, help_text='Date and time at which the entry was created')),
                ('modified_on', models.DateTimeField(auto_now=True, help_text='Date and time at which the entry was modified', null=True)),
                ('due_date', models.DateField()),
                ('text', models.CharField(blank=True, max_length=200, null=True)),
                ('milestone_category', models.ForeignKey(help_text='Which category is this', on_delete=django.db.models.deletion.PROTECT, to='grant_management.MilestoneCategory')),
                ('project', models.ForeignKey(help_text='Project to which the milestone is related', on_delete=django.db.models.deletion.PROTECT, to='project_core.Project')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HistoricalMilestone',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created_on', models.DateTimeField(blank=True, editable=False, help_text='Date and time at which the entry was created')),
                ('modified_on', models.DateTimeField(blank=True, editable=False, help_text='Date and time at which the entry was modified', null=True)),
                ('due_date', models.DateField()),
                ('text', models.CharField(blank=True, max_length=200, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('milestone_category', models.ForeignKey(blank=True, db_constraint=False, help_text='Which category is this', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='grant_management.MilestoneCategory')),
                ('project', models.ForeignKey(blank=True, db_constraint=False, help_text='Project to which the milestone is related', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='project_core.Project')),
            ],
            options={
                'verbose_name': 'historical milestone',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
