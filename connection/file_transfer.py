from scp import SCPClient

def transfer_file_from_vm(client, remote_path, local_path):
    with SCPClient(client.get_transport()) as scp:
        scp.get(remote_path, local_path)
        print(f"File transferred from {remote_path} to {local_path}")