# Generated by Django 2.2.7 on 2020-02-28 07:24

import blog.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_fileupload'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileupload',
            name='upload',
            field=models.FileField(upload_to='uploads/', validators=[blog.validators.validate_file_size, blog.validators.validate_file_extension]),
        ),
    ]