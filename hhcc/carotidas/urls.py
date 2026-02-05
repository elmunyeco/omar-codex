from django.urls import path

from . import views


app_name = "carotidas"

urlpatterns = [
    path("<int:historia_id>/nuevo/", views.nuevo_estudio, name="carotidas_nuevo"),
    path("estudio/<int:pk>/", views.detalle_estudio, name="carotidas_detalle"),
]
