from django.http import HttpResponse

from homepage.views import page
from storage import load_fuels


FUELS_FILE = 'data/fuels.json'


def fuels(request):
    """Показать виды топлива."""
    fuels_list = load_fuels(FUELS_FILE)

    if not fuels_list:
        content = """
            <h1>Топливо</h1>
            <p>Видов топлива пока нет.</p>
        """

        return HttpResponse(
            page('Топливо', content)
        )

    rows = ''

    for fuel in fuels_list:
        rows += f"""
            <tr>
                <td>{fuel.id}</td>
                <td>{fuel.name}</td>
            </tr>
        """

    content = f"""
        <h1>Виды топлива</h1>

        <table class="table table-bordered">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Название</th>
                </tr>
            </thead>

            <tbody>
                {rows}
            </tbody>
        </table>
    """

    return HttpResponse(
        page('Топливо', content)
    )
