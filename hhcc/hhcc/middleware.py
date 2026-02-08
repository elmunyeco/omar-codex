from django.utils import translation


def force_spanish_middleware(get_response):
    def middleware(request):
        translation.activate("es-ar")
        request.LANGUAGE_CODE = "es-ar"
        response = get_response(request)
        translation.deactivate()
        return response

    return middleware
