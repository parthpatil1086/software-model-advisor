import streamlit as st
from utils.model_logic import suggest_model
from utils.cost_estimation import estimate_cost
from utils.budget_optimizer import optimize_budget
from utils.pdf_generator import generate_pdf

st.set_page_config(page_title="Smart Software Model & Budget Suggestion", layout="wide")

st.title("💼 Smart Software Model & Budget Suggestion System")

st.sidebar.title("📂 Navigation")
page = st.sidebar.radio("Go to", [
    "Welcome",
    "Client Input",
    "Model Suggestion",
    "Cost Estimation",
    "Budget Optimizer",
    "Download Quotation"
])

if 'client_input' not in st.session_state:
    st.session_state.client_input = {}

if page == "Welcome":
    st.subheader("Welcome!")
    st.markdown("""
    This system helps you:
    - ✅ Choose the best **software development model**
    - 💰 Get an **AI-based cost estimate**
    - 📉 Optimize your **budget and resources**
    - 📄 Download a **quotation PDF**

    Use the sidebar to begin.
    """)

elif page == "Client Input":
    st.subheader("Enter Detailed Project Requirements")

    client_name = st.text_input("Client Name")
    project_name = st.text_input("Project Name")

    domain = st.selectbox("Project Domain", ["-- Select --", "Web App", "Mobile App", "AI Tool", "Enterprise Software", "Other"])
    goal = st.selectbox("Primary Goal", ["-- Select --", "E-commerce", "Education", "Healthcare", "Finance", "Entertainment", "Other"])
    
    project_duration = st.selectbox("Expected Duration", ["-- Select --", "<1 month", "1–3 months", "3–6 months", ">6 months"])
    team_size = st.slider("Team Size", 1, 50, 5)
    experience = st.selectbox("Average Developer Experience", ["-- Select --", "Beginner", "Intermediate", "Expert"])
    has_manager = st.selectbox("Project Manager Involved?", ["-- Select --", "Yes", "No"])
    has_testing = st.selectbox("Testing Team Available?", ["-- Select --", "Yes", "No"])
    
    complexity = st.selectbox("Project Complexity Level", ["-- Select --", "Low", "Medium", "High"])
    integration = st.selectbox("Integration Requirement", ["-- Select --", "None", "APIs", "Third-party tools", "Hardware"])
    stack_type = st.selectbox("Preferred Technology Stack", ["-- Select --", "Custom", "Open Source", "Hybrid"])
    scalability = st.selectbox("Scalability Requirement", ["-- Select --", "Low", "Medium", "High"])
    
    has_deadline = st.selectbox("Is there a fixed deadline?", ["-- Select --", "Yes", "No"])
    budget_range = st.selectbox("Estimated Budget Range (₹)", ["-- Select --", "<50K", "50K–1L", "1L–5L", ">5L", ">10L"])
    maintenance = st.selectbox("Maintenance Required After Delivery?", ["-- Select --", "Yes", "No"])
    payment_type = st.selectbox("Preferred Payment Type", ["-- Select --", "Hourly", "Fixed Cost", "Milestone-based"])

    risk_tolerance = st.selectbox("Risk Tolerance", ["-- Select --", "Low", "Medium", "High"])
    quality_priority = st.selectbox("Project Priority", ["-- Select --", "Speed", "Cost", "Quality", "Balance"])
    involvement = st.selectbox("Client Involvement Level", ["-- Select --", "Low", "Moderate", "Active"])

    if st.button("✅ Save Project Input"):
        fields = [domain, goal, project_duration, experience, has_manager, has_testing, complexity,
                  integration, stack_type, scalability, has_deadline, budget_range, maintenance,
                  payment_type, risk_tolerance, quality_priority, involvement]
        
        if any(f == "-- Select --" for f in fields) or not client_name or not project_name:
            st.warning("Please fill out all fields before saving!")
        else:
            st.session_state.client_input = {
                "client_name": client_name,
                "project_name": project_name,
                "domain": domain,
                "goal": goal,
                "team_size": team_size,
                "duration": project_duration,
                "experience": experience,
                "manager": has_manager,
                "testing": has_testing,
                "complexity": complexity,
                "integration": integration,
                "stack": stack_type,
                "scalability": scalability,
                "deadline": has_deadline,
                "budget": budget_range,
                "maintenance": maintenance,
                "payment": payment_type,
                "risk": risk_tolerance,
                "priority": quality_priority,
                "involvement": involvement
            }
            st.success("✅ Project details saved successfully!")

elif page == "Model Suggestion":
    st.subheader("🔎 Suggested Development Model")

    if not st.session_state.client_input:
        st.info("Please fill out the Client Input page first.")
    else:
        model = suggest_model(st.session_state.client_input)
        st.markdown(f"### ✅ Recommended Model: **{model}**")

elif page == "Cost Estimation":
    st.subheader("💰 Estimated Project Cost")

    if not st.session_state.client_input:
        st.info("Please fill out the Client Input first.")
    else:
        cost = estimate_cost(st.session_state.client_input)
        st.markdown(f"### 💸 Estimated Cost: ₹**{cost}**")

elif page == "Budget Optimizer":
    st.subheader("📉 Budget Optimization Suggestion")

    if not st.session_state.client_input:
        st.warning("Please fill out the client input first.")
    else:
        client_input = st.session_state.client_input
        estimated_cost = estimate_cost(client_input)
        budget_result = optimize_budget(estimated_cost, client_input["budget"])
        st.markdown(f"### 💡 Optimization Suggestion:\n\n{budget_result['message']}")
        if not budget_result["within_budget"]:
            for suggestion in budget_result["suggestions"]:
                st.markdown(f"- {suggestion}")


elif page == "Download Quotation":
    st.subheader("📄 Download Quotation PDF")

    if not st.session_state.client_input:
        st.warning("Please fill out the client input first.")
    else:
        if st.button("📥 Generate & Download PDF"):
            client_input = st.session_state.client_input
            model = suggest_model(client_input)
            estimated_cost = estimate_cost(client_input)
            budget_result = optimize_budget(estimated_cost, client_input["budget"])
            file_path = generate_pdf(client_input["client_name"], client_input, model, estimated_cost, budget_result)
            with open(file_path, "rb") as f:
                st.download_button("📄 Download Quotation", data=f, file_name="software_quotation.pdf", mime="application/pdf")
