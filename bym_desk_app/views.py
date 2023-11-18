import datetime
from django.http import JsonResponse, HttpResponse
from rest_framework import viewsets, generics, filters
from bym_desk_app.models import Usuario, Analista, Ticket, Mensagem, Bloco, Local, Matricula
from bym_desk_app.serializer import UsuarioSerializer, AnalistaSerializer, TicketSerializer, ListaTicketsUsuarioSerializer, MensagemSerializer, ListaMensagensTicketSerializer, BlocoSerializer, LocalSerializer, MatriculaSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import NotFound
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from collections import defaultdict
import json
from bym_desk_app.producer import publish
import array
import numpy

class UsuariosViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['id']
    search_fields = ['id', 'nome', 'email',  'senha', 'telefone']
    filterset_fields = ['id', 'nome', 'email',  'senha', 'telefone']
class AnalistasViewSet(viewsets.ModelViewSet):
    queryset = Analista.objects.all()
    serializer_class = AnalistaSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['id']
    search_fields = ['id', 'matricula', 'setor']
    filterset_fields = ['id', 'matricula', 'setor']

class TicketsViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['id']
    filterset_fields = ['id', 'solicitante_id', 'analista_id', 'local_id', 'tipo', 'data']

class BlocosViewSet(viewsets.ModelViewSet):
    queryset = Bloco.objects.all()
    serializer_class = BlocoSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['id']
    filterset_fields = ['id', 'nome']

class LocaisViewSet(viewsets.ModelViewSet):
    queryset = Local.objects.all()
    serializer_class = LocalSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['id']
    filterset_fields = ['id', 'nome', 'bloco_id']

class MatriculasViewSet(viewsets.ModelViewSet):
    queryset = Matricula.objects.all()
    serializer_class = MatriculaSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['id']
    filterset_fields = ['id', 'matricula']

class ListaTicketsUsuarioViewSet(generics.ListAPIView):
    def get_queryset(self):
        queryset = Ticket.objects.filter(solicitante_id=self.kwargs['solicitante_id'])
        return queryset
    serializer_class= ListaTicketsUsuarioSerializer

