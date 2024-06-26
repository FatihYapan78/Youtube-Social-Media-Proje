# Generated by Django 4.2.5 on 2024-04-18 20:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "Appsocialmedia",
            "0002_remove_comment_user_remove_post_user_comment_profil_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="likes",
            field=models.ManyToManyField(
                blank=True, related_name="Beğenenler", to="Appsocialmedia.profil"
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="post_save",
            field=models.ManyToManyField(
                blank=True, related_name="Kaydedenler", to="Appsocialmedia.profil"
            ),
        ),
    ]
