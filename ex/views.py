from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Profile, Order
from .serialized import *
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, DjangoObjectPermissions, IsAdminUser
from django.contrib.auth.models import User
from rest_framework import generics
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
import random
from .utils import get_client_ip
from django.shortcuts import get_object_or_404
from pprint import pprint
from django.utils import timezone
from django.shortcuts import redirect
from .permissions import *

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

class BalanceProfileViewSet(viewsets.ModelViewSet):

    queryset = Profile.objects.all()
    serializer_class = BalanceProfileSerializers
    permission_classes = [BalancePermission]

class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = [IsOwnerOrReadOnly_order]
    queryset = Order.objects.all()
    serializer_class = OrderSerializers

#NOTA: non viene effettuato nessun controllo sulla disponibilità di credito o di bitcoin da
#      parte dell'utente che effettua l'ordine. Questa feature potrebbe essere implementata
#      eseguendo determinati controlli in questa classe e modificando la classe create_order
#      in .utils
class CreateOrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = [createOrderPermission]
    queryset = Order.objects.all()
    serializer_class = CreateOrderSerializers

    def list(self, request):
        queryset = {}
        serializer = ProfileSerializers(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        serializer_error = {"error":"Data not found"}
        return Response(serializer_error, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        user_id = User.objects.filter(username=request.user.username).values('pk')
        profile = Profile.objects.filter(user_id=user_id[0]['pk']).values('pk')
        data = {
            'profile' : profile[0]['pk'],
            'published_date' : timezone.now(),
            'quantity' : request.data['quantity'],
            'price' : request.data['price'],
            'status' : request.data['status'],
        }
        serializer = OrderSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return redirect("../orders/")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = [IsOwnerOrReadOnly_user]

    def list(self, request):
        if request.user.is_superuser:
            queryset = User.objects.all()
            serializer = ProfileSerializers(queryset, many=True)
            return Response(serializer.data)
        else:
            queryset = {}
            serializer = ProfileSerializers(queryset, many=True)
            return Response(serializer.data)
