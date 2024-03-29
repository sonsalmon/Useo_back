# from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate  #
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token
from .models import User, FollowingRelation


class RegisterSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'nickname')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            nickname=validated_data['nickname'],
        )

        user.set_password(validated_data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user:
            token = Token.objects.get(user=user) #Token에서 유저 찾아서 응답
            return token,user
            # return {"token": token.key,
            #         "nickname" : user.nickname,
            #         "profile_image" : user.profile_image,
            #         "profile_message" : user.profile_message
            #         }
        raise serializers.ValidationError(
            {"error": "Unable to log in with provided credentials."})


class UserSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(max_length=10, required=False)
    class Meta:
        model = User
        fields = ("id","nickname", "profile_message", "profile_image","library_longitude", "library_latitude")
        extra_kwargs = {"profile_image": {"required": False, "allow_null": True},
                        "nickname":{"required":False},
                        "profile_message":{"required":False},
                        "library_longitude":{"required":False},
                        "library_latitude":{"required":False},
                        }
        # exclude = ("password", "groups", "user_permissions") # Cannot set both 'fields' and 'exclude' options on serializer UserSerializer.

    def validate_nickname(self, value):
        instance = self.context['request'].user # request에서 유저정보 가져옴
        print(instance)
        # 현재 인스턴스의 닉네임과 입력된 닉네임이 동일한 경우, 검사를 건너뛰고 값을 반환합니다.
        if instance and instance.nickname == value:
            return value
        # 그렇지 않은 경우, 기본 유일성 검사를 수행합니다.
        if User.objects.filter(nickname=value).exists():
            raise serializers.ValidationError("user with this nickname already exists.")
        return value

class UserByNicknameSerializer(serializers.Serializer):
    nickname = serializers.CharField(required=True)

class FollowingRelationSerializer(serializers.ModelSerializer):

    class Meta:
        model=FollowingRelation
        fields = '__all__'

class FollowingRelationListSerializer(serializers.ModelSerializer):
    following = UserSerializer()
    class Meta:
        model=FollowingRelation
        fields=['following']
