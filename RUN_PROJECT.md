# Run the Employee API

These instructions use Windows PowerShell and the finished project paths.

## Prerequisites

- Windows PowerShell
- Python 3.11. This workspace has it at `C:\Users\Priya\AppData\Local\Programs\Python\Python311\python.exe`.
- VS Code (optional but recommended)

## Open the project in VS Code

From PowerShell:

```powershell
Set-Location C:\Users\Priya\Desktop\Jtronix
code .
```

## Create and activate the virtual environment

From the project root:

```powershell
& 'C:\Users\Priya\AppData\Local\Programs\Python\Python311\python.exe' -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run this once for the current PowerShell user, then activate again:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

## Install dependencies

```powershell
python -m pip install -r requirements.txt
```

## Start the API

With the virtual environment active:

```powershell
python -m uvicorn app.main:app --reload
```

The base URL is `http://127.0.0.1:8000`. Interactive OpenAPI documentation is at `http://127.0.0.1:8000/docs`.

## Run tests

Open a second PowerShell window, change to the project root, activate `.venv`, and run:

```powershell
Set-Location C:\Users\Priya\Desktop\Jtronix
.\.venv\Scripts\Activate.ps1
python -m pytest -q
```

## Postman demo

Import `postman\Employee_API.postman_collection.json` into Postman. Its `baseUrl` variable defaults to `http://127.0.0.1:8000`. Run the requests in collection order against a freshly started API. The API is in-memory, so a restart restores the seed data and resets created IDs.

If Postman is unavailable, use the interactive docs or the endpoint examples in the collection. The same scenarios are covered by the automated tests.

## Troubleshooting

- Port in use: stop the other process or start with `python -m uvicorn app.main:app --reload --port 8001`, then use `http://127.0.0.1:8001`.
- `ModuleNotFoundError`: confirm the current directory is `C:\Users\Priya\Desktop\Jtronix`, activate `.venv`, and run `python -m pip install -r requirements.txt`.
- Virtual environment not active: run `.\.venv\Scripts\Activate.ps1`; the prompt should show `(.venv)`.
- PowerShell script blocked: run `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`, then activate again.

## Stop and restart

In the terminal running Uvicorn, press `Ctrl+C`. To restart, run the start command again. All in-memory changes are lost on restart.
