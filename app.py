from flask import Flask, render_template, jsonify
import subprocess
import os
import signal

app = Flask(__name__)

processes = {
    'hand': None,
    'voice': None
}

def start_script(script_name):
    """Starts a script and returns its process."""
    if os.name == 'nt':
        # For Windows, create a new process group
        process = subprocess.Popen(
            ['python', script_name],
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
        )
    else:
        # For Unix-like systems, use a new session
        process = subprocess.Popen(
            ['python', script_name],
            preexec_fn=os.setsid
        )
    return process

def stop_process(process):
    """Stops a process and its children, cross-platform."""
    if process and process.poll() is None:
        if os.name == 'nt':
            # For Windows, send CTRL_C_EVENT to the process group
            process.send_signal(signal.CTRL_C_EVENT)
        else:
            # For Unix-like systems, kill the process group
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        process.wait()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start/<script>')
def start(script):
    if script in processes and processes[script] is None:
        if script == 'hand':
            processes['hand'] = start_script('hand_gesture.py')
        elif script == 'voice':
            processes['voice'] = start_script('voice_gesture.py')
        return jsonify(status=f'{script} started')
    return jsonify(status=f'{script} already running')

@app.route('/stop/<script>')
def stop(script):
    if script in processes and processes[script] is not None:
        stop_process(processes[script])
        processes[script] = None
        return jsonify(status=f'{script} stopped')
    return jsonify(status=f'{script} not running')

@app.route('/status')
def status():
    return jsonify({
        'hand': processes['hand'] is not None and processes['hand'].poll() is None,
        'voice': processes['voice'] is not None and processes['voice'].poll() is None
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)
