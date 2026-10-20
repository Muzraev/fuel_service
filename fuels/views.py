from django.shortcuts import render

from storage import load_fuels


FUELS_FILE = 'data/fuels.json'


def fuels(request):
    """Показать виды топлива."""
    fuels_list = load_fuels(FUELS_FILE)

    context = {
        'fuels': fuels_list,
    }

    return render(
        request,
        'fuels/fuel_list.html',
        context
    )
