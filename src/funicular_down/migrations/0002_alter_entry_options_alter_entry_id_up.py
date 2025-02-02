# Generated by Django 5.1.5 on 2025-02-02 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("funicular_down", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="entry",
            options={"verbose_name": "Entry", "verbose_name_plural": "Entries"},
        ),
        migrations.AlterField(
            model_name="entry",
            name="id_up",
            field=models.PositiveBigIntegerField(editable=False, unique=True),
        ),
    ]
