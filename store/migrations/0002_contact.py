# Generated by Django 5.0.4 on 2024-05-04 20:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('photo', models.ImageField(upload_to='')),
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='store.employee')),
            ],
        ),
    ]
