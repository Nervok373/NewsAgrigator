from django.urls import path
from . import views

urlpatterns = [
    path('', views.main),
    path('items', views.show_all, name='main'),
    path('items/<int:item_id>', views.show_item, name='item'),
    path('login', views.login, name='login'),
    path('logout', views.delete_item, name='logout'),
    path('register', views.SignUp.as_view(), name='register'),
    path('api/news', views.MultiNewsAPIView.as_view(), name='api'),
    path('api/news/<int:pk>', views.NewsAPIView.as_view()),
    path('search', views.search, name='search'),
    path('search/', views.SearchResultsView, name='search_req')
]

