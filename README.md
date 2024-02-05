# Google cloud run sidecar backend frontend
![](https://img.shields.io/badge/version-v0.0.1-blue.svg)
![](https://img.shields.io/badge/python-3.9-blue.svg)
[![Docs](https://img.shields.io/badge/docs-confluence-013A97)]()
![](https://img.shields.io/badge/dev-orange.svg)

Deploy an app frontend & backend in a single google cloud run service with a sidecar.

- ingress: frontend
- sidecar: backend
- frontend: typescript + react + nginx
- backend: python + fastapi + uvicorn

## Deploy
Replace $PROJECT, $ARTIFACT, and $YOUR_APP_URL in service.yaml.

Run:
```sh
pip install .
deploy_app --cloud-run --frontend --tox False
```

## Debug
Open 2 terminals and run:

```sh
sh backend.sh
```

```sh
sh frontend.sh
```