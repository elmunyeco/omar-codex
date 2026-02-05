from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from main.models import HistoriaClinica

from .forms import CarotidasForm
from .models import CarotidasEstudio


def nuevo_estudio(request, historia_id):
    historia = get_object_or_404(HistoriaClinica, pk=historia_id)
    estudio = CarotidasEstudio.objects.filter(historia=historia).first()

    if request.method == "POST":
        form = CarotidasForm(request.POST, instance=estudio, initial={"historia": historia})
        if form.is_valid():
            estudio = form.save()
            messages.success(request, "Estudio de carótidas guardado.")
            return redirect("carotidas_detalle", pk=estudio.pk)
    else:
        form = CarotidasForm(instance=estudio, initial={"historia": historia})

    return render(
        request,
        "carotidas/nuevo_estudio.html",
        {
            "form": form,
            "historia": historia,
            "paciente": historia.paciente,
            "estudio": estudio,
        },
    )


def detalle_estudio(request, pk):
    estudio = get_object_or_404(CarotidasEstudio, pk=pk)
    return render(
        request,
        "carotidas/detalle_estudio.html",
        {"estudio": estudio, "historia": estudio.historia, "paciente": estudio.historia.paciente},
    )
