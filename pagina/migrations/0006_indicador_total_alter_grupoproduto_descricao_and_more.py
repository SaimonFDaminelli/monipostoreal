# Generated by Django 5.1.3 on 2024-12-10 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagina', '0005_rename_meta_registro_metas_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='indicador',
            name='total',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='grupoproduto',
            name='descricao',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='indicador',
            name='descricao',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='indicador',
            name='frequencia',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='indicador',
            name='nome_indicador',
            field=models.CharField(max_length=100),
        ),
    ]
