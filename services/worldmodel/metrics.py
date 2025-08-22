"""Optional Prometheus metrics for worldmodel service.

Metrics are opt-in via env ENABLE_METRICS=1. If the prometheus_client package is
unavailable the module falls back to no-op functions so tests/CI don't require it.
"""
import os
import logging
import json
from typing import Optional

_ENABLED = os.environ.get('ENABLE_METRICS', '0') == '1'
_METRICS = {}

def init_metrics():
    global _METRICS
    if not _ENABLED:
        return
    try:
        from prometheus_client import start_http_server, Gauge
        port = int(os.environ.get('WORLDMODEL_METRICS_PORT', '8001'))
        start_http_server(port)
        _METRICS['mse_h1'] = Gauge('cleo_worldmodel_mse_h1', 'Worldmodel MSE at horizon 1')
        _METRICS['rmse_h10'] = Gauge('cleo_worldmodel_rmse_h10', 'Worldmodel RMSE at horizon 10')
        _METRICS['dtw'] = Gauge('cleo_worldmodel_dtw', 'Worldmodel DTW distance')
        logging.info(f'Worldmodel prometheus metrics enabled on port {port}')
    except Exception:
        logging.exception('Failed to enable worldmodel prometheus metrics; continuing without metrics')
        _METRICS = {}


def record_discrepancy(mse_h1: float, rmse_h10: float, dtw: float, artifacts_path: Optional[str] = None):
    """Record discrepancy metrics; emit to Prometheus gauges if enabled and
    persist to artifacts/metrics.json when artifacts_path is provided.
    """
    if _METRICS:
        try:
            if 'mse_h1' in _METRICS:
                _METRICS['mse_h1'].set(mse_h1)
            if 'rmse_h10' in _METRICS:
                _METRICS['rmse_h10'].set(rmse_h10)
            if 'dtw' in _METRICS:
                _METRICS['dtw'].set(dtw)
        except Exception:
            logging.exception('Failed to update prometheus metrics')

    if artifacts_path:
        try:
            os.makedirs(artifacts_path, exist_ok=True)
            out = {
                'MSE_h1': float(mse_h1),
                'RMSE_h10': float(rmse_h10),
                'DTW': float(dtw)
            }
            with open(os.path.join(artifacts_path, 'metrics.json'), 'w', encoding='utf-8') as f:
                json.dump(out, f, indent=2)
        except Exception:
            logging.exception('Failed to write artifacts/metrics.json')


# initialize on import if requested
init_metrics()
