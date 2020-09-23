from rest_framework.decorators import api_view
from .models import Profile, User, Medicines, MedicinesInfo
from rest_framework.response import Response
from .serializers import UserSerializer, MedicinesInfoSerializer, MedicinesSerializer, LoginSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, BasePermission, SAFE_METHODS, AllowAny, \
    IsAuthenticated
from rest_framework.renderers import HTMLFormRenderer
from django.contrib.auth import login, logout
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, csrf_exempt


@api_view(['POST', 'GET'])
def get_or_post_list_of_users(request):
    if request.method == 'GET':
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            print(serializer.errors)
            return Response({"not correct": "not correct"})
        else:
            serializer.save()
            Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_200_OK)


class MedicinesListApi(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        print('hhelo')
        if request.user and request.auth:
            print(request.user)
            token = Token.objects.get(user=request.user)
            print('hhelo')
            user = User.objects.get(username=request.user)
            print('hhelo')
            if request.auth and token:
                # user_serializer = UserSerializer(data=request.user)
                meds = Medicines.objects.filter(user=user)
                serializer = MedicinesSerializer(meds, many=True)
                return Response(serializer.data)
        meds = Medicines.objects.all()
        serializer = MedicinesSerializer(meds)
        return Response({'Some what': 'just test'})


class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        print("Hello 1")
        serializer = UserSerializer(data=request.data)
        if request.user.is_authenticated:
            return Response({'is': 'auth'})
        print(serializer.is_valid())
        if not serializer.is_valid():
            print(serializer.errors)
            return Response(serializer.errors)
        print(serializer.data)
        print("hello 2")
        return Response(serializer.data)


class LogOutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]  # redundant думаю

    def get(self, request):
        try:
            request.user.auth_token.delete()
        except User.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_200_OK)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data['user'])
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        context = {'token': token.key,
                   'user_id': user.pk,
                   'email': user.email}
        return Response(context)


# class UserApi(APIView):
#     permission_classes = (IsAuthenticated,)
#
#     def get(self, request):
#         content = {'message': "Hello world!"}
#         return Response(content)


# class MedicinesList(generics.ListCreateAPIView):
#     queryset = Medicines.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     # renderer_classes = [HTMLFormRenderer]
#     # template_name = 'list.html'
#
#     def list(self, request, *args, **kwargs):
#         print("hello!")
#         user = User.objects.get(username=request.data['username'])
#         # serializer = UserSerializer(user)
#         serializer = self.serializer_class(data=request.data,
#                                            context={'request': request})
#         print(serializer.initial_data)
#         if serializer.is_valid():
#             print("hello serializer exception")
#             user = User.objects.get(username=serializer.data['username'])
#             profile = Profile.objects.get(user=user)
#             print(profile)
#             return Response({'queryset': 'hello'})
#         print("hello! from sadjfhgsjsj")
#         serializer = MedicinesSerializer(self.get_queryset(), many=True)
#         return Response(serializer.data)


# class IsOwnerOrUser(BasePermission):
#
#     def has_object_permission(self, request, view, obj):
#         if request.method in SAFE_METHODS:
#             return True
#         return obj.user == request.user


# class TestUserApi(APIView):
#     authentication_classes = [SessionAuthentication]
#     permission_classes = [IsOwnerOrUser]
#
#     def get(self, request, format=None):
#         content = {
#             'user': str(request.user),
#             'auth': str(request.auth)
#         }
#         return Response(content)



