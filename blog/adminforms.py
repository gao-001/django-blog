from django import forms
from mdeditor.fields import MDTextFormField
from mdeditor.widgets import MDEditorWidget




class PostAdminForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea, label='摘要', required=False)
    content = forms.CharField(widget=MDEditorWidget(),label='正文', required=True)
