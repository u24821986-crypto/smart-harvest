# SmartHarvest System - Rembander Agribusiness

**Module:** BFB 321 - Supply Chain Technologies and Project
**Project:** Semester 2, 2026

## Project Overview
SmartHarvest is a web-based supply chain management solution designed for Rembander Agribusiness (Tsianda Village). The system helps track daily harvesting operations, manage transport vehicle capacity, identify operational bottlenecks (labour vs transport), and ensure deliveries meet the packhouse cut-off time (17:00).

## Group Members
*   **Seloko Mothupi** - 24804232
*   **Mfanelo Shilubana** - 18142002
*   **Chantel Mogale** - 24821986
*   **Livhuwani Ndou** - 23549743

---

## Folder Structure
The project is structured for a Flask application, separating the HTML frontend, and Python logic models.

```text
BFB321_Project/
│
├── app.py                     # Main Flask application file
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
└── templates/                 # HTML files (Jinja2 templates)
    ├── index.html
    ├── login.html
    ├── dashboard.html
    └── operations.html
