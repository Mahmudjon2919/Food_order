from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import RestaurantInfo, Dish, Order, Rating
from .serializers import RestaurantInfoSerializer, DishSerializer, OrderStatusSerializer, RatingSerializer

# GET /api/restaurants/info/
class RestaurantInfoView(generics.ListAPIView):
    queryset = RestaurantInfo.objects.all()
    serializer_class = RestaurantInfoSerializer

# GET /api/restaurants/menu/
class RestaurantMenuView(generics.ListAPIView):
    queryset = Dish.objects.filter(is_active=True)
    serializer_class = DishSerializer

# GET /api/dishes/{id}/
class DishDetailView(generics.RetrieveAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer

# GET /api/orders/{id}/status/
class OrderStatusView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderStatusSerializer

# POST /api/dishes/{id}/rate/
class RateDishView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        dish = Dish.objects.filter(id=id, is_active=True).first()
        if not dish:
            return Response({"error": "Bunday taom mavjud emas yoki o‘chirib tashlangan!"}, status=status.HTTP_404_NOT_FOUND)

        data = {"dish": dish.id, "rating": request.data.get("rating")}
        serializer = RatingSerializer(data=data, context={"request": request})

        if serializer.is_valid():
            serializer.save(user=request.user)
            dish.update_average_rating()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
