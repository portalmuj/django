from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView

from Project import settings
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import OfferForm, UserForm, EmployerForm, OfferResponseForm
from django.views.generic.edit import CreateView
from django.urls import reverse


# strona główna - można przejść do dodawania oferty lub przeglądania ofert
# lista pracodawców
class IndexView(ListView):
    template_name = 'mainapp/index.html'
    model = Employer


# lista wszystkich ofert
class HomeView(ListView):
    model = Offer
    template_name = 'mainapp/home.html'


# informacja o pomyślnym dodaniu odpowiedzi na formularz
class FeedbackView(DetailView):
    template_name = 'mainapp/feedback.html'
    model = Offer
    def get_object(self):
        return get_object_or_404(Offer, pk=self.kwargs.get("pk"))

# informacja o pakiecie VIP
class InfoView(ListView):
    template_name = 'mainapp/info.html'
    model = Offer

# Wyświetlenie szczeółów oferty
class OfferView(DetailView):
    model = Offer
    template_name = 'mainapp/offer.html'

    def get_object(self):
        return get_object_or_404(Offer, pk=self.kwargs.get("pk"))

# Szczegółowy widok pracodawcy, wyświetla listę ofert przez niego dodaną
class OfferListByEmployerView(ListView):
    model = Offer
    template_name = 'mainapp/offer_list_by_employer.html'

    # lista ofert dodana przez danego usera
    def get_queryset(self):
        id = self.kwargs['pk']
        target_employer = get_object_or_404(Employer, pk=id)
        return Offer.objects.filter(company=target_employer)

    # dodanie informacji o pracodawcy żeby można było je wyświetlić
    def get_context_data(self, **kwargs):
        context = super(OfferListByEmployerView, self).get_context_data(**kwargs)
        context['employer'] = get_object_or_404(Employer, pk=self.kwargs['pk'])
        return context


# Wyświetlenie listy odpowiedzi na ofertę
@method_decorator(login_required, name='dispatch')
class ResponseListForOffer(ListView):
    model = Form
    template_name = 'mainapp/response_list_for_offer.html'

    def get_queryset(self):
        id = self.kwargs['pk']
        target_offer = get_object_or_404(Offer, pk=id)
        return Form.objects.filter(offer=target_offer)

    def get_context_data(self, **kwargs):
        context = super(ResponseListForOffer, self).get_context_data(**kwargs)
        context['offer'] = get_object_or_404(Offer, pk=self.kwargs['pk'])
        return context


# Wyswietla liste pytań danej oferty
@method_decorator(login_required, name='dispatch')
class OfferQuestionsView(DetailView):
    model = Offer
    template_name = 'mainapp/question_list.html'
    def get_object(self):
        return get_object_or_404(Offer, pk=self.kwargs.get("pk"))




