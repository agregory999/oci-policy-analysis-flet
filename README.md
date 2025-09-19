# NavRail OCI Management App

[![Docs](https://github.com/<your-username>/<your-repo>/actions/workflows/docs.yml/badge.svg)](https://<your-username>.github.io/<your-repo>/)

A **Flet-based desktop and web app** for exploring Oracle Cloud Infrastructure (OCI) IAM policies, users, groups, and AI-powered insights.  

The app provides:
- A NavRail UI with multiple views (Settings, Policies, Users).
- A token-based login overlay (session token printed to shell).
- Fly-in console log backed by Python’s logging module.
- Rotating log files for server deployments.
- Support for both local OCI profile auth and Instance Principal auth on servers.
- Ready-to-use Sphinx autodoc + GitHub Pages docs.

---

## Features

- NavRail-based navigation between Settings, Policies, Users (and more to come).
- Console log fly-in (toggleable in Settings).
- Rotating log files (`./logs/app.log`) with rollover at 5 MB (5 backups).
- Log level dropdown in Settings (DEBUG, INFO, WARNING, ERROR).
- Clear button for console logs.
- Token-based login overlay (UUID or OCI Vault in future).
- Single source of truth for logs (`logging.Logger`).
- Pre-commit hooks for linting (Ruff) and documentation validation (Sphinx).

---

## Development Workflow

### 1. Install Dependencies

Clone the repo and install requirements:

    git clone https://github.com/<your-username>/<your-repo>.git
    cd <your-repo>
    pip install -r requirements.txt

---

### 2. Run the App

Run in desktop mode:

    flet run app/main.py

Or in browser mode:

    flet run app/main.py --web

On startup, the app prints a session token to the shell:

    🔑 Session token (share with user): 123e4567-e89b-12d3-a456-426614174000

Enter this token in the login overlay to unlock the app.

---

### 3. Logging

All logs use Python’s logging module. Output goes to:

- UI console fly-in (toggle in Settings).
- Rotating log files:

      ./logs/app.log

  (5 MB max, 5 backups).

Control verbosity via the Log Level dropdown on the Settings page.  
Clear console logs via the Clear Console button in the fly-in.

---

### 4. Server Deployment

- Deploy on an OCI Compute Instance with Instance Principal auth enabled.
- Run the app as usual:

      python app/main.py

- Place an OCI Load Balancer in front of the instance:
  - Terminate HTTPS at the Load Balancer.
  - Forward plain HTTP to the app.
- Users access the app via the Load Balancer’s public IP or DNS.

---

### 5. Documentation

We use Sphinx + Furo theme for docs.  

Build docs locally:

    sphinx-apidoc -o docs/ app
    sphinx-build -b html docs/ docs/_build/html

Docs are:
- Validated on every commit (via pre-commit hook).
- Auto-published to GitHub Pages (see `.github/workflows/docs.yml`).

Published docs:  
👉 https://<your-username>.github.io/<your-repo>/

---

### 6. Pre-Commit Hooks

We use pre-commit to enforce style and validate docs before commits.

Install pre-commit hooks once per clone:

    pre-commit install

From then on, every `git commit` will:
- Run Ruff lint/format.
- Build Sphinx docs in strict mode.

Run manually on all files:

    pre-commit run --all-files

---

## Requirements

See `requirements.txt` for dependencies:
- flet (UI)
- oci (OCI Python SDK)
- sphinx, furo (docs)
- ruff, pre-commit (dev)

Or install via pyproject.toml:

    pip install .[dev]

---

## License

MIT License
