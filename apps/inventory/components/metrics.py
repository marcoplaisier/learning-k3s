"""
Prometheus metrics for component operations.
"""
from prometheus_client import Counter, Gauge
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Component

# Prometheus metrics
components_created_total = Counter(
    'inventory_components_created_total',
    'Total number of components created'
)

components_deleted_total = Counter(
    'inventory_components_deleted_total',
    'Total number of components deleted'
)

components_total = Gauge(
    'inventory_components_total',
    'Current total number of components in inventory'
)


def update_component_gauge():
    """Update the gauge with the current component count."""
    components_total.set(Component.objects.count())


@receiver(post_save, sender=Component)
def component_created_handler(sender, instance, created, **kwargs):
    """
    Signal handler for component creation.
    Increments Prometheus counter when a new component is added.
    """
    if created:
        components_created_total.inc()
        update_component_gauge()


@receiver(post_delete, sender=Component)
def component_deleted_handler(sender, instance, **kwargs):
    """
    Signal handler for component deletion.
    Increments Prometheus counter when a component is deleted.
    """
    components_deleted_total.inc()
    update_component_gauge()
