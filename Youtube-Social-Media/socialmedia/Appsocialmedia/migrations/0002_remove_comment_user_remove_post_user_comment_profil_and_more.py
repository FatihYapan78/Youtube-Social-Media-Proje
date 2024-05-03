# Generated by Django 4.2.5 on 2024-04-18 20:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("Appsocialmedia", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="comment",
            name="user",
        ),
        migrations.RemoveField(
            model_name="post",
            name="user",
        ),
        migrations.AddField(
            model_name="comment",
            name="profil",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="Appsocialmedia.profil",
            ),
        ),
        migrations.AddField(
            model_name="post",
            name="profil",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="Appsocialmedia.profil",
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="likes",
            field=models.ManyToManyField(
                blank=True, related_name="Beğenenler", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="post_save",
            field=models.ManyToManyField(
                blank=True, related_name="Kaydedenler", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
