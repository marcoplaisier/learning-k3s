from django.shortcuts import render, get_object_or_404
from .models import Component


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