from django.db import models
from djongo.models.fields import Field, JSONField
from django.conf import settings
import random
from djongo import models as djo
from django import forms
from django.contrib.auth.models import User

class Generic_ip(models.Model):
    ip = models.GenericIPAddressField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.ip

class GenericIpForm(forms.ModelForm):

    class Meta:
        model = Generic_ip
        fields = (
            'ip',
        )



class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    '''
    ips = djo.ArrayField(
                    model_container=Generic_ip,
                    default=[]
                    )
    '''
    ips = Field(default={})
    order_list = Field(default={})
    bitcoin = models.PositiveIntegerField()
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    def __str__(self):
        return self.user.username


class Order(models.Model):

    STATUS_CHOICES = [
        ('SA', 'SALE'),
        ('PU', 'PURCHASE'),
        ('CL', 'CLOSE'),
        ('ST', 'STAND-BY')
    ]

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    published_date = models.DateTimeField(blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='ST')

    def __str__(self):
        return self.profile.user.username + str(self.published_date)
