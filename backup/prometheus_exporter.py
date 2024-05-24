# prometheus_exporter.py

from flask import Flask, Response
from sysbench_metrics_parser import parse_sysbench_metrics, parse_ab_metrics

app = Flask(__name__)

def format_metrics(sysbench_throughput_maria, sysbench_latency_maria, sysbench_throughput_sql, sysbench_latency_sql, ab_metrics):
    lines = []

    # Format sysbench metrics for MariaDB
    for name, value in sysbench_throughput_maria.items():
        lines.append(f"{name}_maria {value}")
    for name, value in sysbench_latency_maria.items():
        lines.append(f"{name}_maria {value}")

    # Format sysbench metrics for SQL
    for name, value in sysbench_throughput_sql.items():
        lines.append(f"{name}_sql {value}")
    for name, value in sysbench_latency_sql.items():
        lines.append(f"{name}_sql {value}")

    # Format ab metrics
    for name, value in ab_metrics.items():
        lines.append(f"{name} {value}")

    return "\n".join(lines)
@app.route('/metrics')
def metrics():
    sysbench_throughput_maria, sysbench_latency_maria = parse_sysbench_metrics('sysbench_metrics_maria.txt')
    sysbench_throughput_sql, sysbench_latency_sql = parse_sysbench_metrics('sysbench_metrics_sql.txt')
    ab_metrics = parse_ab_metrics('ab_metrics.txt')


    prometheus_metrics = format_metrics(sysbench_throughput_maria, sysbench_latency_maria, sysbench_throughput_sql, sysbench_latency_sql, ab_metrics)


    return Response(prometheus_metrics, mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

