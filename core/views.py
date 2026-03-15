from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from .models import UserProfile, MistakeRecord
from .serializers import UserSerializer, UserProfileSerializer, MistakeRecordSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        login(request, user)
        return Response({
            'user': serializer.data,
            'profile': UserProfileSerializer(user.profile).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({
            'user': UserSerializer(user).data,
            'profile': UserProfileSerializer(user.profile).data
        })
    return Response({'error': '用户名或密码错误'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def user_logout(request):
    logout(request)
    return Response({'message': '退出登录成功'})


@api_view(['GET'])
def get_profile(request):
    serializer = UserProfileSerializer(request.user.profile)
    return Response(serializer.data)


class MistakeRecordViewSet(viewsets.ModelViewSet):
    serializer_class = MistakeRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MistakeRecord.objects.filter(user=self.request.user).order_by('-created_at')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # 创建记录
        self.perform_create(serializer)
        
        # 更新用户统计
        profile = request.user.profile
        profile.mistake_count += 1
        profile.last_mistake_date = timezone.now()
        profile.save()
        
        headers = self.get_success_headers(serializer.data)
        return Response({
            'record': serializer.data,
            'profile': UserProfileSerializer(profile).data
        }, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(['GET'])
def get_investment_types(request):
    types = [
        {'value': 'crypto', 'label': '币圈'},
        {'value': 'stock', 'label': 'A股'},
        {'value': 'fund', 'label': '基金'},
        {'value': 'bond', 'label': '债券'},
        {'value': 'futures', 'label': '期货'},
        {'value': 'options', 'label': '期权'},
        {'value': 'real_estate', 'label': '房地产'},
        {'value': 'other', 'label': '其他'},
    ]
    return Response(types)
