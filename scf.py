import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px

# -- Page setup --
st.set_page_config(page_title="Yarmouk University Tuition Smart Contract", layout="centered", page_icon="🎓")

# -- Styling --
primary_color = "#003865"   # Dark Blue
accent_color = "#f39200"    # Orange
background_color = "#f7f9fc"
success_color = "#1e7f3c"

st.markdown(f"""
<style>
body {{
    background-color: {background_color};
    color: {primary_color};
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}}
.stButton>button {{
    background-color: {primary_color};
    color: white;
    font-weight: bold;
    border-radius: 8px;
    padding: 8px 18px;
}}
.stTextInput>div>div>input {{
    border: 2px solid {primary_color};
    border-radius: 6px;
    padding: 8px;
}}
.success-message {{
    color: {success_color};
    font-weight: 700;
    font-size: 20px;
    margin-top: 20px;
}}
.table-header {{
    font-weight: 700;
    font-size: 16px;
    color: {accent_color};
}}
</style>
""", unsafe_allow_html=True)

st.title("🎓 Yarmouk University Tuition Payment Demo")
st.write("---")

# --- Input Form ---
with st.form("payment_form"):
    st.subheader("Student Credentials")
    student_id = st.text_input("University ID", max_chars=10)
    password = st.text_input("Password", type="password")

    st.subheader("Payment Details")
    funding_type = st.selectbox("Select Funding Type", [
        "Royal Scholarship", "Teachers' Scholarship", "Staff Grant",
        "Loans & Grants", "Regular", "Parallel"])

    credit_hours = st.selectbox("Select Number of Credit Hours", options=[9, 12, 15, 21])

    # Determine price per hour based on funding type
    if funding_type == "Royal Scholarship":
        price_per_hour = 45
    elif funding_type == "Teachers' Scholarship":
        price_per_hour = 40
    elif funding_type == "Staff Grant":
        price_per_hour = 35
    elif funding_type == "Loans & Grants":
        price_per_hour = 0
    elif funding_type == "Regular":
        price_per_hour = 50
    elif funding_type == "Parallel":
        price_per_hour = 60
    else:
        price_per_hour = 0

    academic_fees = 60
    tuition_only = credit_hours * price_per_hour
    total_amount = tuition_only + academic_fees

    st.markdown(f"""
        **Credit Hour Price:** {price_per_hour} JOD  
        **Tuition Only:** {tuition_only} JOD  
        **Academic Fees:** {academic_fees} JOD  
        **Total Tuition Fee:** {total_amount} JOD
    """)

    pay_amount = st.number_input("Enter Payment Amount (JOD)", min_value=1, max_value=total_amount, step=1)

    # Gas fee (covered by university)
    gas_fee_rate = 0.02
    gas_fee = round(pay_amount * gas_fee_rate, 2)
    effective_payment = pay_amount

    st.markdown(f"""
        **Estimated Gas Fee (Paid by University):** {gas_fee} JOD  
        **Payment Received:** {effective_payment} JOD
    """)

    submitted = st.form_submit_button("Confirm Payment")

# --- After submission ---
if submitted:
    if not student_id or not password:
        st.error("⚠️ Please enter your university ID and password.")
    elif pay_amount > total_amount:
        st.error("⚠️ Payment cannot exceed total tuition fee.")
    else:
        st.success(f"✅ Payment of {pay_amount} JOD received successfully (Gas Fee: {gas_fee} JOD paid by university)")

        # Installment setup
        months = 3
        installment_amount = total_amount / months
        remaining_amount = total_amount - effective_payment

        today = datetime.today()
        due_dates = [today + timedelta(days=30*i) for i in range(months)]
        reminder_dates = [d - timedelta(days=14) for d in due_dates]

        payments = [effective_payment] + [0]*(months-1)
        statuses = ["Paid" if effective_payment > 0 else "Pending"] + ["Pending"]*(months-1)
        remaining_after_payments = [total_amount - sum(payments[:i+1]) for i in range(months)]

        df = pd.DataFrame({
            "Installment #": [f"#{i+1}" for i in range(months)],
            "Due Date": [d.strftime("%Y-%m-%d") for d in due_dates],
            "Reminder Date (2 weeks before)": [r.strftime("%Y-%m-%d") for r in reminder_dates],
            "Installment Amount (JOD)": [round(installment_amount, 2)]*months,
            "Paid Amount (JOD)": payments,
            "Remaining After Payment": remaining_after_payments,
            "Status": statuses
        })

        st.markdown("### Installment Schedule:")
        st.dataframe(df.style.applymap(
            lambda val: 'color: green;' if val == 'Paid' else ('color: red;' if val == 'Pending' else ''),
            subset=["Status"]))

        # --- KPIs ---
        st.write("---")
        st.subheader("Payment Overview")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Tuition (JOD)", f"{total_amount}")
        col2.metric("Paid (after gas)", f"{effective_payment}")
        col3.metric("Remaining Amount", f"{remaining_amount}")
        paid_installments = sum([1 for s in statuses if s == "Paid"])
        col4.metric("Paid Installments", f"{paid_installments} / {months}")

        # --- Progress bar ---
        progress = effective_payment / total_amount
        st.progress(progress)

        # --- Chart ---
        fig = px.pie(
            names=["Paid", "Remaining"],
            values=[effective_payment, remaining_amount],
            color_discrete_map={"Paid": primary_color, "Remaining": "#cccccc"},
            title="Payment Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)
