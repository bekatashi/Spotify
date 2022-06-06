from rest_framework import serializers
from . import models
from django.db.models import Avg


class SongSerializer(serializers.ModelSerializer):
    performer = serializers.ReadOnlyField(source='performer.email')

    class Meta:
        model = models.Song
        fields = '__all__'

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['likes'] = instance.likes.count()
        repr['rating'] = instance.ratings.aggregate(Avg('mark'))
        repr['favorited'] = instance.favorites.count()
        repr['comments'] = CommentSerializer(instance.comments, many=True).data
        repr['chat'] = 'if you want to chat with others then click on the link: http://10.117.9.143:8080/'
        return repr


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = models.Like
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = models.Favorite
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Genre
        fields = '__all__'
#
#
#


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = models.Comments
        fields = '__all__'
