# Generated by Django 5.0.4 on 2024-05-08 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_promocode'),
    ]

    operations = [
        migrations.CreateModel(
            name='PickUpPoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=100)),
            ],
        ),
    ]