#Dodawanie pytania do oferty
@method_decorator(login_required, name='dispatch')
class OfferQuestionCreate(CreateView):
    model = Question
    fields = ['text', ]

    def get_context_data(self, **kwargs):
        context = super(OfferQuestionCreate, self).get_context_data(**kwargs)
        context['offer'] = get_object_or_404(Offer, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):

        form.instance.offer= get_object_or_404(Offer, pk=self.kwargs['pk'])
        return super(OfferQuestionCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('question_list', kwargs={'pk': self.kwargs['pk'], })


# Wyswietla szczegóły odpowiedzi na ofertę
@method_decorator(login_required, name='dispatch')
class OfferResponseView(DetailView):
    model = Form
    template_name = 'mainapp/response_detail.html'
    def get_object(self):
        return get_object_or_404(Form, pk=self.kwargs.get("pk"))




def OfferResponseCreate(request, pk):
    offer = get_object_or_404(Offer, pk=pk)
    if request.method == 'POST':
        form = OfferResponseForm(request.POST, request.FILES)
        if form.is_valid():

            form.instance.offer = get_object_or_404(Offer, pk=pk)
            form.save()
            message = 'Odpowiedź została dodana'

            subject = "Do Twojej oferty dodano nową odpowiedź !"
            emailMessage = "Ktoś dodał aplikację na stanowisko " + offer.position
            send_mail(subject, emailMessage, settings.EMAIL_HOST_USER, [offer.company.user.email], fail_silently=True)

            return render(request, 'mainapp/info.html', {'templateText': message})
    else:
        form = OfferResponseForm()
    return render(request, 'mainapp/form_form.html', {
        'form': form, 'offer': offer})

# Dodawanie nowej oferty
@login_required
def NewOffer(request):
    if request.method == "POST":

        form = OfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.startDate = timezone.now()
            offer.endDate = timezone.now()
            offer.company = Employer.objects.get(user=request.user)
            offer.save()
            return redirect('question_list', pk=offer.pk)
    else:
        form = OfferForm()
    return render(request, 'mainapp/newoffer.html', {'form': form})


# Dodawanie nowego użytkownika
def UserFormView(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        emp_form = EmployerForm(request.POST)
        if emp_form.is_valid() and user_form.is_valid():
            user = user_form.save(commit=False)
            emp = emp_form.save(commit=False)
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']
            user.set_password(password)
            user.save()
            emp.user = user
            emp.save()
            subject = 'Dziękujemy za zarejestrowanie konta!'
            message = 'Od teraz możesz korzystać w pełni z naszego portalu pracy!\n \n Twoje dane:\n\t-Login: '
            message += username
            message += '\n\t-Hasło: '
            message += password
            message += '\n\nPamiętaj, aby nikomu nie udostępniać swoich danych!\n\nPozdrawiam\nAdministrator Portalu Pracy'
            send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=True)
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('index')

            return redirect('index')
    else:
        user_form = UserForm()
        emp_form = EmployerForm()
    return render(request, 'mainapp/signin.html', {'user_form': user_form, 'emp_form': emp_form})



# Wyszukiwanie
from functools import reduce
import operator
from django.db.models import Q
class OfferSearchListView(HomeView):
    def get_queryset(self):
        result = super(OfferSearchListView, self).get_queryset()

        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(branch__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(position__icontains=q) for q in query_list))
            )
        return result


@login_required
def offerDelete(request, pk):
    offer = get_object_or_404(Offer, pk=pk)
    if offer.company.user != request.user:
        message = 'Odmowa dostępu!'
        return render(request, 'mainapp/info.html', {'templateText': message})
    if request.method == 'POST':
        offer.delete()
        message = 'Oferta została usunięta.'
        return render(request, 'mainapp/info.html', {'templateText': message})
    return render(request, 'mainapp/delete_confirmation.html')

@login_required
def offerEdit(request, pk):
    message = 'Edycja oferty'
    offer = get_object_or_404(Offer, pk=pk)
    if offer.company.user != request.user:
        message = 'Odmowa dostępu'
        return render(request, 'mainapp/info.html',
                      {'templateText': message})

    form = OfferForm(request.POST or None, instance=offer)
    if form.is_valid():
        form.save()
        return redirect('question_list', pk=offer.pk)
    return render(request, 'mainapp/newoffer.html', {'form': form, 'message': message})


@login_required
def employerEdit(request, pk):
    message = 'Edycja profilu'
    employer = get_object_or_404(Employer, pk=pk)
    if employer.user != request.user:
        message = 'Odmowa dostępu.'
        return render(request, 'mainapp/info.html', {'templateText': message})

    form = EmployerForm(request.POST or None, instance=employer)
    if form.is_valid():
        form.save()
        return redirect('offer_list_by_employer', pk=employer.pk)
    return render(request, 'mainapp/employer_edit.html', {'form': form, 'message': message})


@login_required
def questionDelete(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if question.offer.company.user != request.user:
        message = 'Brak dostępu'
        return render(request, 'mainapp/info.html', {'templateText': message})
    if request.method == 'POST':
        question.delete()
        return redirect('question_list', pk=question.offer.pk)
    text = 'pytanie'
    return render(request, 'mainapp/delete_confirmation.html', {'text':text})


# Logowanie
def LogIn(request):
    form = UserForm()
    return render(request, 'mainapp/../templates/registration/login.html', {'form': form})

