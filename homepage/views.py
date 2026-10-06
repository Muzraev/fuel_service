from django.http import HttpResponse


def page(title: str, content: str) -> str:
    """Сформировать общую HTML-страницу."""
    bootstrap = (
        'https://cdn.jsdelivr.net/npm/bootstrap@5.3.3'
        '/dist/css/bootstrap.min.css'
    )

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{bootstrap}">
    <style>
        body {{
            background: #f5f5f5;
        }}

        .navbar {{
            background: #222;
        }}

        .navbar a {{
            color: white;
        }}

        .card,
        .btn,
        .table {{
            border-radius: 0;
        }}

        .content {{
            background: white;
            padding: 30px;
            margin-top: 30px;
            border: 1px solid #ddd;
        }}
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg">
        <div class="container">
            <a class="navbar-brand" href="/">
                Сервис учета топлива
            </a>

            <div class="navbar-nav">
                <a class="nav-link" href="/">Главная</a>
                <a class="nav-link" href="/cars/">
                    Автомобили
                </a>
                <a class="nav-link" href="/fuels/">
                    Топливо
                </a>
                <a class="nav-link" href="/refuelings/">
                    Заправки
                </a>
            </div>
        </div>
    </nav>

    <main class="container">
        <div class="content">
            {content}
        </div>
    </main>
</body>
</html>"""


def index(request):
    """Главная страница."""
    content = """
        <h1>Сервис учета топлива</h1>

        <p class="lead">
            Веб-приложение для просмотра информации
            об автомобилях, топливе, расходе и заправках.
        </p>

        <hr>

        <h2 class="h4">Основные разделы</h2>

        <a href="/refuelings/"
           class="btn btn-dark me-2">
            Заправки
        </a>

        <a href="/cars/"
           class="btn btn-outline-dark me-2">
            Автомобили
        </a>

        <a href="/fuels/"
           class="btn btn-outline-dark">
            Топливо
        </a>
    """

    return HttpResponse(
        page(
            'Сервис учета топлива',
            content
        )
    )


def page_not_found(request, exception):
    """Страница ошибки 404."""
    content = """
        <h1>404 — страница не найдена</h1>

        <p>
            Такой страницы не существует.
        </p>

        <a href="/" class="btn btn-dark">
            Вернуться на главную
        </a>
    """

    return HttpResponse(
        page(
            'Ошибка 404',
            content
        ),
        status=404
    )
