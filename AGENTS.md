# Repository Guidelines

## Project Structure & Module Organization

This repository implements a FIFA 22 data-science workflow. Run the notebooks in numeric order: `notebooks/01_limpeza.ipynb` prepares the raw data, `02_eda.ipynb` performs exploratory analysis, and `03_modelagem.ipynb` trains and evaluates the models. Generated datasets live in `data/`; trained artifacts and dashboard metadata live in `models/`. The Streamlit entry point is `dashboard/app.py`. The `docs/` directory contains project documentation, including implementation specifications in `docs/specs/`. Update `README.md` when the workflow changes.

## Specifications & Task Tracking

Create one Markdown file in `docs/specs/` for each feature or change. Use a numeric prefix and descriptive slug, for example `docs/specs/001-data-validation.md`. Each specification must state its objective, functional and technical requirements, validation tests, minimum acceptance criteria, and a numbered implementation task list (`1.`, `2.`, `3.`). Keep task numbering stable while work is in progress so commits and pull requests can reference a specific task.

After completing an implementation task, immediately update the corresponding specification to mark that task as completed. When every task and acceptance criterion has been satisfied, update the specification status to `Finalizada`. Do not report work as complete while its specification still shows it as pending.

## Setup and Development Commands

Use Python 3.10 or newer and, preferably, an isolated virtual environment.

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
jupyter notebook
streamlit run dashboard/app.py
```

The notebook server supports the analysis workflow. Streamlit starts at `http://localhost:8501`. There is no separate build step. After dependency changes, update `requirements.txt` with deliberate constraints.

## Coding Style & Naming Conventions

Follow PEP 8: use four-space indentation, `snake_case` for functions and variables, and `UPPER_SNAKE_CASE` for constants such as `DATA_DIR`. Group standard-library imports before third-party imports. Resolve paths through `pathlib.Path`. Use Portuguese or English consistently within each module. Keep notebook cells focused, executable in order, and document non-obvious transformations in Markdown. No formatter or linter is configured, so review formatting before committing.

## Testing and Data Validation

No automated test suite or coverage threshold exists. Validate changes by restarting the kernel and running affected notebooks from top to bottom. For dashboard changes, launch Streamlit and exercise all three tabs, filters, empty-result states, and the value simulator. Confirm that regenerated CSV files preserve expected columns and that `models/metadados.json` remains compatible with the serialized model. If adding tests, place them in `tests/` and name files `test_*.py` for pytest discovery.

## Commit & Pull Request Guidelines

History favors short summaries, sometimes in Portuguese and sometimes in English. Use a concise imperative subject that identifies the scope, for example `Update clustering evaluation`. Keep generated data and model changes in the same commit as the code that produces them. Pull requests should explain the analytical or UI change, list validation commands, and identify regenerated artifacts. Link relevant issues and include screenshots for visible dashboard changes. Do not commit virtual environments, notebook checkpoints, credentials, or large raw datasets.
