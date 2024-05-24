# prometheus_exporter.py

from flask import Flask, Response
from sysbench_metrics_parser import parse_sysbench_metrics, parse_ab_metrics

app = Flask(__name__)

def format_metrics(sysbench_throughput, sysbench_latency, ab_metrics):
    lines = []

    # Format sysbench metrics for MariaDB
    for name, value in sysbench_throughput.items():
        lines.append(f"{name} {value}")
    for name, value in sysbench_latency.items():
        lines.append(f"{name} {value}")


    # Format ab metrics
    for name, value in ab_metrics.items():
        lines.append(f"{name} {value}")

    return "\n".join(lines)
@app.route('/metrics')
def metrics():
    sysbench_throughput, sysbench_latency = parse_sysbench_metrics('sysbench_metrics.txt')
    ab_metrics = parse_ab_metrics('lb_metrics.txt')


    prometheus_metrics = format_metrics(sysbench_throughput, sysbench_latency, ab_metrics)


    return Response(prometheus_metrics, mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

