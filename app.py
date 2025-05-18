import streamlit as st
from datetime import date, timedelta

st.set_page_config(page_title="Smart Contract with Fixed Installments", page_icon="📄")

st.title("📄 Smart Contract for Course Registration with University Installments")

# Student information
student_id = st.text_input("University ID:")
password = st.text_input("University Password:", type="password")

# Registration details
credit_hours = st.number_input("Number of Credit Hours:", min_value=1, step=1)
hour_price = 50  # fixed price per credit hour
total_amount = credit_hours * hour_price
st.info(f"💡 Total tuition fee: ${total_amount}")

# Fixed installment terms set by the university
num_installments = 3
duration_months = 3
installment_amount = total_amount / num_installments

st.markdown(f"""
### Installment Terms Set by the University
- Number of installments: **{num_installments} payments**
- Installment duration: **{duration_months} months**
- Amount per installment: **${installment_amount:.2f}**
""")

# Contract start date is today
start_date = date.today()
# Contract end date after installment duration
end_date = start_date + timedelta(days=duration_months*30)  # approximately 3 months

# Warning if close to installment period end (within 10 days)
days_left = (end_date - start_date).days
if days_left <= 10:
    st.warning(f"⚠️ Reminder: Only {days_left} days left to complete the payments")

# Amount paid now
amount_paid = st.number_input("Amount paid now:", min_value=0.0, step=10.0)

# Contract activation check
if st.button("Activate Contract"):
    if not student_id or not password:
        st.error("❌ Please enter your university ID and password.")
    elif amount_paid >= installment_amount:
        st.success("✅ Conditions met, contract activated and payment process can start.")
        st.markdown("---")
        st.markdown("### 📑 Smart Contract Summary")

        st.markdown(f"""
        - Student ID: **{student_id}**
        - Credit Hours: **{credit_hours}**
        - Total Price: **${total_amount}**
        - Amount per Installment: **${installment_amount:.2f}**
        - Number of Installments: **{num_installments}**
        - Installment Duration: **{duration_months} months**
        - Amount Paid Now: **${amount_paid}**
        - Installment Start Date: **{start_date}**
        - Installment End Date: **{end_date}**
        """)
    else:
        st.error(f"❌ You must pay at least the first installment: ${installment_amount:.2f}")
