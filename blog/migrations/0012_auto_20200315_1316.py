# Generated by Django 2.2.7 on 2020-03-15 07:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_auto_20200302_0219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileupload',
            name='entry',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='blog.Entry'),
        ),
    ]