from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserRegisterForm, PostForm, CommentForm
from django.contrib import messages
from .models import Post, Comment

# User Registration
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto-login after registration
            return redirect('profile')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})

# User Profile
@login_required
def profile(request):
    if request.method == 'POST':
        request.user.email = request.POST.get("email")
        request.user.save()
        return redirect('profile')
    return render(request, 'blog/profile.html')

# Login (built-in)
class CustomLoginView(LoginView):
    template_name = 'blog/login.html'

# Logout (built-in)
class CustomLogoutView(LogoutView):
    template_name = 'blog/logout.html'
    
    
    
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, DetailView,
    CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from .models import Post
from .forms import PostForm


# List all posts
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'  # custom template
    context_object_name = 'posts'
    ordering = ['-published_date']


# Detail view for a single post
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'


# Create new post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# Update existing post
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


# Delete post
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    
# Display post + comments + add new comment
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all().order_by('-created_at')

    if request.method == "POST":
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                messages.success(request, "Your comment has been added.")
                return redirect('post-detail', pk=post.pk)
        else:
            messages.error(request, "You must be logged in to comment.")
            return redirect('login')
    else:
        form = CommentForm()

    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'form': form})


@login_required
def comment_update(request, pk):
    comment = get_object_or_404(Comment, pk=pk, author=request.user)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Your comment has been updated.")
            return redirect('post-detail', pk=comment.post.pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/comment_form.html', {'form': form})


@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk, author=request.user)
    post_id = comment.post.pk
    if request.method == "POST":
        comment.delete()
        messages.success(request, "Your comment has been deleted.")
        return redirect('post-detail', pk=post_id)
    return render(request, 'blog/comment_confirm_delete.html', {'comment': comment})
