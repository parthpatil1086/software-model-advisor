import streamlit as st
from utils.model_logic import suggest_model
from utils.cost_estimation import estimate_cost
from utils.budget_optimizer import optimize_budget
from utils.pdf_generator import generate_pdf

# --- Page Config ---
# st.image("assets/logo.png", width=120)  # adjust width as needed
st.set_page_config(page_title="Software Model & Budget Suggestion", layout="wide")

# --- App Title ---
st.title("Smart Software Model & Budget Suggestion System")

# --- Sidebar Navigation ---
st.sidebar.title("📂 Navigation")
page = st.sidebar.radio("Go to", [
    "Welcome",
    "Client Input",
    "Model Suggestion",
    "Cost Estimation",
    "Budget Optimizer",
    "Download Quotation"
])

# --- Session State for Client Input ---
if 'client_input' not in st.session_state:
    st.session_state.client_input = {}  

# --- Page 1: Welcome ---
if page == "Welcome":
    st.subheader("Welcome!")
    st.markdown("""
    This tool helps software engineers:
    - Choose the **right development model**
    - Get **cost estimates**
    - Suggest **improvements**
    - Export **quotations as PDF**
    
    Use the sidebar to begin.
    """)

# --- Page 2: Client Input ---
elif page == "Client Input":
    st.subheader("Enter Project Requirements")
    
    # Input widgets with empty defaults
    domain_options = ["-- Select --", "Web App", "Mobile App", "AI Tool", "Enterprise Software", "Other"]
    domain = st.selectbox("What type of software is being developed?", domain_options, index=0)
    
    team_size = st.slider("Team Size", 1, 20, 1)  # start at 1 (not saved until user clicks Save)
    
    duration_options = ["-- Select --", "<1 month", "1–3 months", "3–6 months", ">6 months"]
    project_duration = st.selectbox("Expected Duration", duration_options, index=0)
    
    deadline_options = ["-- Select --", "Yes", "No"]
    has_fixed_deadline = st.selectbox("Is there a fixed deadline?", deadline_options, index=0)
    
    budget_options = ["-- Select --", "<50K", "50K–1L", "1L–5L", ">5L"]
    budget_range = st.selectbox("Estimated Budget Range (₹)", budget_options, index=0)
    
    # Save button only works if user actually selected real options
    if st.button("✅ Save Project Input"):
        # Validate selections
        if domain == "-- Select --" or project_duration == "-- Select --" or has_fixed_deadline == "-- Select --" or budget_range == "-- Select --":
            st.warning("Please fill out all fields before saving!")
        else:
            st.session_state.client_input = {
                "domain": domain,
                "team_size": team_size,
                "duration": project_duration,
                "deadline": has_fixed_deadline,
                "budget": budget_range
            }
            st.success("Project input saved! Now you can go to other pages.")

# --- Page 3: Model Suggestion ---
elif page == "Model Suggestion":
    st.subheader("🔎 Suggested Development Model")

    if not st.session_state.client_input:
        st.info("No suggestion yet. Please fill out the Client Input first.")
    else:
        model = suggest_model(st.session_state.client_input)
        st.markdown(f"### ✅ Recommended Model: **{model}**")

# --- Page 4: Cost Estimation ---
elif page == "Cost Estimation":
    st.subheader("💰 Estimated Project Cost")

    if not st.session_state.client_input:
        st.info("No cost estimation yet. Please fill out the Client Input first.")
    else:
        cost = estimate_cost(st.session_state.client_input)
        st.markdown(f"### 💸 Estimated Cost: ₹**{cost}**")

# --- Page 5: Budget Optimizer ---
elif page == "Budget Optimizer":
    st.subheader("📉 Budget Optimization Suggestion")

    if not st.session_state.client_input:
        st.warning("Please fill out the client input first.")
    else:
        client_input = st.session_state.client_input
        # Get estimated cost first
        estimated_cost = estimate_cost(client_input)
        # Pass estimated_cost and client budget to optimizer
        budget_result = optimize_budget(estimated_cost, client_input["budget"])
        st.markdown(f"### 💡 Optimization Suggestion:\n\n{budget_result['message']}")
        if not budget_result["within_budget"]:
            for suggestion in budget_result["suggestions"]:
                st.markdown(f"- {suggestion}")

# --- Page 6: PDF Download ---
elif page == "Download Quotation":
    st.subheader("📄 Download Quotation PDF")

    if not st.session_state.client_input:
        st.warning("Please fill out the client input first.")
    else:
        if st.button("📥 Generate & Download PDF"):
            client_input = st.session_state.client_input
            client_name = client_input.get("client_name", "Unknown")
            # Calculate model, cost, and budget result
            model = suggest_model(client_input)
            estimated_cost = estimate_cost(client_input)
            budget_result = optimize_budget(estimated_cost, client_input["budget"])
            # Generate PDF
            file_path = generate_pdf(client_name, client_input, model, estimated_cost, budget_result)
            st.success(f"PDF generated: {file_path}")
            with open(file_path, "rb") as f:
                st.download_button(
                    label="📄 Download Quotation",
                    data=f,
                    file_name="software_quotation.pdf",
                    mime="application/pdf"
                )
