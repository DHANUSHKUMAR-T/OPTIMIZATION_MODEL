from flask import Flask, render_template, request
import pulp

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get user inputs
        profit_A = float(request.form["profit_A"])
        profit_B = float(request.form["profit_B"])
        labor_A = float(request.form["labor_A"])
        labor_B = float(request.form["labor_B"])
        material_A = float(request.form["material_A"])
        material_B = float(request.form["material_B"])
        labor_limit = float(request.form["labor_limit"])
        material_limit = float(request.form["material_limit"])

        # Define the LP problem
        model = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)
        x1 = pulp.LpVariable("Product_A", lowBound=0, cat="Continuous")
        x2 = pulp.LpVariable("Product_B", lowBound=0, cat="Continuous")

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

        return render_template("result.html", product_A=product_A, product_B=product_B, total_profit=total_profit)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True,port=5000)
