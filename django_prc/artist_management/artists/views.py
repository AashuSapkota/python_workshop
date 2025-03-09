from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated
from .models import Artists, Music
from .serializers import ArtistSerializer, MusicSerializer
import csv
from rest_framework.parsers import FileUploadParser
from django.http import HttpResponse


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
        

class ListArtistMusicAPI(APIView):
    serializer_class = MusicSerializer
    template_name = 'artists/list_artists_music.html'

    def get(self, request, *args, **kwargs):
        artist_id = kwargs["artist_id"]
        return render(request, self.template_name, {'artist_id':artist_id})
    
    def post(self, request, *args, **kwargs):
        artist_id = kwargs["artist_id"]
        print(artist_id)
        musics = Music.objects.filter(artist_id=artist_id)
        serializer = self.serializer_class(musics, many=True)
        return Response(serializer.data, status=200)


class RegisterMusicAPI(APIView):
    template_name = 'artists/register_artist_music.html'

        
    def get(self, request, *args, **kwargs):
        artist_id = kwargs["artist_id"]
        genre_choices = Music.GENRE_CHOICES
        return render(request, self.template_name, {'genre_choices': genre_choices, 'artist_id': artist_id})
    def post(self, request, *args, **kwargs):
        serializer = MusicSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return Response({'Status': 'Success', 'Message': 'Artist Added Successfully'}, status=201)
        except serializers.ValidationError as e:
            print(e)
            return Response({'Status': 'Error', 'Message': str(e.detail)}, status=400)


class DeleteArtistMusicAPI(APIView):
    def delete(self, request, *args, **kwargs):
        music_id = kwargs["music_id"]
        try:
            artist = Music.objects.get(pk=music_id)
            artist.delete()
            print("music deleted")
            return Response({'Status': 'Success', 'Message': 'Music Deleted Successfully'}, status=200)

        except Exception as e:
            return Response({'Status': 'Error', 'Message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class UpdateArtistMusicAPI(APIView):
    template_name='artists/update_artists_music.html'
    
    def get(self, request, *args, **kwargs):
        print("GET")
        id = kwargs['music_id']
        genre_choices = Music.GENRE_CHOICES
        try:
            music = Music.objects.get(id=id)
            artist_id = music.artist_id
            artist = Artists.objects.get(id = artist_id)
            return render(request, self.template_name, {'music':music, 'artist':artist, 'genre_choices':genre_choices})
        except Exception as e:
            print(str(e))
    def put(self, request, *args, **kwargs):
        id = kwargs['music_id']
        try:
            artist = Music.objects.get(pk=id)
            serializer = MusicSerializer(artist, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'Status': 'Success', 'Message': 'Music Updated Succesfully'}, status=200)
            else:
                return Response({'Status': 'Error', 'Message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Artists.DoesNotExist:
            return Response({'Status': 'Error', 'Message': 'Music does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'Status': 'Error', 'Message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ArtistsExportAPI(APIView):
    def get(self, request, *args, **kwargs):
        artists = Artists.objects.all()

        # create the CSV response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="artists.csv"'

        # create a csv writer
        writer = csv.writer(response)

        # write the header row
        writer.writerow(['Name', 'DOB', 'Gender', 'Address', 'First Release Year', 'No of Albums'])

        # write artist data rows
        for artist in artists:
            writer.writerow([artist.name, artist.dob.date(), artist.gender, artist.address, artist.first_release_year, artist.no_of_albums_released])
        
        return response
    

class ArtistsUploadAPI(APIView):
    permission_classes = [IsAuthenticated]
    parser_class = (FileUploadParser,)

    def post(self, request, format=None):
        try:
            file = request.data['file']
        except Exception as e:
            return Response({'Status':'Error', 'Message':'No file found.'}, status=400)
        
        artists_data = file.read().decode('utf-8')
        artists_list = list(csv.DictReader(artists_data.splitlines()))
        serializer = ArtistSerializer(data=artists_list, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'Status': 'Success', 'Message': 'Artists Uploaded Successfully'}, status=201)
        return Response({'Status':'Error', 'Message':str(serializer.errors)}, status=400)
