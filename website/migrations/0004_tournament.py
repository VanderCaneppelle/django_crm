# Generated by Django 4.2.6 on 2023-10-13 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_record_side'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date', models.DateField(auto_now=True)),
                ('max_players', models.IntegerField(max_length=3)),
                ('players', models.ManyToManyField(to='website.record')),
            ],
        ),
    ]
