# SmartHarvest System - Rembander Agribusiness

**Module:** BFB 321 - Supply Chain Technologies and Project
**Project:** Semester 2, 2026

## Project Description
SmartHarvest is a web-based supply chain management solution designed for Rembander Agribusiness (Tsianda Village). The system helps track daily harvesting operations, manage transport vehicle capacity, identify operational bottlenecks (labour vs transport), and ensure deliveries meet the packhouse cut-off time (17:00).

## Group Members
*   **Seloko Mothupi** - 24804232
*   **Mfanelo Shilubana** - 18142002
*   **Chantel Mogale** - 24821986
*   **Livhuwani Ndou** - 23549743

---

## Installation & Setup Instructions

This submission focuses on the frontend prototype (HTML/CSS/JS) and Python logic models. No external server or database installation is required to view the UI.

**To view the web application:**
1. Download or clone this repository to your local machine.
2. Open the `templates` folder.
3. Double-click on `index.html` to open the Home page in any web browser (Chrome, Edge, Firefox, etc.).
4. Use the navigation buttons on the screen to move between the Login, Dashboard, and Operations pages.

**To view the Python logic models and tests:**
1. Open the `models` folder to view the calculation logic (e.g., `harvest_model.py`, `transport_model.py`).
2. Open the `tests` folder to view the Python unit tests written to validate the models.

---

## Folder Structure
```text
smart-harvest/
│
├── README.md                  # This file
├── .gitignore                 # Git ignore file
│
├── models/                    # Python logic files
│   ├── bottleneck_model.py
│   ├── harvest_model.py
│   ├── optimisation_model.py
│   └── transport_model.py
│
├── tests/                     # Unit tests for models
│   ├── test_bottleneck_model.py
│   ├── test_harvest_model.py
│   ├── test_optimisation_model.py
│   └── test_transport_model.py
│
└── templates/                 # HTML files (Frontend prototype)
    ├── index.html
    ├── login.html
    ├── dashboard.html
    └── operations.html
