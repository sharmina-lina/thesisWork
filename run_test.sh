#!/bin/bash

# Initialize thread counter

threads=5

while true; do
    # Run sysbench and redirect output to sysbench_metrics.txt
    sysbench /usr/share/sysbench/oltp_read_write.lua \
      --db-driver=mysql \
      --mysql-db=sysbench_maria \
      --mysql-user=root \
      --mysql-password=123 \
      --mysql-host=172.17.0.3 \
      --mysql-port=3306 \
      --tables=5 \
      --table-size=1000000 \
      --threads=$threads \
      --time=60 \
      --report-interval=10 \
      --percentile=99 \
      run > sysbench_metrics_maria.txt
    sleep 20

    sysbench /usr/share/sysbench/oltp_read_write.lua \
      --db-driver=mysql \
      --mysql-db=sysbench_sql \
      --mysql-user=root \
      --mysql-password=123 \
      --mysql-host=172.17.0.2 \
      --mysql-port=3306 \
      --tables=5 \
      --table-size=1000000 \
      --threads=$threads \
      --time=60 \
      --report-interval=10 \
      --percentile=99 \
      run > sysbench_metrics_sql.txt

    # Run Apache Bench and redirect output to ab_metrics.txt
    ab -n 1000 -c 10 http://10.196.37.246/ > ab_metrics.txt
    sleep 10

    # Increase thread count by two if less than 30, otherwise reset to 5
    if [ $threads -lt 30 ]; then
            ((therads += 2))
    else
            threads=5
    fi

    scp sysbench_metrics_maria.txt ubuntu@10.196.37.231:/home/ubuntu/
    scp sysbench_metrics_sql.txt ubuntu@10.196.37.231:/home/ubuntu/
    scp ab_metrics.txt ubuntu@10.196.37.231:/home/ubuntu/

    # Wait for 1 minute before running again
    sleep 60
done

