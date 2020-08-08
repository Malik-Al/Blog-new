from django import forms
from webapp.models import Article, Comment




class ArticleForm(forms.ModelForm):
    tags = forms.CharField(max_length=200, required=False, label='Тэги')
    class Meta:
        model = Article
        exclude = []




class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = []



class ArticleCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = []


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label="Найти")




#Tag.objects.get_or_create(name='Food')[0].id
