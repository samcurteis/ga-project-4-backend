from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
# this can create timestamps in different formats
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.models import Q
import jwt

from .serializers.common import UserSerializer
from .serializers.populated import PopulatedUserSerializer

User = get_user_model()


class RegisterView(APIView):
    def post(self, request):
        user_to_create = UserSerializer(data=request.data)
        if user_to_create.is_valid():
            user_to_create.save()
            return Response({'message': "Registration successful!"}, status=status.HTTP_201_CREATED)
        return Response(user_to_create.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user_to_login = User.objects.get(email=email)
        except User.DoesNotExist:
            raise PermissionDenied(detail="Invalid Credentials")
        if not user_to_login.check_password(password):
            raise PermissionDenied(detail="Invalid Credentials")

        dt = datetime.now() + timedelta(days=7)  # how long the token will be valid for

        token = jwt.encode(
            {'sub': user_to_login.id, 'exp': int(dt.strftime('%s'))},
            settings.SECRET_KEY,
            algorithm='HS256'
        )

        return Response({'token': token, 'message': f"Welcome back, {user_to_login.username}!"})


class UserListView(APIView):
    def get(self, _request):
        users = User.objects.all()
        serialized_users = UserSerializer(users, many=True)
        return Response(serialized_users.data, status=status.HTTP_200_OK)


class UserDetailView(APIView):
    def get(self, _request, pk):
        user = User.objects.get(pk=pk)
        serialized_user = PopulatedUserSerializer(user)
        return Response(serialized_user.data, status=status.HTTP_200_OK)


class UserSearchView(APIView):
    def get(self, request):
        query = request.GET.get('search')
        print(query)
        results = User.objects.filter(Q(first_name__icontains=query) | Q(
            last_name__icontains=query) | Q(
            username__icontains=query))
        serialized_results = UserSerializer(results, many=True)
        return Response(serialized_results.data)
