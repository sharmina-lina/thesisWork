# sysbench_metrics_parser.py

import re
import yaml

def load_config(config_file):
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    return config

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


    return throughput_metrics, latency_metrics

def parse_cpu_usage(filename):
    cpu_usage = None
    with open(filename, 'r') as f:
        lines = f.readlines()

    for line in lines:
        if 'total time:' in line:
            cpu_usage = float(re.search(r'total time:\s+(\d+\.\d+)', line).group(1))

    return cpu_usage

def parse_memory_usage(filename):
    memory_usage = None
    with open(filename, 'r') as f:
        lines = f.readlines()

    for line in lines:
        if 'total time:' in line:
            memory_usage = float(re.search(r'total time:\s+(\d+\.\d+)', line).group(1))

    return memory_usage

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

def main():
    config = load_config("config.yaml")
    metrics_to_collect = config.get('metrics', [])

    sysbench_throughput, sysbench_latency = {}, {}
    cpu_usage, memory_usage = None, None
    ab_metrics = {}

 
    if 'sysbench_throughput' in metrics_to_collect or 'sysbench_latency' in metrics_to_collect:
        sysbench_throughput, sysbench_latency = parse_sysbench_metrics('sysbench_metrics.txt')

    if 'cpu_usage' in metrics_to_collect:
        cpu_usage = parse_cpu_usage('cpu_usage.txt')

    if 'memory_usage' in metrics_to_collect:
        memory_usage = parse_memory_usage('mem_usage.txt')

    if 'ab_throughput' in metrics_to_collect or 'ab_time_per_request' in metrics_to_collect:
        ab_metrics = parse_ab_metrics('lb_metrics.txt')

    print("sysbench_metrics throughput:", sysbench_throughput)
    print("sysbench_metrics latency:", sysbench_latency)
    print("CPU Usage", cpu_usage)
    print("Memory Usage", memory_usage)
    print("Load Balancing metrics:", ab_metrics)
if __name__ == '__main__':
    main()

"""if __name__ == '__main__':
    sysbench_throughput, sysbench_latency = parse_sysbench_metrics('sysbench_metrics.txt')
    ab_metrics = parse_ab_metrics('lb_metrics.txt')
    cpu_usage = parse_cpu_usage('cpu_usage.txt')
    memory_usage = parse_memory_usage('mem_usage.txt')
    print("sysbench_metrics throughput:", sysbench_throughput)
    print("sysbench_metrics latency:", sysbench_latency)
    print("Load Balancing metrics:", ab_metrics)
    print("CPU Usage", cpu_usage)
    print("Memory Usage", memory_usage)
"""
