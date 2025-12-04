from django.urls import path
from . import views

urlpatterns = [
path('', views.home, name='home'),
path('page/<int:page>/', views.home, name='home-paged'),
path('post/<slug:slug>/', views.post_detail, name='post_detail'),
path('create/', views.post_create, name='post_create'),
path('edit/<slug:slug>/', views.post_edit, name='post_edit'),
path('delete/<slug:slug>/', views.post_delete, name='post_delete'),
path('category/<slug:slug>/', views.category_posts, name='category_posts'),
path('search/', views.search_posts, name='search_posts'),
path('dashboard/', views.dashboard, name='dashboard'),
path('signup/', views.signup_view, name='signup'),
path('login/', views.login_view, name='login'),
path('logout/', views.logout_view, name='logout'),
path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
path('comment-delete/<int:pk>/', views.comment_delete, name='comment_delete'),
]