from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import CommentForm, PostForm, UserProfileForm
from .models import Category, Comment, Post

User = get_user_model()


# Список постов с учётом прав
def get_posts_for_user(request, author=None):
    now = timezone.now()
    if author is not None:
        posts = Post.objects.filter(author=author)
    else:
        posts = Post.objects.all()

    if request.user.is_authenticated and author == request.user:
        return posts
    return posts.filter(
        is_published=True,
        pub_date__lte=now,
        category__is_published=True
    )


# Миксин для проверки доступа к отдельному посту
class PostAccessMixin:
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        is_public = (
            self.object.is_published and
            self.object.pub_date <= timezone.now() and
            self.object.category.is_published
        )
        if not (is_public or (request.user.is_authenticated and request.user == self.object.author)):
            raise Http404("Пост не найден")
        return super().dispatch(request, *args, **kwargs)


# Главная страница
class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'page_obj'
    paginate_by = 10
    ordering = '-pub_date'

    def get_queryset(self):
        return get_posts_for_user(self.request)


# Страница категории
class CategoryPostsView(ListView):
    template_name = 'blog/category.html'
    context_object_name = 'page_obj'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )
        return get_posts_for_user(self.request).filter(
            category=self.category
        ).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


# Профиль пользователя
class ProfileView(ListView):
    template_name = 'blog/profile.html'
    context_object_name = 'page_obj'
    paginate_by = 10

    def get_queryset(self):
        self.profile_user = get_object_or_404(User, username=self.kwargs['username'])
        return get_posts_for_user(self.request, author=self.profile_user).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.profile_user
        return context


# Детали поста
class PostDetailView(PostAccessMixin, DetailView):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Форма комментария только для авторизованных
        context['form'] = CommentForm() if self.request.user.is_authenticated else None
        # Комментарии с авторами, от старых к новым
        context['comments'] = self.object.comments.select_related('author').order_by('created_at')
        return context


# Миксин для создания/редактирования поста 
class PostEditMixin:
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    
    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.object.author.username})


# Создание поста
class PostCreateView(LoginRequiredMixin, PostEditMixin, CreateView):
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# Редактирование поста
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, PostEditMixin, UpdateView):
    pk_url_kwarg = 'post_id'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def get_success_url(self):
        return reverse('post_detail', args=[self.object.id])


# Удаление поста
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/confirm_delete.html'
    pk_url_kwarg = 'post_id'
    success_url = reverse_lazy('index') 
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    def get_success_url(self):
        return reverse('blog:index')  


# ----- Комментарии -----

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
    return redirect('blog:post_detail', post_id=post_id)


# Редактирование комментария
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.object.post.id])


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление комментария."""
    model = Comment
    template_name = 'blog/confirm_delete.html'
    pk_url_kwarg = 'comment_id'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.object.post.id])


# Редактирование профиля 
class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'blog/profile_edit.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def test_func(self):
        return self.request.user == self.get_object()

    def get_success_url(self):
        return reverse('blog:profile', args=[self.request.user.username])
