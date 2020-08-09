from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.http import urlencode
from django.views import View

from webapp.forms import ArticleForm, CommentForm, SimpleSearchForm, FullSearchForm
from webapp.models import Article
from django.views.generic import TemplateView, ListView, DeleteView, UpdateView, FormView


class IndexView(ListView):
    context_object_name = 'articles'
    model = Article
    template_name = 'article/index.html'
    ordering = ['-created_at']
    paginate_by = 3
    paginate_orphans = 1


    def get(self, request, *args, **kwargs):
        form = SimpleSearchForm(self.request.GET)
        query = None
        if form.is_valid():
            query = form.cleaned_data['search']
        self.form = form
        self.query = query
        return super().get(request, *args, **kwargs)


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        if self.query:
            context['query'] = urlencode({'search': self.query})
        tag_filter = self.request.GET
        if 'tag' in tag_filter:
            context['articles'] = Article.objects.filter(tags__name=tag_filter.get('tag'))
        context['form'] = self.form
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.query:
            queryset = queryset.filter(Q(title__icontains=self.query) | Q(author__icontains=self.query) | Q(tags__name__iexact=self.query))
        return queryset



    def form_valid(self, form):
        self.object = form.save()
        self.parser()
        return redirect(self.get_success_url())

    def parser(self):
        tags = self.request.POST.get('tags')
        tag_list = tags.split(',')
        for tag in tag_list:
            tag, created = Tag.objects.get_or_create(name=tag)
            self.object.tags.add(tag)

    def get_success_url(self):
        return reverse('article_view', kwargs={'pk': self.object.pk})





class ArticleSearchView(FormView):
    template_name = 'article/search.html'
    form_class = FullSearchForm

    def form_valid(self, form):
        text = form.cleaned_data.get('text')
        query = Q()
        if text:
            query = query & self.get_text_query(form, text)

        articles = Article.objects.filter(query).distinct()
        context = self.get_context_data(articles=articles)
        return self.render_to_response(context)


    def get_text_query(self, form, text):
        query = Q()
        in_title = form.cleaned_data.get('in_title')
        if in_title:
            query = query | Q(title__icontains=text)
        in_text = form.cleaned_data.get('in_text')
        if in_text:
            query = query | Q(text__icontains=text)
        in_tags = form.cleaned_data.get('in_tags')
        if in_tags:
            query = query | Q(tags__name__iexact=text)
        in_comment_text = form.cleaned_data.get('in_comment_text')
        if in_comment_text:
            query = query | Q(comments__text__icontains=text)
        return query


class ArticleView(TemplateView):
    template_name = 'article/article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article_pk = kwargs.get('pk')
        article = get_object_or_404(Article, pk=article_pk)
        context['article'] = article
        context['form'] = CommentForm()
        comments = article.comments.order_by('-created_at')
        paginator = Paginator(comments, 3, 0)
        page_numder = self.request.GET.get('page', 1)
        page = paginator.get_page(page_numder)
        context['paginator'] = paginator
        context['page_obj'] = page
        context['comments'] = page.object_list
        context['is_paginated'] = page.has_other_pages()
        return context




class  ArticleCreateView(View):
    def get(self, request, *args, **kwargs):
        form = ArticleForm()
        return render(request, 'article/create.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            article = Article.objects.create(
                title=form.cleaned_data['title'],
                author=form.cleaned_data['author'],
                text=form.cleaned_data['text'],
                category=form.cleaned_data['category']
            )
            return redirect('article_view', pk=article.pk)
        else:
            return render(request, 'article/create.html', context={'form': form})


class ArticleUpdateView(UpdateView):
    model = Article
    template_name = 'article/update.html'
    form_class = ArticleForm
    context_object_name = 'article'


    def get_success_url(self):
        return reverse('article_view', kwargs={'pk': self.object.pk})

    def update_tag(self):
        tags = self.request.POST.get('tags')
        tags_list = tags.split(',')
        self.object.tags.clear()
        for tag in tags_list:
            tag, created = Tag.objects.get_or_create(name=tag)
            self.object.tags.add(tag)

    def get_form(self, form_class=None):
        form = super().get_form(form_class=None)
        querry = self.object.tags.values('name')
        res = ''
        for tag in querry:
            res += tag['name'] + ','
        form.fields['tags'].initial = res.replace(' ', '').strip(',')
        return form

    def form_valid(self, form):
        self.object = form.save()
        self.update_tag()
        return redirect(self.get_success_url())







class ArticleDeleteView(DeleteView):
    template_name = 'article/delete.html'
    model = Article
    context_key = 'article'
    success_url = reverse_lazy('index')