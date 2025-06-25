from rest_framework import viewsets
from rest_framework.permissions import SAFE_METHODS
from .models import Category
from .serializers import CategorySerializer
from .permissions import IsSuperUser, IsStaff
from product.models import Review
from product.serializers import ReviewSerializer
from rest_framework.permissions import IsAuthenticated

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS: 
            return []
        return [IsSuperUser()] 
    

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.request.method in ['POST']:
            return [IsAuthenticated()]  # создание — только авторизованные
        elif self.request.method in SAFE_METHODS:
            return []  # просмотр — всем
        else:
            return [IsStaff()]  # изменение/удаление — только staff

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)