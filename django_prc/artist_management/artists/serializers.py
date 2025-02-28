from rest_framework import serializers
from .models import Artists, Music
from datetime import datetime


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artists
        fields = ['id','name', 'dob', 'gender', 'address', 'first_release_year',
                   'no_of_albums_released', 'created_at', 'updated_at']

    def create(self, validated_data):
        created_at = datetime.now()
        updated_at = datetime.now()
        artist = Artists.objects.create(created_at=created_at,
                                         updated_at=updated_at, **validated_data)
        return artist

    def validate_no_of_albums_released(self, value):
        if value <= 0:
            raise serializers.ValidationError({
                "Status": "Error",
                "Message":"Invalid number of albums released. Must be a positive integer"
            })
        return value
    
    def validate_first_release_year(self, value):
        if not str(value).isdigit() or len(str(value)) != 4 or int(value) > datetime.now().year:
            raise serializers.ValidationError({
                "Status": "Error",
                "Message":"Invalid first release year. Must be a valid 4-digit year between 1900 and the current year."
            })
        return value
    

class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = ['id', 'artist_id', 'title', 'album_name', 'genre', 'created_at', 'updated_at']
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)

        try:
            artist_id = Artists.objects.get(pk=ret['artist_id'])
            artist_name = artist_id.name
            ret['artist_name'] = artist_name
        except:
            ret['artist_name'] = ""
        
        return ret
    
    def validate(self, attrs):
        artist_id = attrs.get('artist_id')
        if artist_id:
            try:
                artist = Artists.objects.get(pk=artist_id)
            except Artists.DoesNotExist:
                raise serializers.ValidationError({
                    'Status': 'Error',
                    'Message': 'Invalid artist_id'
                })
        return attrs

    
    def create(self, validated_data):
        created_at = datetime.now()
        updated_at = datetime.now()
        music = Music.objects.create(created_at=created_at, updated_at=updated_at, **validated_data)
        return music