from django import forms
from webapp.models import Article, Comment




class ArticleForm(forms.ModelForm):
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
