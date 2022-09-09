from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('collections', views.CollectionViewSet)
router.register('products', views.ProductViewSet)

# URLConf
urlpatterns = router.urls
