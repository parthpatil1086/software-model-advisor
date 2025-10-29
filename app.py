import streamlit as st
from utils.model_logic import suggest_model
from utils.cost_estimation import estimate_cost
from utils.budget_optimizer import optimize_budget
from utils.pdf_generator import generate_pdf

# --- Page setup ---
st.set_page_config(page_title="Smart Software Model & Budget Suggestion", layout="wide")
st.title("💼 Smart Software Model & Budget Suggestion System")

# --- Sidebar navigation ---
st.sidebar.title("📂 Navigation")
page = st.sidebar.radio("Go to", [
    "Welcome",
    "Client Input",
    "Model Suggestion",
    "Cost Estimation",
    "Budget Optimizer",
    "Download Quotation"
])

# --- Initialize session state for client input ---
if 'client_input' not in st.session_state:
    st.session_state.client_input = {}

# --- Restore saved inputs into individual session keys ---
for key, value in st.session_state.client_input.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --- Pages ---
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

    # --- Restore previously saved inputs into individual session keys ---
    for key, value in st.session_state.client_input.items():
        if key not in st.session_state:
            st.session_state[key] = value

    with st.form("client_form"):
        client_name = st.text_input("Client Name", key="client_name")
        project_name = st.text_input("Project Name", key="project_name")

        domain = st.selectbox("Project Domain", ["-- Select --", "Web App", "Mobile App", "AI Tool", "Enterprise Software", "Other"], key="domain")
        goal = st.selectbox("Primary Goal", ["-- Select --", "E-commerce", "Education", "Healthcare", "Finance", "Entertainment", "Other"], key="goal")
        duration = st.selectbox("Expected Duration", ["-- Select --", "<1 month", "1–3 months", "3–6 months", ">6 months"], key="duration")
        team_size = st.slider("Team Size", 1, 50, 5, key="team_size")
        experience = st.selectbox("Average Developer Experience", ["-- Select --", "Beginner", "Intermediate", "Expert"], key="experience")
        manager = st.selectbox("Project Manager Involved?", ["-- Select --", "Yes", "No"], key="manager")
        testing = st.selectbox("Testing Team Available?", ["-- Select --", "Yes", "No"], key="testing")

        complexity = st.selectbox("Project Complexity Level", ["-- Select --", "Low", "Medium", "High"], key="complexity")
        integration = st.selectbox("Integration Requirement", ["-- Select --", "None", "APIs", "Third-party tools", "Hardware"], key="integration")
        stack = st.selectbox("Preferred Technology Stack", ["-- Select --", "Custom", "Open Source", "Hybrid"], key="stack")
        scalability = st.selectbox("Scalability Requirement", ["-- Select --", "Low", "Medium", "High"], key="scalability")

        deadline = st.selectbox("Is there a fixed deadline?", ["-- Select --", "Yes", "No"], key="deadline")
        budget = st.selectbox("Estimated Budget Range (₹)", ["-- Select --", "<50K", "50K–1L", "1L–5L", ">5L", ">10L"], key="budget")
        maintenance = st.selectbox("Maintenance Required After Delivery?", ["-- Select --", "Yes", "No"], key="maintenance")
        payment = st.selectbox("Preferred Payment Type", ["-- Select --", "Hourly", "Fixed Cost", "Milestone-based"], key="payment")

        risk = st.selectbox("Risk Tolerance", ["-- Select --", "Low", "Medium", "High"], key="risk")
        priority = st.selectbox("Project Priority", ["-- Select --", "Speed", "Cost", "Quality", "Balance"], key="priority")
        involvement = st.selectbox("Client Involvement Level", ["-- Select --", "Low", "Moderate", "Active"], key="involvement")

        # --- Submit button inside form ---
        submitted = st.form_submit_button("✅ Save Project Input")

    # --- Only update client_input after form is submitted ---
    if submitted:
        fields = [
            domain, goal, duration, experience, manager, testing,
            complexity, integration, stack, scalability,
            deadline, budget, maintenance, payment,
            risk, priority, involvement
        ]
        if any(f == "-- Select --" for f in fields) or not client_name or not project_name:
            st.warning("⚠️ Please fill out all fields before saving!")
        else:
            # Update client_input dictionary safely
            st.session_state.client_input = {
                "client_name": client_name,
                "project_name": project_name,
                "domain": domain,
                "goal": goal,
                "team_size": team_size,
                "duration": duration,
                "experience": experience,
                "manager": manager,
                "testing": testing,
                "complexity": complexity,
                "integration": integration,
                "stack": stack,
                "scalability": scalability,
                "deadline": deadline,
                "budget": budget,
                "maintenance": maintenance,
                "payment": payment,
                "risk": risk,
                "priority": priority,
                "involvement": involvement
            }
            st.success("✅ Project details saved successfully! ")


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
            st.session_state.client_input = {k: st.session_state[k] for k in st.session_state if k not in ["client_input"]}
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
