from django.shortcuts import render, redirect
from Juniors.models import Interest
from django.contrib.admin.views.decorators import user_passes_test
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch


def reportsPage(request):
    if request.user.is_superuser:
        all_Status = Interest.objects.all()
        selected_reportsType = request.GET.get('reportType')
        if selected_reportsType == 'Hired':
            all_Status = all_Status.filter(status='hired')

        # Export to PDF
        if request.GET.get('export') == 'pdf':
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="Status Report.pdf"'

            # Create a PDF document with ReportLab
            doc = SimpleDocTemplate(response, pagesize=landscape(letter))
            elements = []

            # Table data
            table_data = []
            table_data.append(['Candidate name', 'Status'])
            for status in all_Status:
                table_data.append([status.name, status.status])

            # Define table style
            table_style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1),
                 [colors.white, colors.lightgrey]),
            ])

            # Create the table and apply the style
            table = Table(table_data, colWidths=[3 * inch, 2 * inch])
            table.setStyle(table_style)

            # Add the table to the PDF document
            elements.append(table)

            # Build the PDF document
            doc.build(elements)
            return response

        return render(request, 'reports.html', {'all_Status': all_Status})
    else:
        return redirect('home')
