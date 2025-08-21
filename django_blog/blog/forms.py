from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment, Tag

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags'] 
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write your comment...'}),
        }
        
class TagWidget(forms.TextInput):
    
    """
    Custom widget for entering tags as comma-separated values.
    """
    def format_value(self, value):
        if isinstance(value, list):
            return ", ".join([tag.name for tag in value])
        return value


class PostForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        widget=TagWidget(attrs={'placeholder': 'Enter tags separated by commas'})
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()

        # Handle tags
        tags_data = self.cleaned_data.get('tags', '')
        tag_names = [t.strip() for t in tags_data.split(',') if t.strip()]

        instance.tags.clear()
        for name in tag_names:
            tag, created = Tag.objects.get_or_create(name=name)
            instance.tags.add(tag)

        return instance