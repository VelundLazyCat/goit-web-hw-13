from django.forms import ModelForm, CharField, TextInput, ModelChoiceField, ModelMultipleChoiceField, SelectMultiple
from .models import Tag, Quote, Author


class TagForm(ModelForm):
    name = CharField(min_length=3, max_length=125,
                     required=True, widget=TextInput())

    class Meta:
        model = Tag
        fields = ['name']


class QuoteForm(ModelForm):
    quote = CharField(required=True, widget=TextInput())
    author = ModelChoiceField(required=False, queryset=Author.objects.all(), widget=SelectMultiple(
        attrs={"class": "form-select", "size": "7"}))
    tags = CharField(required=False, widget=TextInput())

    class Meta:
        model = Quote
        fields = ['quote', 'tags', 'author']


class AuthorForm(ModelForm):
    fullname = CharField(max_length=250, widget=TextInput())
    born_date = CharField(widget=TextInput())
    born_location = CharField(widget=TextInput())
    description = CharField(widget=TextInput())

    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']
