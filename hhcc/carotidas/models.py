from django.db import models

from main.models import HistoriaClinica


class CarotidasEstudio(models.Model):
    """
    Estudio de carótidas (doppler vasos del cuello / QIMT).
    Basado en la tabla legacy `carotidas`.
    """

    historia = models.ForeignKey(
        HistoriaClinica,
        on_delete=models.CASCADE,
        related_name="carotidas_estudios",
    )
    com_derecha = models.CharField(max_length=20, null=True, blank=True)
    int_derecha = models.CharField(max_length=20, null=True, blank=True)
    ext_derecha = models.CharField(max_length=20, null=True, blank=True)
    com_izquierda = models.CharField(max_length=20, null=True, blank=True)
    int_izquierda = models.CharField(max_length=20, null=True, blank=True)
    ext_izquierda = models.CharField(max_length=20, null=True, blank=True)
    art_vertebrales = models.CharField(max_length=20, null=True, blank=True)
    sugerencias = models.CharField(max_length=20, null=True, blank=True)
    id_com_der = models.PositiveIntegerField(default=0)
    id_com_izq = models.PositiveIntegerField(default=0)
    esp_int_med_der = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True
    )
    esp_int_med_izq = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True
    )

    class Meta:
        db_table = "carotidas"
        verbose_name = "Estudio de carótidas"
        verbose_name_plural = "Estudios de carótidas"
        indexes = [
            models.Index(fields=["historia"], name="carotidas_historia_idx"),
            models.Index(fields=["id_com_der", "id_com_izq"], name="carotidas_com_idx"),
        ]

    def __str__(self):
        return f"Carótidas HC {self.historia_id} - Estudio {self.pk or 'nuevo'}"
