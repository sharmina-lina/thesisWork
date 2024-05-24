# sysbench_metrics_parser.py

import re

def parse_sysbench_metrics(filename):
    throughput_metrics = {}
    latency_metrics = {}

    with open(filename, 'r') as f:
        lines = f.readlines()

    for line in lines:
        if 'tps:' in line:
            tps = float(re.search(r'tps:\s+(\d+\.\d+)', line).group(1))
            throughput_metrics['sysbench_throughput'] = tps

        if '99th percentile:' in line:
            latency_99th = float(re.search(r'99th percentile:\s+(\d+\.\d+)', line).group(1))
            latency_metrics['sysbench_latency_99th'] = latency_99th

    return throughput_metrics,latency_metrics

def parse_ab_metrics(filename):
    metrics = {}

    with open(filename, 'r') as f:
        lines = f.readlines()

    for line in lines:
        if 'Requests per second:' in line:
            throughput = float(re.search(r'Requests per second:\s+(\d+\.\d+)', line).group(1))
            metrics['ab_throughput'] = throughput

        if 'Time per request:' in line:
            time_per_request = float(re.search(r'Time per request:\s+(\d+\.\d+)', line).group(1))
            metrics['ab_time_per_request'] = time_per_request

    return metrics

def format_metrics(metrics):
    lines = []
    for metric, value in metrics.items():
        lines.append(f'{metric} {value}')

    return '\n'.join(lines)

if __name__ == '__main__':
    sysbench_throughput, sysbench_latency = parse_sysbench_metrics('sysbench_metrics.txt')
    ab_metrics = parse_ab_metrics('lb_metrics.txt')
    print("sysbench_metrics throughput:", sysbench_throughput)
    print("sysbench_metrics latency:", sysbench_latency)
    print("Load Balancing metrics:", lb_metrics)

