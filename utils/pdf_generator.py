from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def generate_pdf(client_name, client_input, model, estimated_cost, budget_result):
    """Generates a professional quotation PDF for a software project."""
    
    # File path
    file_path = f"quotation_{client_name.replace(' ', '_')}.pdf"
    
    # Create canvas
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4
    
    # Title
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, height - 50, "Software Project Quotation")
    
    # Client & Project Info
    c.setFont("Helvetica", 12)
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
    c.drawString(50, y, f"Estimated Cost: ₹{estimated_cost}")
    y -= line_spacing
    c.drawString(50, y, f"Budget Status: {budget_result['message']}")
    
    # Optimization Suggestions (if over budget)
    if not budget_result["within_budget"] and budget_result.get("suggestions"):
        y -= line_spacing
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Optimization Suggestions:")
        c.setFont("Helvetica", 12)
        y -= line_spacing
        for s in budget_result["suggestions"]:
            # Wrap long suggestion text
            if len(s) > 80:
                wrapped_lines = [s[i:i+80] for i in range(0, len(s), 80)]
                for line in wrapped_lines:
                    c.drawString(70, y, f"• {line}")
                    y -= line_spacing
            else:
                c.drawString(70, y, f"• {s}")
                y -= line_spacing
    
    # Save PDF
    c.save()
    return file_path