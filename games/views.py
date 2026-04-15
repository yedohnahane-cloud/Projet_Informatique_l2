from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Game
from .serializers import GameSerializer


class StudentGameListView(generics.ListAPIView):
    serializer_class = GameSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Game.objects.filter(is_active=True)

        category = self.request.query_params.get("category")
        if category:
            queryset = queryset.filter(category=category)

        return queryset