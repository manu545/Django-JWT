from django.urls import path
from . import views
from . views import userdata

user_obj = userdata()
urlpatterns = [
    path('hello/', views.HelloView.as_view(), name='hello'),
    path('get_token/student', user_obj.get_token, name="student"),
    path('get_token/teacher', user_obj.get_token, name="teacher"),
    path('get_data/student/', user_obj.get_data, name="student"),
    path('get_data/teacher/', user_obj.get_data, name="teacher"),
    path('update/teacher', user_obj.patch_data, name="teacher"),
    path('update/student', user_obj.patch_data, name="student"),
    path('view', user_obj.view_data, name="student"),
]