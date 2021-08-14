from rest_framework import routers

from services.account_recovery import views

router = routers.SimpleRouter()
router.register('users', views.UserRecoverPasswordViewSet,
                basename='users-recover-password')
urlpatterns = router.urls
