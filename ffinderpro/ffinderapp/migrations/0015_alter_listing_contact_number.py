# Generated by Django 4.2.10 on 2024-04-21 22:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ffinderapp", "0014_remove_playerprofile_address_remove_team_user_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="listing",
            name="contact_number",
            field=models.CharField(default="", max_length=15),
        ),
    ]
