# Create your views here.
from django.shortcuts import render, redirect
from .models import News
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.core.paginator import Paginator

from rest_framework import generics
from .serializers import NewsSerializer

from .search_engine import duck_duck_go


def show_all(request):
    news = News.objects.all().order_by("-time")
    paginator = Paginator(news, 16)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'app_1/show_all.html',
        {'news': page_obj
         }
    )


def main(request):
    return redirect('main')


def page_not_found(request, *args, **argv):
    return redirect('main')


def show_item(request, item_id):
    item = News.objects.get(pk=item_id)
    return render(
        request,
        'app_1/show_item.html',
        {'item': item}
    )


def delete_item(request, item_id):
    News.objects.filter(pk=item_id).delete()
    return redirect('main')


def login(request):
    return render(request, 'app_1/login.html')


def SearchResultsView(request):
    query = request.GET.get("q")
    google_response, ddg_response = duck_duck_go(query=query), duck_duck_go(query=query)
    data = ddg_response + google_response

    return render(
        request,
        'app_1/search_result.html',
        {'news': data}
    )


def search(request):
    return render(request, 'app_1/search.html')


class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'


# Api Serializer
class MultiNewsAPIView(generics.ListCreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class NewsAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
