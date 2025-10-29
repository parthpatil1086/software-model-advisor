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

    # --- Form container for clean submission ---
    with st.form("client_form"):

        st.write("### 👤 Basic Details")
        client_name = st.text_input("Client Name", key="client_name")
        project_name = st.text_input("Project Name", key="project_name")

        st.write("### 💻 Project Details")
        domain = st.selectbox(
            "Project Domain",
            ["-- Select --", "Web App", "Mobile App", "AI Tool", "Enterprise Software", "Other"],
            key="domain"
        )
        goal = st.selectbox(
            "Primary Goal",
            ["-- Select --", "E-commerce", "Education", "Healthcare", "Finance", "Entertainment", "Other"],
            key="goal"
        )

        project_duration = st.selectbox(
            "Expected Duration",
            ["-- Select --", "<1 month", "1–3 months", "3–6 months", ">6 months"],
            key="duration"
        )
        team_size = st.slider("Team Size", 1, 50, 5, key="team_size")
        experience = st.selectbox(
            "Average Developer Experience",
            ["-- Select --", "Beginner", "Intermediate", "Expert"],
            key="experience"
        )
        has_manager = st.selectbox(
            "Project Manager Involved?",
            ["-- Select --", "Yes", "No"],
            key="manager"
        )
        has_testing = st.selectbox(
            "Testing Team Available?",
            ["-- Select --", "Yes", "No"],
            key="testing"
        )

        st.write("### ⚙️ Technical Details")
        complexity = st.selectbox(
            "Project Complexity Level",
            ["-- Select --", "Low", "Medium", "High"],
            key="complexity"
        )
        integration = st.selectbox(
            "Integration Requirement",
            ["-- Select --", "None", "APIs", "Third-party tools", "Hardware"],
            key="integration"
        )
        stack_type = st.selectbox(
            "Preferred Technology Stack",
            ["-- Select --", "Custom", "Open Source", "Hybrid"],
            key="stack"
        )
        scalability = st.selectbox(
            "Scalability Requirement",
            ["-- Select --", "Low", "Medium", "High"],
            key="scalability"
        )

        st.write("### 💰 Budget & Delivery")
        has_deadline = st.selectbox(
            "Is there a fixed deadline?",
            ["-- Select --", "Yes", "No"],
            key="deadline"
        )
        budget_range = st.selectbox(
            "Estimated Budget Range (₹)",
            ["-- Select --", "<50K", "50K–1L", "1L–5L", ">5L", ">10L"],
            key="budget"
        )
        maintenance = st.selectbox(
            "Maintenance Required After Delivery?",
            ["-- Select --", "Yes", "No"],
            key="maintenance"
        )
        payment_type = st.selectbox(
            "Preferred Payment Type",
            ["-- Select --", "Hourly", "Fixed Cost", "Milestone-based"],
            key="payment"
        )

        st.write("### ⚖️ Project Priorities")
        risk_tolerance = st.selectbox(
            "Risk Tolerance",
            ["-- Select --", "Low", "Medium", "High"],
            key="risk"
        )
        quality_priority = st.selectbox(
            "Project Priority",
            ["-- Select --", "Speed", "Cost", "Quality", "Balance"],
            key="priority"
        )
        involvement = st.selectbox(
            "Client Involvement Level",
            ["-- Select --", "Low", "Moderate", "Active"],
            key="involvement"
        )

        # --- Submit button ---
        submitted = st.form_submit_button("✅ Save Project Input")

    # --- After submission ---
    if submitted:
        fields = [
            st.session_state.domain, st.session_state.goal,
            st.session_state.duration, st.session_state.experience,
            st.session_state.manager, st.session_state.testing,
            st.session_state.complexity, st.session_state.integration,
            st.session_state.stack, st.session_state.scalability,
            st.session_state.deadline, st.session_state.budget,
            st.session_state.maintenance, st.session_state.payment,
            st.session_state.risk, st.session_state.priority,
            st.session_state.involvement
        ]

        if any(f == "-- Select --" for f in fields) or not st.session_state.client_name or not st.session_state.project_name:
            st.warning("⚠️ Please fill out all fields before saving!")
        else:
            st.session_state.client_input = {
                "client_name": st.session_state.client_name,
                "project_name": st.session_state.project_name,
                "domain": st.session_state.domain,
                "goal": st.session_state.goal,
                "team_size": st.session_state.team_size,
                "duration": st.session_state.duration,
                "experience": st.session_state.experience,
                "manager": st.session_state.manager,
                "testing": st.session_state.testing,
                "complexity": st.session_state.complexity,
                "integration": st.session_state.integration,
                "stack": st.session_state.stack,
                "scalability": st.session_state.scalability,
                "deadline": st.session_state.deadline,
                "budget": st.session_state.budget,
                "maintenance": st.session_state.maintenance,
                "payment": st.session_state.payment,
                "risk": st.session_state.risk,
                "priority": st.session_state.priority,
                "involvement": st.session_state.involvement
            }
            st.success("✅ Project details saved successfully! Data will persist across all tabs.")

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