@csrf_exempt
def checkAdmin(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        usuario = Usuario.objects.filter(id=body['usuario_id'])

        if usuario.exists() == False:
            raise NotFound('Usuário não existe')

        usuario = Usuario.objects.get(id=body['usuario_id'])

        if usuario.admin == None or usuario.admin == 0  or usuario.admin == False:
            error = {
                'error': 'Usuário não existe'
            }

            return JsonResponse(error, status=400)


        userFormatted = {
            'id': usuario.id,
            'nome': usuario.nome,
            'email': usuario.email,
            'telefone': usuario.telefone,
            'role': usuario.role,
            "admin": usuario.admin
        }

        return JsonResponse(userFormatted)

@csrf_exempt
def createBloco(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        usuario = Usuario.objects.filter(id=body['usuario_id'])

        if usuario.exists() == False:
            error = {
                'error': 'Usuário não existe'
            }

            return JsonResponse(error, status=400)

        usuario = Usuario.objects.get(id=body['usuario_id'])

        if usuario.admin == None or usuario.admin == 0:
            error = {
                'error': 'Usuário não existe'
            }

            return JsonResponse(error, status=400)


        bloco = {
            'nome': body['bloco']
        }

        blocoSerializer = BlocoSerializer(data=bloco)
        blocoSerializer.is_valid(raise_exception=True)
        blocoSerializer.save()

        blocoFormatted = {
            'id': blocoSerializer.data['id'],
            'matricula': blocoSerializer.data['nome'],
        }

        return JsonResponse(blocoFormatted)

@csrf_exempt
def createBlocoLocal(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        usuario = Usuario.objects.filter(id=body['usuario_id'])

        if usuario.exists() == False:
            error = {
                'error': 'Usuário não existe'
            }

            return JsonResponse(error, status=400)

        usuario = Usuario.objects.get(id=body['usuario_id'])

        if usuario.admin == None or usuario.admin == 0:
            error = {
                'error': 'Usuário não existe'
            }

            return JsonResponse(error, status=400)

        bloco = {
            'nome': body['bloco']
        }

        blocoSerializer = BlocoSerializer(data=bloco)
        blocoSerializer.is_valid(raise_exception=True)
        blocoSerializer.save()


        local = {
            'bloco_id': blocoSerializer.data['id'],
            'nome': body['nome']
        }

        localSerializer = LocalSerializer(data=local)
        localSerializer.is_valid(raise_exception=True)
        localSerializer.save()

        blocoFormatted = {
            'local_id': localSerializer.data['id'],
            'nome_local': localSerializer.data['nome'],
            'bloco_id': blocoSerializer.data['id'],
            'nome_bloco': blocoSerializer.data['nome'],
        }

        return JsonResponse(blocoFormatted)

def createLocal(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        usuario = Usuario.objects.filter(id=body['usuario_id'])

        if usuario.exists() == False:
            error = {
                'error': 'Usuário não existe'
            }

            return JsonResponse(error, status=400)

        usuario = Usuario.objects.get(id=body['usuario_id'])

        if usuario.admin == None or usuario.admin == 0:
            error = {
                'error': 'Usuário não existe'
            }

            return JsonResponse(error, status=400)

        bloco = Bloco.objects.filter(id=body['bloco_id'])

        if bloco.exists == False:
            error = {
                'error': 'Bloco não existe'
            }

            return JsonResponse(error, status=400)


        local = {
            'bloco_id': body['bloco_id'],
            'nome': body['nome']
        }

        localSerializer = LocalSerializer(data=local)
        localSerializer.is_valid(raise_exception=True)
        localSerializer.save()

        blocoFormatted = {
            'id': localSerializer.data['id'],
            'nome': localSerializer.data['nome'],
            'bloco_id': localSerializer.data['bloco_id'],
        }

        return JsonResponse(blocoFormatted)

@csrf_exempt
def createMatricula(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        usuario = Usuario.objects.filter(id=body['usuario_id'])

        if usuario.exists() == False:
            error = {
                'error': 'Usuário não existe'
            }

            return JsonResponse(error, status=400)

        usuario = Usuario.objects.get(id=body['usuario_id'])

        if usuario.admin == None or usuario.admin == 0:
            error = {
                'error': 'Usuário não existe'
            }

            return JsonResponse(error, status=400)

        matricula = {
            'matricula': body['matricula']
        }


        matriculaSerializer = MatriculaSerializer(data=matricula)
        matriculaSerializer.is_valid(raise_exception=True)
        matriculaSerializer.save()

        matriculaFormatted = {
            'id': matriculaSerializer.data['id'],
            'matricula': matriculaSerializer.data['matricula'],
        }

        return JsonResponse(matriculaFormatted)

@csrf_exempt
def createAnalista(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        matricula = Matricula.objects.filter(matricula=body['matricula'])

        if matricula.exists() == False:
            error = {
                'error': 'Matricula não existe'
            }

            return JsonResponse(error, status=400)

        usuario = {
            'nome': body['nome'],
            'email': body['email'],
            'senha': body['senha'],
            'telefone': body['telefone'],
            'role': body['role'],
        }
        userSerializer = UsuarioSerializer(data=usuario)
        userSerializer.is_valid(raise_exception=True)
        userSerializer.save()

        analista = {
            'matricula': body['matricula'],
            'setor': body['setor'],
            'usuario_id': userSerializer.data['id']
        }
        analistaSerializer = AnalistaSerializer(data=analista)
        analistaSerializer.is_valid(raise_exception=True)
        analistaSerializer.save()

        analistaFormatted = {
            'id': userSerializer.data['id'],
            'nome': body['nome'],
            'email': body['email'],
            'telefone': body['telefone'],
            'role': body['role'],
            'analista_id': analistaSerializer.data['id'],
            'matricula': body['matricula'],
            'setor': body['setor']
        }

        return JsonResponse(analistaFormatted)

@csrf_exempt
def createUser(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        usuario = {
            'nome': body['nome'],
            'email': body['email'],
            'senha': body['senha'],
            'telefone': body['telefone'],
            'role': body['role'],
        }
        userSerializer = UsuarioSerializer(data=usuario)
        userSerializer.is_valid(raise_exception=True)
        userSerializer.save()

        userFormatted = {
            'id': userSerializer.data['id'],
            'nome': body['nome'],
            'email': body['email'],
            'telefone': body['telefone'],
            'role': body['role'],
            "admin": userSerializer.data['admin']
        }

        return JsonResponse(userFormatted)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        usuario = Usuario.objects.filter(email=body['email'], senha=body['senha'])

        if usuario.exists():
            usuario = Usuario.objects.get(email=body['email'], senha=body['senha'])
            serializedUser = {
                'id': usuario.id,
                'nome': usuario.nome,
                'email': usuario.email,
                'telefone': usuario.telefone,
                'role': usuario.role,
                'admin': usuario.admin,
                'setor': None
            }

            analista = Analista.objects.filter(usuario_id=usuario.id)

            if analista.exists():
                analista = Analista.objects.get(usuario_id=usuario.id)
                serializedUser['setor'] = analista.setor

            return JsonResponse(serializedUser)
        else:
            return JsonResponse({
                'error': 'E-mail ou senha incorreta'
            }, status=400)
@csrf_exempt
def listTicketsSolicitante(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        usuarioFiltered = Usuario.objects.filter(id=body['usuario_id'])

        if usuarioFiltered.exists() == False:
            error = {
                'error': 'Solicitante não existe'
            }

            return JsonResponse(error)

        usuario = Usuario.objects.get(id=body['usuario_id'])

        q = Q()

        q &= Q(solicitante_id=usuario.id)
        Tickets = Ticket.objects.all().filter(q).values()

        formattedTickets = []
        for ticket in Tickets:
            local = Local.objects.get(id=ticket.get("local_id_id")).__dict__
            bloco = Bloco.objects.get(id=local.get("bloco_id_id")).__dict__
            solicitante = Usuario.objects.get(id=ticket.get("solicitante_id_id"))

            matricula = ''
            if ticket.get("analista_id_id") is not None:
                analista = Analista.objects.get(id=ticket.get("analista_id_id"))
                matricula = analista.matricula


            formattedResult = {
                'id': ticket.get("id"),
                'nome_solicitante': solicitante.nome,
                'solicitante_id': ticket.get("solicitante_id_id"),
                'matricula_analista': matricula,
                'analista_id': ticket.get("analista_id_id"),
                'local_id': ticket.get("local_id_id"),
                'nome_local': local.get("nome"),
                'bloco_id': local.get("bloco_id_id"),
                'nome_bloco': bloco.get("nome"),
                'status': ticket.get("status"),
                'tipo': ticket.get("tipo"),
                'data': ticket.get("data")
            }

            formattedTickets.append(formattedResult)

        return JsonResponse(json.loads(json.dumps(formattedResult)), safe=False)

@csrf_exempt
def vinculaAnalistaTicket(request, ticket_id):
    if request.method == 'PUT':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        usuario = Usuario.objects.get(id=body['usuario_id'])

        analista = Analista.objects.filter(usuario_id=usuario.id)

        q = Q()

        if analista.exists():
            analista = Analista.objects.get(id=body['analista_id'])
            update = {
                'analista_id': analista.id,
                'status': 'Em andamento'
            }
            Ticket.objects.update_or_create(update, defaults={'id':ticket_id})


            return JsonResponse({'message':'ok'})

        error = {
            'error': 'Analista não existe'
        }

        return JsonResponse(error, status=400)

@csrf_exempt
def atualizaStatusTicket(request, ticket_id):
    if request.method == 'PUT':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        analista = Analista.objects.filter(id=body['analista_id'])

        q = Q()

        if analista.exists():
            analista = Analista.objects.get(id=body['analista_id'])
            ticket = Ticket.objects.get(id=ticket_id)
            ticket.status = body['status']
            ticket.analista_id = analista
            ticket.save()

            return JsonResponse({'message':'ok'})

        error = {
            'error': 'Analista não existe'
        }

        return JsonResponse(error, status=400)

@csrf_exempt
def listTicketsAnalista(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        usuario = Usuario.objects.get(id=body['usuario_id'])

        analista = Analista.objects.filter(usuario_id=usuario.id)

        q = Q()

        if analista.exists():
            analista = Analista.objects.get(usuario_id=usuario.id)
            q = Q(tipo=analista.setor)
            Tickets = Ticket.objects.all().filter(q).values()

            formattedTickets = []

            for ticket in Tickets:
                local = Local.objects.get(id=ticket.get("local_id_id")).__dict__
                bloco = Bloco.objects.get(id=local.get("bloco_id_id")).__dict__
                solicitante = Usuario.objects.get(id=ticket.get("solicitante_id_id"))

                matricula = ''
                if ticket.get("analista_id_id") is not None:
                    analista = Analista.objects.get(id=ticket.get("analista_id_id"))
                    matricula = analista.matricula

                formattedResult = {
                    'id': ticket.get("id"),
                    'solicitante_id': ticket.get("solicitante_id_id"),
                    'nome_solicitante': solicitante.nome,
                    'matricula_analista': matricula,
                    'analista_id': ticket.get("analista_id_id"),
                    'local_id': ticket.get("local_id_id"),
                    'nome_local': local.get("nome"),
                    'bloco_id': local.get("bloco_id_id"),
                    'nome_bloco': bloco.get("nome"),
                    'status': ticket.get("status"),
                    'tipo': ticket.get("tipo"),
                    'data': ticket.get("data")
                }

                formattedTickets.append(formattedResult)

            return JsonResponse(json.loads(json.dumps(formattedResult)), safe=False)

        error = {
            'error': 'Analista não existe'
        }

        return JsonResponse(error, status=400)

@csrf_exempt
def listTicketsAdmin(request):
    if request.method == 'GET':
        body_unicode = request.body.decode('utf-8')

        tickets = Ticket.objects.all().values()

        formattedResult =  []

        for ticket in tickets:
            local = Local.objects.get(id=ticket.get("local_id_id")).__dict__
            bloco = Bloco.objects.get(id=local.get("bloco_id_id")).__dict__
            solicitante = Usuario.objects.get(id=ticket.get("solicitante_id_id"))

            matricula = ''
            if ticket.get("analista_id_id") is not None:
                analista = Analista.objects.get(id=ticket.get("analista_id_id"))
                matricula = analista.matricula

            formattedTicket = {
                'id': ticket.get("id"),
                'solicitante_id': ticket.get("solicitante_id_id"),
                'nome_solicitante': solicitante.nome,
                'matricula_analista': matricula,
                'analista_id': ticket.get("analista_id_id"),
                'local_id': ticket.get("local_id_id"),
                'nome_local': local.get("nome"),
                'bloco_id': local.get("bloco_id_id"),
                'nome_bloco': bloco.get("nome"),
                'status': ticket.get("status"),
                'tipo': ticket.get("tipo"),
                'data': ticket.get("data")
            }

            formattedResult.append(formattedTicket)

        return JsonResponse(json.loads(json.dumps(formattedResult)), safe=False)


class MensagensViewSet(viewsets.ModelViewSet):
    queryset = Mensagem.objects.all()
    serializer_class = MensagemSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['id']
    filterset_fields = ['id', 'ticket_id', 'mensagem']

class ListaMensagensTicketViewSet(generics.ListAPIView):
    def get_queryset(self):
        queryset = Ticket.objects.filter(ticket_id=self.kwargs['ticket_id'])
        return queryset
    serializer_class= ListaMensagensTicketSerializer

@csrf_exempt
def testPublish(request):
    if request.method == 'POST':
        publish({'nome': 'Breno', 'email': 'bsampaio8@hotmail.com', 'setor':'PCC'})


    return JsonResponse({'POSTADO': True})

@csrf_exempt
def createTicket(request):
    if request.method == 'POST':
        data = request.POST.dict()
        solicitanteId = data.get("solicitante_id")
        tipo = data.get("tipo")
        localId = data.get("local_id")
        status = data.get("status")
        descricao = data.get("descricao")
        imagem = request.FILES['imagem']
        current_date = datetime.date.today()

        ticket = {
            'solicitante_id': solicitanteId,
            'tipo': tipo,
            'local_id': localId,
            'status': status,
            'data': current_date.strftime("%d/%m/%Y %H:%M:%S")
        }

        ticketSerializer = TicketSerializer(data=ticket)
        ticketSerializer.is_valid(raise_exception=True)
        ticketSerializer.save()

        ticketFormatted = {
            'id': ticketSerializer.data['id'],
            'solicitante_id': solicitanteId,
            'tipo': tipo,
            'local_id': localId,
            'status': status,
            'data': current_date.strftime("%d/%m/%Y %H:%M:%S"),
            'descricao': descricao
        }

        mensagem = {
            'ticket_id': ticketFormatted['id'],
            'imagem': imagem,
            'mensagem': descricao,
            'usuario_id': solicitanteId
        }

        mensagemSerializer = MensagemSerializer(data=mensagem)
        mensagemSerializer.is_valid(raise_exception=True)
        mensagemSerializer.save()

        analistasSetor = Analista.objects.filter(setor=tipo).values()

        for analista in analistasSetor:
            analista_id = analista.get("usuario_id_id")
            analistaInfos = Usuario.objects.get(id=analista_id)

            publish({'nome': analistaInfos.nome, 'email': analistaInfos.email, 'setor':tipo})


        return JsonResponse(ticketFormatted)

@csrf_exempt
def getBlocoLocal(request):
    if request.method == 'GET':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        bloco = Bloco.objects.filter(id=body['bloco_id'])
        if bloco.exists()==False:
            error = {
                'error': 'Bloco não existe'
            }

            return JsonResponse(error)

        locais_bloco = Local.objects.filter(bloco_id=body['bloco_id']).values_list('id', 'nome', flat=True)

        return JsonResponse(locais_bloco)

@csrf_exempt
def getMensagensTicket(request, ticket_id):
    if request.method == 'GET':

        ticket = Ticket.objects.filter(id=ticket_id)

        if ticket.exists()==False:
            error = {
                'error': 'Ticket não existe'
            }

            return JsonResponse(error, status=400)
        mensagensTicket = Mensagem.objects.filter(ticket_id=ticket_id).values()

        mensagens = []

        for mensagem in mensagensTicket:
            usuarioRemetente = mensagem.get("usuario_id_id")
            usuario = Usuario.objects.get(id=usuarioRemetente)
            ticket = Ticket.objects.get(id=ticket_id)


            mensagem = {
                'id': mensagem.get("id"),
                'usuario_id': mensagem.get("usuario_id_id"),
                'nome_usuario': usuario.nome,
                'mensagem': mensagem.get("mensagem"),
                'imagem': mensagem.get("imagem"),
                'data': ticket.data
            }

            mensagens.append(mensagem)

        return JsonResponse(json.loads(json.dumps(mensagens)), safe=False)

@csrf_exempt
def createMessage(request, idTicket):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        ticket = Ticket.objects.filter(id=idTicket)

        if ticket.exists()==False:
            error = {
                'error': 'Ticket não existe'
            }

            return JsonResponse(error, status=400)
        message = {
            'mensagem': body['mensagem'],
            'imagem': body['imagem'],
            'ticket_id': idTicket,
            'usuario_id': body['usuario_id'],
        }

        mensagemSerializer = MensagemSerializer(data=message)
        mensagemSerializer.is_valid(raise_exception=True)
        mensagemSerializer.save()

        messageFormatted = {
            'id': mensagemSerializer['id'],
            'mensagem': body['mensagem'],
            'imagem': body['imagem'],
            'ticket_id': idTicket,
            'usuario_id': body['usuario_id'],
        }

        return JsonResponse(messageFormatted)