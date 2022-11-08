import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


def link_callback(uri, rel):
    if uri.find(settings.MEDIA_URL) != -1:
        path = os.path.join(
            settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, '')
        )
    elif uri.find(settings.STATIC_URL) != -1:
        path = os.path.join(
            settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, '')
        )
    else:
        path = None
    return path


def html_to_pdf(template, context):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'filename="report.pdf"'
    template = get_template(template)
    html = template.render(context)
    pdf = pisa.CreatePDF(
        html, dest=response,
        encoding="utf-8",
        link_callback=link_callback
    )
    if not pdf.err:
        return response
    return None
