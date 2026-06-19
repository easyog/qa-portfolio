"""UI/E2E-тесты на Playwright (демо-приложение TodoMVC).

Проверяют базовые пользовательские сценарии: открытие страницы, добавление
и завершение задач. Скриншот при падении включён в pytest.ini.
"""
import pytest
from playwright.sync_api import Page, expect

APP = "https://demo.playwright.dev/todomvc"
NEW_TODO = "What needs to be done?"


def test_page_opens_with_correct_title(page: Page):
    page.goto(APP)
    expect(page).to_have_title("React • TodoMVC")


def test_add_single_todo(page: Page):
    page.goto(APP)
    box = page.get_by_placeholder(NEW_TODO)
    box.fill("Купить молоко")
    box.press("Enter")
    expect(page.get_by_test_id("todo-title")).to_have_text("Купить молоко")


def test_add_multiple_todos(page: Page):
    page.goto(APP)
    box = page.get_by_placeholder(NEW_TODO)
    for task in ["Задача 1", "Задача 2", "Задача 3"]:
        box.fill(task)
        box.press("Enter")
    expect(page.get_by_test_id("todo-title")).to_have_count(3)


def test_complete_a_todo(page: Page):
    page.goto(APP)
    box = page.get_by_placeholder(NEW_TODO)
    box.fill("Сделать тест")
    box.press("Enter")

    # на странице два чекбокса ("отметить всё" и галочка задачи) —
    # целимся в галочку конкретной задачи, иначе строгий режим отклонит
    page.locator(".todo-list li .toggle").check()

    expect(page.locator(".todo-list li")).to_have_class("completed")


@pytest.mark.parametrize("text", ["короткая", "Задача с пробелами и цифрами 123"])
def test_various_todo_texts(page: Page, text):
    page.goto(APP)
    box = page.get_by_placeholder(NEW_TODO)
    box.fill(text)
    box.press("Enter")
    expect(page.get_by_test_id("todo-title")).to_have_text(text)
