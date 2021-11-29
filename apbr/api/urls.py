from rest_framework import routers
from .views import ApbrProfileViewSet

router = routers.DefaultRouter()
router.register('profiles', ApbrProfileViewSet)
urlpatterns = router.urls