from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generate_pdf(client_name, client_input, model, estimated_cost, budget_result):
    """Generates a formatted quotation PDF"""
    file_path = f"quotation_{client_name.replace(' ', '_')}.pdf"
    c = canvas.Canvas(file_path, pagesize=A4)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, "Software Project Quotation")

    c.setFont("Helvetica", 12)
    c.drawString(50, 770, f"Client Name: {client_name}")
    c.drawString(50, 750, f"Project Name: {client_input['project_name']}")
    c.drawString(50, 730, f"Domain: {client_input['domain']}")
    c.drawString(50, 710, f"Recommended Model: {model}")
    c.drawString(50, 690, f"Estimated Cost: ₹{estimated_cost}")
    c.drawString(50, 670, f"Budget Status: {budget_result['message']}")

    if not budget_result["within_budget"]:
        y = 650
        c.drawString(50, y, "Optimization Suggestions:")
        for s in budget_result["suggestions"]:
            y -= 20
            c.drawString(70, y, f"- {s}")

    c.save()
    return file_path
