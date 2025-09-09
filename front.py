from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('multiply.html')

@app.route('/multiply', methods=['GET', 'POST'])
def multiply():
    if request.method == 'POST':
        num1 = float(request.form.get('num1'))
        num2 = float(request.form.get('num2'))
        return f"Result: {num1 * num2}"
    return render_template('multiply.html')

if __name__ == '__main__':
    app.run(debug=True)