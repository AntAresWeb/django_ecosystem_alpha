from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)
from api.views import (
    CategorySubcategoryListViewSet,
    ProductListViewSet,
    ShoppingCartViewSet
)


router = routers.DefaultRouter()

router.register(r'categories',
                CategorySubcategoryListViewSet, basename='category')
router.register(r'products',
                ProductListViewSet, basename='product')
router.register(r'shoppingcarts',
                ShoppingCartViewSet, basename='shoppingcart')
# router.register(r'users',
#                 UserViewSet, basename='user')

urlpatterns = (
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
)
