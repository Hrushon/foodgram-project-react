from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


def html_to_pdf(template, context):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'filename="shopping_cart.pdf"'
    template = get_template(template)
    html = template.render(context)
    pdf = pisa.CreatePDF(html, dest=response, encoding="utf-16")
    if not pdf.err:
        return response
    return None
