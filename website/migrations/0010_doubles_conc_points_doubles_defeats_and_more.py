# Generated by Django 4.2.6 on 2023-10-23 13:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0009_remove_tournament_matches_match_tournament_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='doubles',
            name='conc_points',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='doubles',
            name='defeats',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='doubles',
            name='scored_points',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='doubles',
            name='wins',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='match',
            name='tournament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches', to='website.tournament'),
        ),
    ]