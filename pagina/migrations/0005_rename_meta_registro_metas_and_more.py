# Generated by Django 5.1.3 on 2024-12-04 22:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pagina', '0004_metas_usuario_alter_indicador_frequencia_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registro',
            old_name='meta',
            new_name='metas',
        ),
        migrations.AlterUniqueTogether(
            name='indicadorposto',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='produtoindicador',
            unique_together=set(),
        ),
    ]