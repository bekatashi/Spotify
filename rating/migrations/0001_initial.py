# Generated by Django 4.0.4 on 2022-06-02 14:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('song', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ratings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.PositiveSmallIntegerField(choices=[(1, 'Looser of loosers'), (2, 'Looser'), (3, 'Satisfied'), (4, 'Good'), (5, 'Perfect')])),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to=settings.AUTH_USER_MODEL)),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='song.song')),
            ],
            options={
                'verbose_name': 'rating',
                'unique_together': {('owner', 'song')},
            },
        ),
    ]
