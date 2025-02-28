from .import views
from django.urls import path

app_name = 'users'

urlpatterns = [
    path('',views.DashboardView.as_view(),name="dashboard_view"),
    
    path('login/', views.UserLogin.as_view(), name='login'),
    path('logout/', views.UserLogout.as_view(), name='logout'),

    
    path('get-user-info/', views.GetUserInfo.as_view(), name='user_info'),

    path('register/', views.RegisterUserAPI.as_view(), name='register_user'),
    path('list/', views.ListUsersAPI.as_view(), name='list_users'),
    path('update/<int:user_id>', views.UpdateUserAPI.as_view(), name='update_user'),
    path('delete/<int:user_id>', views.DeleteUserAPI.as_view(), name='delete_user'),
]