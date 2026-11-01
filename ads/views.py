from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Ad, Review
from .serializers import AdSerializer, ReviewSerializer
from .permissions import IsOwnerOrAdmin


# 1. СПИСОК И СОЗДАНИЕ ОБЪЯВЛЕНИЙ
class AdListCreateView(generics.ListCreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    # Анонимный может читать, авторизованный - создавать
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# 2. ДЕТАЛИ, РЕДАКТИРОВАНИЕ И УДАЛЕНИЕ ОБЪЯВЛЕНИЯ
class AdDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    # Читать может любой, редактировать - только владелец или админ
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrAdmin]


# 3. СПИСОК И СОЗДАНИЕ ОТЗЫВОВ
class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # Список комментариев и создание — только для авторизованных (по заданию)
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# 4. ДЕТАЛИ, РЕДАКТИРОВАНИЕ И УДАЛЕНИЕ ОТЗЫВА
class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # Читать может любой авторизованный, редактировать - только владелец или админ
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]