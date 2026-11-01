from django.urls import path
from .views import AdListCreateView, AdDetailView, ReviewListCreateView, ReviewDetailView

urlpatterns = [
    path('', AdListCreateView.as_view(), name='ad-list-create'),
    path('<int:pk>/', AdDetailView.as_view(), name='ad-detail'),
    path('reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'), # <--- Новый путь
]