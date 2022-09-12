from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('collections', views.CollectionViewSet)
router.register('products', views.ProductViewSet)
router.register('carts', views.CartViewSet)
router.register('customers', views.CustomerViewSet)

carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', views.CartItemViewSet, basename='cart-items')

# URLConf
urlpatterns = router.urls + carts_router.urls
