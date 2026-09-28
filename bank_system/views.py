from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.views.generic import CreateView,DetailView,ListView,FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView,LogoutView

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

class Login(LoginView):
    authentication_form = LoginForm
    template_name = 'login.html'

    def get_success_url(self):
        if Account.objects.filter(user = self.request.user).exists():
            account = Account.objects.get(user =self.request.user)
            return reverse_lazy('acc_detail',kwargs = {'pk':account.pk})
        return reverse_lazy('create_account')

class Logout(LogoutView):
    next_page = reverse_lazy('login')


class AccountCreate(CreateView):
    model = Account
    form_class = AccountForm
    template_name = 'account_create.html'

    def dispatch(self, request, *args, **kwargs):
        if Account.objects.filter(user = request.user).exists():
            account = Account.objects.get(user = request.user)
            return redirect('acc_detail',pk = account.pk)
        return super().dispatch(request, *args, **kwargs)
  

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('acc_detail',kwargs = {'pk':self.object.pk})

class AccountDetail(DetailView):
    model = Account
    template_name = 'account_detail.html'
    context_object_name = 'account'
    
    def get_queryset(self):
        return Account.objects.filter(user = self.request.user)


class CreateCard(CreateView):
    model = Card
    form_class = CardForm
    template_name = 'create_card.html'
    success_url = reverse_lazy('cards')

    def form_valid(self, form):
        account = Account.objects.get(user = self.request.user)
        form.instance.owner = account
        return super().form_valid(form)


class CardDetail(DetailView):
    model = Card
    template_name = 'card_detail.html'
    context_object_name = 'card'

    def get_queryset(self):
        account = Account.objects.get(user = self.request.user)
        return Card.objects.filter(owner = account)

class CardList(ListView):
    model = Card
    template_name = 'my_cards.html'
    context_object_name = 'cards'

    def get_queryset(self):
        account = Account.objects.get(user = self.request.user)
        return Card.objects.filter(owner = account)

class TransferView(FormView):
    form_class = TransferForm
    template_name = 'transfer.html'

    def form_valid(self, form):
        source = form.cleaned_data['source']
        destination = form.cleaned_data['destination']
        amount = form.cleaned_data['amount']


        if amount <= 0:
            form.add_error('amount', 'Amount must be greater than 0')
            return self.form_invalid(form)

        account = None
        card = None

        if User.objects.filter(phone=source).exists():
            user = User.objects.get(phone=source)
            account = Account.objects.get(user=user)

            if account.user != self.request.user:
                form.add_error('source', 'This is not your account')
                return self.form_invalid(form)
            
            if account.balance < amount:
                form.add_error('amount', 'Not enough money')
                return self.form_invalid(form)

        elif Card.objects.filter(card_number=source).exists():
            card = Card.objects.get(card_number=source)

            if card.owner.user != self.request.user:
                form.add_error('source', 'This is not your card')
                return self.form_invalid(form)

            if card.balance < amount:
                form.add_error('amount', 'Not enough money')
                return self.form_invalid(form)

        else:
            form.add_error('source', 'Source not found')
            return self.form_invalid(form)

        destination_account = None
        destination_card = None

        if User.objects.filter(phone=destination).exists():
            user = User.objects.get(phone=destination)
            destination_account = Account.objects.get(user=user)

        elif Card.objects.filter(card_number=destination).exists():
            destination_card = Card.objects.get(card_number=destination)

        else:
            form.add_error('destination', 'Destination not found')
            return self.form_invalid(form)


        if account and destination_account:
            account.balance -= amount
            destination_account.balance += amount
            account.save()
            destination_account.save()
            Transaction.objects.create(source_account=account,destination_account=destination_account,amount=amount)

        
        elif account and destination_card:
            account.balance -= amount
            destination_card.balance += amount
            account.save()
            destination_card.save()
            Transaction.objects.create(source_account=account,destination_card=destination_card,amount=amount)


        elif card and destination_account:
            card.balance -= amount
            destination_account.balance += amount
            card.save()
            destination_account.save()
            Transaction.objects.create(source_card=card,destination_account=destination_account,amount=amount)


        elif card and destination_card:
            card.balance -= amount
            destination_card.balance += amount
            card.save()
            destination_card.save()
            Transaction.objects.create(source_card=card,destination_card=destination_card,amount=amount)

        return super().form_valid(form)
    
    def get_success_url(self):
        account = Account.objects.get(user = self.request.user)
        return reverse_lazy('acc_detail',kwargs = {'pk':account.pk})


class TransactionList(ListView):
    model = Transaction
    template_name = 'transactions.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        account = Account.objects.get(user=self.request.user)
        cards = Card.objects.filter(owner=account)

        transactions = []

        filter_type = self.request.GET.get('type')

        
        if filter_type == 'all' or filter_type is None:

            account_sent = Transaction.objects.filter(source_account=account)

            for transaction in account_sent:
                transactions.append(transaction)

            account_received = Transaction.objects.filter(destination_account=account)

            for transaction in account_received:
                transactions.append(transaction)

            for card in cards:

                card_sent = Transaction.objects.filter(source_card=card)

                for transaction in card_sent:
                    transactions.append(transaction)

                card_received = Transaction.objects.filter(destination_card=card)

                for transaction in card_received:
                    transactions.append(transaction)

        
        elif filter_type == 'sent':

            account_sent = Transaction.objects.filter(source_account=account)

            for transaction in account_sent:
                transactions.append(transaction)

            for card in cards:

                card_sent = Transaction.objects.filter(source_card=card)

                for transaction in card_sent:
                    transactions.append(transaction)


        elif filter_type == 'received':
            account_received = Transaction.objects.filter(destination_account=account)
            for transaction in account_received:
                transactions.append(transaction)
            for card in cards:
                card_received = Transaction.objects.filter(destination_card=card)
                for transaction in card_received:
                    transactions.append(transaction)
        return transactions


class CheckPhoneView(FormView):
    form_class = CheckPhoneForm
    template_name = 'check_phone.html'

    def form_valid(self, form):
        phone = form.cleaned_data['phone']
        if User.objects.filter(phone=phone).exists():
            user = User.objects.get(phone=phone)
            account = Account.objects.get(user=user)
            return render(self.request, self.template_name, { 'form': form, 'firstname': account.firstname, 'lastname': account.lastname })

        return render(self.request, self.template_name, { 'form': form, 'error': 'User not found'})


class CheckCardView(FormView):
    form_class = CheckCardForm
    template_name = 'check_card.html'

    def form_valid(self, form):
        card_number = form.cleaned_data['card_number']

        if Card.objects.filter(card_number=card_number).exists():
            card = Card.objects.get(card_number=card_number)
            account = card.owner

            return render(self.request, self.template_name, {
                'form': form,
                'firstname': account.firstname,
                'lastname': account.lastname
            })

        return render(self.request, self.template_name, {
            'form': form,
            'error': 'Card not found'
        })