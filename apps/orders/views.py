from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """ Faqatgina foydalanuvchining o‘z buyurtmalarini ko‘rsatish """
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """ Yangi buyurtma yaratishda foydalanuvchini avtomatik bog‘lash """
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """ Buyurtma o‘chirilganda total price yangilansin """
        order = self.get_object()
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
