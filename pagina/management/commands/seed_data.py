from django.core.management.base import BaseCommand
from pagina.models import Produto, GrupoProduto, Indicador

class Command(BaseCommand):
    help = 'Popula o banco de dados com dados iniciais'

    def handle(self, *args, **kwargs):
        # Criação de grupos de produtos
        grupos = ['Conveniencia', 'Pista', 'Combustiveis']
        for nome in grupos:
            GrupoProduto.objects.get_or_create(nome=nome)

        # Adicionar produtos
        produtos = [
            {'nome': 'Água Mineral', 'grupo_nome': 'Conveniencia'},
            {'nome': 'Biscoito', 'grupo_nome': 'Conveniencia'},
            {'nome': 'Gasolina', 'grupo_nome': 'Combustiveis'},
            {'nome': 'Diesel', 'grupo_nome': 'Combustiveis'},
            {'nome': 'Lubrificante', 'grupo_nome': 'Pista'},
        ]
        for produto in produtos:
            grupo = GrupoProduto.objects.get(nome=produto['grupo_nome'])
            Produto.objects.get_or_create(nome=produto['nome'], grupo=grupo)

        # Indicadores
        Indicador.objects.get_or_create(nome='Volume de Vendas', tipo='Quantidade')
        Indicador.objects.get_or_create(nome='Faturamento', tipo='Monetário')

        self.stdout.write(self.style.SUCCESS('Banco de dados populado com sucesso!'))
