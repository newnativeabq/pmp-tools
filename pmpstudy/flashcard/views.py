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
class FlashCardHomeView(TemplateView):
    template_name = "flashcard/flashcard.html"
    context_object_name = 'card'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_app'] = 'flashcards'
        return context

class CardListView(ListView):
    queryset = FlashCard.objects.filter(activated=True)
    template_name = "flashcard/card_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_app'] = 'flashcards'
        return context
    

class CardDetailView(DetailView):
    model = FlashCard
    template_name = "flashcard/card_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_app'] = 'flashcards'
        return context

class CardCreateView(CreateView):
    form_class = FlashCardForm
    model = FlashCard
    template_name = "flashcard/card_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_app'] = 'flashcards'
        return context

class CardUpdateView(UpdateView):
    form_class = FlashCardForm
    model = FlashCard
    template_name = "flashcard/card_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_app'] = 'flashcards'
        return context

class CardDeleteView(DeleteView):
    success_url = reverse_lazy('card_list')

class CardDraftList(ListView):
    queryset = FlashCard.objects.filter(activated__isnull=True).order_by('-created_date')
    template_name = "flashcard/card_draft_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_app'] = 'flashcards'
        return context