from rest_framework import serializers
from .models import Profile, Order
from django.contrib.auth.models import User

class ProfileSerializers(serializers.ModelSerializer):


    class Meta:
        model = Profile
        fields = [
            'user',
            'ips',
            'order_list',
            'bitcoin',
            'balance',
        ]
#togliere classe profile e aggiungere in aut con user. prova con save post

class OrderSerializers(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = [
            'profile',
            'published_date',
            'quantity',
            'price',
            'status',
        ]

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
