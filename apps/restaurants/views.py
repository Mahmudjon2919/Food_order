from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import RestaurantInfo, Dish, Rating
from .serializers import RestaurantInfoSerializer, DishSerializer, RatingSerializer

class RestaurantInfoView(generics.RetrieveAPIView):
    queryset = RestaurantInfo.objects.all()
    serializer_class = RestaurantInfoSerializer

    def get_object(self):
        return RestaurantInfo.objects.first()

class RestaurantMenuView(generics.ListAPIView):
    queryset = Dish.objects.filter(is_active=True)
    serializer_class = DishSerializer

class DishDetailView(generics.RetrieveAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer

class RateDishView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        dish = Dish.objects.filter(id=id, is_active=True).first()
        if not dish:
            return Response({"error": "Bunday taom mavjud emas!"}, status=status.HTTP_404_NOT_FOUND)

        data = {"dish": dish.id, "rating": request.data.get("rating")}
        serializer = RatingSerializer(data=data, context={"request": request})

        if serializer.is_valid():
            serializer.save(user=request.user)
            dish.update_average_rating()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
