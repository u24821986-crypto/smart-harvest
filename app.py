from flask import Flask, render_template, request

app = Flask(__name__)

# 1. Page Routes (This loads your HTML files)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/operations')
def operations():
    return render_template('operations.html')


# 2. Form Routes (This catches the data when you click submit)
@app.route('/Team-Leader', methods=['POST'])
def team_leader():
    return "Team data submitted! <a href='/operations'>Go back</a>"

@app.route('/Harvesting', methods=['POST'])
def harvesting():
    return "Harvest data submitted! <a href='/operations'>Go back</a>"

@app.route('/Logistics', methods=['POST'])
def logistics():
    return "Logistics data submitted! <a href='/operations'>Go back</a>"

@app.route('/Summary', methods=['POST'])
def summary():
    return "Notes submitted! <a href='/operations'>Go back</a>"


# 3. Run the app
if __name__ == '__main__':
    app.run(debug=True)
