# UmojaMath Tutoring Business Simulator

## Overview

This is an interactive Streamlit application that simulates an African-centered math tutoring business called "UmojaMath Tutoring." The application demonstrates how advanced precalculus concepts can be applied to real-world business operations through mathematical modeling and optimization.

The simulator provides interactive visualizations and analysis for various business aspects including pricing strategies, advertising campaigns, tutor scheduling, profit analysis, and seasonal demand patterns.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web application
- **Layout**: Wide layout with expandable sidebar navigation
- **Visualization**: Plotly for interactive charts and graphs
- **Navigation**: Radio button sidebar for section selection

### Backend Architecture
- **Structure**: Modular design with separate model classes
- **Models**: Individual Python classes for each business aspect
- **Utilities**: Shared visualization functions
- **Data Processing**: NumPy and Pandas for numerical computations

### Mathematical Models
- **Pricing**: Piecewise function implementation
- **Advertising**: Exponential growth and logarithmic models
- **Scheduling**: Linear programming optimization
- **Profit**: Quadratic profit functions
- **Seasonality**: Trigonometric functions for seasonal patterns

## Key Components

### 1. Pricing Model (`models/pricing.py`)
- **Purpose**: Implements tiered pricing structure using piecewise functions
- **Features**: 
  - Three-tier pricing ($30, $28, $25 per hour)
  - Revenue optimization
  - Budget-based package recommendations
- **Mathematical Concept**: Piecewise-defined functions

### 2. Advertising Model (`models/advertising.py`)
- **Purpose**: Models advertising reach and cost optimization
- **Features**:
  - Exponential growth model for reach calculation
  - CPM-based cost calculations
  - Budget optimization algorithms
- **Mathematical Concept**: Exponential and logarithmic functions

### 3. Scheduling Model (`models/scheduling.py`)
- **Purpose**: Optimizes tutor scheduling using linear programming
- **Features**:
  - Constraint-based optimization
  - Tutor-subject assignment matrix
  - Demand satisfaction algorithms
- **Mathematical Concept**: Linear programming and optimization

### 4. Profit Model (`models/profit.py`)
- **Purpose**: Analyzes profit optimization using quadratic functions
- **Features**:
  - Fixed and variable cost modeling
  - Break-even analysis
  - Optimal student capacity calculation
- **Mathematical Concept**: Quadratic functions and optimization

### 5. Seasonality Model (`models/seasonality.py`)
- **Purpose**: Models seasonal enrollment patterns
- **Features**:
  - Trigonometric enrollment modeling
  - Peak/trough identification
  - High/low season analysis
- **Mathematical Concept**: Trigonometric functions

### 6. Visualization Utilities (`utils/visualizations.py`)
- **Purpose**: Creates interactive plots for mathematical models
- **Features**:
  - Piecewise function visualization
  - Exponential and logarithmic plots
  - Quadratic and trigonometric visualizations

## Data Flow

1. **User Input**: Users select business aspects through sidebar navigation
2. **Model Instantiation**: Relevant mathematical models are created with default or user-specified parameters
3. **Calculation**: Models perform mathematical computations using NumPy and SciPy
4. **Visualization**: Results are displayed using Plotly interactive charts
5. **Analysis**: Key metrics and insights are presented to the user

## External Dependencies

### Core Libraries
- **Streamlit**: Web application framework
- **NumPy**: Numerical computations
- **Pandas**: Data manipulation
- **Plotly**: Interactive visualizations
- **SciPy**: Scientific computing and optimization

### Mathematical Libraries
- **scipy.optimize**: Linear programming solver
- **math**: Mathematical functions
- **numpy**: Advanced mathematical operations

## Deployment Strategy

### Development Environment
- **Platform**: Replit-compatible Python environment
- **Configuration**: Streamlit application with wide layout
- **Structure**: Modular architecture for easy maintenance

### File Organization
- `app.py`: Main application entry point
- `models/`: Mathematical model implementations
- `utils/`: Shared utility functions
- `attached_assets/`: Documentation and requirements

### Running the Application
The application is designed to run with: `streamlit run app.py`

### Key Features for Deployment
- **Responsive Design**: Wide layout optimized for various screen sizes
- **Interactive Elements**: Real-time mathematical calculations
- **Educational Focus**: Clear explanations of mathematical concepts
- **Performance**: Efficient calculations using optimized libraries

The application serves as both an educational tool and a business simulation, demonstrating practical applications of precalculus concepts in real-world scenarios.