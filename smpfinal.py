from datetime import datetime, timedelta

# ----------------------------
# Funding Types and Hourly Rates
# ----------------------------
funding_options = {
    "Royal Grant": 45,
    "Teachers Grant": 40,
    "Staff Grant": 35,
    "Loans and Scholarships": 0,
    "Regular": 50,
    "Parallel": 60
}

# ----------------------------
# Input Section
# ----------------------------
# Student input (these would typically come from a UI in a real application)
selected_funding = "Teachers Grant"  # Dropdown: user selects from funding_options keys
credit_hours = 15                    # Number of credit hours student will register
university_fee = 60                 # Fixed university fee

payment_type = "Partial"            # Options: "Full" or "Partial"
amount_paid = 400                   # If Partial, how much the student paid

# ----------------------------
# Tuition Calculation
# ----------------------------
price_per_hour = funding_options[selected_funding]
tuition_cost = price_per_hour * credit_hours
total_due = tuition_cost + university_fee

# ----------------------------
# Installment Setup
# ----------------------------
installments = []
installment_amount = round(total_due / 3, 2)

# Example due dates
due_dates = [
    datetime(2025, 5, 18),
    datetime(2025, 6, 17),
    datetime(2025, 7, 17)
]

# Remaining amount to distribute across installments
remaining_payment = amount_paid if payment_type == "Partial" else total_due

# ----------------------------
# Generate Installments
# ----------------------------
for i in range(3):
    current_due = installment_amount
    paid = 0

    if payment_type == "Full":
        paid = current_due
    elif payment_type == "Partial":
        if remaining_payment >= current_due:
            paid = current_due
            remaining_payment -= current_due
        else:
            paid = remaining_payment
            remaining_payment = 0

    remaining_after_payment = round(max(current_due - paid, 0), 2)
    status = "Paid" if paid == current_due else "Partial" if paid > 0 else "Pending"

    installment = {
        "Installment #": f"#{i + 1}",
        "Due Date": due_dates[i].strftime("%Y-%m-%d"),
        "Reminder Date": (due_dates[i] - timedelta(days=14)).strftime("%Y-%m-%d"),
        "Installment Amount (JOD)": current_due,
        "Paid Amount (JOD)": round(paid, 2),
        "Remaining After Payment (JOD)": remaining_after_payment,
        "Status": status
    }

    installments.append(installment)

# ----------------------------
# Output Summary
# ----------------------------
print("🧾 Payment Summary:")
print({
    "Funding Type": selected_funding,
    "Credit Hour Price (JOD)": price_per_hour,
    "Credit Hours": credit_hours,
    "University Fee (JOD)": university_fee,
    "Total Amount Due (JOD)": total_due,
    "Payment Type": payment_type,
    "Amount Paid (JOD)": amount_paid if payment_type == "Partial" else total_due
})

print("\n📅 Installment Breakdown:\n")
for installment in installments:
    print(installment)

