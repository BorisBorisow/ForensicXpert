# Generated by Django 4.2.3 on 2023-08-17 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_alter_employee_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactperson',
            name='gender',
            field=models.CharField(blank=True, choices=[('female', 'Female'), ('male', 'Male'), ('diverse', 'Diverse'), ('unknown', 'Unknown')], default='Unknown', max_length=9),
        ),
    ]
