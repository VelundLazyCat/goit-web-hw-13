from django.shortcuts import render, get_object_or_404, redirect
from .utils import get_mongodb
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Author, Tag, Quote
from .forms import TagForm, QuoteForm, AuthorForm


def main(request, page=1):
    quotes = Quote.objects.filter().all()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(request, 'quotes/index.html', context={"quotes": quotes_on_page})


@login_required()
def tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotes:main')
        else:
            return render(request, 'quotes/tag.html', {'form': form})

    return render(request, 'quotes/tag.html', {'form': TagForm()})


@login_required()
def quote(request):
    tags = Quote.objects.all()

    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_note = form.save()
            form.save()
            choice_tags = Tag.objects.filter(
                name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                new_note.tags.add(tag)

            return redirect(to='quotes:main')
        else:
            return render(request, 'quotes/quote.html', {"tags": tags, 'form': form})

    return render(request, 'quotes/quote.html', {"tags": tags, 'form': QuoteForm()})


@login_required()
def author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotes:main')
        else:
            return render(request, 'quotes/authoradd.html', {'form': form})

    return render(request, 'quotes/authoradd.html', {'form': AuthorForm()})


def detail(request, quote_id):
    quote = get_object_or_404(Quote, pk=quote_id)
    return render(request, 'quotes/detail.html', {"quote": quote})


@login_required
def delete_quote(request, quote_id):
    Quote.objects.get(pk=quote_id).delete()
    return redirect(to='quotes:main')


def author_page(request, fullname):
    authors = get_object_or_404(Author, fullname=fullname)

    return render(request, "quotes/author.html", {"author": authors})
