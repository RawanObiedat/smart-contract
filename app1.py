import streamlit as st
import plotly.express as px
from datetime import datetime, timedelta

# ----- إعدادات الصفحة -----
st.set_page_config(
    page_title="Yarmouk Smart Contract Demo",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ----- الشعار -----
st.image("https://upload.wikimedia.org/wikipedia/en/e/e7/Yarmouk_University_Logo.png", width=150)

# ----- العنوان -----
st.markdown("<h1 style='color:#006400;'>Smart Tuition Payment System - Yarmouk University</h1>", unsafe_allow_html=True)

st.markdown("<h4 style='color:#444444;'>Pay your university fees securely and flexibly without intermediaries</h4>", unsafe_allow_html=True)

# ----- بيانات الطالب -----
st.subheader("🔐 Student Login")
student_id = st.text_input("University ID")
password = st.text_input("Password", type="password")

# ----- تحديد الساعات -----
st.subheader("🎓 Registration Info")
credit_hours = st.slider("Select number of credit hours", 9, 12, 15, 21)
hour_price = 48  # دينار
total_amount = credit_hours * hour_price
st.markdown(f"<p style='color:#006400;'>Total Tuition Fees: <strong>{total_amount} JD</strong></p>", unsafe_allow_html=True)

# ----- طريقة الدفع -----
st.subheader("💳 Payment Options")
payment_type = st.radio("Choose payment method", ["Full Payment", "Installments"])

# ----- شروط الدفع بالتقسيط -----
installments_ok = True
installment_schedule = []

if payment_type == "Installments":
    st.info("You must complete 3 equal payments within 3 months.")
    today = datetime.today()
    installment_amount = total_amount / 3
    for i in range(3):
        due_date = today + timedelta(days=30 * (i + 1))
        installment_schedule.append((f"Installment {i+1}", f"{installment_amount:.2f} JD", due_date.strftime("%Y-%m-%d")))
    for name, amount, date in installment_schedule:
        st.markdown(f"🔸 **{name}**: {amount} due on {date}")
else:
    st.success(f"You will pay the full amount of {total_amount} JD.")

# ----- تنفيذ الدفع -----
if st.button("🟢 Confirm Payment"):
    if student_id and password:
        st.success("✅ Payment Confirmed")
        st.balloons()

        # ----- داشبورد -----
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<h2 style='color:#006400;'>📊 Dashboard Overview</h2>", unsafe_allow_html=True)

        # حالة الدفع
        if payment_type == "Full Payment":
            paid = total_amount
            remaining = 0
        else:
            paid = installment_amount
            remaining = total_amount - paid

        # شارت دائري
        fig = px.pie(
            names=["Paid", "Remaining"],
            values=[paid, remaining],
            color_discrete_sequence=["#006400", "#D3D3D3"]
        )
        st.plotly_chart(fig, use_container_width=True)

        # KPIs
        st.markdown("### 📌 Key Info")
        st.markdown(f"""
        <div style='background-color:#F0F8F0;padding:15px;border-radius:10px;'>
        <ul style='color:#006400;font-size:16px;'>
            <li><strong>Student ID:</strong> {student_id}</li>
            <li><strong>Total Fees:</strong> {total_amount:.2f} JD</li>
            <li><strong>Paid:</strong> {paid:.2f} JD</li>
            <li><strong>Remaining:</strong> {remaining:.2f} JD</li>
            <li><strong>Payment Method:</strong> {payment_type}</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.error("Please enter both your University ID and password.")
