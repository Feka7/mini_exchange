from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Profile, Order
from .serialized import ProfileSerializers, OrderSerializers, UserSerializers
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, DjangoObjectPermissions, IsAdminUser
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
import random
from .utils import get_client_ip
from django.shortcuts import get_object_or_404
from pprint import pprint

class IsOwnerOrReadOnly_order(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        if request.user.is_superuser:
            return True

        if request.user.is_authenticated:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        if request.user.is_superuser:
            return True

        return str(obj.profile) == str(request.user)

class IsOwnerOrReadOnly_profile(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        if request.user.is_superuser:
            return True

        if request.user.is_authenticated and request.method != "POST":
            return True

        return False

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        if request.user.is_superuser:
            return True

        return str(obj.user) == str(request.user)

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializers
    permission_classes = [IsOwnerOrReadOnly_profile]

    def list(self, request):
        if request.user.is_superuser:
            queryset = Profile.objects.all()
            serializer = ProfileSerializers(queryset, many=True)
            return Response(serializer.data)
        elif request.user.is_authenticated:
            myuser = request.user
            queryset = Profile.objects.all().filter(user=myuser)
            serializer = ProfileSerializers(queryset, many=True)
            return Response(serializer.data)
        else:
            queryset = {}
            serializer = ProfileSerializers(queryset, many=True)
            return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Profile.objects.all()
        if request.user.is_superuser:
            user = get_object_or_404(queryset, pk=pk)
            serializer = ProfileSerializers(user)
            return Response(serializer.data)
        elif request.user.is_authenticated:
            user_pk = Profile.objects.filter(user=request.user).values('pk')
            if user_pk[0]['pk'] != int(pk):
                pk = -1
            user = get_object_or_404(queryset, pk=pk)
            serializer = ProfileSerializers(user)
            return Response(serializer.data)
        else:
            user = get_object_or_404(queryset, pk=-1)
            serializer = ProfileSerializers(user)
            return Response(serializer.data)

#get object limit




class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = [IsOwnerOrReadOnly_order]
    queryset = Order.objects.all()
    serializer_class = OrderSerializers

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializers
