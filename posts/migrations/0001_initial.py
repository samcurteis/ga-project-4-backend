# Generated by Django 4.1.5 on 2023-01-19 11:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='albums', to=settings.AUTH_USER_MODEL)),
                ('post_favorites', models.ManyToManyField(blank=True, related_name='post_favorites', to=settings.AUTH_USER_MODEL)),
                ('post_likes', models.ManyToManyField(blank=True, related_name='post_likes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
