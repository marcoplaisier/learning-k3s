#!/usr/bin/env python
"""Create test data for the inventory app."""
import os
import sys
import django
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory.settings')
django.setup()

from components.models import Component

# Create test components
test_components = [
    {
        'name': 'Arduino Uno R3',
        'description': 'Microcontroller board based on the ATmega328P with 14 digital input/output pins, 6 analog inputs, and USB connection.',
        'pub_date': datetime.now()
    },
    {
        'name': 'Raspberry Pi 4 Model B',
        'description': 'Single-board computer with quad-core ARM processor, up to 8GB RAM, dual-band WiFi, and Gigabit Ethernet.',
        'pub_date': datetime.now()
    },
    {
        'name': 'NE555 Timer IC',
        'description': 'Precision timing integrated circuit capable of producing accurate time delays or oscillation in astable or monostable configurations.',
        'pub_date': datetime.now()
    },
    {
        'name': 'LED RGB 5mm Common Cathode',
        'description': 'Full-color light-emitting diode with red, green, and blue elements in a single 5mm package with common cathode configuration.',
        'pub_date': datetime.now()
    },
    {
        'name': 'HC-SR04 Ultrasonic Sensor',
        'description': 'Distance measuring sensor module with ultrasonic transmitter and receiver, measuring range 2cm to 400cm with high accuracy.',
        'pub_date': datetime.now()
    }
]

print("Creating test components...")
created_count = 0

for component_data in test_components:
    component, created = Component.objects.get_or_create(
        name=component_data['name'],
        defaults={
            'description': component_data['description'],
            'pub_date': component_data['pub_date']
        }
    )
    if created:
        print(f"✓ Created: {component.name}")
        created_count += 1
    else:
        print(f"- Already exists: {component.name}")

print(f"\nCreated {created_count} new components")
print(f"Total components in database: {Component.objects.count()}")
