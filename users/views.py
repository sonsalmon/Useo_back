import os

from django.db.models import Q
from haversine import haversine
from rest_framework import generics, status, permissions, serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

# from django.contrib.auth.models import User

from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, UserByNicknameSerializer, \
    FollowingRelationSerializer, FollowingRelationListSerializer
from .models import User, FollowingRelation


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
        if data.get('nickname'): # 받았으면 수정
            if user.nickname != data['nickname']:
                user.nickname = data['nickname']
        if data.get('profile_image'): # 받았으면 수정
            print(request.data['profile_image'])
            print('프로필 이미지', user.profile_image)
            old_image_path = user.profile_image.path if user.profile_image else ''
            # request.data.get('profile_image').name = user.username + '_profile.png'
            user.profile_image = data['profile_image']
        if data.get('profile_message'): # 받았으면 수정
            user.profile_message = data['profile_message']
        if data.get('library_longitude'): # 받았으면 수정
            user.library_longitude = data['library_longitude']
        if request.data.get('library_latitude'): # 받았으면 수정
            user.library_latitude = data['library_latitude']
        user.save()

        #기존 프로필 이미지 삭제
        if(os.path.exists(old_image_path)):
            os.remove(old_image_path)
        return Response({"result": "ok"},
                        status=status.HTTP_206_PARTIAL_CONTENT)

    def get(self, request, *args, **kwargs):
        # user = User.objects.get(username=request.user)
        nickname = request.query_params.get('nickname', None)

        if nickname:
            user = User.objects.get(username_nickname=nickname)
        else:
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




class UserListByContainedKeyword(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        current_user = self.request.user
        queryset = User.objects.all().exclude(id=current_user.id) #현재 사용자 제외
        search_keyword = self.request.query_params.get('query', None)
        print(search_keyword)
        if search_keyword:
            queryset = queryset.filter(
                Q(nickname__icontains=search_keyword) # icontains : 대소문자 구분 x
            )
        else :
            queryset = User.objects.none()
            print('no keword');
        return queryset

class UserListByNearPosition(generics.ListAPIView):
    serializer_class =UserSerializer

    LATITUDE_ONE_KM = 0.01  #   약 1KM에 해당하는 위도 값 차이
    LONGITUDE_ONE_KM = 0.015    # 약 1KM에 해당하는 경도 값 차이
    검색_반경 = 10



    def get_queryset(self):
        print('거리 구하는 함수')
        latitude = float(self.request.query_params.get('library_latitude', 0))
        longitude = float(self.request.query_params.get('library_longitude', 0))
        user_position = (latitude, longitude)
        condition=(
            Q(library_latitude__range = (latitude - (self.LATITUDE_ONE_KM * 20),latitude + (self.LATITUDE_ONE_KM * 20))) &
            Q(library_longitude__range = (longitude - (self.LONGITUDE_ONE_KM * 20),longitude + (self.LONGITUDE_ONE_KM * 20)))&
            Q(is_staff=False)
            # Q(id != self.request.user.id) #현재 사용자 제외
        )
        user_queryset = User.objects.filter(condition).exclude(id=self.request.user.id)
        sorted_by_distance = sorted(user_queryset, key=lambda info:haversine(user_position,(info.library_latitude,info.library_longitude)))
        print(user_queryset.exists)

        return sorted_by_distance[:self.검색_반경]
    # def get(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = self.serializer_class(queryset,many=True)
    #     return Response(serializer.data)










class FollowingRelationView(generics.GenericAPIView):
    serializer_class = FollowingRelationSerializer

    # 유저 팔로우 하기
    def get(self, request):
        user = request.user
        follow_target = User.objects.get(nickname= request.query_params.get('nickname'))
        want_to_check = request.query_params.get('wantToCheck',None)
        print(user)
        print(follow_target)
        if user == follow_target:
            return Response({'error : 자신을 팔로우 할 수 없습니다.'}, status=400)
        #팔로우 중인지 확인
        if want_to_check == 'true':
            follow_relation_exist = FollowingRelation.objects.filter(follower=user, following=follow_target).exists()
            if follow_relation_exist:
                return Response({"follow": "true"})
            else:
                return Response({"follow": "false"})


        # 팔로우 토글 실행
        else:
            follow_relation, created = FollowingRelation.objects.get_or_create(follower=user,following=follow_target)
            if not created:
                follow_relation.delete()
                return Response({"follow": "false"})
            else:
                return Response({"follow": "true"})


        return Response({"follower" :user.username, "following" : follow_target.username}, status=200)

class FollowingRelationListView(generics.ListAPIView):
    # serializer_class = FollowingRelationListSerializer
    serializer_class = UserSerializer

    def get_queryset(self):
        target_nickname = self.request.query_params.get('nickname', None)
        user = self.request.user

        following = user.followings.values_list('following', flat=True)
        return User.objects.filter(id__in=following)
        # # username이 주어지지 않았거나 요청을 보낸 사용자와 일치하는 경우
        # if not target_nickname:
        #     return FollowingRelation.objects.filter(follower=user)
        # #
        # # nickname으로 다른 사용자의 정보를 조회하려는 경우 (예: 관리자 등)
        # queryed_user = User.objects.get(nickname=target_nickname)
        # return FollowingRelation.objects.filter(follower=queryed_user)
