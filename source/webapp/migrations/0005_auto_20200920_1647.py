# Generated by Django 2.2 on 2020-09-20 10:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_auto_20200920_1456'),
    ]

    operations = [
        migrations.RenameField(
            model_name='basket',
            old_name='amount',
            new_name='qty',
        ),
    ]
