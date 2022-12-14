# Generated by Django 4.0.4 on 2022-11-14 14:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0009_alter_recipes_text_alter_tag_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipes',
            name='text',
            field=models.TextField(blank=True, null=True, validators=[django.core.validators.MaxLengthValidator(9999, 'Maximum length of text')], verbose_name='Recipe description'),
        ),
    ]
