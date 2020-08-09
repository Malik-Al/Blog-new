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




class FullSearchForm(forms.Form):
    text = forms.CharField(max_length=100, required=False, label='По тексту')
    in_title = forms.BooleanField(initial=True, required=False, label='В заголовке')
    in_text = forms.BooleanField(initial=True, required=False, label='В тексте')
    in_tags = forms.BooleanField(initial=True, required=False, label='В тегах')
    in_comment_text = forms.BooleanField(initial=False, required=False, label='В комментариях')

    author = forms.CharField(max_length=100, required=False, label='По автору')
    article_author = forms.BooleanField(initial=True, required=False, label='Статьи')
    comment_author = forms.BooleanField(initial=False, required=False, label='Комментария')

    def clean(self):
        super().clean()
        data = self.cleaned_data
        if data.get('text'):
            if not (data.get('in_title') or data.get('in_text')
                    or data.get('in_tags') or data.get('in_comment_text')):
                raise ValidationError('One of the following checkboxes should be checked: '
                                  'In title, In text, In tags, In comment text ',
                                  code='text_search_criteria_empty')
        if data.get('author'):
            if not (data.get('article_author') or data.get('comment_author')):
                raise ValidationError('One of the following checkboxes should be checked: '
                                      'articles, comments  ',
                                      code='author_search_criteria_empty')


        if not data.get('text') and not data.get('author'):
            raise ValidationError('One of the following checkboxes should be checked: '
                                  'Text search or Author search')

        return data
