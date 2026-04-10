# AutoRent — Vehicle Rental Management System

A command-line business management system built in Python, simulating the core operations of a vehicle rental company. Developed as part of a Data Analysis course (CESAE Digital, 2026).

---

## What it does

AutoRent manages the full lifecycle of a vehicle rental business:

- **Vehicles** — register, list, edit and track availability
- **Clients** — register with full data validation (Portuguese NIF, phone, email, date of birth)
- **Rentals** — create, monitor, close and cancel rental contracts with automatic pricing and monthly quota enforcement
- **Logging** — every operation is written to a log file with timestamp and category

---

## Technical highlights

- **Modular architecture** — logic split across dedicated modules (`viaturas`, `clientes`, `alugueres`, `validacoes`, `logger`, `database`)
- **SQLite database** — relational schema with 3 tables, foreign keys, UNIQUE constraints and CHECK constraints for data integrity
- **Input validation** — Portuguese NIF check digit algorithm, licence plate format (3 formats), phone, email, date of birth (minimum age 18)
- **Business rules** — monthly quota enforcement per client, automatic rental pricing, vehicle availability state machine (`Available` → `Rented` → `Available`)
- **Audit log** — structured log entries per event category (`VEHICLE`, `CLIENT`, `RENTAL`, `ERROR`)

---

## Project structure

```
autorent/
├── main.py          # Entry point and menu navigation
├── database.py      # SQLite initialisation and table creation
├── viaturas.py      # Vehicle management (CRUD + availability)
├── clientes.py      # Client management (CRUD + validation)
├── alugueres.py     # Rental management (create, close, cancel)
├── validacoes.py    # Input validation (NIF, plate, email, dates)
├── logger.py        # Audit logging to log.txt
└── README.md
```

---

## How to run

**Requirements:** Python 3.8+, no external libraries needed (standard library only)

```bash
git clone https://github.com/diogomacosta29/autorent.git
cd autorent
python main.py
```

The SQLite database (`autorent.db`) is created automatically on first run.

---

## Database schema

```
viaturas    — id, marca, modelo, matricula (UNIQUE), num_assentos, valor_dia, estado, disponibilidade
clientes    — id, nome, data_nascimento, sexo, nif (UNIQUE), telemovel, email (UNIQUE), cota_mensal
alugueres   — id, viatura_id (FK), cliente_id (FK), data_inicio, data_fim, valor_total, estado
```

Rental states: `Previsto` → `Em curso` → `Terminado` / `Cancelado`

---

## Skills demonstrated

`Python` `SQLite` `modular design` `data validation` `error handling` `business logic` `CLI application`

---

## Author

Diogo Costa — [LinkedIn](www.linkedin.com/in/diogo-costa-8b1704295) · [diogomacosta29@gmail.com](mailto:diogomacosta29@gmail.com)

*Part of a broader data analysis portfolio — see other repositories for SQL and Power BI projects.*