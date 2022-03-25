# Generated by Django 3.2.6 on 2022-03-25 09:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20220322_0054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientsinrecipe',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients_list', to='recipes.ingredient', verbose_name='Рецепт'),
        ),
        migrations.AlterField(
            model_name='ingredientsinrecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_in_recipe', to='recipes.recipe', verbose_name='Ингредиент'),
        ),
    ]