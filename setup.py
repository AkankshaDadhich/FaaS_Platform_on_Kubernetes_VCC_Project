import os
from kubernetes import client, config

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

    # Load Kubernetes configuration
    config.load_kube_config()

    # Initialize Kubernetes API client
    api_instance = client.CoreV1Api()

    # Define the container to be added
    new_container = client.V1Container(
        name=f"random-quote{next_port}",  # Use the incremented port number in the container name
        image="prerna14/final-random-quote1",
        ports=[client.V1ContainerPort(container_port=next_port)],  # Use the incremented port number
        env=[client.V1EnvVar(name="PORT", value=str(next_port))]  # Use the incremented port number as string
        # Add additional container configuration here if needed
    )

    # Define the pod's container list
    containers = [new_container]

    # Fetch the existing pod's configuration
    pod = api_instance.read_namespaced_pod(name=pod_name, namespace=namespace)

    # Append the new container to the existing list of containers
    if pod.spec.containers is not None:
        containers += pod.spec.containers

    # Update the pod's configuration with the new container
    pod.spec.containers = containers

    # Apply the updated pod configuration
    api_instance.replace_namespaced_pod(name=pod_name, namespace=namespace, body=pod)

    # Save the next port number for the next function call
    save_current_port(next_port)

    return f'Container added successfully with port: {next_port}', 200

# Example usage
pod_name = "random-quote-2-7bf8d5c786-9fw67"
namespace = "default"
response, status_code = add_container(pod_name, namespace)
print(response)
print(status_code)