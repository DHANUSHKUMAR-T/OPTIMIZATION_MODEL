# Import necessary libraries
import pulp
import pandas as pd
import matplotlib.pyplot as plt

# Define the problem as a maximization problem
model = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define decision variables
x1 = pulp.LpVariable("Product_A", lowBound=0, cat="Continuous")
x2 = pulp.LpVariable("Product_B", lowBound=0, cat="Continuous")

# Sample input values (Assuming realistic inputs)
profit_A = 20
profit_B = 15
labor_A = 2
labor_B = 3
material_A = 3
material_B = 2
labor_limit = 50
material_limit = 50

# Objective Function
model += profit_A * x1 + profit_B * x2, "Total_Profit"

# Constraints
model += labor_A * x1 + labor_B * x2 <= labor_limit, "Labor_Constraint"
model += material_A * x1 + material_B * x2 <= material_limit, "Material_Constraint"

# Solve the problem
model.solve(pulp.PULP_CBC_CMD(msg=False))

# Get results
product_A = x1.varValue
product_B = x2.varValue
total_profit = pulp.value(model.objective)

# Create a DataFrame for insights
data = {
    "Variable": ["Product_A", "Product_B", "Total_Profit"],
    "Optimal Value": [product_A, product_B, total_profit]
}
df_results = pd.DataFrame(data)

# Generate a plot
plt.figure(figsize=(6, 4))
plt.bar(["Product A", "Product B"], [product_A, product_B], color=["blue", "orange"])
plt.xlabel("Products")
plt.ylabel("Optimal Units Produced")
plt.title("Optimal Production Levels")
plt.ylim(0, max(product_A, product_B) + 5)
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Save the plot
plot_path = "optimal_production.png"
plt.savefig(plot_path)

# Save results to a CSV
csv_path = "optimization_results.csv"
df_results.to_csv(csv_path, index=False)

# Save as Jupyter notebook files
problem_setup_path = "problem_setup.ipynb"
analysis_path = "analysis.ipynb"

# Generate Jupyter notebook content dynamically
from nbformat import v4 as nbf

# Problem Setup Notebook
nb1 = nbf.new_notebook()
nb1.cells = [
    nbf.new_markdown_cell("# Optimization Problem Setup\nThis notebook sets up and solves a simple linear programming problem using PuLP."),
    nbf.new_code_cell("""
import pulp

# Define the problem
model = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define variables
x1 = pulp.LpVariable("Product_A", lowBound=0, cat="Continuous")
x2 = pulp.LpVariable("Product_B", lowBound=0, cat="Continuous")

# Coefficients
profit_A = 20
profit_B = 15
labor_A = 2
labor_B = 3
material_A = 3
material_B = 2
labor_limit = 50
material_limit = 50

# Objective Function
model += profit_A * x1 + profit_B * x2, "Total_Profit"

# Constraints
model += labor_A * x1 + labor_B * x2 <= labor_limit, "Labor_Constraint"
model += material_A * x1 + material_B * x2 <= material_limit, "Material_Constraint"

# Solve
model.solve(pulp.PULP_CBC_CMD(msg=False))

# Display results
x1.varValue, x2.varValue, pulp.value(model.objective)
""")
]

# Analysis Notebook
nb2 = nbf.new_notebook()
nb2.cells = [
    nbf.new_markdown_cell("# Optimization Results Analysis\nThis notebook analyzes and visualizes the results from the optimization problem."),
    nbf.new_code_cell("""
import pandas as pd
import matplotlib.pyplot as plt

# Load results
df = pd.read_csv('optimization_results.csv')

# Display results
df
"""),
    nbf.new_code_cell("""
# Plot results
plt.figure(figsize=(6, 4))
plt.bar(df['Variable'][:-1], df['Optimal Value'][:-1], color=['blue', 'orange'])
plt.xlabel("Products")
plt.ylabel("Optimal Units Produced")
plt.title("Optimal Production Levels")
plt.ylim(0, max(df['Optimal Value'][:-1]) + 5)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()
""")
]

# Save notebooks
with open(problem_setup_path, "w") as f:
    f.write(nbf.writes(nb1))

with open(analysis_path, "w") as f:
    f.write(nbf.writes(nb2))

# Return file paths
problem_setup_path, analysis_path, plot_path, csv_path
