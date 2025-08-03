from flask import Flask, request, render_template ,redirect
import os
import subprocess
import time

app = Flask(__name__)


PORT_FILE = "current_port.txt"

def get_current_port():
    # Check if the port file exists
    if os.path.exists(PORT_FILE):
        # Read the current port number from the file
        with open(PORT_FILE, "r") as f:
            return int(f.read().strip())
    else:
        # If the file doesn't exist, start from port 5000
        return 5000

@app.route('/')
def index():
    return render_template('index.html')

def fun():
    return render_template('deployed.html')



# @app.route('/deployed.html', methods=['POST'])
@app.route('/deployed.html', methods=['GET', 'POST'])
def deploy_function():
    # Trigger code when the deploy button is clicked
    print("Deploy button clicked!")
    subprocess.run(['bash', "run.sh"], check=True)
    # time.sleep(300)
    print("Deployed!")
    port = get_current_port()-1
    return render_template('deployed.html',port=port)
    # return redirect('file:///home/akanksha/Music/vcc_project/deployed.html')
    

@app.route('/delete', methods=['POST'])
def delete_function():
        if 'user_id' in request.form:
            user_id = request.form['user_id']
        # Run your script with the user_id as needed
            subprocess.run(['bash', 'delete.sh', user_id], check=True)
            return redirect('/')  # Redirect to homepage or any other page
        else:
            return "User ID not found in the form"


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)
