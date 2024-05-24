#!/bin/bash

# Load configuration from config.yaml
CONFIG_FILE="config.yaml"

# Load database parameters using yq
DB_HOST=$(yq eval '.database.host' $CONFIG_FILE)
DB_PORT=$(yq eval '.database.port' $CONFIG_FILE)
DB_NAME=$(yq eval '.database.db_name' $CONFIG_FILE)
DB_USER=$(yq eval '.database.username' $CONFIG_FILE)
DB_PASS=$(yq eval '.database.password' $CONFIG_FILE)

THREADS=$(yq eval '.testing_parameters.threads' $CONFIG_FILE)

# Load other parameters
LOAD_BALANCER_HOST=$(yq eval '.load_balancer.host' $CONFIG_FILE)
LOAD_BALANCER_PORT=$(yq eval '.load_balancer.port' $CONFIG_FILE)
# Load application and testing parameters...

# Execute Sysbench and Apache Benchmark tests using the parameters from the config file
# Update the script to use these parameters accordingly

if [$THREADS -lt 16 ]; then
sysbench /usr/share/sysbench/oltp_read_write.lua \
  --db-driver=mysql \
  --mysql-db=$DB_NAME \
  --mysql-user=$DB_USER \
  --mysql-password=$DB_PASS \
  --mysql-host=$DB_HOST \
  --mysql-port=3306 \
  --tables=5 \
  --table-size=1000000 \
  --threads=$THREADS \
  --time=60 \
  --report-interval=10 \
  --percentile=99 \
  run > sysbench_metrics.txt

sleep 20
#run CPU testing
sysbench cpu --threads=$THREADS --time=60 run > cpu_usage.txt
sleep 10

#Run Memory testing
sysbench memory --memory-block-size=1K --memory-total-size=10G --threads=$THREADS --time=60 run > mem_usage.txt
sleep 10

$((THREADS =+ 2))

else
	THREADS=5
fi

# Run Apache Bench and redirect output to ab_metrics.txt
ab -n 1000 -c 10 http://$LOAD_BALANCER_HOST/ > ab_metrics.txt
sleep 20


# send metrics file to the monitoring VM
scp sysbench_metrics.txt ubuntu@10.196.37.231:/home/ubuntu/
scp lb_metrics.txt ubuntu@10.196.37.231:/home/ubuntu/
scp cpu_usage.txt ubuntu@10.196.37.231:/home/ubuntu/
scp mem_usage.txt ubuntu@10.196.37.231:/home/ubuntu/
scp config.yaml ubuntu@10.196.37.231:/home/ubuntu/
