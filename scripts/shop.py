"""Shop page: Jay C. Villaceran — live filters, search and basket totals."""
from pyscript import document, when

active_category = "all"
basket = {}

def update_visible_products():
    """INPUT/CLICK EVENTS: filter by category and case-insensitive search."""
    term = document.querySelector("#product-search").value.strip().lower()
    shown = 0
    for card in document.querySelectorAll(".product-card"):
        category_matches = active_category == "all" or card.dataset.category == active_category
        matches_search = term in card.dataset.name
        card.hidden = not (category_matches and matches_search)
        shown += 0 if card.hidden else 1
    document.querySelector("#shop-count").textContent = f"{shown} item(s) shown"
    document.querySelector("#shop-empty").hidden = shown != 0

@when("click", ".filter-button")
def on_filter_click(event):
    global active_category
    active_category = event.currentTarget.dataset.filter
    for button in document.querySelectorAll(".filter-button"):
        button.classList.remove("active")
    event.currentTarget.classList.add("active")
    update_visible_products()

@when("input", "#product-search")
def on_search_input(event):
    update_visible_products()

def render_basket():
    """DYNAMIC DOM UPDATE: show names, quantities and total after each click."""
    panel = document.querySelector("#basket-items")
    panel.replaceChildren()
    total = 0
    if not basket:
        panel.textContent = "No items yet"
    else:
        for name, item in basket.items():
            total += item["quantity"] * item["price"]
            row = document.createElement("div")
            label = document.createElement("span")
            label.textContent = f"{name} × {item['quantity']}"
            amount = document.createElement("strong")
            amount.textContent = f"₱{item['quantity'] * item['price']:,.2f}"
            row.appendChild(label)
            row.appendChild(amount)
            panel.appendChild(row)
    document.querySelector("#basket-total").textContent = f"₱{total:,.2f}"

@when("click", ".add-item")
def add_to_basket(event):
    button = event.currentTarget
    name = button.dataset.name
    price = float(button.dataset.price)
    if name not in basket:
        basket[name] = {"price": price, "quantity": 0}
    basket[name]["quantity"] += 1
    render_basket()

update_visible_products()
render_basket()
