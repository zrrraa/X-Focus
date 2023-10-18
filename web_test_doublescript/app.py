from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

# 定义两个脚本的运行状态
script1_running = False
script2_running = False

def run_script(script):
    global script1_running, script2_running
    if script == "script1":
        script1_running = True
        subprocess.call(["python", "scripts/script1.py"])  # 替换为脚本1的运行命令
        script1_running = False
    elif script == "script2":
        script2_running = True
        subprocess.call(["python", "scripts/script2.py"])  # 替换为脚本2的运行命令
        script2_running = False

@app.route('/check_status', methods=['GET'])
def check_status():
    script = request.args.get('script')
    status = ""
    if script == "script1":
        status = "running" if script1_running else "stopped"
    elif script == "script2":
        status = "running" if script2_running else "stopped"
    return jsonify({'status': status})

@app.route('/stop_script', methods=['GET'])
def stop_script():
    script = request.args.get('script')
    if script == "script1":
        global script1_running
        script1_running = False
    elif script == "script2":
        global script2_running
        script2_running = False
    return jsonify({'message': f'{script} stopped'})

@app.route('/run_script', methods=['GET'])
def start_script():
    script = request.args.get('script')
    if script == "script1" and not script1_running:
        run_script("script1")
    elif script == "script2" and not script2_running:
        run_script("script2")
    return jsonify({'message': f'{script} started'})

if __name__ == '__main__':
    app.run()