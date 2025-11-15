# Deployment Guide (Render)

## Prerequisites
- Render account with permission to create a Web Service
- GitHub/Render integration pointing to this repository
- `uv` CLI available locally (for parity with production install)

## Deploying
1. Push the latest code to GitHub.
2. In Render, create a new **Web Service** and connect it to the repo.
3. Use the generated `render.yaml` (root of repo) for configuration:
   - Build: `uv pip install -r requirements.txt`
   - Start: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
4. Ensure the following environment variables are set (Render UI):
   - `PYTHON_VERSION=3.12` (matches `.python-version`)
   - Optional: `STREAMLIT_BROWSER_GAP=0` to suppress banner

## Post-Deploy Checklist
- Open the Render URL and test both “All States” and a specific state (e.g., California)
- Validate the new interpretability visuals load quickly (<1s)
- Check logs for any warnings related to `state_cz_mapping.csv`

## Ongoing Maintenance
- Use `uv pip compile/uv add` locally to modify dependencies, then push and redeploy.
- Update `render.yaml` if additional services or background workers are introduced.
