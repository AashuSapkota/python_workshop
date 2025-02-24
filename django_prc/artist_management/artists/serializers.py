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
    
    