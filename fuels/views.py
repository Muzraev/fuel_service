from django.shortcuts import render

from db.database import fetch_all


def fuels(request):
    """Показать виды топлива из SQLite."""
    return render(
        request, 'fuels/fuel_list.html', {'fuels': fetch_all('fuels')}
    )
