from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from .models import Actor, Genre, CinemaHall, Movie
from .serializers import ActorSerializer, GenreSerializer, CinemaHallSerializer, MovieSerializer


# Genre - APIView
class GenreListCreateAPIView(APIView):
    def get(self, request):
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GenreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GenreDetailAPIView(APIView):
    def get_object(self, pk):
        return Genre.objects.get(pk=pk)

    def get(self, request, pk):
        genre = self.get_object(pk)
        serializer = GenreSerializer(genre)
        return Response(serializer.data)

    def put(self, request, pk):
        genre = self.get_object(pk)
        serializer = GenreSerializer(genre, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def patch(self, request, pk):
        genre = self.get_object(pk)
        serializer = GenreSerializer(genre, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        genre = self.get_object(pk)
        genre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Actor - GenericAPIView
class ActorListCreateAPIView(GenericAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

    def get(self, request):
        actors = self.get_queryset()
        serializer = self.get_serializer(actors, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ActorDetailAPIView(GenericAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

    def get_object(self, pk):
        return self.get_queryset().get(pk=pk)

    def get(self, request, pk):
        actor = self.get_object(pk)
        serializer = self.get_serializer(actor)
        return Response(serializer.data)

    def put(self, request, pk):
        actor = self.get_object(pk)
        serializer = self.get_serializer(actor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def patch(self, request, pk):
        actor = self.get_object(pk)
        serializer = self.get_serializer(actor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        actor = self.get_object(pk)
        actor.delete()
        return Response(status=204)


# CinemaHall - GenericViewSet
class CinemaHallViewSet(viewsets.GenericViewSet,
                        generics.ListAPIView,
                        generics.CreateAPIView,
                        generics.RetrieveAPIView,
                        generics.UpdateAPIView,
                        generics.DestroyAPIView):
    queryset = CinemaHall.objects.all()
    serializer_class = CinemaHallSerializer


# Movie - ModelViewSet
class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
