from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Comment
from .forms import PostForm, CommentForm, RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login,logout
from django.db.models import Q

def home(request):
    query = request.GET.get('query')
    category_slug = request.GET.get('category')
    posts = Post.objects.filter(status='published').order_by('-created_at')
    
    if query:
        posts = posts.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(category__name__icontains=query)
        )
    if category_slug:
        posts = posts.filter(category__slug=category_slug)

    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    categories = Category.objects.all()
    recent_posts = Post.objects.filter(status='published').order_by('-created_at')[:5]
    
    return render(request, 'blog/home.html', {'posts': posts, 'query': query, 'category_slug': category_slug, 'categories': categories, 'recent_posts': recent_posts})

def category_posts(request, slug):
    # Get category based on slug
    category = get_object_or_404(Category, slug=slug)

    # Get all posts inside this category
    posts = Post.objects.filter(category=category,status='published').order_by('-created_at')

    return render(request, 'blog/home.html', {
        'category': category,
        'posts': posts
    })

def recent_posts(request):
    posts = Post.objects.filter(status='published').order_by('-created_at')[:5]
    return render(request, 'home.html', {'posts': posts})

def search_posts(request):
    query = request.GET.get('query', '')  
    posts = []

    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(category__name__icontains=query)
        ).order_by('-created_at')

    return render(request, 'blog/search_results.html', {
        'query': query,
        'posts': posts
    })

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    comments = post.comments.all()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to comment')
            return redirect('login')
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect(post.get_absolute_url())
        else:
            messages.warning(request,"Comment cannot be empty.")
    else:
        comment_form = CommentForm()

    return render(request, 'blog/post_detail.html', {'post': post, 'comments': post.comments.all(),'comment_form': comment_form})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('home')   # change if needed
    else:
        form = UserCreationForm()

    return render(request, 'blog/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('home')   # update if needed
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'blog/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')   

@login_required
def dashboard(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, 'blog/dashboard.html', {'posts': posts})

@login_required
def post_create(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created')
            return redirect('dashboard')
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated')
            return redirect('dashboard')
    return render(request, 'blog/post_form.html', {'form': form, 'post': post})

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        body = request.POST.get("body")

        if body:
            Comment.objects.create(
                post=post,
                user=request.user,
                body=body,
            )
            messages.success(request, "Comment added successfully!")
        else:
            messages.warning(request, "Comment cannot be empty.")

        return redirect('post_detail', slug=post.slug)

    return redirect('post_detail', slug=post.slug)

@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    # Permission: user must be comment owner, post author, or staff
    if request.user == comment.user or request.user == comment.post.user or request.user.is_staff:
        comment.delete()
        messages.success(request, "Comment deleted successfully.")
    else:
        messages.error(request, "You do not have permission to delete this comment.")

    return redirect('post_detail', slug=comment.post.slug)

@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        post.delete()
        messages.success(request, "Post has been deleted successfully.")
        return redirect('dashboard')  # Replace 'post_list' with your list view name

    # If GET request, show a confirmation page
    return render(request, 'post_confirm_delete.html', {'post': post})
