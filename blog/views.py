from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Blog, Comment
from django.urls.base import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login
# Create your views here.


class IndexView(ListView):
    template_name = 'index.html'
    model = Blog


class RegistrationView(CreateView):
    template_name = 'sign_up.html'
    model = User
    success_url = reverse_lazy('index')
    fields = ['username', 'email', 'password']

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class MyBlogsView(ListView):
    template_name = 'myblogs.html'
    model = Blog

    def get_queryset(self):
        return Blog.objects.filter(
            author_id=self.request.user.id
        )


class AddBlogView(CreateView):
    template_name = 'add_blog.html'
    model = Blog
    success_url = '/'
    fields = ['title', 'content', 'tags', 'image']

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            form.instance.author = User(pk=request.user.id)
            return self.form_valid(form)
        return self.form_invalid(form)


class EditBlogView(UpdateView):
    template_name = 'add_blog.html'
    model = Blog
    success_url = '/'
    fields = ['title', 'content', 'tags', 'image']

    def get(self, request, *args, **kwargs):
        get_object_or_404(Blog,
            pk=kwargs['pk'], author_id=request.user.id
        )
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        get_object_or_404(Blog,
            pk=kwargs['pk'], author_id=request.user.id
        )
        return super().post(request, *args, **kwargs)


class DeleteBlogView(DeleteView):
    template_name = 'delete_blog.html'
    model = Blog
    success_url = reverse_lazy('index')
    fields = ['author', 'title', 'content', 'image']

    def get(self, request, *args, **kwargs):
        get_object_or_404(Blog,
                          pk=kwargs['pk'], author_id=request.user.id
                          )
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        get_object_or_404(Blog,
                          pk=kwargs['pk'], author_id=request.user.id
                          )
        return super().post(request, *args, **kwargs)


class AddCommentView(CreateView):
    template_name = 'comments.html'
    model = Comment
    success_url = '/'
    fields = ['comment']

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid() and request.user.is_authenticated:
            form.instance.username = request.user.username
            form.instance.blog = Blog(pk=kwargs['pk'])
            self.form_valid(form)
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blog'] = get_object_or_404(Blog, pk=self.kwargs['pk'])
        context['comments'] = Comment.objects.filter(blog_id=Blog(pk=self.kwargs['pk']))
        return context


class SearchView(ListView):
    template_name = 'index.html'
    model = Blog

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Blog.objects.filter(tags__contains=query)
