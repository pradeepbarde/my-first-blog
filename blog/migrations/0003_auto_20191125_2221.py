# Generated by Django 2.2.7 on 2019-11-25 16:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_entry'),
    ]

    operations = [
        migrations.RenameField(
            model_name='entry',
            old_name='topic',
            new_name='topic_id',
        ),
    ]
