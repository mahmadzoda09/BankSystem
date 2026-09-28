from django.urls import path
from .views import *

urlpatterns = [
    path('register',RegisterView.as_view(),name = 'register'),
    path('login',Login.as_view(),name = 'login'),
    path('logout',Logout.as_view(),name = 'logout'),
    path('create/acc',AccountCreate.as_view(),name = 'create_account'),
    path('acc/detail/<int:pk>',AccountDetail.as_view(),name = 'acc_detail'),
    path('create/card',CreateCard.as_view(),name = 'create_card'),
    path('card/detail/<int:pk>',CardDetail.as_view(),name = 'card_detail'),
    path('cards',CardList.as_view(),name = 'cards'),
    path('transfer',TransferView.as_view(),name = 'transfer'),
    path('transactions',TransactionList.as_view(),name = 'transactions'),
    path('check/phone', CheckPhoneView.as_view(), name='check_phone'),
    path('check/card', CheckCardView.as_view(), name='check_card'),
]
