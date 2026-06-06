from flask import Flask, render_template_string, request

app = Flask(__name__)

# Temporary data storage for Vercel
daily_report = {
    "total_cash": 0.0,
    "total_weight": 0.0,
    "orders": []
}

# Per Kg-r Default Rate (Tumi chaile pore change korte paro)
rates = {
    "broiler": 180,
    "desi": 320,
    "layer": 220
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chicken Shop Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f4f6f9; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .card { border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: none; }
        .btn-success { background-color: #2da44e; border: none; }
        .btn-success:hover { background-color: #2c974b; }
    </style>
</head>
<body>
    <div class="container py-5">
        <h2 class="text-center mb-5 fw-bold text-dark">🐓 Chicken Shop Management System</h2>
        
        <div class="row g-4">
            <div class="col-md-5">
                <div class="card p-4">
                    <h4 class="text-success mb-4 fw-bold">New Sale / নতুন মেমো</h4>
                    <form action="/add_sale" method="POST">
                        <div class="mb-3">
                            <label class="form-label fw-semibold">Chicken Type (মুরগির ধরন)</label>
                            <select name="type" id="type" class="form-select form-select-lg" onchange="calculateLiveTotal()">
                                <option value="broiler">Broiler (₹180/kg)</option>
                                <option value="desi">Desi (₹320/kg)</option>
                                <option value="layer">Layer (₹220/kg)</option>
                            </select>
                        </div>
                        <div class="mb-4">
                            <label class="form-label fw-semibold">Weight in Kg (ওজন)</label>
                            <input type="number" name="weight" id="weight" step="0.001" class="form-control form-control-lg" placeholder="0.000" required oninput="calculateLiveTotal()">
                        </div>
                        <div class="p-3 bg-light rounded mb-4 border-start border-success border-4">
                            <h5 class="text-muted mb-1 small text-uppercase">Estimated Price</h5>
                            <h3 class="fw-bold text-dark" id="live-total">₹0.00</h3>
                        </div>
                        <button type="submit" class="btn btn-success btn-lg w-100 fw-bold">Save Sale (জমা করুন)</button>
                    </form>
                </div>
            </div>

            <div class="col-md-7">
                <div class="row g-3 mb-4">
                    <div class="col-6">
                        <div class="card bg-primary text-white p-4 text-center">
                            <span class="small text-uppercase opacity-75">Total Revenue</span>
                            <h2 class="fw-bold mt-1">₹{{ report.total_cash }}</h2>
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="card bg-warning text-dark p-4 text-center">
                            <span class="small text-uppercase opacity-75">Total Weight Sold</span>
                            <h2 class="fw-bold mt-1">{{ report.total_weight }} Kg</h2>
                        </div>
                    </div>
                </div>

                <div class="card p-4">
                    <h5 class="fw-bold text-secondary mb-3">Today's Sales History (আজকের বিক্রি)</h5>
                    <div class="table-responsive">
                        <table class="table table-striped align-middle">
                            <thead class="table-dark">
                                <tr>
                                    <th>Item Type</th>
                                    <th>Weight (Kg)</th>
                                    <th>Total Amount</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for order in report.orders %}
                                <tr>
                                    <td class="text-capitalize fw-semibold">{{ order.type }}</td>
                                    <td>{{ order.weight }} kg</td>
                                    <td class="fw-bold text-success">₹{{ order.amount }}</td>
                                </tr>
                                {% else %}
                                <tr>
                                    <td colspan="3" class="text-center text-muted py-4">No sales recorded yet.</td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const rates = { broiler: 180, desi: 320, layer: 220 };
        
        function calculateLiveTotal() {
            let type = document.getElementById('type').value;
            let weight = parseFloat(document.getElementById('weight').value) || 0;
            let total = weight * rates[type];
            document.getElementById('live-total').innerText = "₹" + total.toFixed(2);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, report=daily_report)

@app.route('/add_sale', methods=['POST'])
def add_sale():
    item_type = request.form.get('type')
    weight = float(request.form.get('weight', 0))
    
    if weight > 0:
        rate = rates.get(item_type, 0)
        amount = round(weight * rate, 2)
        
        daily_report["total_cash"] = round(daily_report["total_cash"] + amount, 2)
        daily_report["total_weight"] = round(daily_report["total_weight"] + weight, 3)
        daily_report["orders"].insert(0, {"type": item_type, "weight": weight, "amount": amount})
        
    return render_template_string(HTML_TEMPLATE, report=daily_report)
  
