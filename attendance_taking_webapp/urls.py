"""attendance_taking_webapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Swagger documentation setup
from main import views

schema_view = get_schema_view(
    openapi.Info(
        title="Attendance Taking APP API",
        default_version='v1',
        description="A web based attendance taking system with facial recognition",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="peng0099@e.ntu.edu.sg"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.IsAuthenticated, ),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('docs/', include_docs_urls(title='Attendance Taking Webapp')),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


# API Views
api_prefix = "api"

# ViewSet routers, order matters
router = DefaultRouter()
router.register(api_prefix + r'/course', views.CourseViewSet)
router.register(api_prefix + r'/labgroup', views.LabGroupViewSet)
router.register(api_prefix + r'/labsession', views.LabSessionViewSet)
router.register(api_prefix + r'/labgroupstudentpair', views.LabGroupStudentPairViewSet)
router.register(api_prefix + r'/student', views.StudentViewSet)
router.register(api_prefix + r'/attendancerecord', views.AttendanceRecordViewSet)
urlpatterns += router.urls
