# Generated by Django 3.1.3 on 2020-12-02 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing_software', '0002_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='barcode',
            field=models.CharField(default=0, max_length=13),
            preserve_default=False,
        ),
    ]