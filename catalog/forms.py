from django import forms
from .models import Author

class BookFilterForm(forms.Form):
    authors = forms.ModelMultipleChoiceField(
        queryset=Author.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False  # Щоб можна було надсилати форму без вибору авторів
    )
