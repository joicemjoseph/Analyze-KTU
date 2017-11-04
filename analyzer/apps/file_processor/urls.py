# -*- coding: utf-8 -*-
from rest_framework import routers

from django.conf.urls import url

from .views import CourseViewSet, list

router = routers.DefaultRouter()
router.register(r'api/course', CourseViewSet)

urlpatterns = [
    url(r'^list/$', list, name='list'),
]
urlpatterns += router.urls
