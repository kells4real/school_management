from django.urls import path

import landing_page.views as home_views


urlpatterns = [
    path('', home_views.home, name="home"),
]