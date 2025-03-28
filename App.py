import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# App Title and Description
st.title("Enhanced Turo Car Rental ROI Calculator")
st.markdown("""
This advanced calculator estimates your Return on Investment (ROI) and the time required to recoup your car purchase cost when renting it out on Turo.
It offers detailed calculations, visualizations, and insights to support your decision-making process.

**Assumptions:**
- The monthly income is calculated as: **Daily Rental Rate x Rental Days per Month**.
- The model does not account for maintenance, insurance, depreciation, or seasonal variations.
""")

def calculate_roi(car_cost, daily_rental, monthly_rentals):
    """
    Calculate the monthly income, months to recoup the car purchase cost, and monthly ROI.

    Parameters:
    - car_cost (float): Purchase cost of the car.
    - daily_rental (float): Daily rental rate.
    - monthly_rentals (int): Number of days the car is rented per month.

    Returns:
    - monthly_income (float): Total income per month.
    - months_to_recoup (float): Number of months needed to recoup the investment.
    - roi (float): Monthly ROI as a percentage.
    """
    monthly_income = daily_rental * monthly_rentals
    if monthly_income == 0:
        return None, None, None  # Prevent division by zero
    months_to_recoup = car_cost / monthly_income
    roi = (monthly_income / car_cost) * 100
    return monthly_income, months_to_recoup, roi

# Sidebar for Inputs
st.sidebar.header("Input Parameters")
car_cost = st.sidebar.number_input("Car Purchase Cost ($):", min_value=0.0, step=1000.0, format="%.2f", value=25000.00)
daily_rental = st.sidebar.number_input("Daily Rental Rate ($):", min_value=0.0, step=10.0, format="%.2f", value=50.00)
monthly_rentals = st.sidebar.number_input("Estimated Rental Days per Month:", min_value=0, step=1, value=15)
st.sidebar.markdown("*(Note: This calculation assumes a steady rental income and does not include other expenses.)*")

# Calculate ROI when the button is clicked
if st.sidebar.button("Calculate ROI"):
    if car_cost > 0 and daily_rental > 0 and monthly_rentals > 0:
        monthly_income, months_to_recoup, roi = calculate_roi(car_cost, daily_rental, monthly_rentals)
        if monthly_income is not None:
            st.subheader("Calculation Results")
            st.write(f"**Monthly Income:** ${monthly_income:.2f}")
            st.write(f"**Estimated Months to Recoup Investment:** {months_to_recoup:.2f} months")
            st.write(f"**Monthly ROI:** {roi:.2f}%")
            
            st.markdown("### Detailed Calculation Breakdown")
            st.markdown(f"- **Monthly Income:** `Daily Rental Rate x Rental Days` = ${daily_rental:.2f} x {monthly_rentals} = ${monthly_income:.2f}")
            st.markdown(f"- **Recoupment Time:** `Car Cost / Monthly Income` = ${car_cost:.2f} / ${monthly_income:.2f} = {months_to_recoup:.2f} months")
            st.markdown(f"- **Monthly ROI:** `(Monthly Income / Car Cost) x 100` = ({monthly_income:.2f} / ${car_cost:.2f}) x 100 = {roi:.2f}%")
            
            # Generate a graph for cumulative income over time
            st.markdown("### Cumulative Income Visualization")
            max_months = int(months_to_recoup * 1.2)  # extend timeline 20% beyond recoupment time
            months = np.arange(1, max_months + 1)
            cumulative_income = monthly_income * months

            fig, ax = plt.subplots()
            ax.plot(months, cumulative_income, label="Cumulative Income", color='blue', marker='o')
            ax.axhline(y=car_cost, color='red', linestyle='--', label="Car Cost")
            ax.set_xlabel("Months")
            ax.set_ylabel("Cumulative Income ($)")
            ax.set_title("Cumulative Income vs. Investment")
            ax.legend()
            st.pyplot(fig)

            # Display a table of monthly milestones
            st.markdown("### Milestone Table")
            milestone_data = {"Month": months, "Cumulative Income ($)": cumulative_income}
            st.table(milestone_data)
            
            st.markdown("### Considerations & Next Steps")
            st.markdown("""
            **Additional Factors to Consider:**
            - **Maintenance & Insurance:** Ongoing costs that affect net ROI.
            - **Depreciation:** The decline in the car's value over time.
            - **Market Demand:** Rental frequency may vary seasonally.
            
            For a comprehensive analysis, consider integrating these factors into a detailed financial model.
            """)
        else:
            st.error("Calculation error: Monthly income is zero. Please adjust your inputs.")
    else:
        st.error("Please enter valid positive values for all parameters.")
