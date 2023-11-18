from django.db import models

class Usuario(models.Model):
    nome = models.CharField(max_length=100, null=False)
    email = models.CharField(max_length=100, null=False, unique=True)
    senha = models.CharField(max_length=100, null=False)
    telefone = models.CharField(max_length=100, null=False)
    role = models.CharField(max_length=100, null=False)
    admin = models.BooleanField(null=True)

    def __str__(self):
        return self.nome

class Analista(models.Model):
    setor = models.CharField(max_length=100, null=False)
    matricula = models.CharField(max_length=100, null=False, unique=True)
    usuario_id = models.ForeignKey('Usuario', on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return self.matricula

class Bloco(models.Model):
    nome = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.nome

class Local(models.Model):
    nome = models.CharField(max_length=100, null=False)
    bloco_id = models.ForeignKey('Bloco', on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class Ticket(models.Model):
    tipo = models.CharField(max_length=100, null=False)
    data = models.CharField(max_length=100, null=False)
    status = models.CharField(max_length=100, null=False)
    solicitante_id = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    analista_id = models.ForeignKey('Analista', on_delete=models.CASCADE, null=True)
    local_id = models.ForeignKey('Local', on_delete=models.CASCADE)

    def __str__(self):
        return self.tipo

class Matricula(models.Model):
    matricula = models.CharField(max_length=100, null=False, unique=True)

class Mensagem(models.Model):
    mensagem = models.CharField(max_length=255, null=False)
    imagem = models.ImageField(null=True)
    ticket_id = models.ForeignKey('Ticket', on_delete=models.CASCADE)
    usuario_id = models.ForeignKey('Usuario', on_delete=models.CASCADE)

    def __str__(self):
        return self.mensagem
