"""Home page: Celestino II D. Regis — interactive student need selector."""
from pyscript import document, when

SUGGESTIONS = {
    "print": ("▧", "Plan your print", "Use the pickup request demo to check your print settings and expected cost.", "pickup.html"),
    "computer": ("⌘", "Find computer access", "View our proposed computer rental rate of ₱20 per hour and calculate your cost.", "services.html"),
    "shop": ("◈", "Grab the essentials", "Browse sample school supplies and snacks and add them to a mini basket.", "shop.html"),
}

@when("click", ".choice")
def recommend_service(event):
    """CLICK EVENT: display the service suggested by the selected student task."""
    button = event.currentTarget
    need = button.dataset.need
    icon, title, description, link = SUGGESTIONS[need]
    for choice in document.querySelectorAll(".choice"):
        choice.classList.remove("active")
    button.classList.add("active")
    document.querySelector("#recommend-icon").textContent = icon
    document.querySelector("#recommend-title").textContent = title
    document.querySelector("#recommend-text").textContent = description
    document.querySelector("#recommend-link").href = link
