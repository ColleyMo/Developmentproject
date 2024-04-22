# Generated by Django 4.2.10 on 2024-04-21 22:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("ffinderapp", "0013_listing_user_profile"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="playerprofile",
            name="address",
        ),
        migrations.RemoveField(
            model_name="team",
            name="user",
        ),
        migrations.AddField(
            model_name="listing",
            name="contact_number",
            field=models.CharField(default=" ", max_length=15),
        ),
        migrations.AddField(
            model_name="team",
            name="location",
            field=models.CharField(default="", max_length=100),
        ),
        migrations.AlterField(
            model_name="application",
            name="player",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="ffinderapp.playerprofile",
            ),
        ),
        migrations.AlterField(
            model_name="team",
            name="photo",
            field=models.ImageField(
                blank=True, null=True, upload_to="media/team_photos/"
            ),
        ),
        migrations.DeleteModel(
            name="Player",
        ),
    ]
