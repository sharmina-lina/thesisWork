#!/bin/bash

# Load configuration from config.yaml
CONFIG_FILE="config.yaml"

# Load database parameters using yq
DB_HOST=$(yq eval '.database.host' $CONFIG_FILE)
DB_PORT=$(yq eval '.database.port' $CONFIG_FILE)
DB_NAME=$(yq eval '.database.db_name' $CONFIG_FILE)
DB_USER=$(yq eval '.database.username' $CONFIG_FILE)
DB_PASS=$(yq eval '.database.password' $CONFIG_FILE)

# Load testing parameters
THREADS=$(yq eval '.testing_parameters.threads' $CONFIG_FILE)
MAX_THREADS=$(yq eval '.testing_parameters.max_threads' $CONFIG_FILE)
INCREMENT=$(yq eval '.testing_parameters.increment' $CONFIG_FILE)
DURATION=$(yq eval '.testing_parameters.duration' $CONFIG_FILE)

# Load other parameters
LOAD_BALANCER_HOST=$(yq eval '.load_balancer.host' $CONFIG_FILE)
LOAD_BALANCER_PORT=$(yq eval '.load_balancer.port' $CONFIG_FILE)

while true; do
  # Execute Sysbench OLTP test
  sysbench /usr/share/sysbench/oltp_read_write.lua \
    --db-driver=mysql \
    --mysql-db=$DB_NAME \
    --mysql-user=$DB_USER \
    --mysql-password=$DB_PASS \
    --mysql-host=$DB_HOST \
    --mysql-port=$DB_PORT \
    --tables=5 \
    --table-size=1000000 \
    --threads=$THREADS \
    --time=$DURATION \
    --report-interval=10 \
    --percentile=99 \
    run > sysbench_metrics.txt

  sleep 20

  # Execute CPU test
  sysbench cpu --threads=$THREADS --time=$DURATION run > cpu_usage.txt
  sleep 10

  # Execute Memory test
  sysbench memory --memory-block-size=1K --memory-total-size=10G --threads=$THREADS --time=$DURATION run > mem_usage.txt
  sleep 10

  # Increment the number of threads or reset
  if [ $THREADS -lt $MAX_THREADS ]; then
    THREADS=$((THREADS + INCREMENT))
  else
    THREADS=$(yq eval '.testing_parameters.threads' $CONFIG_FILE)
  fi

  # Execute Apache Bench test
  ab -n 1000 -c 10 http://$LOAD_BALANCER_HOST:$LOAD_BALANCER_PORT/ > ab_metrics.txt
  sleep 20

  # Send metrics files to the monitoring VM
  scp sysbench_metrics.txt ubuntu@10.196.37.231:/home/ubuntu/
  scp cpu_usage.txt ubuntu@10.196.37.231:/home/ubuntu/
  scp mem_usage.txt ubuntu@10.196.37.231:/home/ubuntu/
  scp ab_metrics.txt ubuntu@10.196.37.231:/home/ubuntu/
done

