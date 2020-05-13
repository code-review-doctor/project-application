# Generated by Django 3.0.5 on 2020-05-13 12:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_core', '0118_calls_need_to_be_part_of_a_funding_instrument'),
        ('grant_management', '0042_improves_project_data_publications_social_media_types'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='title',
            field=models.CharField(blank=True, help_text='Title of the blog post', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='doi',
            field=models.CharField(blank=True, help_text='Digital object identifier of dataset', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='project',
            field=models.ForeignKey(help_text='Project to which is the dataset is related', on_delete=django.db.models.deletion.PROTECT, to='project_core.Project'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='published_date',
            field=models.DateField(blank=True, help_text='Date on which dataset was published', null=True),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='title',
            field=models.CharField(help_text='Title of dataset', max_length=1000),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='url',
            field=models.URLField(blank=True, help_text='URL of dataset if it does not have a DOI', null=True),
        ),
        migrations.AlterField(
            model_name='projectsocialnetwork',
            name='project',
            field=models.ForeignKey(help_text='Project to which this social network page is related', on_delete=django.db.models.deletion.PROTECT, to='project_core.Project'),
        ),
        migrations.AlterField(
            model_name='projectsocialnetwork',
            name='social_network',
            field=models.ForeignKey(help_text='Social network with information about the project', on_delete=django.db.models.deletion.PROTECT, to='grant_management.SocialNetwork'),
        ),
        migrations.AlterField(
            model_name='projectsocialnetwork',
            name='url',
            field=models.URLField(blank=True, help_text='URL of social network (e.g. https://twitter.com/SwissPolar)', null=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='doi',
            field=models.CharField(blank=True, help_text='Digital object identifier of publication', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='project',
            field=models.ForeignKey(help_text='Project to which the publication is related', on_delete=django.db.models.deletion.PROTECT, to='project_core.Project'),
        ),
        migrations.AlterField(
            model_name='publication',
            name='published_date',
            field=models.DateField(blank=True, help_text='Date on which the resource was published', null=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='reference',
            field=models.CharField(blank=True, help_text='Full reference of publication', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='title',
            field=models.CharField(help_text='Title of publication', max_length=1000),
        ),
        migrations.AlterField(
            model_name='socialnetwork',
            name='name',
            field=models.CharField(help_text='Social network name (e.g. Twitter, Facebook, Instagram, Blog)', max_length=100),
        ),
    ]
