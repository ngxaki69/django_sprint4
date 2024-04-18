from django import forms

from .models import Post, Comment


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateInput(attrs={'type': 'datetime-local',
                                               'format': '%Y-%m-%dT%H:%M'})}


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        exclude = ('author', 'post', 'pub_date', 'is_published',)
