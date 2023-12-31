# Generated by Django 4.2.6 on 2023-10-20 16:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_remove_match_tournament_tournament_matches'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tournament',
            name='matches',
        ),
        migrations.AddField(
            model_name='match',
            name='tournament',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='matches', to='website.tournament'),
        ),
        migrations.AddField(
            model_name='tournament',
            name='match_instances',
            field=models.ManyToManyField(blank=True, related_name='tournament_matches', to='website.match'),
        ),
    ]
