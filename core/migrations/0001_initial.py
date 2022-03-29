# Generated by Django 4.0.3 on 2022-03-29 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clocked_in', models.DateTimeField(auto_now_add=True)),
                ('clocked_out', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
