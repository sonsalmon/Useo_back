import os

from rest_framework import generics, status, permissions, serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

# from django.contrib.auth.models import User

from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, UserByNicknameSerializer
from .models import User


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token,user = serializer.validated_data # validate() 리턴값 받아옴
        return Response({"token": token.key
                         }, status=status.HTTP_200_OK)


class UserView(generics.GenericAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


    def patch(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user)#인증 토큰으로 누군지 확인함.
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        old_image_path = ''
        if user.nickname != data['nickname']:
            user.nickname = data['nickname']
        user.profile_message = data['profile_message']
        if request.data.get('profile_image'):
            old_image_path = user.profile_image.path
            # request.data.get('profile_image').name = user.username + '_profile.png'
            user.profile_image = request.data['profile_image']
        user.save()

        #기존 프로필 이미지 삭제
        if(os.path.exists(old_image_path)):
            os.remove(old_image_path)
        return Response({"result": "ok"},
                        status=status.HTTP_206_PARTIAL_CONTENT)

    def get(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user)
        serializer = self.get_serializer(user)
        # return Response({"nickname": user.nickname, "profile_image": user.profile_image or None, "profile_message":user.profile_message})
        return Response(serializer.data)
    # def get(self, request, *args, **kwargs):
    #     nickname = request.query_params.get('nickname')
    #     print(request.user)
    #
    #     if not nickname:
    #         return Response({"error": "닉네임을 제공해주세요."}, status=400)
    #     try:
    #         user = User.objects.get(nickname=nickname)
    #         return Response({"nickname": user.nickname, "profile_image": user.profile_image or None, "profile_message":user.profile_message})
    #     except User.DoesNotExist:
    #         return Response({"error": "해당 닉네임의 유저를 찾을 수 없습니다."}, status=404)


class UserByNicknameView(APIView):
    serializer_class = UserByNicknameSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    queryset = User.objects.all()
    lookup_field = 'nickrname'
    lookup_url_kwarg = 'nickname'
    def get(self, request, *args, **kwargs):
        nickname = request.query_params.get('nickname')
        if not nickname:
            return Response({"error": "닉네임을 제공해주세요."}, status=400)
        try:
            user = User.objects.get(nickname=nickname)
            return Response({"nickname": user.nickname, "profile_image": user.profile_image or None, "profile_message":user.profile_message})
        except User.DoesNotExist:
            return Response({"error": "해당 닉네임의 유저를 찾을 수 없습니다."}, status=404)