# Generated by Django 4.2.5 on 2024-04-23 21:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Appsocialmedia", "0003_alter_post_likes_alter_post_post_save"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="comment_count",
            field=models.IntegerField(default=0),
        ),
    ]