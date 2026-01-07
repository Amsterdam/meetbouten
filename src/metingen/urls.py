from django.urls import path

from metingen.views import proxy_image

urlpatterns = [
    path("admin/proxy_image/meetbouten_pictures/<path:path>", proxy_image, name="proxy_image"),
]
