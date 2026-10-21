"""Pickup page: Jhon Kyle T. Ramos — live estimate and file feedback."""
from pyscript import document, when

RATES = {"bw": 2.50, "color": 8.50}
HANDLING_FEE = 15.00

def money(value):
    return f"₱{value:,.2f}"

def get_amounts():
    try:
        pages = int(document.querySelector("#pickup-pages").value)
        copies = int(document.querySelector("#pickup-copies").value)
        if not 1 <= pages <= 500 or not 1 <= copies <= 50:
            return None
        return pages, copies
    except (TypeError, ValueError):
        return None

def refresh_estimate():
    """INPUT/CHANGE EVENTS: show a quote before the form is submitted."""
    data = get_amounts()
    if data is None:
        document.querySelector("#pickup-total").textContent = "—"
        document.querySelector("#pickup-subtotal").textContent = "—"
        return
    pages, copies = data
    price = RATES[document.querySelector("#pickup-type").value]
    subtotal = pages * copies * price
    document.querySelector("#pickup-subtotal").textContent = money(subtotal)
    document.querySelector("#pickup-total").textContent = money(subtotal + HANDLING_FEE)

@when("input", "#pickup-pages, #pickup-copies")
@when("change", "#pickup-type")
def on_settings_change(event):
    refresh_estimate()

@when("change", "#pickup-file")
def show_filename(event):
    """FILE CHANGE EVENT: only show the chosen filename; do not upload contents."""
    files = document.querySelector("#pickup-file").files
    filename = files.item(0).name if files.length else "No file selected"
    document.querySelector("#file-feedback").textContent = filename + " — local selection only; not uploaded."

refresh_estimate()
