# Generated by Django 4.2.6 on 2023-11-08 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0012_doubles_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doubles',
            name='balance',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='doubles',
            name='conc_points',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='doubles',
            name='defeats',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='doubles',
            name='scored_points',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='doubles',
            name='wins',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
    ]
