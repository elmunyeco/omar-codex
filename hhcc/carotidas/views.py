from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from main.utils import static_file_url
from django.template.loader import render_to_string

from weasyprint import HTML

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
            messages.success(request, "Estudio doppler de vasos de cuello guardado.")
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse(
                    {
                        "success": True,
                        "estudio_id": estudio.pk,
                        "historia_id": historia.pk,
                    }
                )
            return redirect("carotidas:carotidas_detalle", pk=estudio.pk)
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"success": False, "errors": form.errors}, status=400)
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


def imprimir_estudio(request, estudio_id, historia_id):
    estudio = get_object_or_404(CarotidasEstudio, pk=estudio_id)
    if estudio.historia_id != historia_id:
        return JsonResponse({"success": False, "error": "Historia clínica no coincide."}, status=404)

    informe_items = []

    def add_item(label, *parts):
        contenido = " ".join([p for p in parts if p]).strip()
        if contenido:
            informe_items.append((label, contenido))

    add_item("Carótida Común Derecha:", estudio.com_der_texto(), estudio.com_derecha)
    add_item("Carótida Interna Derecha:", estudio.int_derecha)
    add_item("Carótida Externa Derecha:", estudio.ext_derecha)
    add_item("Carótida Común Izquierda:", estudio.com_izq_texto(), estudio.com_izquierda)
    add_item("Carótida Interna Izquierda:", estudio.int_izquierda)
    add_item("Carótida Externa Izquierda:", estudio.ext_izquierda)
    add_item("Arterias Vertebrales:", estudio.art_vertebrales)
    add_item("Imágenes agregadas y sugerencias:", estudio.sugerencias)

    espesor_items = []
    if estudio.esp_int_med_der is not None:
        espesor_items.append(("Derecha:", f"{estudio.esp_int_med_der} mm"))
    if estudio.esp_int_med_izq is not None:
        espesor_items.append(("Izquierda:", f"{estudio.esp_int_med_izq} mm"))

    context = {
        "estudio": estudio,
        "historia": estudio.historia,
        "paciente": estudio.historia.paciente,
        "fecha_estudio": estudio.fecha_estudio or timezone.localdate(),
        "informe_items": informe_items,
        "espesor_items": espesor_items,
        "print_logo_path": static_file_url("main/images/logo.png"),
        "print_site_text": "www.cardioprietohc.com",
        "print_header_text": "Consultorio Cardiológico Doctor Omar Prieto",
        "print_css_path": static_file_url("main/css/print.css"),
    }
    html = render_to_string("carotidas/imprimir_estudio.html", context)
    pdf = HTML(string=html).write_pdf()
    filename = f"carotidas_{estudio_id}_{historia_id}.pdf"
    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = f"inline; filename={filename}"
    return response
