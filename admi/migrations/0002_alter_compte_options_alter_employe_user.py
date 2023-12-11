# Generated by Django 4.0 on 2023-12-01 12:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('admi', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='compte',
            options={'ordering': ['annee']},
        ),
        migrations.AlterField(
            model_name='employe',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='uzer', to='auth.user'),
        ),
    ]
