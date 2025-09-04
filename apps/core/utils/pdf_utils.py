import io
import qrcode
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch, mm
from reportlab.lib.colors import Color, black, white, HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from django.http import HttpResponse
from django.conf import settings
import os
import base64

def registrar_fuentes():
    """Registrar fuentes personalizadas si están disponibles."""
    try:
        # Intentar registrar fuentes comunes
        fuentes_disponibles = {
            'Helvetica': None,
            'Helvetica-Bold': None,
            'Courier': None,
            'Courier-Bold': None,
        }
        
        # Puedes añadir fuentes personalizadas aquí si las tienes
        # Ejemplo: pdfmetrics.registerFont(TTFont('MiFuente', 'path/to/font.ttf'))
        
    except:
        # Usar fuentes por defecto si hay error
        pass

def generar_qr_image(data, size=200):
    """Generar imagen QR."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    return ImageReader(img_buffer)

def generar_pdf_reserva(reserva):
    """Generar PDF profesional para reserva de hotel."""
    buffer = io.BytesIO()
    
    # Configurar documento
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Estilos
    styles = getSampleStyleSheet()
    estilo_titulo = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=HexColor('#2c3e50')
    )
    
    estilo_subtitulo = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        textColor=HexColor('#34495e')
    )
    
    estilo_normal = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6
    )
    
    estilo_destacado = ParagraphStyle(
        'CustomBold',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6,
        fontName='Helvetica-Bold'
    )
    
    # Contenido del PDF
    story = []
    
    # Encabezado
    story.append(Paragraph("COMPROBANTE DE RESERVA", estilo_titulo))
    story.append(Spacer(1, 20))
    
    # Información de la reserva
    datos_reserva = [
        ['Código de Reserva:', reserva.codigo_reserva],
        ['Hotel:', reserva.hotel.nombre],
        ['Dirección:', reserva.hotel.direccion],
        ['Check-in:', f"{reserva.fecha_entrada} a las {reserva.hotel.check_in}"],
        ['Check-out:', f"{reserva.fecha_salida} a las {reserva.hotel.check_out}"],
        ['Noches:', str(reserva.noches)],
        ['Huéspedes:', f"{reserva.adultos} adultos, {reserva.ninos} niños"],
        ['Habitaciones:', str(reserva.habitaciones)],
    ]
    
    tabla_reserva = Table(datos_reserva, colWidths=[100, 300])
    tabla_reserva.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
        ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 10),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('PADDING', (0, 0), (-1, -1), 4),
    ]))
    
    story.append(tabla_reserva)
    story.append(Spacer(1, 20))
    
    # Información del huésped
    story.append(Paragraph("INFORMACIÓN DEL HUÉSPED", estilo_subtitulo))
    datos_huesped = [
        ['Nombre:', reserva.nombre_huesped],
        ['Email:', reserva.email_huesped],
        ['Teléfono:', reserva.telefono_huesped or 'No especificado'],
    ]
    
    tabla_huesped = Table(datos_huesped, colWidths=[100, 300])
    tabla_huesped.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
        ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 10),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('PADDING', (0, 0), (-1, -1), 4),
    ]))
    
    story.append(tabla_huesped)
    story.append(Spacer(1, 20))
    
    # Detalles de pago
    story.append(Paragraph("DETALLES DE PAGO", estilo_subtitulo))
    datos_pago = [
        ['Precio total:', f"{reserva.precio_total} {reserva.moneda}"],
        ['Impuestos:', f"{reserva.impuestos} {reserva.moneda}"],
        ['Comisión:', f"{reserva.comision} {reserva.moneda}"],
        ['Método de pago:', reserva.metodo_pago or 'No especificado'],
        ['Referencia:', reserva.referencia_pago or 'No especificada'],
        ['Fecha de pago:', reserva.fecha_pago.strftime('%d/%m/%Y %H:%M') if reserva.fecha_pago else 'Pendiente'],
    ]
    
    tabla_pago = Table(datos_pago, colWidths=[100, 300])
    tabla_pago.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
        ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 10),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('PADDING', (0, 0), (-1, -1), 4),
    ]))
    
    story.append(tabla_pago)
    story.append(Spacer(1, 20))
    
    # Código QR
    story.append(Paragraph("CÓDIGO DE VERIFICACIÓN", estilo_subtitulo))
    
    # Generar QR
    qr_data = reserva.generar_codigo_qr()
    qr_image = generar_qr_image(qr_data, size=150)
    
    # Crear tabla para centrar el QR
    qr_table = Table([[qr_image]], colWidths=[150], rowHeights=[150])
    qr_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    story.append(qr_table)
    story.append(Spacer(1, 10))
    story.append(Paragraph(f"Código: {reserva.codigo_reserva}", estilo_normal))
    story.append(Spacer(1, 20))
    
    # Instrucciones
    story.append(Paragraph("INSTRUCCIONES", estilo_subtitulo))
    instrucciones = [
        "• Presente este comprobante y documento de identidad al check-in",
        "• El check-in está disponible a partir de las 14:00",
        "• El check-out debe realizarse antes de las 12:00",
        "• Para cancelaciones, contacte con el hotel con 24h de antelación",
        "• Conserve este documento durante toda su estancia"
    ]
    
    for instruccion in instrucciones:
        story.append(Paragraph(instruccion, estilo_normal))
    
    # Generar PDF
    doc.build(story)
    
    # Obtener el PDF del buffer
    pdf = buffer.getvalue()
    buffer.close()
    
    return pdf

def descargar_pdf_reserva(reserva, filename=None):
    """Crear respuesta HTTP para descargar PDF de reserva."""
    if filename is None:
        filename = f"reserva_{reserva.codigo_reserva}.pdf"
    
    pdf_content = generar_pdf_reserva(reserva)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    response.write(pdf_content)
    
    return response

def generar_pdf_simple(contexto, template_name):
    """Generar PDF simple a partir de template HTML (para resultados de búsqueda)."""
    from django.template.loader import render_to_string
    import pdfkit
    
    html_content = render_to_string(template_name, contexto)
    
    # Configurar opciones de PDF
    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'no-outline': None,
        'quiet': '',
    }
    
    # Generar PDF
    pdf = pdfkit.from_string(html_content, False, options=options)
    return pdf
