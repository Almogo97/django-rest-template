from rest_framework import routers

from services.users import views

router = routers.SimpleRouter()
router.register('users', views.UserViewSet, basename='users')
urlpatterns = router.urls
