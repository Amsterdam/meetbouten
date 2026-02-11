from django.contrib.admin.widgets import AdminFileWidget
from django.urls import reverse


class ProxyImageWidget(AdminFileWidget):
    """
    Custom widget that displays the image link through a proxy URL
    """

    template_name = "admin/widgets/proxy_clearable_file_input.html"

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        if value and hasattr(value, "name"):
            filename = value.name.replace("meetbouten_pictures/", "")

            try:
                proxy_url = reverse("proxy_image", kwargs={"path": filename})
                context["proxy_url"] = proxy_url
            except Exception:
                context["proxy_url"] = getattr(value, "url", "")
        else:
            context["proxy_url"] = ""

        return context
