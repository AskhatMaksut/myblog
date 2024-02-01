from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView, LoginView


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(
        template_name='login.html',
        next_page=reverse_lazy('index')
    ), name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('index')), name='logout'),
    path('my_blogs/', MyBlogsView.as_view(), name='my_blogs'),
    path('add_blog/', AddBlogView.as_view(), name='add_blog'),
    path('edit_blog/<int:pk>/', EditBlogView.as_view(), name='edit_blog'),
    path('delete_blog/<int:pk>/', DeleteBlogView.as_view(), name='delete_blog'),
    path('add_comment/<int:pk>/', AddCommentView.as_view(), name='add_comment'),
    path('search/', SearchView.as_view(), name='search')
]