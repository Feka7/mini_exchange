from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile
from .serialized import ProfileSerializers, UserSerializers
import random
from pprint import pprint
from rest_framework.response import Response
from rest_framework import status


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        print(instance)
        user = User.objects.filter(username=instance).values('pk')
        data = {
            'user' : user[0]['pk'],
            'ips' : {},
            'order_list' : {} ,
            'bitcoin' : random.randint(1, 10),
            'balance': random.randint(10000, 100000),
        }
        serializer = ProfileSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
