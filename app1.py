import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Tuition Smart Contract", layout="centered")

# Custom CSS for colors (Yarmouk University color palette)
st.markdown(
    """
    <style>
    .main {
        background-color: #f7f9fc;
    }
    .stButton>button {
        color: white;
        background-color: #003865;
    }
    .stTextInput>div>div>input {
        background-color: #ffffff;
    }
    .success-message {
        color: #1e7f3c;
        font-weight: bold;
        font-size: 18px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🎓 Tuition Payment Demo - Yarmouk University")

st.subheader("Enter Your Information:")

student_id = st.text_input("University ID:")
password = st.text_input("Password", type="password")

credit_hours = st.selectbox("Select Credit Hours", [9, 12, 15, 21])
price_per_hour = 45
total_due = credit_hours * price_per_hour

st.write(f"**Total Tuition Fee: {total_due} JOD**")

installment_now = st.number_input("Enter amount to pay now (JOD):", min_value=0, step=1)

if st.button("Pay Now"):
    if not student_id or not password:
        st.warning("Please enter your university ID and password.")
    elif installment_now <= 0:
        st.warning("Payment must be greater than 0.")
    elif installment_now > total_due:
        st.warning("You cannot pay more than the total due.")
    else:
        # Logic
        remaining = total_due - installment_now
        monthly_due = round(total_due / 3)
        today = datetime.today()
        dates = [today, today + timedelta(days=30), today + timedelta(days=60)]
        paid = [installment_now if i == 0 else 0 for i in range(3)]
        status = ["Paid" if paid[i] > 0 else "Pending" for i in range(3)]
        remaining_after = []

        temp = total_due
        for i in range(3):
            temp -= paid[i]
            remaining_after.append(temp)

        # DataFrame
        df = pd.DataFrame({
            "Installment #": ["1", "2", "3"],
            "Due Date": [d.strftime("%Y-%m-%d") for d in dates],
            "Installment Amount (JOD)": [monthly_due]*3,
            "Paid Amount (JOD)": paid,
            "Remaining After Payment": remaining_after,
            "Status": status
        })

        # Success message
        st.markdown('<div class="success-message">✅ Payment successful! Below is your updated installment schedule.</div>', unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True)
