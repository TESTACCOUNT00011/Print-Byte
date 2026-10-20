"""Services page: Lance Steven G. Yano — live pricing with PyScript events."""
from pyscript import document, when

RATES = {"bw": 2.50, "color": 8.50, "copy": 2.50, "scan": 10.00, "rental": 20.00}

def money(value):
    return f"₱{value:,.2f}"

def update_quote():
    """INPUT/CHANGE EVENTS: recalculate price and update the DOM instantly."""
    service = document.querySelector("#service-type").value
    rental = service == "rental"
    document.querySelector("#quantity-label").textContent = "Hours" if rental else "Pages per copy"
    document.querySelector("#copies-field").hidden = rental
    document.querySelector("#pickup-fee-line").hidden = rental or service == "scan"
    try:
        qty = int(document.querySelector("#service-quantity").value)
        copies = 1 if rental else int(document.querySelector("#service-copies").value)
        if not 1 <= qty <= 500 or not 1 <= copies <= 50:
            raise ValueError
    except (ValueError, TypeError):
        document.querySelector("#service-total").textContent = "—"
        document.querySelector("#estimate-breakdown").textContent = "Enter valid positive amounts."
        document.querySelector("#calculator-message").textContent = "Pages/hours: 1–500. Copies: 1–50."
        return
    fee = 15 if (not rental and service != "scan" and document.querySelector("#service-pickup").checked) else 0
    amount = qty * copies * RATES[service] + fee
    unit = "hour(s)" if rental else "page(s)"
    detail = f"{qty} {unit} × {copies} × {money(RATES[service])}"
    document.querySelector("#service-total").textContent = money(amount)
    document.querySelector("#estimate-breakdown").textContent = detail + (" + ₱15 pickup" if fee else "")
    document.querySelector("#calculator-message").textContent = "Estimate only — no charge or order was created."

@when("input", "#service-quantity, #service-copies")
@when("change", "#service-type, #service-pickup")
def on_estimate_change(event):
    update_quote()

update_quote()
