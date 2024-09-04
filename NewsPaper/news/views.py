from datetime import datetime
from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView , CreateView, UpdateView , DeleteView
from .models import Post
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin



class PostList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'post_list.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        context['next_sale'] = None
        return context
    


class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'post_detail.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()  # Добавляет текущую UTC дату и время
        return context


class PostSearch(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'post_search.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET , queryset = queryset )
        return self.filterset.qs
     
    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       # Добавляем в контекст объект фильтрации.
       context['filterset'] = self.filterset
       return context

class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    

    def get_template_names(self):
        if self.request.path == '/news/articles/create/':
            return 'post_article_create.html'
        return'post_create.html'

    def form_valid(self, form):
        
        post = form.save(commit=False)
        if self.request.path == '/news/articles/create/':

            post.choice = 'AR'
        post.save()
        return super().form_valid(form)

class PostUpdate(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    

    def get_template_names(self):
        if self.request.path == '/articles/<int:pk>/edit/':
            return 'post_articles_update.html'
        return'post_update.html'
    
    def form_valid(self, form):
        
        post = form.save(commit=False)
        if self.request.path == '/articles/<int:pk>/edit/':

            post.choice = 'AR'
        post.save()
        return super().form_valid(form)
    
  

class PostDelete(DeleteView):
    model = Post
    

    def get_template_names(self):
        if self.request.path == '/articles/<int:pk>/delete/':
            return 'post_articles_delete.html'
        return'post_delete.html'
    
    def form_valid(self, form):
        
        post = form.save(commit=False)
        if self.request.path == '/articles/<int:pk>/delete/':

            post.choice = 'AR'
        post.save()
        return super().form_valid(form)

    
    