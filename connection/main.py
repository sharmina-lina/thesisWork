from db_connect import load_config, connect_to_database, close_database_connection
from sysbench_install import install_sysbench, ssh_connect
from sysbench_test import perform_sysbench_test, prepare_database
from file_transfer import transfer_file_from_vm
from parse_sysbench import parse_sysbench_output
from plot_dashboard import plot_sysbench_dashboard
import pandas as pd

    
def main():
    # Step 1: Establish database connection
    config = load_config()

    db_config = config['database']
    
    connection = connect_to_database(db_config)
    if connection is None:
        print("Error connecting to the database. Exiting.")
        return
    
    # Step 2: Establish ssh connection from local host to VM
    client = ssh_connect(config)
    
    # Step 3: Install sysbench if not already installed
    install_sysbench(client)

    # Step 4: Prepare the database
    prepare_database(client, config)

    # Step 5: Perform sysbench test (if needed)
    perform_sysbench_test(client, config)

    # Transfer the sysbench metrics file from the VM to the local machine
    transfer_file_from_vm(client, 'sysbench_metrics.txt', 'sysbench_metrics.txt')

    

    # Parsing output
    local_sysbench_output = 'sysbench_metrics.txt'
    transfer_file_from_vm(client, local_sysbench_output, local_sysbench_output)

    # Close SSH connection
    client.close()

    # Close database connection
    close_database_connection(connection)


    # Step 7: Parse the sysbench output file ans save as CSV
    df_intermediate, final_stats, latency_stats, fairness_stats = parse_sysbench_output('sysbench_metrics.txt')

    # Debug: Check if DataFrame is populated
    if not df_intermediate.empty:
        print("DataFrame has data. Writing to CSV.")
        df_intermediate.to_csv("sysbench_intermediate.csv", index=False)
    else:
        print("DataFrame is empty. Check input file or parsing logic.")

    # Optionally, save parsed data to CSV (or process it)
    df_intermediate.to_csv('sysbench_intermediate.csv', index=False)
    pd.Series(final_stats).to_csv('sysbench_sql_stats.csv')
    pd.Series(latency_stats).to_csv('sysbench_latency_stats.csv')
    pd.Series(fairness_stats).to_csv('sysbench_fairness_stats.csv')

    print("Parsing complete. Data saved to CSV files.")

    # Ploting dashboard for visualization of Output
    plot_sysbench_dashboard()

    
    

if __name__ == "__main__":
    main()
