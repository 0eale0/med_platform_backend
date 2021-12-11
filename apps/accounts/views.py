from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class MyTokenObtainPairView(TokenObtainPairView):
    @classmethod
    def get_extra_actions(cls):
        return []


class MyTokenRefreshView(TokenRefreshView):
    @classmethod
    def get_extra_actions(cls):
        return []
