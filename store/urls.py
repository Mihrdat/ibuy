from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('collections', views.CollectionViewSet)

# URLConf
urlpatterns = router.urls
