import os
import subprocess

# File to store the current port number
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

def save_current_port(port):
    # Save the current port number to the file
    with open(PORT_FILE, "w") as f:
        f.write(str(port))

def add_container(pod_name, namespace):
    # Get the current port number
    current_port = get_current_port()

    # Increment the port number by one for the next container
    next_port = current_port + 1

    # Define the kubectl command to add a container to the pod
    kubectl_command = f"kubectl get pod {pod_name} -n {namespace} -o yaml | kubectl replace --force -f -"

    # Define the YAML snippet to add the new container
    yaml_snippet = f"""
        spec:
          containers:
          - name: random-quote{next_port}
            image: prerna14/final-random-quote1
            ports:
            - containerPort: {next_port}
            env:
            - name: PORT
              value: "{next_port}"
    """

    # Execute the kubectl command with the YAML snippet
    process = subprocess.Popen(kubectl_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate(input=yaml_snippet.encode())

    if process.returncode != 0:
        # Handle error if kubectl command failed
        return f'Error: {stderr.decode()}', 500

    # Save the next port number for the next function call
    save_current_port(next_port)

    return f'Container added successfully with port: {next_port}', 200

# Example usage
pod_name = "apiVersion: v1
kind: Pod
metadata:
  name: mypod
spec:
  containers:
  - name: main-container
    image: main-image:latest
    ports:
    - containerPort: 80
  initContainers:
  - name: new-container
    image: new-container-image:latest
    command: ['sh', '-c', 'echo "Hello from the new container"']
"
namespace = "default"
response, status_code = add_container(pod_name, namespace)
print(response)
print(status_code)
