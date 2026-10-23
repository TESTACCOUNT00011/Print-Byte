"""Pickup page: Jhon Kyle T. Ramos — validation and local draft receipt."""
from datetime import date
from pyscript import document, when, window

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

@when("submit", "#pickup-form")
def create_draft(event):
    """SUBMIT EVENT: validate and display an unsent, printable request summary."""
    event.preventDefault()
    form = document.querySelector("#pickup-form")
    error = document.querySelector("#pickup-error")
    if not form.checkValidity():
        form.reportValidity()
        error.textContent = "Please complete all required fields correctly."
        return
    amounts = get_amounts()
    if amounts is None:
        error.textContent = "Pages must be 1–500 and copies must be 1–50."
        return
    requested_date = document.querySelector("#pickup-date").value
    if requested_date < date.today().isoformat():
        error.textContent = "Please choose today or a future pickup date."
        return
    error.textContent = ""
    pages, copies = amounts
    print_type = document.querySelector("#pickup-type").value
    subtotal = pages * copies * RATES[print_type]
    selected_files = document.querySelector("#pickup-file").files
    filename = selected_files.item(0).name if selected_files.length else "Not selected"
    # textContent, rather than innerHTML, keeps customer input as literal text.
    lines = [
        "BYTE & PRINT — LOCAL REQUEST DRAFT (NOT SUBMITTED)",
        "------------------------------------------------",
        "Customer: " + document.querySelector("#customer-name").value.strip(),
        "Email: " + document.querySelector("#customer-email").value.strip(),
        "Print type: " + ("Black & white" if print_type == "bw" else "Color"),
        "Paper size: " + document.querySelector("#pickup-paper").value,
        f"Pages per copy: {pages} | Copies: {copies}",
        "Preferred date: " + requested_date,
        "Preferred time: " + document.querySelector("#pickup-time").value,
        "Selected filename (NOT uploaded): " + filename,
        "Preferred payment: " + document.querySelector("#pickup-payment").value,
        "Instructions: " + (document.querySelector("#pickup-notes").value.strip() or "None"),
        "------------------------------------------------",
        "Printing: " + money(subtotal),
        "Pickup handling: " + money(HANDLING_FEE),
        "ESTIMATED TOTAL: " + money(subtotal + HANDLING_FEE),
        "------------------------------------------------",
        "DEMO ONLY — No order, file, or payment was sent.",
        "Contact the shop separately to confirm an actual order.",
    ]
    document.querySelector("#request-summary").textContent = "\n".join(lines)
    panel = document.querySelector("#request-result")
    panel.hidden = False
    panel.scrollIntoView()

@when("click", "#print-summary")
def print_draft(event):
    """CLICK EVENT: use the browser's built-in print/save-to-PDF dialog."""
    window.print()

refresh_estimate()
