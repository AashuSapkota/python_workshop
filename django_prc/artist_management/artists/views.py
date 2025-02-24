from django.shortcuts import render, get_list_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Artists
from .serializers import ArtistSerializer
from .forms import ArtistForm


class RegisterArtistAPI(APIView):
    template_name = 'artists/register_artist.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        serializer = ArtistSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Status': 'Success', 'Message': 'Artist added successfully'}, status=201)
        return Response({'Status': 'Error', 'Message': str(serializer.errors)}, status=400)
    


class ListArtistsAPI(APIView):
    serializer_class = ArtistSerializer
    template_name = 'artists/list_artists.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        artists = Artists.objects.all()
        serializer = self.serializer_class(artists, many=True)
        return Response(serializer.data, status=200)
   
    
class UpdateArtistAPI(APIView):
    serializer_class = ArtistSerializer
    template_name='artists/update_artist.html'

    def get(self, request, *args, **kwargs):
        id = kwargs['artist_id']
        try:
            artist = Artists.objects.get(id=id)
            return render(request, self.template_name, {'artist':artist})
        except Exception as e:
            print(str(e))

    def put(self, request, *args, **kwargs):
        id = kwargs['artist_id']
        try:
            artist = Artists.objects.get(pk=id)
            serializer = ArtistSerializer(artist, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'Status': 'Success', 'Message': 'Artist updated successfully'}, status=200)
            else:
                return Response({'Status': 'Error', 'Message': str(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)
        except Artists.DoesNotExist:
            return Response({'Status': 'Error', 'Message': 'Artist does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'Status': 'Error', 'Message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteArtistAPI(APIView):
    def delete(self, request, *args, **kwargs):
        id = kwargs['artist_id']
        try:
            artist = Artists.objects.get(id=id)
            artist.delete()
            return Response({'Status': 'Success', 'Message': 'Artist Deleted Successfully'}, status=200)
        except Exception as e:
            return Response({'Status': 'Error', 'Message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


