from api.views import (CategorySubcategoryListViewSet, ProductListViewSet,
                       ShoppingCartViewSet)
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

router = routers.DefaultRouter()

router.register(r'categories',
                CategorySubcategoryListViewSet, basename='category')
router.register(r'products',
                ProductListViewSet, basename='product')
router.register(r'shoppingcarts',
                ShoppingCartViewSet, basename='shoppingcart')

urlpatterns = (
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
)
