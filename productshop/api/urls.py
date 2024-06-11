from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# from api.views import (IngredientViewSet, RecipeViewSet, TagViewSet,
#                        TokenLoginView, TokenLogoutView, UserViewSet)

router = routers.DefaultRouter()

# router.register(r'ingredients',
#                 IngredientViewSet, basename='ingredient')
# router.register(r'recipes',
#                 RecipeViewSet, basename='recipe')
# router.register(r'tags',
#                 TagViewSet, basename='tag')
# router.register(r'users',
#                 UserViewSet, basename='user')

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('auth/token/login/', TokenLoginView.as_view(), name='login'),
    # path('auth/token/logout/', TokenLogoutView.as_view(), name='logout'),
    path('', include(router.urls)),
]
