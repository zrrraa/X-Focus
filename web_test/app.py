from flask import Flask, render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_program')
def run_program():
    try:
        output = subprocess.check_output(['python', 'scripts/your_program.py'])
        return output.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return f'Error: {e.output.decode("utf-8")}'

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)