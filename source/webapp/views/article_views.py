from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View

from webapp.forms import ArticleForm, CommentForm
from webapp.models import Article
from django.views.generic import TemplateView, ListView, DeleteView, UpdateView


class IndexView(ListView):
    context_object_name = 'articles'
    model = Article
    template_name = 'article/index.html'
    ordering = ['-created_at']
    paginate_by = 3
    paginate_orphans = 1



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



#
# class ArticleUpdateView(View):
#     def get(self, request, *args, **kwargs):
#         article_pk = kwargs.get('pk')
#         article = get_object_or_404(Article, pk=article_pk)
#         form = ArticleForm(data={
#             'title': article.title,
#             'text': article.text,
#             'author': article.author,
#             'category': article.category_id
#
#         })
#         return render(request, 'article/update.html', context={'form': form, 'article': article})
#
#     def post(self, request, *args, **kwargs):
#         article_pk = kwargs.get('pk')
#         article = get_object_or_404(Article, pk=article_pk)
#         form = ArticleForm(data=request.POST)
#         if form.is_valid():
#             article.title = form.cleaned_data['title']
#             article.text = form.cleaned_data['text']
#             article.author = form.cleaned_data['author']
#             article.category = form.cleaned_data['category']
#             article.save()
#             return redirect('article_view', pk=article.pk)
#         else:
#             return render(request, 'article/update.html', context={'form': form, 'article': article})
#


# class ArticleDeleteView(View):
#     def get(self, request, *args, **kwargs):
#         article_pk = kwargs.get('pk')
#         article = get_object_or_404(Article, pk=article_pk)
#         return render(request, 'article/delete.html', context={'article': article})
#
#     def post(self, request, *args, **kwargs):
#         article_pk = kwargs.get('pk')
#         article = get_object_or_404(Article, pk=article_pk)
#         article.delete()
#         return redirect('index')


class ArticleUpdateView(UpdateView):
    model = Article
    template_name = 'article/update.html'
    form_class = ArticleForm
    context_object_name = 'article'

    def get_success_url(self):
        return reverse('article_view', kwargs={'pk': self.object.pk})






class ArticleDeleteView(DeleteView):
    template_name = 'article/delete.html'
    model = Article
    context_key = 'article'
    success_url = reverse_lazy('index')