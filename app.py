"""
UmojaMath Tutoring Business Simulator - Standalone Version
All models included in single file for easy deployment

This application requires the following dependencies:
- streamlit>=1.28.0
- numpy>=1.24.0
- pandas>=2.0.0
- plotly>=5.15.0
- scipy>=1.10.0
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import math
from scipy.optimize import linprog

# ===== PRICING MODEL =====
class PricingModel:
    def __init__(self, tier1_rate=30, tier1_max=5, tier2_rate=28, tier2_max=10, tier3_rate=25):
        self.tier1_rate = tier1_rate
        self.tier1_max = tier1_max
        self.tier2_rate = tier2_rate
        self.tier2_max = tier2_max
        self.tier3_rate = tier3_rate
    
    def calculate_cost(self, hours):
        """Calculate cost based on piecewise function"""
        if hours <= self.tier1_max:
            return self.tier1_rate * hours
        elif hours <= self.tier2_max:
            return self.tier2_rate * hours
        else:
            return self.tier3_rate * hours

# ===== ADVERTISING MODEL =====
class AdvertisingModel:
    def __init__(self, max_reach=5000, growth_rate=0.1, cpm=5):
        self.max_reach = max_reach
        self.growth_rate = growth_rate
        self.cpm = cpm
    
    def calculate_reach(self, days):
        """Calculate reach using exponential growth model"""
        return self.max_reach * (1 - math.exp(-self.growth_rate * days))
    
    def calculate_cost(self, reach):
        """Calculate cost based on CPM"""
        return (reach / 1000) * self.cpm

# ===== PROFIT MODEL =====
class ProfitModel:
    def __init__(self, fixed_costs=2000, variable_cost=50, scaling_factor=0.5, avg_revenue_per_student=200):
        self.fixed_costs = fixed_costs
        self.variable_cost = variable_cost
        self.scaling_factor = scaling_factor
        self.avg_revenue_per_student = avg_revenue_per_student
    
    def calculate_expenses(self, students):
        """Calculate total expenses: E(s) = fixed_costs + variable_cost * s + scaling_factor * s²"""
        return self.fixed_costs + self.variable_cost * students + self.scaling_factor * (students ** 2)
    
    def calculate_revenue(self, students):
        """Calculate total revenue: R(s) = avg_revenue_per_student * s"""
        return self.avg_revenue_per_student * students
    
    def calculate_profit(self, students):
        """Calculate profit: P(s) = R(s) - E(s)"""
        return self.calculate_revenue(students) - self.calculate_expenses(students)
    
    def calculate_break_even(self):
        """Calculate break-even point where profit = 0"""
        a = -self.scaling_factor
        b = self.avg_revenue_per_student - self.variable_cost
        c = -self.fixed_costs
        
        discriminant = b**2 - 4*a*c
        
        if discriminant < 0:
            return None
        
        s1 = (-b + math.sqrt(discriminant)) / (2*a)
        s2 = (-b - math.sqrt(discriminant)) / (2*a)
        
        solutions = [s for s in [s1, s2] if s > 0]
        return min(solutions) if solutions else None
    
    def calculate_optimal_students(self):
        """Calculate optimal number of students for maximum profit"""
        optimal = (self.avg_revenue_per_student - self.variable_cost) / (2 * self.scaling_factor)
        return max(0, optimal)

# ===== SEASONALITY MODEL =====
class SeasonalityModel:
    def __init__(self, base_enrollment=50, amplitude1=20, amplitude2=10, phase1=0, phase2=0):
        self.base_enrollment = base_enrollment
        self.amplitude1 = amplitude1
        self.amplitude2 = amplitude2
        self.phase1 = phase1
        self.phase2 = phase2
    
    def calculate_enrollment(self, month):
        """Calculate enrollment using trigonometric model"""
        term1 = self.amplitude1 * math.sin(math.pi * (month + self.phase1) / 6)
        term2 = self.amplitude2 * math.cos(math.pi * (month + self.phase2) / 3)
        return self.base_enrollment + term1 + term2
    
    def generate_yearly_data(self):
        """Generate enrollment data for all 12 months"""
        months = np.arange(1, 13)
        enrollments = [self.calculate_enrollment(month) for month in months]
        return months, enrollments
    
    def find_peak_month(self):
        """Find the month with peak enrollment"""
        months, enrollments = self.generate_yearly_data()
        peak_idx = np.argmax(enrollments)
        return months[peak_idx], enrollments[peak_idx]

# ===== VISUALIZATION FUNCTIONS =====
def create_piecewise_plot(pricing_model, tier1_max, tier2_max, max_hours=20):
    """Create visualization for piecewise pricing function"""
    hours = np.linspace(1, max_hours, 200)
    costs = [pricing_model.calculate_cost(h) for h in hours]
    
    fig = go.Figure()
    
    # Add pricing curve
    fig.add_trace(go.Scatter(
        x=hours, y=costs,
        mode='lines',
        name='Pricing Function',
        line=dict(color='blue', width=3)
    ))
    
    # Add tier boundaries
    fig.add_vline(x=tier1_max, line_dash="dash", line_color="gray", annotation_text="Tier 1 Limit")
    fig.add_vline(x=tier2_max, line_dash="dash", line_color="gray", annotation_text="Tier 2 Limit")
    
    fig.update_layout(
        title="Piecewise Pricing Function",
        xaxis_title="Hours per Month",
        yaxis_title="Monthly Cost ($)",
        hovermode='x unified',
        height=500
    )
    
    return fig

def create_exponential_plot(advertising_model, current_days, target_percentage):
    """Create visualization for exponential advertising reach"""
    days = np.linspace(1, 30, 100)
    reach_values = [advertising_model.calculate_reach(d) for d in days]
    
    fig = go.Figure()
    
    # Reach curve
    fig.add_trace(go.Scatter(
        x=days, y=reach_values,
        mode='lines',
        name='Reach Over Time',
        line=dict(color='blue', width=3)
    ))
    
    # Current day marker
    current_reach = advertising_model.calculate_reach(current_days)
    fig.add_trace(go.Scatter(
        x=[current_days], y=[current_reach],
        mode='markers',
        marker=dict(size=12, color='red'),
        name='Current Day'
    ))
    
    # Target line
    target_reach = advertising_model.max_reach * target_percentage
    fig.add_hline(y=target_reach, line_dash="dash", line_color="green", 
                  annotation_text=f"{target_percentage*100}% Target")
    
    fig.update_layout(
        title="Exponential Advertising Reach Model",
        xaxis_title="Days",
        yaxis_title="People Reached",
        hovermode='x unified',
        height=500
    )
    
    return fig

def create_quadratic_plot(profit_model, current_students):
    """Create visualization for quadratic profit model"""
    students = np.linspace(1, 200, 200)
    
    revenues = [profit_model.calculate_revenue(s) for s in students]
    expenses = [profit_model.calculate_expenses(s) for s in students]
    profits = [profit_model.calculate_profit(s) for s in students]
    
    fig = go.Figure()
    
    # Revenue line
    fig.add_trace(go.Scatter(
        x=students, y=revenues,
        mode='lines',
        name='Revenue',
        line=dict(color='green', width=2)
    ))
    
    # Expenses curve
    fig.add_trace(go.Scatter(
        x=students, y=expenses,
        mode='lines',
        name='Expenses',
        line=dict(color='red', width=2)
    ))
    
    # Profit curve
    fig.add_trace(go.Scatter(
        x=students, y=profits,
        mode='lines',
        name='Profit',
        line=dict(color='blue', width=3)
    ))
    
    # Current position
    current_profit = profit_model.calculate_profit(current_students)
    fig.add_trace(go.Scatter(
        x=[current_students], y=[current_profit],
        mode='markers',
        marker=dict(size=12, color='purple'),
        name='Current Position'
    ))
    
    # Break-even point
    break_even = profit_model.calculate_break_even()
    if break_even:
        fig.add_vline(x=break_even, line_dash="dash", line_color="orange", 
                     annotation_text="Break-even")
    
    # Optimal point
    optimal_students = profit_model.calculate_optimal_students()
    optimal_profit = profit_model.calculate_profit(optimal_students)
    fig.add_trace(go.Scatter(
        x=[optimal_students], y=[optimal_profit],
        mode='markers',
        marker=dict(size=12, color='gold', symbol='star'),
        name='Optimal Point'
    ))
    
    fig.update_layout(
        title="Quadratic Profit Model",
        xaxis_title="Number of Students",
        yaxis_title="Amount ($)",
        hovermode='x unified',
        height=500
    )
    
    return fig

def create_trigonometric_plot(seasonality_model, current_month):
    """Create visualization for trigonometric seasonality model"""
    months = np.linspace(1, 12, 100)
    enrollments = [seasonality_model.calculate_enrollment(m) for m in months]
    
    month_points = np.arange(1, 13)
    monthly_enrollments = [seasonality_model.calculate_enrollment(m) for m in month_points]
    
    fig = go.Figure()
    
    # Continuous curve
    fig.add_trace(go.Scatter(
        x=months, y=enrollments,
        mode='lines',
        name='Enrollment Trend',
        line=dict(color='blue', width=3)
    ))
    
    # Monthly points
    fig.add_trace(go.Scatter(
        x=month_points, y=monthly_enrollments,
        mode='markers',
        marker=dict(size=8, color='red'),
        name='Monthly Values'
    ))
    
    # Current month marker
    current_enrollment = seasonality_model.calculate_enrollment(current_month)
    fig.add_trace(go.Scatter(
        x=[current_month], y=[current_enrollment],
        mode='markers',
        marker=dict(size=15, color='purple', symbol='star'),
        name='Current Month'
    ))
    
    # Add horizontal line for base enrollment
    fig.add_hline(y=seasonality_model.base_enrollment, line_dash="dash", 
                 line_color="gray", annotation_text="Base Enrollment")
    
    fig.update_layout(
        title="Seasonal Enrollment Patterns",
        xaxis_title="Month",
        yaxis_title="Number of Students",
        xaxis=dict(
            tickmode='array',
            tickvals=list(range(1, 13)),
            ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                     'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        ),
        hovermode='x unified',
        height=500
    )
    
    return fig

# ===== MAIN APPLICATION =====
def main():
    st.set_page_config(
        page_title="UmojaMath Tutoring Business Simulator",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("📚 UmojaMath Tutoring Business Simulator")
    st.markdown("""
    An interactive simulation of an African-centered math tutoring service using advanced precalculus concepts.
    This educational tool demonstrates how mathematical modeling applies to real-world business operations.
    """)
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    section = st.sidebar.radio(
        "Select a business aspect to explore:",
        ["Overview", "Pricing Model", "Advertising Campaign", "Profit Analysis", "Seasonal Trends"]
    )
    
    if section == "Overview":
        show_overview()
    elif section == "Pricing Model":
        show_pricing_model()
    elif section == "Advertising Campaign":
        show_advertising_model()
    elif section == "Profit Analysis":
        show_profit_model()
    elif section == "Seasonal Trends":
        show_seasonality_model()

def show_overview():
    st.header("🎯 Business Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("UmojaMath Tutoring Service")
        st.markdown("""
        **Mission**: Providing African-centered online math tutoring with cultural relevance and mathematical rigor.
        
        **Target Market**: African American high school students (grades 9-12)
        
        **Subjects Offered**:
        - Algebra II
        - Trigonometry
        - Precalculus
        
        **Format**: Zoom sessions (1-on-1 or small group)
        """)
    
    with col2:
        st.subheader("Mathematical Concepts Applied")
        st.markdown("""
        This simulation demonstrates:
        
        1. **Piecewise Functions** - Pricing structure optimization
        2. **Exponential Functions** - Advertising reach modeling
        3. **Quadratic Functions** - Profit maximization
        4. **Trigonometric Functions** - Seasonal trend analysis
        """)
    
    st.info("Use the sidebar to navigate through different business aspects and explore the mathematical models behind each component.")

def show_pricing_model():
    st.header("💰 Pricing Model - Piecewise Functions")
    
    st.markdown("""
    **Mathematical Concept**: Piecewise-defined functions to model different pricing tiers.
    
    The tutoring cost structure is defined as:
    """)
    
    st.latex(r"""
    f(x) = \begin{cases}
    30x & \text{if } 1 \leq x \leq 5 \text{ (discounted package)} \\
    28x & \text{if } 6 \leq x \leq 10 \text{ (bulk rate)} \\
    25x & \text{if } x > 10 \text{ (subscription)}
    \end{cases}
    """)
    
    # Interactive controls
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Pricing Parameters")
        tier1_rate = st.slider("Tier 1 Rate (1-5 hours)", 20, 40, 30)
        tier1_max = st.slider("Tier 1 Maximum Hours", 3, 8, 5)
        
        tier2_rate = st.slider("Tier 2 Rate (6-10 hours)", 20, 35, 28)
        tier2_max = st.slider("Tier 2 Maximum Hours", 8, 15, 10)
        
        tier3_rate = st.slider("Tier 3 Rate (11+ hours)", 15, 30, 25)
    
    with col2:
        st.subheader("Customer Analysis")
        hours_input = st.slider("Hours per month", 1, 20, 8)
        
        pricing_model = PricingModel(tier1_rate, tier1_max, tier2_rate, tier2_max, tier3_rate)
        cost = pricing_model.calculate_cost(hours_input)
        
        st.metric("Monthly Cost", f"${cost:.2f}")
        st.metric("Hourly Rate", f"${cost/hours_input:.2f}")
        
        if hours_input <= tier1_max:
            tier = "Tier 1 (Discounted Package)"
        elif hours_input <= tier2_max:
            tier = "Tier 2 (Bulk Rate)"
        else:
            tier = "Tier 3 (Subscription)"
        
        st.info(f"Customer is in: {tier}")
    
    # Create visualization
    fig = create_piecewise_plot(pricing_model, tier1_max, tier2_max)
    st.plotly_chart(fig, use_container_width=True)

def show_advertising_model():
    st.header("📈 Advertising Campaign - Exponential Functions")
    
    st.markdown("""
    **Mathematical Concept**: Exponential growth models to simulate advertising reach.
    
    The advertising reach model is defined as:
    """)
    
    st.latex(r"R(t) = R_{max}(1 - e^{-kt})")
    
    # Interactive controls
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Campaign Parameters")
        max_reach = st.slider("Maximum Reach", 1000, 10000, 5000)
        growth_rate = st.slider("Growth Rate (k)", 0.01, 0.5, 0.1)
        budget = st.slider("Budget ($)", 50, 1000, 200)
        cpm = st.slider("CPM (Cost per 1000 views)", 1, 20, 5)
    
    with col2:
        st.subheader("Campaign Analysis")
        
        target_percentage = 0.8
        days_to_target = -math.log(1 - target_percentage) / growth_rate
        
        st.metric("Days to reach 80% of max reach", f"{days_to_target:.1f} days")
        
        days_elapsed = st.slider("Days elapsed", 1, 30, 7)
        
        advertising_model = AdvertisingModel(max_reach, growth_rate, cpm)
        current_reach = advertising_model.calculate_reach(days_elapsed)
        cost_so_far = advertising_model.calculate_cost(current_reach)
        
        st.metric("Current Reach", f"{current_reach:,.0f} people")
        st.metric("Cost So Far", f"${cost_so_far:.2f}")
        
        max_reach_with_budget = (budget / cpm) * 1000
        st.metric("Max Reach with Budget", f"{max_reach_with_budget:,.0f} people")
    
    # Create visualization
    fig = create_exponential_plot(advertising_model, days_elapsed, target_percentage)
    st.plotly_chart(fig, use_container_width=True)

def show_profit_model():
    st.header("💹 Profit Analysis - Quadratic Modeling")
    
    st.markdown("""
    **Mathematical Concept**: Quadratic functions to model profit optimization.
    
    **Models**:
    - Total Expenses: E(s) = 2000 + 50s + 0.5s²
    - Revenue: R(s) = 200s
    - Profit: P(s) = R(s) - E(s) = -0.5s² + 150s - 2000
    
    Where *s* is the number of students.
    """)
    
    # Interactive controls
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Business Parameters")
        fixed_costs = st.slider("Fixed Costs ($)", 1000, 5000, 2000)
        variable_cost = st.slider("Variable Cost per Student ($)", 30, 100, 50)
        scaling_factor = st.slider("Scaling Factor", 0.1, 2.0, 0.5)
        
        avg_revenue_per_student = st.slider("Average Revenue per Student ($)", 100, 400, 200)
    
    with col2:
        st.subheader("Current Analysis")
        current_students = st.slider("Current Number of Students", 1, 200, 50)
        
        profit_model = ProfitModel(fixed_costs, variable_cost, scaling_factor, avg_revenue_per_student)
        
        current_revenue = profit_model.calculate_revenue(current_students)
        current_expenses = profit_model.calculate_expenses(current_students)
        current_profit = profit_model.calculate_profit(current_students)
        
        st.metric("Monthly Revenue", f"${current_revenue:,.2f}")
        st.metric("Monthly Expenses", f"${current_expenses:,.2f}")
        st.metric("Monthly Profit", f"${current_profit:,.2f}")
        
        break_even = profit_model.calculate_break_even()
        st.metric("Break-even Point", f"{break_even:.0f} students")
    
    # Create visualization
    fig = create_quadratic_plot(profit_model, current_students)
    st.plotly_chart(fig, use_container_width=True)
    
    # Optimization analysis
    st.subheader("Profit Optimization")
    col1, col2 = st.columns(2)
    
    with col1:
        optimal_students = profit_model.calculate_optimal_students()
        max_profit = profit_model.calculate_profit(optimal_students)
        st.metric("Optimal Student Count", f"{optimal_students:.0f}")
        st.metric("Maximum Profit", f"${max_profit:,.2f}")
    
    with col2:
        st.markdown("**Mathematical Solution:**")
        st.latex(r"P(s) = -0.5s^2 + 150s - 2000")
        st.latex(r"\frac{dP}{ds} = -s + 150 = 0")
        st.latex(r"s = 150")
        st.write(f"Optimal students: {optimal_students:.0f}")

def show_seasonality_model():
    st.header("🌊 Seasonal Trends - Trigonometric Modeling")
    
    st.markdown("""
    **Mathematical Concept**: Trigonometric functions to model seasonal enrollment patterns.
    
    **Model**: S(t) = 50 + 20sin(πt/6) + 10cos(πt/3)
    
    Where *t* is months since January.
    """)
    
    # Interactive controls
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Seasonal Parameters")
        base_enrollment = st.slider("Base Enrollment", 20, 100, 50)
        amplitude1 = st.slider("Primary Amplitude", 5, 40, 20)
        amplitude2 = st.slider("Secondary Amplitude", 2, 20, 10)
        
        phase1 = st.slider("Primary Phase (months)", -6, 6, 0)
        phase2 = st.slider("Secondary Phase (months)", -6, 6, 0)
    
    with col2:
        st.subheader("Current Analysis")
        current_month = st.slider("Current Month", 1, 12, 9)
        
        seasonality_model = SeasonalityModel(base_enrollment, amplitude1, amplitude2, phase1, phase2)
        
        current_enrollment = seasonality_model.calculate_enrollment(current_month)
        st.metric("Predicted Enrollment", f"{current_enrollment:.0f} students")
        
        peak_month, peak_enrollment = seasonality_model.find_peak_month()
        st.metric("Peak Month", f"Month {peak_month:.0f}")
        st.metric("Peak Enrollment", f"{peak_enrollment:.0f} students")
    
    # Create visualization
    fig = create_trigonometric_plot(seasonality_model, current_month)
    st.plotly_chart(fig, use_container_width=True)
    
    # Seasonal analysis
    st.subheader("Seasonal Analysis")
    months, enrollments = seasonality_model.generate_yearly_data()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Average Enrollment", f"{np.mean(enrollments):.0f}")
        st.metric("Maximum Enrollment", f"{np.max(enrollments):.0f}")
    
    with col2:
        st.metric("Minimum Enrollment", f"{np.min(enrollments):.0f}")
        st.metric("Seasonal Variation", f"{np.std(enrollments):.0f}")

if __name__ == "__main__":
    main()