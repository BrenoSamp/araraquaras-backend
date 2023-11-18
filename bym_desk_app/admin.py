from django.contrib import admin
from bym_desk_app.models import Usuario, Analista, Ticket, Mensagem, Bloco, Local, Matricula

class Usuarios(admin.ModelAdmin):
    list_display = ('id', 'nome', 'email', 'senha', 'telefone', 'role')
    list_display_links = ('id', 'nome', 'email', 'senha', 'telefone', 'role')
    search_fields = ('id', 'nome', 'email',  'senha', 'telefone', 'role')
    ordering = ('id',)

admin.site.register(Usuario, Usuarios)

class Analistas(admin.ModelAdmin):
    list_display = ('id', 'matricula', 'setor')
    list_display_links = ('id', 'matricula', 'setor')
    search_fields = ('id', 'matricula', 'setor')
    ordering = ('id',)

admin.site.register(Analista, Analistas)

class Tickets(admin.ModelAdmin):
    list_display = ('id', 'solicitante_id', 'analista_id', 'local_id', 'tipo', 'data', 'status')
    list_display_links = ('id', 'solicitante_id', 'analista_id', 'local_id', 'tipo', 'data', 'status')
    search_fields = ('id', 'solicitante_id', 'analista_id', 'local_id', 'tipo', 'data', 'status')
    ordering = ('id',)

admin.site.register(Ticket, Tickets)

class Matriculas(admin.ModelAdmin):
    list_display = ('id', 'matricula')
    list_display_links = ('id', 'matricula')
    search_fields = ('id', 'matricula')
    ordering = ('id',)

admin.site.register(Matricula, Matriculas)

class Mensagens(admin.ModelAdmin):
    list_display = ('id', 'ticket_id', 'mensagem', 'imagem')
    list_display_links = ('id', 'ticket_id', 'mensagem', 'imagem')
    search_fields = ('id', 'ticket_id', 'mensagem', 'imagem')
    ordering = ('id',)

admin.site.register(Mensagem, Mensagens)

class Blocos(admin.ModelAdmin):
    list_display = ('id', 'nome')
    list_display_links = ('id', 'nome')
    search_fields = ('id', 'nome')
    ordering = ('id',)

admin.site.register(Bloco, Blocos)

class Locais(admin.ModelAdmin):
    list_display = ('id', 'nome', 'bloco_id')
    list_display_links = ('id', 'nome', 'bloco_id')
    search_fields = ('id', 'nome', 'bloco_id')
    ordering = ('id',)

admin.site.register(Local, Locais)