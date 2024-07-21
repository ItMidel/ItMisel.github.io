import json
import flet as ft
import os

def main(page: ft.Page):
    page.title = "Магазин"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START

    # Додавання логотипу у верхній лівий кут
    logo_path = "img/Logo-removebg-preview.png"
    if os.path.exists(logo_path):
        logo = ft.Image(src=logo_path, width=50, height=50)
    else:
        print("Logo file not found at:", logo_path)
        logo = ft.Text("Logo not found", size=16, weight=ft.FontWeight.BOLD)

    # Список товарів
    items = [
        {"name": "Burger", "price": 1.99, "image": "🍔"},
        {"name": "Fries", "price": 1.49, "image": "🍟"},
        {"name": "Hotdog", "price": 2.49, "image": "🌭"},
        {"name": "Taco", "price": 3.99, "image": "🌮"},
        {"name": "Pizza", "price": 7.99, "image": "🍕"},
        {"name": "Donut", "price": 1.49, "image": "🍩"},
        {"name": "Meet", "price": 4.99, "image": "🥩"},
        {"name": "Buterbrod", "price": 7.99, "image": "🥪"},
        {"name": "Gomilka", "price": 3.49, "image": "🍗"},
        {"name": "Ice cream", "price": 4.99, "image": "🍦"},
        {"name": "Milk", "price": 7.99, "image": "🥛"},
        {"name": "Polunusa", "price": 3.49, "image": "🍓"},
    ]

    # Список вибраних товарів у корзині
    cart_items = []

    def update_cart_view():
        cart_view.controls.clear()
        if cart_items:
            for item in cart_items:
                cart_view.controls.append(
                    ft.Card(
                        content=ft.ListTile(
                            leading=ft.Text(item["image"], size=30),
                            title=ft.Text(item["name"], size=16, weight=ft.FontWeight.BOLD),
                            subtitle=ft.Text(f'${item["price"]:.2f}', size=14),
                            trailing=ft.IconButton(
                                icon=ft.icons.DELETE,
                                icon_size=20,
                                on_click=lambda e, item=item: remove_from_cart(item),
                                tooltip="Remove"
                            ),
                        ),
                        width=280,
                        height=70,
                    )
                )
            cart_view.controls.append(
                ft.Text(
                    f'Total: ${sum(item["price"] for item in cart_items):.2f}',
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER
                )
            )
        else:
            cart_view.controls.append(ft.Text("Your cart is empty", size=14))
        cart_view.update()

    def add_to_cart(item):
        cart_items.append(item)
        update_cart_view()

    def remove_from_cart(item):
        cart_items.remove(item)
        update_cart_view()

    def close_dialog(page):
        page.dialog.open = False
        page.update()

    def buy_product(page):
        # Зберігання списку покупок у JSON об'єкт
        with open('purchase_history.json', 'w') as f:
            json.dump(cart_items, f, indent=4)
        print("Purchase history saved to 'purchase_history.json'")
        page.app.stop()  # Зупинка додатку

    def build_item(item):
        return ft.Card(
            content=ft.Column(
                [
                    ft.Text(item["image"], size=40),
                    ft.Text(f'{item["name"]} - ${item["price"]:.2f}', size=14),
                    ft.ElevatedButton("ADD", on_click=lambda e: add_to_cart(item)),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            width=150,  # Ширина контейнера для кожного товару
        )

    # Створення списку рядків, кожен рядок містить 3 елементи
    rows = []
    row = []
    for index, item in enumerate(items):
        row.append(build_item(item))
        if (index + 1) % 3 == 0 or index == len(items) - 1:
            rows.append(ft.Row(row, spacing=20, alignment=ft.MainAxisAlignment.CENTER))  # Центрування рядка
            row = []

    # Додаємо прокручуваний список товарів
    product_list_view = ft.ListView(
        controls=[
            ft.Column(
                rows,
                alignment=ft.MainAxisAlignment.START,
                spacing=20,
            )
        ],
        expand=True,
        spacing=20,
    )

    # Корзина товарів
    cart_view = ft.ListView(
        spacing=10,
        expand=True,
    )

    # Діалогове вікно з корзиною
    page.dialog = ft.AlertDialog(
        title=ft.Text("Корзина"),
        content=cart_view,
        actions=[
            ft.ElevatedButton("Закрити", on_click=lambda _: close_dialog(page)),
            ft.ElevatedButton("Купити", on_click=lambda _: buy_product(page))
        ],
    )

    # Функція показу корзини
    def show_cart(e):
        cart_view.controls.clear()
        update_cart_view()
        page.dialog.open = True
        page.update()

    # Додавання кнопки корзини
    page.add(
        ft.Row(
            [
                logo,  # Додавання логотипу у верхній лівий кут
                ft.IconButton(
                    icon=ft.icons.SHOPPING_CART,
                    icon_size=30,
                    on_click=show_cart,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        product_list_view  # Додаємо скролінг для продуктів
    )

if __name__ == '__main__':
    ft.app(target=main, view=ft.WEB_BROWSER)
