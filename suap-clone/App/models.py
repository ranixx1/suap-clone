# App/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Card(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()

    def __str__(self):
        return self.titulo

class Chamado(models.Model):
    STATUS_CHOICES = [
        ('aberto', 'Aberto'),
        ('em_analise', 'Em Análise'),
        ('resolvido', 'Resolvido'),
        ('fechado', 'Fechado'),
    ]

    URGENCIA_CHOICES = [
        ('baixa', 'Baixa'),
        ('media', 'Média'),
        ('alta', 'Alta'),
    ]

    SETOR_CHOICES = [
    ('ti', 'TI'),
    ('rh', 'RH'),
    ('financeiro', 'Financeiro'),
    ('manutencao', 'Manutenção'),
    ('limpeza', 'Limpeza'),
    ('outros', 'Outros'),
    ('chat_suporte', 'Chat de Suporte'),
]

    criado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    assunto = models.CharField(max_length=200)
    descricao = models.TextField()
    setor = models.CharField(max_length=20, choices=SETOR_CHOICES)
    urgencia = models.CharField(max_length=10, choices=URGENCIA_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aberto')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    chat_room_name = models.CharField(max_length=255, unique=True, null=True, blank=True) # <--- NOVO CAMPO AQUI

    def __str__(self):
        return f"Chamado #{self.id} - {self.assunto}"

class AtualizacaoChamado(models.Model):
    chamado = models.ForeignKey(Chamado, on_delete=models.CASCADE)
    responsavel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status_anterior = models.CharField(max_length=20)
    status_novo = models.CharField(max_length=20)
    mensagem = models.TextField(blank=True)
    data_atualizacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Atualização #{self.id}"

class ChatMessage(models.Model):
    room_name = models.CharField(max_length=255) # Para qual sala de chat a mensagem pertence
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False) # Certifique-se que este campo está aqui

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.user.username} - {self.message[:50]}"