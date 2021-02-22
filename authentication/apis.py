from datetime import datetime

from django.forms import model_to_dict
from django.utils import timezone
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from authentication.models import User, Profile
from authentication.serializers import SmsConfirmationSerializer, UserSerializer, ProfileSerializer


class LoginApi(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context=dict(request=request))
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user.last_login = timezone.make_aware(datetime.now(), timezone.get_default_timezone())

        token, created = Token.objects.get_or_create(user=user)
        if not created:
            token.delete()
            token, created = Token.objects.get_or_create(user=user)

        data = dict(token=token.key)
        data.update(model_to_dict(user,
                                  exclude=['password', 'is_superuser', 'is_staff', 'notification_token', 'is_active',
                                           'visible', 'user_permissions', 'groups']))
        data.update({'profile': model_to_dict(user.profile, exclude=['created_at'])})

        return Response(data)


class OtpApi(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        serializer = SmsConfirmationSerializer(data=request.GET)
        result = serializer.resend()
        if result:
            response = dict(status=True, code=5)
        else:
            response = dict(status=False, code=21)
        return Response(response)

    def put(self, request):
        serializer = SmsConfirmationSerializer(data=request.data)
        result = serializer.activate()
        if result:
            response = dict(status=True, code=5)
        else:
            response = dict(status=False, code=20)
        return Response(response)


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action == 'create' or self.action == 'register':
            return [permissions.AllowAny()]
        else:
            return [permissions.IsAuthenticatedOrReadOnly()]

    @action(methods=['post'], detail=False, url_path='register', permission_classes=[permissions.AllowAny()])
    def register(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.status_code = 201
        if response:
            response.data = dict(status=True, code=4)
        return response

    def create(self, request, *args, **kwargs):
        return self.register(request, *args, **kwargs)


class ProfileViewSet(ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.filter(visible=True)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(methods=['get'], detail=True, url_path='by-user-id')
    def get_by_user_id(self, request, *args, **kwargs):
        profile = get_object_or_404(self.get_queryset(), user_id=self.kwargs.get("pk"))
        serializer = self.get_serializer(profile)
        return Response(serializer.data)
