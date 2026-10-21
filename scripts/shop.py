"""Shop page: Jay C. Villaceran — live filters and search."""
from pyscript import document, when

active_category = "all"

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

update_visible_products()
