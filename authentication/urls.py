from django.urls import path

from authentication import apis

from rest_framework.routers import SimpleRouter

from authentication.apis import ProfileViewSet, UserViewSet

app_name = 'authentication'

router = SimpleRouter()
router.register('profiles', ProfileViewSet, basename='profiles')
router.register('users', UserViewSet, basename='users')

urlpatterns = [
                  path('login/', apis.LoginApi.as_view()),
                  path('otp/', apis.OtpApi.as_view()),
              ] + router.urls
