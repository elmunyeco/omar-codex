from django.db import models

from main.models import HistoriaClinica


class EcostressEstudio(models.Model):
    """
    Estudio de ecostress cardiaco.
    Basado en la tabla legacy `stress`.
    """

    id_stress = models.AutoField(primary_key=True, db_column="idStress")
    historia = models.ForeignKey(
        HistoriaClinica,
        on_delete=models.CASCADE,
        related_name="ecostress_estudios",
        db_column="idHC",
    )
    indicacion_estudio = models.TextField(null=True, blank=True, db_column="indicacionEstudio")
    tipo_apremio = models.TextField(null=True, blank=True, db_column="tipoApremio")
    medicacion_momento_estudio = models.TextField(
        null=True, blank=True, db_column="medicacionMomentoEstudio"
    )
    medico_solicitante = models.TextField(null=True, blank=True, db_column="medicoSolicitante")
    frecuencia_cardiaca_basal = models.TextField(
        null=True, blank=True, db_column="frecuenciaCardiacaBasal"
    )
    frecuencia_cardiaca_maxima = models.TextField(
        null=True, blank=True, db_column="frecuenciaCardiacaMaxima"
    )
    presion_arterial_basal_inicial = models.TextField(
        null=True, blank=True, db_column="presionArterialBasalInicial"
    )
    presion_arterial_basal_final = models.TextField(
        null=True, blank=True, db_column="presionArterialBasalFinal"
    )
    presion_arterial_maxima_inicial = models.TextField(
        null=True, blank=True, db_column="presionArterialMaximaInicial"
    )
    presion_arterial_maxima_final = models.TextField(
        null=True, blank=True, db_column="presionArterialMaximaFinal"
    )
    informe_ergometria = models.TextField(null=True, blank=True, db_column="informeErgometria")
    datos_ecocardiograficos_basales = models.TextField(
        null=True, blank=True, db_column="datosEcocardiograficosBasales"
    )
    datos_ecocardiograficos_post_esfuerzo_inmediato = models.TextField(
        null=True, blank=True, db_column="datosEcocardiograficosPostEsfuerzoInmediato"
    )
    conclusion = models.TextField(null=True, blank=True, db_column="conclusion")
    fecha_estudio = models.DateField(null=True, blank=True)

    class Meta:
        db_table = "stress"
        verbose_name = "Estudio de ecostress"
        verbose_name_plural = "Estudios de ecostress"
        indexes = [
            models.Index(fields=["historia"], name="stress_historia_idx"),
        ]

    def __str__(self):
        return f"Ecostress HC {self.historia_id} - Estudio {self.pk or 'nuevo'}"
