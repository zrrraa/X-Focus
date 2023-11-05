import subprocess
from flask import Flask, render_template, request
import threading

app = Flask(__name__)

script1_process = None
script2_process = None
script2_running = False

@app.route('/')
def index():
    return render_template('index.html')

def run_script1():
    global script1_process
    script1_process = subprocess.Popen(['python', 'scripts/script1.py'])
    # script1_process = subprocess.Popen(['python', 'wifi_upload.py'])

def run_script2():
    global script2_process, script2_running
    script2_running = True
    script2_process = subprocess.Popen(['python', 'scripts/script2.py'])
    # script2_process = subprocess.Popen(['python', 'SVMImageClassification/SVM.py'])
    script2_process.wait()  # Wait for script2 to finish
    script2_running = False

@app.route('/run_script1')
def run_script1_endpoint():
    global script1_process, script2_process
    if script1_process is None or script1_process.poll() is not None:
        thread = threading.Thread(target=run_script1)
        thread.start()
        return '监听开始！'
    else:
        return '监听正在进行中，请勿重复点击'

@app.route('/run_script2')
def run_script2_endpoint():
    global script2_process
    if script2_process is None or script2_process.poll() is not None:
        thread = threading.Thread(target=run_script2)
        thread.start()
        return '生成报告中······'
    else:
        return '报告正在生成中，请勿重复点击'

@app.route('/check_script2')
def check_script2():
    global script2_running
    if script2_running:
        return '生成报告中······'
    else:
        return '报告生成完毕！'

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
