# Generated by Django 4.2.1 on 2023-06-04 13:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Juniors', '0014_interest_juniors_applied_jobs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interest',
            name='junior',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Juniors.juniors'),
        ),
    ]
