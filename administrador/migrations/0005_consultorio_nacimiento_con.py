# Generated by Django 4.2.3 on 2023-07-29 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrador', '0004_auditoria'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultorio',
            name='nacimiento_con',
            field=models.DateField(null=True),
        ),
    ]
