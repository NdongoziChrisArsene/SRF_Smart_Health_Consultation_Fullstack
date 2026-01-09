from django.urls import path
from .views import RegisterView, LoginView, AdminUserStatsView

app_name = "users"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("admin/users/stats/", AdminUserStatsView.as_view(), name="admin-users-stats"),
]





































# from django.urls import path
# from .views import RegisterView, LoginView, AdminUserStatsView 

# app_name = "users"

# urlpatterns = [
#     path("register/", RegisterView.as_view(), name="register"),
#     path("login/", LoginView.as_view(), name="login"), 
#     path("admin/users/stats/", AdminUserStatsView.as_view(), name="admin-users-stats"),
# ]
