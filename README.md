# QA Portfolio — примеры автотестов

Набор автотестов на Python (**pytest**): API, UI, SQL и unit-уровень.
Все тесты запускаемые и проходят.

```
33 passed
```

## Состав

| Файл | Область | Что показывает |
|------|---------|----------------|
| `test_api.py` | API-тестирование (`requests`) | Статус-коды (200/201/404), схема и типы JSON, негативные кейсы, параметризация |
| `test_ui_playwright.py` | UI / E2E (Playwright) | Автоматизация браузера: переход, ввод, клик, проверка; скриншот при падении; точные локаторы |
| `test_sql.py` | SQL / БД (SQLite) | SELECT/WHERE/JOIN/GROUP BY/агрегаты + проверки целостности (нет отрицательных балансов, нет «сирот», ограничения CHECK) |
| `test_subtitle_qa.py` | Тест-дизайн | Критерии приёмки для недетерминированного ML-вывода; граничный анализ |
| `subtitle_qa.py` | — | Модуль под тестом |

## Запуск

```bash
pip install pytest pytest-playwright requests
playwright install chromium
pytest
```

## Технологии

Python · pytest · pytest-playwright · requests · SQLite · Playwright (Chromium)
