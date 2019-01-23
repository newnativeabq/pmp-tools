# Django Utility classes/functions
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect

# Local Classes
from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm

# Django View Classes
from django.views.generic import (
    TemplateView, ListView,
    DetailView, CreateView,
    UpdateView, DeleteView
)

## For Function-Based Views specifically
from django.contrib.auth.decorators import login_required

## Tagging
from tagging.models import Tag


# Create your views here.
class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    model = Post

    def get_queryset(self):
        # __lte stands for less than or equal to in Django ORM query
        # ..(-pub...) the minus sign reverses sort order
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[:5]

class PostDetailView(DetailView):
    model = Post
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_app'] = 'blog'
        return context

class CreatePostView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog:post_detail'

    form_class = PostForm
    model = Post
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_app'] = 'blog'
        return context

    def form_valid(self, form):
        model = form.save(commit=False)
        # Space for further form work if necessary
        model.save()
        return HttpResponseRedirect(reverse('blog:post_detail', args=(model.pk,)))

class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'admin:login'
    redirect_field_name = 'blog:post_detail'

    form_class = PostForm
    model = Post
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_app'] = 'blog'
        return context

class PostDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'admin:login'
    model = Post
    redirect_field_name = 'blog/post_detail.html'
    success_url = reverse_lazy('blog:post_list')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_app'] = 'blog'
        return context

class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login'
    redirect_field_name = 'blog:post_drafts'

    def get_queryset(self):
        # __lte stands for less than or equal to in Django ORM query
        # ..(-pub...) the minus sign reverses sort order
        return Post.objects.filter(published_date__isnull=True).order_by('-published_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_app'] = 'blog'
        return context


###############################
###############################
# Function-Based comment views

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('blog:post_detail', pk=pk)


@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # variable object 'comment' could be named anything here.
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = CommentForm()
    
    return render(request, 'blog/comment_form.html', context={'form':form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('blog:post_detail', pk=comment.post.pk)

@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('blog:post_detail', pk=post_pk)

## tagging
# UNDER CONSTRUCTION
@login_required
def tag_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    newTags = request.newTags
    Tag.objects.add_tag(post, newTags)
    