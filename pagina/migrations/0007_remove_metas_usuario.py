# Generated by Django 5.1.3 on 2024-12-12 03:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pagina', '0006_indicador_total_alter_grupoproduto_descricao_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='metas',
            name='usuario',
        ),
    ]
