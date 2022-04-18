# Generated by Django 3.2.9 on 2022-02-14 19:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('django_artisan', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('django_forum', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='artisanforumprofile',
            name='avatar',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to='django_forum.avatar'),
        ),
        migrations.AddField(
            model_name='artisanforumprofile',
            name='profile_user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]