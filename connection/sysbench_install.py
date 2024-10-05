import paramiko
import sys
import yaml

# Remote server details from config.yaml
def load_config():
    with open("config.yaml", "r") as file:
        return yaml.safe_load(file)

# Function to establish SSH connection
def ssh_connect(config,env):
    try:
        ssh_key_path = config[env]['ssh']['key_path']
        key = paramiko.RSAKey.from_private_key_file(ssh_key_path)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(config[env]['ssh']['host'], username=config[env]['ssh']['username'], pkey=key)
        print(f"Successfully connected to {config[env]['ssh']['host']}")
        return client
    except Exception as e:
        print(f"Error: Unable to connect to {config[env]['ssh']['host']}. {e}")
        sys.exit(1)

# Function to check if sysbench is installed on remote VM
def install_sysbench(client):
    print("Checking if sysbench is installed...")
    stdin, stdout, stderr = client.exec_command("sysbench --version")
    sysbench_version = stdout.read().decode().strip()
    if "sysbench" in sysbench_version:
        print(f"Sysbench is installed: {sysbench_version}")
    else:
        print("Sysbench is not installed. Installing sysbench...")
        install_command = "sudo apt-get update && sudo apt-get install -y sysbench"
        stdin, stdout, stderr = client.exec_command(install_command)
        stdout.channel.recv_exit_status()  # Wait for the command to complete
        print("Sysbench installed successfully.")
