from django.contrib.auth.models import AbstractUser, Group, Permission, User
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    telefone = models.CharField(max_length=15, blank=True, null=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)

    # Resolver conflitos de related_name
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",  # Adicionar um related_name único
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_set",  # Adicionar um related_name único
        blank=True
    )


class GrupoProduto(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nome


class SetorProduto(models.Model):
    grupo = models.ForeignKey(GrupoProduto, on_delete=models.CASCADE, related_name='setores')
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome


class Produto(models.Model):
    setor = models.ForeignKey(SetorProduto, on_delete=models.CASCADE, related_name='produtos')
    nome_produto = models.CharField(max_length=255)
    tipo_produto = models.CharField(max_length=100)

    def __str__(self):
        return self.nome_produto


class ProdutoIndicador(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='indicadores')
    indicador = models.ForeignKey('Indicador', on_delete=models.CASCADE, related_name='produtos')

    class Metas:
        unique_together = ('produto', 'indicador')


class Posto(models.Model):
    nome_posto = models.CharField(max_length=255)

    def __str__(self):
        return self.nome_posto


class Indicador(models.Model):
    FREQUENCIA_CHOICES = [
        (1, 'Diário'),
        (2, 'Semanal'),
        (3, 'Mensal'),
    ]
    
    nome_indicador = models.CharField(max_length=100)
    total = models.IntegerField(default=0)
    frequencia = models.IntegerField(default=0)
    unidade_medida = models.CharField(max_length=50)
    descricao = models.TextField(blank=True, null=True)  # Adicione o campo descrição se necessário

    def __str__(self):
        return self.nome_indicador

class IndicadorPosto(models.Model):
    indicador = models.ForeignKey(Indicador, on_delete=models.CASCADE, related_name='postos')
    posto = models.ForeignKey(Posto, on_delete=models.CASCADE, related_name='indicadores')

    class Metas:
        unique_together = ('indicador', 'posto')


class Metas(models.Model):
    indicador = models.ForeignKey(Indicador, on_delete=models.CASCADE)
    descricao = models.TextField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    dt_inicio = models.DateField()
    dt_fim = models.DateField()

    def __str__(self):
        return f"{self.indicador.nome_indicador} - {self.descricao}"
    
class Registro(models.Model):
    data_coleta = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    unidade_medida = models.CharField(max_length=50)
    indicador = models.ForeignKey(Indicador, on_delete=models.CASCADE, related_name='registros')
    metas = models.ForeignKey(Metas, on_delete=models.CASCADE, null=True, blank=True, related_name='registros')

    def __str__(self):
        return f"{self.indicador.nome_indicador} - {self.data_coleta}"


class ConjuntoIndicadores(models.Model):
    tipo_relacao = models.CharField(max_length=255)
    indicador = models.ForeignKey(Indicador, on_delete=models.CASCADE, related_name='conjuntos')

    def __str__(self):
        return f"{self.tipo_relacao} - {self.indicador}"
