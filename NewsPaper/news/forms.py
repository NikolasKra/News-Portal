from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):
    

    class Meta:
        model = Post
        fields = ['post_author', 'title', 'post_text','category' ]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        post_text = cleaned_data.get("post_text")
        category = cleaned_data.get("category")




        if title == post_text:
            raise ValidationError(
                "Заголовок не должен быть идентичен содержанию."
            )

        return cleaned_data