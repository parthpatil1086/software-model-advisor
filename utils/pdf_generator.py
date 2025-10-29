from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

def generate_pdf(client_name, client_input, model, estimated_cost, budget_result):
    """Generates a professional quotation PDF with Rupee symbol."""
    
    # Register a TTF font that supports ₹
    pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSans.ttf'))  # Make sure DejaVuSans.ttf is in your project folder
    
    file_path = f"quotation_{client_name.replace(' ', '_')}.pdf"
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4
    
    # Title
    c.setFont("DejaVu", 18)
    c.drawString(50, height - 50, "Software Project Quotation")
    
    # Client & Project Info
    c.setFont("DejaVu", 12)
    y = height - 100
    line_spacing = 20
    c.drawString(50, y, f"Client Name: {client_name}")
    y -= line_spacing
    c.drawString(50, y, f"Project Name: {client_input['project_name']}")
    y -= line_spacing
    c.drawString(50, y, f"Domain: {client_input['domain']}")
    y -= line_spacing
    c.drawString(50, y, f"Recommended Model: {model}")
    y -= line_spacing
    c.drawString(50, y, f"Estimated Cost: ₹{estimated_cost}")  # ₹ will now appear
    y -= line_spacing
    c.drawString(50, y, f"Budget Status: {budget_result['message']}")
    
    # Suggestions
    if not budget_result["within_budget"] and budget_result.get("suggestions"):
        y -= line_spacing
        c.setFont("DejaVu", 12)
        c.drawString(50, y, "Optimization Suggestions:")
        y -= line_spacing
        for s in budget_result["suggestions"]:
            c.drawString(70, y, f"• {s}")
            y -= line_spacing
    
    c.save()
    return file_path