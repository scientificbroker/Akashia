Banco de sueños para el análisis semántico entre regiones

Run locally
--------------

1. Create a virtual environment and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Run the app:

```powershell
python app.py
```

The form will be available at http://127.0.0.1:5000/ and submissions are stored in `submissions.csv`.

Deploy to GitHub Container Registry and Render
--------------------------------------------

1. (Optional) If GHCR publishing requires a PAT with package write permissions, create a Personal Access Token with `write:packages` and add it to the repository secrets as `GHCR_TOKEN`.

2. (Optional) To trigger an automatic deploy on Render after the image is published:
	- Create a Web Service in Render connected to this repository or create a Deploy Hook in the Render dashboard.
	- Copy the webhook URL and add it as a repository secret named `RENDER_WEBHOOK` (Settings → Secrets).

The workflow `docker-publish.yml` will build and push the image to `ghcr.io/<owner>/akashia:latest` on pushes to `main`. If `RENDER_WEBHOOK` is set, it will POST to that URL to trigger the deploy.


