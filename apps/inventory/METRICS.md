# Prometheus Metrics Documentation

This application exposes Prometheus metrics for monitoring component operations in the inventory system.

## Metrics Endpoint

The metrics are available at:
```
http://localhost:8000/metrics/
```

## Available Metrics

### Component Metrics

1. **inventory_components_created_total** (Counter)
   - Description: Total number of components created since the application started
   - Type: Counter
   - Increments: When a new component is added via Django admin or API

2. **inventory_components_deleted_total** (Counter)
   - Description: Total number of components deleted since the application started
   - Type: Counter
   - Increments: When a component is deleted via Django admin or API

3. **inventory_components_total** (Gauge)
   - Description: Current total number of components in the inventory
   - Type: Gauge
   - Updates: Real-time count of all components in the database

## How It Works

The instrumentation is implemented using Django signals:

- **Signal Handlers** (components/metrics.py:28):
  - `component_created_handler`: Triggered on component creation
  - `component_deleted_handler`: Triggered on component deletion

- **Metrics Registration** (components/apps.py:8):
  - Signals are registered in the `ComponentsConfig.ready()` method
  - This ensures metrics are tracked from application startup

## Testing Metrics

### Via Django Admin

1. Access the admin interface: http://localhost:8000/admin/
2. Add a new component
3. Check the metrics endpoint - `inventory_components_created_total` should increment
4. Delete a component
5. Check the metrics endpoint - `inventory_components_deleted_total` should increment

### Via Prometheus Scraping

Configure Prometheus to scrape this endpoint:

```yaml
scrape_configs:
  - job_name: 'inventory'
    static_configs:
      - targets: ['inventory-service:8000']
    metrics_path: '/metrics/'
    scrape_interval: 15s
```

## Metrics Format

The metrics are exposed in Prometheus text format:

```
# HELP inventory_components_created_total Total number of components created
# TYPE inventory_components_created_total counter
inventory_components_created_total 42.0

# HELP inventory_components_deleted_total Total number of components deleted
# TYPE inventory_components_deleted_total counter
inventory_components_deleted_total 5.0

# HELP inventory_components_total Current total number of components in inventory
# TYPE inventory_components_total gauge
inventory_components_total 37.0
```

## Production Considerations

1. **Performance**: The gauge is updated on each metrics request and when components are created/deleted
2. **Persistence**: Counters reset when the application restarts (this is standard Prometheus behavior)
3. **Multiprocess Mode**: For production with multiple workers, consider using prometheus_client's multiprocess mode
4. **Security**: Consider adding authentication to the /metrics endpoint in production

## Related Files

- `components/metrics.py` - Prometheus metrics definitions and signal handlers
- `components/apps.py` - Signal registration
- `components/views.py` - Metrics endpoint view
- `inventory/urls.py` - Metrics URL routing
