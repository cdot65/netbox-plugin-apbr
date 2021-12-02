from rest_framework import routers

from .views import ApbrViewSet

router = routers.DefaultRouter()
router.register('apbr', ApbrViewSet)


urlpatterns = router.urls