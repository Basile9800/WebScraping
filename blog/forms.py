from django import forms

from .models import Post, CSVImport

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)
        
class CSVImportForm(forms.ModelForm):
    class Meta:
        model = CSVImport
        fields = ('csv_file',)