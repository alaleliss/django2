from django.shortcuts import render, redirect
from .models import Article, Comment
from . import forms
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator


# Create your views here.
@login_required(login_url='/users/sign_in')
def home(request):
    search = request.GET.get('search')
    articles = Article.objects.all().order_by('-date')
    pages = Paginator(articles, 3)
    page = request.GET.get('page')
    articles = pages.get_page(page)
    articles = articles.filter(Q(title__icontains=search) | Q(text__icontains=search)) if search else articles
    return render(request, 'home.html', {'articles': articles})


@login_required(login_url='/users/sign_in')
def post_detail(request, slug):
    post = Article.objects.get(slug=slug)
    form = forms.CommentForm(request.POST or None)
    post_comments = post.comment_set.all()
    pages = Paginator(post_comments, 3)
    page = request.GET.get('page')
    post_comments = pages.get_page(page)
    if request.method == 'POST' and form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.post = post
        instance.save()
        return redirect('blog:post_detail', slug=post.slug)
    return render(request, 'post.html', {'post': post, 'form': form, 'post_comments': post_comments})


@login_required(login_url='/users/sign_in')
def post_create(request):
    if request.method == 'POST':
        form = forms.ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect('blog:home')
    form = forms.ArticleForm()
    return render(request, 'article_create.html', {'form': form})


@login_required(login_url='/users/sign_in')
def post_delete(request, slug):
    post = Article.objects.get(slug=slug)
    if request.user != post.author:
        return render(request, 'error.html', {'post': post, 'delete': True})
    if request.method == 'POST':
        post.delete()
        return redirect('blog:home')
    return render(request, 'post_delete.html', {'post': post})


@login_required(login_url='/users/sign_in')
def post_edit(request, slug):
    post = Article.objects.get(slug=slug)
    if request.user != post.author:
        return render(request, 'error.html', {'post': post, 'edit': True})
    if request.method == 'POST':
        form = forms.ArticleForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', slug=request.POST.get('slug'))
    form = forms.ArticleForm(instance=post)
    return render(request, 'post_edit.html', {'form': form, 'post': post})


@login_required(login_url='/users/sign_in')
def like(request, slug):
    post = Article.objects.get(slug=slug)
    if request.user == post.author:
        return render(request, 'error.html', {'like': True, 'post': post})
    if request.user not in post.likes.all():
        post.likes.add(request.user)
        post.dislikes.remove(request.user)
    elif request.user in post.likes.all():
        post.likes.remove(request.user)
    return redirect('blog:post_detail', slug=slug)


@login_required(login_url='/users/sign_in')
def dislike(request, slug):
    post = Article.objects.get(slug=slug)
    if request.user == post.author:
        return render(request, 'error.html', {'dislike': True, 'post': post})
    if request.user not in post.dislikes.all():
        post.dislikes.add(request.user)
        post.likes.remove(request.user)
    elif request.user in post.dislikes.all():
        post.dislikes.remove(request.user)
    return redirect('blog:post_detail', slug=slug)


def delete_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    if request.user != comment.user:
        return render(request, 'restrict.html', {'delete': True, 'post': comment.post})
    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', slug=comment.post.slug)
    return render(request, 'delete_comment.html', {'post': comment.post})


def edit_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    if request.user != comment.user:
        return render(request, 'restrict.html', {'edit': True, 'post': comment.post})
    if request.method == 'POST':
        form = forms.CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
        return redirect('blog:post_detail', slug=comment.post.slug)
    form = forms.CommentForm(instance=comment)
    return render(request, 'edit_comment.html', {'form': form, 'post': comment.post})
