from django import forms
from .models import Comment
import mistune

class CommentForm(forms.ModelForm):


    def clean_content(self):
        cleaned_data = self.cleaned_data['content']
        return mistune.markdown(cleaned_data)

    content = forms.CharField(
        max_length=128,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'style': "width:60%",'placeholder':'写个评论吧'})
    )

    class Meta:
        model = Comment
        fields = ['content']
