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


class BalanceProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'user',
            'balance',
        ]

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

class CreateOrderSerializers(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = [
            'quantity',
            'price',
            'status',
        ]

class UserSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
