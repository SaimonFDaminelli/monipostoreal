from django.contrib import admin
from .models import (
    CustomUser, GrupoProduto, SetorProduto, Produto, ProdutoIndicador, Posto,
    Indicador, IndicadorPosto, Metas, Registro, ConjuntoIndicadores
)

@admin.register(Indicador)
class IndicadorAdmin(admin.ModelAdmin):
    # Atualize os nomes para refletir os campos reais no modelo Indicador
    list_display = ('nome_indicador', 'frequencia', 'unidade_medida', 'descricao')
    search_fields = ('nome_indicador',)
    list_filter = ('frequencia', 'unidade_medida')

@admin.register(Metas)
class MetasAdmin(admin.ModelAdmin):
    list_display = ('indicador', 'descricao', 'valor', 'dt_inicio', 'dt_fim')
    search_fields = ('descricao', 'indicador__nome_indicador')
    list_filter = ('dt_inicio', 'dt_fim')

@admin.register(Registro)
class RegistroAdmin(admin.ModelAdmin):
    list_display = ('indicador', 'data_coleta', 'valor', 'unidade_medida', 'metas')
    search_fields = ('indicador__nome_indicador', 'metas__descricao')
    list_filter = ('data_coleta', 'unidade_medida')

admin.site.register(CustomUser)
admin.site.register(GrupoProduto)
admin.site.register(SetorProduto)
admin.site.register(Produto)
admin.site.register(ProdutoIndicador)
admin.site.register(Posto)
admin.site.register(IndicadorPosto)
admin.site.register(ConjuntoIndicadores)
