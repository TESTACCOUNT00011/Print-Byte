"""Services page: Lance Steven G. Yano — live pricing with PyScript events."""
from pyscript import document, when

RATES = {"bw": 2.50, "color": 8.50, "copy": 2.50, "scan": 10.00, "rental": 20.00}

def money(value):
    return f"₱{value:,.2f}"

def valid_integer(selector, maximum):
    """Return a bounded positive number; avoid negative or non-numeric estimates."""
    try:
        value = int(document.querySelector(selector).value)
        if 1 <= value <= maximum:
            return value
    except (ValueError, TypeError):
        pass
    return None

def update_quote():
    """INPUT/CHANGE EVENTS: recalculate price and update the DOM instantly."""
    service = document.querySelector("#service-type").value
    rental = service == "rental"
    document.querySelector("#quantity-label").textContent = "Hours" if rental else "Pages per copy"
    document.querySelector("#copies-field").hidden = rental
    document.querySelector("#pickup-fee-line").hidden = rental or service == "scan"
    qty = valid_integer("#service-quantity", 500)
    copies = 1 if rental else valid_integer("#service-copies", 50)
    message = document.querySelector("#calculator-message")
    if qty is None or copies is None:
        document.querySelector("#service-total").textContent = "—"
        document.querySelector("#estimate-breakdown").textContent = "Enter valid positive amounts."
        message.textContent = "Pages/hours: 1–500. Copies: 1–50."
        return
    fee = 15 if (not rental and service != "scan" and document.querySelector("#service-pickup").checked) else 0
    amount = qty * copies * RATES[service] + fee
    unit = "hour(s)" if rental else "page(s)"
    detail = f"{qty} {unit} × {copies} × {money(RATES[service])}"
    document.querySelector("#service-total").textContent = money(amount)
    document.querySelector("#estimate-breakdown").textContent = detail + (" + ₱15 pickup" if fee else "")
    message.textContent = "Estimate only — no charge or order was created."

@when("input", "#service-quantity, #service-copies")
@when("change", "#service-type, #service-pickup")
def on_estimate_change(event):
    update_quote()

update_quote()
