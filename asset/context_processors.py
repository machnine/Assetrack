"""context processors for the asset app"""

from asset.models import MaintenanceRecordMenu


def maintenance_menu_items(request):
    """add maintenance menu items to the context"""
    return {"maintenance_menu_items": MaintenanceRecordMenu.objects.all()}
