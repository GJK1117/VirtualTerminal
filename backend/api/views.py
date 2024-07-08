from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from VirtualTerminal import settings
from api.command_dict import COMMAND_DICT
from api.command_exec import Command_Exec
from api.models import Item
from api.serializers import ItemSerializer


# Create your views here.

# 기존 장고 방식
def hello_django(request):
    return HttpResponse('Hello, Django!')

# DRF 방식
@api_view(['GET'])  # rest_framework 를 사용하기 위한 데코레이터(rest_framework 사용시 필수로 넣어줘야함)
def hello_django_drf(request):
    return Response({'message': 'Hello, Django!'})

@api_view(['POST'])
def connect_user(request):
    if request.method == 'POST':
        user_instance = request.data
        print(user_instance)
        settings.set_user_instance(user_instance['username'], user_instance['hostname'])

    return Response({'message': 'User instance is set.'})



# 문제에 들어가면 문제에 대한 정보 db에서 조회하고 저장하는 뷰
@api_view(['POST'])
def get_problem(request):
    pass

@api_view(['POST'])
def execute_command(request):
    if request.method == 'POST':
        command = request.data

        ### DB에서 가져와야 하는 값
        allowed_commands = ['cd', 'pwd', 'mkdir', 'ls', 'touch']
        template = None
        ###

        print(command)
        command_parts = command['call'].split(' ')
        output: str = Command_Exec(COMMAND_DICT[command_parts[0]]).execute(command_parts, allowed_commands, template)
        return Response({'output': output})

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer



