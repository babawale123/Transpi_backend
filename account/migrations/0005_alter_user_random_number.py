# Generated by Django 4.2.4 on 2024-02-28 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_user_random_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='random_number',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
    ]
