from django.db.models import Avg
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.text import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from account.models import Follower
from song.serializers import CommentSerializer, FavoriteSerializer, LikeSerializer

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(min_length=6, required=True, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2', 'is_author')

    def validate(self, attrs):
        password2 = attrs.pop('password2')
        if attrs.get('password') != password2:
            raise serializers.ValidationError('passwords did not match')
        if not attrs.get('password').isalnum():
            raise serializers.ValidationError('password must contain alpha and nums')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(TokenObtainPairSerializer):
    password = serializers.CharField(min_length=6, write_only=True)

    def validate(self, attrs):
        email = attrs.pop('email')
        password = attrs.pop('password')
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User not ')
        user = authenticate(username=email, password=password)
        if user and user.is_active:
            refresh = self.get_token(user)
            attrs['refresh'] = str(refresh)
            attrs['access'] = str(refresh.access_token)
        else:
            raise serializers.ValidationError('invalid password')
        return attrs


class CreateNewPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=30, required=True)
    code = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(min_length=6, required=True)
    password2 = serializers.CharField(min_length=6, required=True)

    def validate(self, attrs):
        password = attrs['password']
        password2 = attrs.pop('password2')
        if password != password2:
            raise serializers.ValidationError('passwords did not match')
        email = attrs['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('Email does not exists')
        code = attrs['code']
        if user.activation_code != code:
            raise serializers.ValidationError('Code is incorrect')
        attrs['user'] = user
        return attrs

    def save(self, **kwargs):
        data = self.validated_data
        user = data['user']
        user.set_password(data['password'])
        user.activation_code = ''
        user.save()

        return user


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=25, required=True)


class LogOutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    default_error_messages = {
        'bad_token': _('Token is invalid or expired!')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')


class CreateAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('is_author', )

        def validate(self, attrs):
            if attrs.get('is_author') is True:
                return KeyError('You are already have rights to release tracks')
            else:
                return attrs


class FollowerSerializer(serializers.ModelSerializer):
    listener = serializers.ReadOnlyField(source='listener.email')

    class Meta:
        model = Follower
        fields = ('listener', 'singer')


class UserViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('password', 'is_superuser', 'user_permissions')


class UserListViewSerializer(serializers.ModelSerializer):
    class Meta:
        model =User
        fields = ('id', 'email', 'last_name', 'first_name', 'is_author', 'date_joined' )

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['likes'] = LikeSerializer(instance.likes, many=True).data
        repr['rating'] = instance.ratings.aggregate(Avg('mark'))
        repr['favorites'] = FavoriteSerializer(instance.favorites, many=True).data
        repr['comments'] = CommentSerializer(instance.comments, many=True).data
        return repr


