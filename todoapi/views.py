from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from todoapi.serializers import UserSerializer,TodoSerializer
from rest_framework import authentication,permissions
from django.contrib.auth.models import User
from tasks.models import Todo

class UserView(ModelViewSet):
    serializer_class=UserSerializer
    queryset=User.objects.all()
    model=User
    # def create(self, request, *args, **kwargs):
    #     serializer=UserSerializer(data=request.data)
    #     if serializer.is_valid():
    #         usr=User.objects.create_user(**serializer.validated_data)
    #         serializer=UserSerializer(usr)
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors)



class TodoView(ModelViewSet):
    serializer_class=TodoSerializer
    queryset=Todo.objects.all()
    # authentication_classes=[authentication.BasicAuthentication]
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer=TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
    


    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)


    

    # create,list,retrive,update,destroy

# Create your views here.
# user creation api
# login
# todo create
# todo list
# todo detail
# todo edit
# todo delete

# task application api aan ith
