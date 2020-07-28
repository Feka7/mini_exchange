from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Profile, Order
from .serialized import ProfileSerializers, OrderSerializers, UserSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, DjangoObjectPermissions, IsAdminUser
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
import random

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        if request.user.is_superuser:
            return True

        return str(obj.profile) == str(request.user)

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializers

    def list(self, request):
        if request.user.is_authenticated:
            myuser = request.user
            queryset = Profile.objects.all().filter(user=myuser)
            serializer = ProfileSerializers(queryset, many=True)
            return Response(serializer.data)
        else:
            queryset = {}
            serializer = ProfileSerializers(queryset, many=True)
            return Response(serializer.data)

    def create(self, request):
        serializer = ProfileSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    @action(detail=False)
    def recent_users(self, request):
        recent_users = Profile.objects.all().order_by('-balance')

        page = self.paginate_queryset(recent_users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(recent_users, many=True)
        return Response(serializer.data)




class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Order.objects.all()
    serializer_class = OrderSerializers
