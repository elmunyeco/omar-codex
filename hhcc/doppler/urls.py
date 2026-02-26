from django.urls import path

from . import views


app_name = "doppler"

urlpatterns = [
    path("<int:historia_id>/nuevo/", views.nuevo_estudio, name="doppler_nuevo"),
    path(
        "imprimir_estudio/<int:estudio_id>/<int:historia_id>/",
        views.imprimir_estudio,
        name="doppler_imprimir",
    ),
]
