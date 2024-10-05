from db_connect import load_config, connect_to_database, close_database_connection
from sysbench_install import install_sysbench, ssh_connect
from sysbench_test import perform_sysbench_test, prepare_database
from file_transfer import transfer_file_from_vm

def select_environment():
    print("Select environment:")
    print("1. OpenStack")
    print("2. AWS")
    
    choice = input("Enter your choice (1/2): ")
    if choice == "1":
        return "openstack"
    elif choice == "2":
        return "aws"
    else:
        print("Invalid choice")
        return None
    
def main():
    # Step 1: Establish database connection
    config = load_config()
    # Select environment (OpenStack or AWS)
    env = select_environment()
    if env is None:
        return

    db_config = config[env]['database']
    #db_config = config['database']

    connection = connect_to_database(db_config)
    if connection is None:
        print("Error connecting to the database. Exiting.")
        return
    
    # Step 2: Establish ssh connection from local host to VM
    client = ssh_connect(config, env)
    
    # Step 3: Install sysbench if not already installed
    #install_sysbench(client)

    # Step 4: Prepare the database
    #prepare_database(client, config, env)

    # Step 5: Perform sysbench test (if needed)
    perform_sysbench_test(client, config, env)

    # Transfer the sysbench metrics file from the VM to the local machine
    transfer_file_from_vm(client, 'sysbench_metrics.txt', 'sysbench_metrics.txt')

    # Close SSH connection
    client.close()

    # Close database connection
    close_database_connection(connection)

if __name__ == "__main__":
    main()
