# prometheus_exporter.py

from flask import Flask, Response
from sysbench_metrics_parser import parse_sysbench_metrics, parse_ab_metrics, parse_cpu_usage, parse_memory_usage

app = Flask(__name__)

def format_metrics(sysbench_metrics, ab_metrics, cpu_usage,memory_usage):
    lines = []

    # Format sysbench metrics for MariaDB
    for name, value in sysbench_metrics.items():
        lines.append(f"{name} {value}")
    


    # Format ab metrics
    for name, value in ab_metrics.items():
        lines.append(f"{name} {value}")

    # Add CPU and memory usage metrics
    if cpu_usage is not None:
        lines.append(f"cpu_usage {cpu_usage}")
    if memory_usage is not None:
        lines.append(f"memory_usage {memory_usage}")
    

    return "\n".join(lines)

@app.route('/metrics')
def metrics():
    sysbench_metrics = parse_sysbench_metrics('sysbench_metrics.txt')
    ab_metrics = parse_ab_metrics('lb_metrics.txt')
    cpu_usage = parse_cpu_usage('cpu_usage.txt')
    memory_usage = parse_memory_usage('mem_usage.txt')


    prometheus_metrics = format_metrics(sysbench_metrics, ab_metrics, cpu_usage, memory_usage)


    return Response(prometheus_metrics, mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

