from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import User
from django.db import transaction
from django.contrib.auth.hashers import make_password
from .serializers import UserSerializer
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
import json
import requests
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes
from rest_framework_simplejwt.tokens import RefreshToken


from django.shortcuts import render, redirect
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class DashboardView(APIView):
    template_name = 'artists/base.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class GetUserInfo(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            user_email = user.email
            return Response({'Status': 'Success', 'Message': user_email}, status=200)
        except Exception as e:
            return Response({'Status': 'Error', 'Message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class UserLogin(APIView):
    template_name = 'registration/login.html'
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        email = request.data['email']
        password = request.data['password']
        current_domain = request.build_absolute_uri('/')
        target_path = '/api/token/'
        token_url = current_domain.rstrip('/') + target_path
        payload = {
            "email": email,
            "password": password
        }
        try:
            usr = User.objects.get(email=email)
            if usr:
                try:
                    response = requests.post(token_url, data=payload)
                    json_data = json.loads(response.text)
                    print(json_data)
                    if response.status_code == 401:
                        return Response(
                            {
                                'Status':'Error',
                                'Message':'Invalid Username or Password' 
                            },
                            status=response.status_code)
                    elif response.status_code == 200:
                        return Response(
                            {
                                'Status':'Success',
                                'Message':json_data
                            },
                            status=response.status_code)
                    else:
                        return Response(
                            {
                                'Status':'Error',
                                'Message':'Something Went Wrong'
                            },
                            status=500
                        )
                except Exception as e:
                    return Response(
                            {
                                'Status':'Error',
                                'Message':str(e)
                            },
                            status=500
                        )
        except Exception as e:
                return Response(
                            {
                                'Status':'Error',
                                'Message':str(e)
                            },
                            status=500
                        )


class UserLogout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            try:
                token.blacklist()
            except Exception as e:
                print(str(e))
            return Response({"Status":"Success", "Message":"User Logged Out Succesfully"}, status=200)
        except Exception as e:
            return Response({"Status":"Error", "Message":str(e)}, status=200)
        

class ListUsersAPI(APIView):
    serializer_class = UserSerializer
    template_name = 'users/list_users.html'
    pagination_class = PageNumberPagination


    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return []

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        users = User.objects.all()
        paginator = self.pagination_class()
        paginator.page_size = 2
        paginated_users = paginator.paginate_queryset(users, request)
        serializer = self.serializer_class(paginated_users, many=True)
        return paginator.get_paginated_response(serializer.data)
    

class RegisterUserAPI(APIView):
    template_name = 'users/register_user.html'
    permission_classes = [AllowAny]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return []
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Status': 'Success', 'Message': 'User Created Successfully'}, status=201)
        return Response({'Status': 'Error', 'Message': str(serializer.errors)}, status=400)
    

class UpdateUserAPI(APIView):
    template_name='users/update_user.html'

    def get(self, request, *args, **kwargs):
        id = kwargs['user_id']
        try:
            usr = User.objects.get(id=id)
            print('user exists:',usr)
            return render(request, self.template_name, {'user':usr})
        except Exception as e:
            print(str(e))
            print('user does not exists')
    def put(self, request, *args, **kwargs):
        id = kwargs['user_id']
        print(request.data)
        try:
            user = User.objects.get(pk=id)
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                print('valid')
                serializer.save()
                # return Response(serializer.data)
                return Response({'Status': 'Success', 'Message': 'User Updated Succesfully'}, status=200)
            else:
                return Response({'Status': 'Error', 'Message': str(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'Status': 'Error', 'Message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(str(e))
            return Response({'Status': 'Error', 'Message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class DeleteUserAPI(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, user_id, *args, **kwargs):
        try:
            user = User.objects.get(pk=user_id)
            user.delete()
            return Response({'Status': 'Success', 'Message': 'User Deleted Successfully'}, status=200)

        except Exception as e:
            return Response({'Status': 'Error', 'Message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)