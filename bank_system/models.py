from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser
import random


class User(AbstractUser):
    username = None
    phone = models.CharField(max_length=50,unique=True)
    
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []


class Account(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    address = models.CharField( max_length=50)
    passport_id = models.CharField(max_length=50,unique=True)
    balance = models.IntegerField(default=1000)
    user = models.OneToOneField(User , on_delete=models.CASCADE)


def generate_cvv():
    return random.randint(100,999)

def generate_pin():
    return random.randint(1000,9999)

class Card(models.Model):
    card_number = models.CharField(max_length=50,unique=True)
    cvv = models.IntegerField(default=generate_cvv)
    date = models.DateField()
    balance = models.IntegerField(default=500)
    type = models.CharField(max_length=50)
    pin = models.IntegerField(default=generate_pin)
    owner = models.ForeignKey( Account ,on_delete=models.CASCADE)


class Transaction(models.Model):
    source_account = models.ForeignKey(Account,on_delete=models.CASCADE,null=True,blank=True,related_name='sent_transactions')
    source_card = models.ForeignKey(Card,on_delete=models.CASCADE,null=True,blank=True,related_name='sent_card_transactions')
    destination_account = models.ForeignKey(Account,on_delete=models.CASCADE,null=True,blank=True,related_name='received_transactions')
    destination_card = models.ForeignKey(Card, on_delete=models.CASCADE, null=True, blank=True, related_name='received_card_transactions')
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

