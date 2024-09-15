from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Global variables to hold the data
people_salaries = {}
item_expenses = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/collect_salaries', methods=['GET', 'POST'])
def collect_salaries():
    if request.method == 'POST':
        num_people = int(request.form['num_people'])
        return render_template('salaries.html', num_people=num_people)
    return redirect(url_for('index'))

@app.route('/submit_salaries', methods=['POST'])
def submit_salaries():
    global people_salaries
    num_people = int(request.form['num_people'])
    total_salaries = 0
    for i in range(num_people):
        name = request.form[f'name_{i}']
        salary = int(request.form[f'salary_{i}'])
        people_salaries[name] = salary
        total_salaries += salary
    return render_template('expenses.html', total_salaries=total_salaries)

@app.route('/submit_expenses', methods=['POST'])
def submit_expenses():
    global item_expenses
    total_expenses = 0
    items = request.form.getlist('item[]')
    prices = request.form.getlist('price[]')

    for item, price in zip(items, prices):
        item_expenses[item] = int(price)
        total_expenses += int(price)

    total_salaries = sum(people_salaries.values())
    remaining_amount = total_salaries - total_expenses

    return render_template('results.html', total_salaries=total_salaries, 
                           total_expenses=total_expenses, remaining_amount=remaining_amount)

if __name__ == '__main__':
    app.run(debug=True)
