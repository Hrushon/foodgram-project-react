# Generated by Django 2.2.19 on 2022-11-06 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('head', '0004_auto_20221106_1655'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='shoppingcart',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_user_recipe'),
        ),
    ]
