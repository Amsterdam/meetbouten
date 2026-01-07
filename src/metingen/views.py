import mimetypes

from django.contrib.admin.views.decorators import staff_member_required
from django.core.files.storage import default_storage
from django.http import Http404, HttpResponse


@staff_member_required
def proxy_image(request, path):
    try:
        full_path = f"meetbouten_pictures/{path}"
        if not default_storage.exists(full_path):
            raise Http404("Image not found")

        file = default_storage.open(full_path, "rb")
        content_type, _ = mimetypes.guess_type(full_path)
        if content_type is None:
            content_type = "application/octet-stream"

        response = HttpResponse(file.read(), content_type=content_type)
        response["Cache-Control"] = "private, max-age=3600"

        file.close()
        return response

    except Exception as e:
        raise Http404(f"Error serving image: {str(e)}")
