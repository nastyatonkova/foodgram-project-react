# Generated by Django 4.0.4 on 2022-11-04 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150, verbose_name='Name of the ingredient')),
                ('measurement_unit', models.CharField(max_length=50, verbose_name='Unit of measure')),
            ],
            options={
                'verbose_name': 'Ingredient',
                'verbose_name_plural': 'Ingredients',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='IngredientInRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(default=1, verbose_name='Number of ingredients')),
            ],
        ),
        migrations.CreateModel(
            name='Recipes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Recipe name')),
                ('image', models.TextField(blank=True, null=True, verbose_name='Image')),
                ('text', models.TextField(blank=True, null=True, verbose_name='Recipe description')),
                ('cooking_time', models.IntegerField(blank=True, null=True, verbose_name='Cooking time (in minutes)')),
                ('pub_date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Recipe publication date')),
            ],
            options={
                'verbose_name': 'Recipe',
                'verbose_name_plural': 'Recipes',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Tag')),
                ('color', models.CharField(max_length=50, verbose_name='Unit of measure')),
                ('slug', models.SlugField(unique=True, verbose_name='Slug')),
            ],
        ),
    ]
