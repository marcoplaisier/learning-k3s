from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from .models import Component
from .metrics import update_component_gauge


def component_list(request):
    """Display a list of all components."""
    components = Component.objects.all().order_by('-pub_date')
    context = {
        'components': components
    }
    return render(request, 'components/component_list.html', context)


def component_detail(request, component_id):
    """Display details of a specific component."""
    component = get_object_or_404(Component, pk=component_id)
    context = {
        'component': component
    }
    return render(request, 'components/component_detail.html', context)


def metrics(request):
    """
    Expose Prometheus metrics endpoint.
    Returns metrics in Prometheus text format.
    """
    # Ensure the gauge is up-to-date before generating metrics
    update_component_gauge()

    metrics_data = generate_latest()
    return HttpResponse(metrics_data, content_type=CONTENT_TYPE_LATEST)