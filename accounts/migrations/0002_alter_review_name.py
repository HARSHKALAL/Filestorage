# Generated by Django 4.1.7 on 2023-03-23 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("accounts", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="review",
            name="name",
            field=models.CharField(blank=True, max_length=100, null=True),
        )
    ]
