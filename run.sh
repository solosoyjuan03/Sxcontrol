#!/usr/bin/env bash
# Arranca SXcontrol en el entorno virtual local.
# Uso: ./run.sh   (o: ./run.sh test  para ejecutar las pruebas)
set -euo pipefail

cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
    echo "No existe venv/. Creándolo..."
    python3 -m venv venv
    ./venv/bin/pip install --upgrade pip
    ./venv/bin/pip install -r requirements.txt
fi

if [ "${1:-}" = "test" ]; then
    exec ./venv/bin/python -m unittest discover -s tests -v
fi

echo "Iniciando SXcontrol en http://127.0.0.1:5000"
exec ./venv/bin/python app.py
