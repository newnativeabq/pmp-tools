from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect

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
    template_name = "flashcard/card_about.html"

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

class CardShowView(TemplateView):
    template_name = "flashcard/card_launch.html"

    # Query available cards and create a list to pass to JS in template
    queryset = FlashCard.objects.filter(activated=True)
    cards_info = []
    for card in queryset:
        cards_info.append(card.frontface)
        cards_info.append(card.backface)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_app'] = 'flashcards'
        context['cards'] = self.cards_info
        context['card_count'] = self.queryset.count()
        return context

class CardCreateView(CreateView):
    form_class = FlashCardForm
    model = FlashCard
    template_name = "flashcard/card_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_app'] = 'flashcards'
        return context
    
    def form_valid(self, form):
        model = form.save(commit=False)
        # Space for further form work if necessary
        model.owner = self.request.user
        model.save()
        return HttpResponseRedirect(reverse('flashcards:card_create'))

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


## Publication/Activation Functions
def activateCardView(request, pk):
    card = get_object_or_404(FlashCard, pk=pk)
    card.activate_card()
    card.save()
    return redirect('flashcards:card_detail', pk=pk)

def deactivateCardView(request, pk):
    card = get_object_or_404(FlashCard, pk=pk)
    print('card info to deactivatedebug', card.pk)
    card.deactivate_card()
    card.save()
    return redirect('flashcards:card_detail', pk=pk)