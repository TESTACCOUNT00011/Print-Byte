# BYTE & PRINT — Event-Driven Programming Final Project

> “Print it, pick it up, and grab what you need.”

An interactive, **database-free student business website** for the Byte & Print concept described in the group's feasibility study near Cebu Eastern College, Cebu City. Built with semantic HTML, responsive CSS, and **PyScript (Python in the browser)** to demonstrate Event-Driven Programming.

## Team / founders

- **Celestino II D. Regis** — home/branding, styling & service recommendation
- **Lance Steven G. Yano** — services & real-time cost calculator
- **Jhon Kyle T. Ramos** — pickup request, validation & printable summary
- **Jay C. Villaceran** — shop catalog, search, filters & basket

## Run this project

1. Clone or download this repository.
2. In a terminal, navigate to the directory containing `index.html`.
3. Run: `python -m http.server 8000`
4. Open [http://localhost:8000](http://localhost:8000) in an up-to-date browser with internet access.
5. Explore the five pages and try the PyScript interactions.

No package installation, backend or database is required to host the site — the CDN provides the PyScript runtime at page load, so an internet connection is needed. Opening `index.html` directly via `file://` is not recommended due to browser module restrictions.

## Pages

| Page | Interactive features |
|---|---|
| `index.html` | Pick a student need; click handler updates the recommendation panel |
| `services.html` | Price calculator updates on input/change; validates quantities, handles rental mode and pickup fee |
| `pickup.html` | Print-cost estimate; file-name preview; validated, printable local request draft |
| `shop.html` | Live search, category filters, add-to-basket, running total and clear basket |
| `about.html` | Concept, founders, proposed location and feasibility-study findings |

## Important prototype limits

**No file upload, order submission, reservation, stock control, purchase, online payment or email happens here.** The pickup form creates a draft **within the browser only** and lets customers print/save it. Choosing a file reveals its name locally, but file bytes are never transmitted or stored. Contact the shop through an actual communication channel outside this prototype to submit documents.

Pricing for printing, scanning, computer rental and pickup uses the proposed rates from the feasibility report. Individual shop-item prices are illustrative for the interactive catalog demo.

## Tech stack

- **HTML5** — five linked, semantic pages
- **CSS3** — responsive layout, cards, forms and tables
- **PyScript** — pinned to the `2026.7.3` CDN; `@when` event decorators, DOM updates, Python business logic
- **Python `unittest`** — six offline logic checks with a mock DOM, no external dependencies

PyScript reference: https://docs.pyscript.net/2026.7.3/

## Project structure

```text
index.html / services.html / pickup.html / shop.html / about.html
styles.css
assets/mark.svg
scripts/home.py
scripts/services.py
scripts/pickup.py
scripts/shop.py
tests/test_logic.py
```

## Test

```bash
python -m unittest discover -s tests -v
```

The six offline tests cover the estimate calculations, pickup draft and date validation, shop filtering and basket totals, and the home recommendation click handler — all without a network or browser.
