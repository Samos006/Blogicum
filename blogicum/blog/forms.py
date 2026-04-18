from django import forms
from django.contrib.auth import get_user_model
from .models import Post, Comment

User = get_user_model()


class PostForm(forms.ModelForm):
    """Форма для создания и редактирования поста."""
    class Meta:
        model = Post
        fields = ('title', 'text', 'pub_date', 'location', 'category', 'image')
        widgets = {
        'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class CommentForm(forms.ModelForm):
    """Форма для добавления комментария."""
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ваш комментарий...'}),
        }


class UserProfileForm(forms.ModelForm):
    """Форма для редактирования профиля пользователя."""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
