"""Services page: Lance Steven G. Yano — live pricing with PyScript events."""
from pyscript import document

RATES = {"bw": 2.50, "color": 8.50, "copy": 2.50, "scan": 10.00, "rental": 20.00}

def money(value):
    return f"₱{value:,.2f}"

def update_quote():
    """INPUT/CHANGE EVENTS: recalculate the estimate when values change."""
    service = document.querySelector("#service-type").value
    try:
        qty = int(document.querySelector("#service-quantity").value)
        copies = int(document.querySelector("#service-copies").value)
        if qty < 1 or copies < 1:
            raise ValueError
    except (ValueError, TypeError):
        document.querySelector("#service-total").textContent = "—"
        document.querySelector("#calculator-message").textContent = "Enter valid positive amounts."
        return
    amount = qty * copies * RATES[service]
    document.querySelector("#service-total").textContent = money(amount)
    document.querySelector("#calculator-message").textContent = "Estimate only — no charge or order was created."

update_quote()
