# Generated by Django 5.1.7 on 2025-04-07 21:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_customuser_favorite_stores'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='favorite_stores',
            new_name='favorites',
        ),
    ]
