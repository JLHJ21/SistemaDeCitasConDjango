# Generated by Django 4.2.3 on 2023-07-23 20:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuario', '0001_initial'),
        ('administrador', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultorio',
            name='id_cit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usuario.citas'),
        ),
    ]
