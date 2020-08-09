from django import forms
from django.core.exceptions import ValidationError

from webapp.models import Article, Comment




class ArticleForm(forms.ModelForm):
    tags = forms.CharField(max_length=200, required=False, label='Тэги')
    class Meta:
        model = Article
        exclude = ['created_at, updated_at']

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) <= 10:
            raise ValidationError('Title is too short!')
        return title

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['text'] == cleaned_data['title']:
            raise ValidationError("Text of the article should not duplicate it's title!")
        return cleaned_data



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
