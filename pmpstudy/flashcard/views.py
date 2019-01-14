from django.shortcuts import render
from django.urls import reverse_lazy

# Local Classes
from .models import FlashCard
from .forms import FlashCardForm

# Django View Classes
from django.views.generic import(
    TemplateView, ListView,
    DetailView, CreateView,
    UpdateView, DeleteView
)

# Create your views here.
class CardListView(ListView):
    model = FlashCard

    def get_queryset(self):
        return FlashCard.objects.filter(activated=True)

class CardDetailView(DetailView):
    model = FlashCard

class CardCreateView(CreateView):
    form_class = FlashCardForm
    model = FlashCard

class CardUpdateView(UpdateView):
    form_class = FlashCardForm
    model = FlashCard

class CardDeleteView(DeleteView):
    success_url = reverse_lazy('card_list')

class CardDraftList(ListView):

    def get_queryset(self):
        return FlashCard.objects.filter(activated__isnull=True).order_by('-created_date')