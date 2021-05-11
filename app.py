import time

from flask import Flask, render_template, request

app=Flask(__name__)

@app.route('/')
def main():
    return render_template('index1.html', datetime= time.strftime("%H:%M:%S"))

@app.route('/index2.html')
def gif():
    return render_template('index2.html')

@app.route('/index3.html')
def index3():
    return render_template('index3.html')

@app.route('/calculator.html')
def calculator():
    return render_template('calculator.html')

@app.route('/send', methods=['POST'])
def send():
    try:
        if request.method == 'POST':
            num1 = request.form['num1']
            num2 = request.form['num2']
            operation = request.form['operation']

            if operation == 'add':
                add=f"{float(num1)} + {float(num2)} = {float(num1) + float(num2)}"
                return render_template('calculator.html', sum=add)

            elif operation == 'subtract':
                sub = f"{float(num1)} - {float(num2)} = {float(num1) - float(num2)}"
                return render_template('calculator.html', sum=sub)

            elif operation == 'multiply':
                mul = f"{float(num1)} * {float(num2)} = {float(num1) * float(num2)}"
                return render_template('calculator.html', sum=mul)

            elif operation == 'divide':
                try:
                    div = f"{float(num1)} / {float(num2)} = {float(num1) / float(num2)}"
                except ZeroDivisionError as a:
                    return render_template('calculator.html', sum=f" Try again: {a}")
                else:
                    return render_template('calculator.html', sum=div)
            else:
                return render_template('calculator.html')
    except:
        return render_template('calculator.html', sum= f"Sorry,error appear")

@app.route('/word/')
def word1():
    return "Enter the information"

@app.route('/word/<name>')
def word(name):
    if len(name)%2==0:
        return name
    else:
        return name[::2]