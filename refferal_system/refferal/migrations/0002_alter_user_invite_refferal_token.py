# Generated by Django 4.2.4 on 2023-08-20 12:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("refferal", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="invite_refferal_token",
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]