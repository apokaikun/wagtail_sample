# Generated by Django 4.0.7 on 2022-09-24 03:26

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.blocks
import wagtail.contrib.routable_page.models
import wagtail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0001_initial'),
        ('wagtailcore', '0076_modellogentry_revision'),
    ]

    operations = [
        migrations.CreateModel(
            name='BulletinBoard',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('body', wagtail.fields.StreamField([('section_title', wagtail.blocks.CharBlock(blank=True, help_text='Specify the title of this section.', max_length=255, required=True)), ('pages', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(blank=True, help_text='Specify an altername title of the document.', max_length=255, required=False)), ('page', wagtail.blocks.PageChooserBlock(required=True))]))], use_json_field=True, verbose_name='Bulletin Board Body')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='ProjectUpdateIndexPage',
            fields=[
                ('standardpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='base.standardpage')),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtail.contrib.routable_page.models.RoutablePageMixin, 'base.standardpage'),
        ),
        migrations.CreateModel(
            name='ProjectUpdatePage',
            fields=[
                ('standardpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='base.standardpage')),
                ('subtitle', models.CharField(blank=True, max_length=255)),
                ('date_published', models.DateTimeField(blank=True, null=True, verbose_name='Date article published')),
            ],
            options={
                'abstract': False,
            },
            bases=('base.standardpage',),
        ),
        migrations.CreateModel(
            name='ProjectUpdatePageTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProjectUpdatePersonnelRelationship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='projectupdate_person_relationship', to='bulletin.projectupdatepage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
