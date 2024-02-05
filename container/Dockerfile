FROM python:3.9-slim

RUN pip install --upgrade pip

COPY MANIFEST.in model/MANIFEST.in
COPY pyproject.toml model/pyproject.toml
RUN mkdir -p model/tmp

COPY requirements.txt model/requirements.txt
RUN pip install -r model/requirements.txt

COPY README.md model/README.md
COPY setup.cfg model/setup.cfg
COPY src/ model/src/

RUN cd model && pip install . && cd ..

# app
ENV PORT 81
COPY src/demo/frontend/api/app.py app/app.py
WORKDIR app
ENTRYPOINT sh -c "uvicorn app:app --host 0.0.0.0 --port ${PORT}"