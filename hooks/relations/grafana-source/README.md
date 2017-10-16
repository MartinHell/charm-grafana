# Overview

This interface layer implements grafana source protocol

# Usage

## Provides

Example implementation:
```python
@when('grafana-source.available')
def configure_grafana(grafana-source):
    grafana-source.provide('prometheus', 9090, 'Juju generated source')
```

## Requires

Require part is currently only used by the grafana charm
