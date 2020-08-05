from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile, Order
from .serialized import ProfileSerializers, UserSerializers
import random
from pprint import pprint
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.signals import user_logged_in


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def perform_some_action_on_login(sender, user, request, **kwargs):
    ip = get_client_ip(request)
    profile = Profile.objects.filter(user=user).update(ips=ip)
    return

user_logged_in.connect(perform_some_action_on_login)

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

@receiver(post_save, sender=Order)
def create_order(sender, instance, **kwargs):
    if instance.status == 'SA':
        orders = Order.objects.filter(status='PU').order_by('-price', 'published_date').values()
        for order in orders:
            if float(order['price']) >= instance.price and instance.status == 'SA':

                #controllo bitcoin usati, prezzo utilizzato è quello di vendita
                number_bitcoin = float(min(order['quantity'], instance.quantity))
                money_used = float(instance.price) * number_bitcoin

                #aggiorno dati profili
                profile_buyer = Profile.objects.filter(id=order['profile_id']).values('balance', 'bitcoin')
                Profile.objects.filter(id=order['profile_id']).update(
                                        balance=float(profile_buyer[0]['balance'])-money_used,
                                        bitcoin=int(profile_buyer[0]['bitcoin'])+number_bitcoin)

                profile_seller = Profile.objects.filter(id=instance.profile_id).values('balance', 'bitcoin')
                Profile.objects.filter(id=instance.profile_id).update(
                                        balance=float(profile_seller[0]['balance'])+money_used,
                                        bitcoin=int(profile_seller[0]['bitcoin'])-number_bitcoin)

                #aggiorno ordine, decido quale chiudere
                if number_bitcoin - order['quantity'] == 0:
                    Order.objects.filter(id=order['id']).update(status='CL')
                else:
                    Order.objects.filter(id=order['id']).update(quantity=float(order['quantity'])-number_bitcoin)

                if number_bitcoin - instance.quantity == 0:
                    Order.objects.filter(id=instance.id).update(status='CL')
                else:
                    Order.objects.filter(id=instance.id).update(quantity=instance.quantity-number_bitcoin)
            else:
                break

    elif instance.status == 'PU':
        orders = Order.objects.filter(status='SA').order_by('price', 'published_date').values()
        for order in orders:
            if float(order['price']) <= instance.price and instance.status == 'PU':

                #controllo bitcoin usati, prezzo utilizzato è sempre quello di vendita
                number_bitcoin = float(min(order['quantity'], instance.quantity))
                money_used = float(order['price']) * number_bitcoin

                #aggiorno dati profili
                profile_buyer = Profile.objects.filter(id=instance.profile_id).values('balance', 'bitcoin')
                Profile.objects.filter(id=instance.profile_id).update(
                                        balance=float(profile_buyer[0]['balance'])-money_used,
                                        bitcoin=int(profile_buyer[0]['bitcoin'])+number_bitcoin)

                profile_seller = Profile.objects.filter(id=order['profile_id']).values('balance', 'bitcoin')
                Profile.objects.filter(id=order['profile_id']).update(
                                        balance=float(profile_seller[0]['balance'])+money_used,
                                        bitcoin=int(profile_seller[0]['bitcoin'])-number_bitcoin)

                #aggiorno ordine, decido quale chiudere
                if number_bitcoin - order['quantity'] == 0:
                    Order.objects.filter(id=order['id']).update(status='CL')
                else:
                    Order.objects.filter(id=order['id']).update(quantity=float(order['quantity'])-number_bitcoin)

                if number_bitcoin - instance.quantity == 0:
                    Order.objects.filter(id=instance.id).update(status='CL')
                else:
                    Order.objects.filter(id=instance.id).update(quantity=instance.quantity-number_bitcoin)
            else:
                break
    else:
        return
