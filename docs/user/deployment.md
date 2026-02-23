# Deployment

Astris can be deployed to Cloudflare Pages in two ways:

1. Deploy from your local machine with `astris deploy`.
2. Connect your Git repository in Cloudflare Pages and let Cloudflare build on each push.

## 1) Configure your project

Create or update `pyproject.toml` with Astris settings:

```toml
[tool.astris.build]
output_dir = "dist"
clean_urls = true

[tool.astris.deploy]
provider = "cloudflare"

[tool.astris.deploy.cloudflare]
project_name = "your-cloudflare-pages-project"
# branch = "main" # optional

[tool.astris.env]
# Add runtime variables used while building pages.
# DATABASE_URL = "postgresql://..."
```

### What these options do

- `clean_urls = true` generates pages as `path/index.html` and rewrites internal links as `/path`.
- `output_dir` is the folder uploaded to Cloudflare Pages.
- `tool.astris.env` variables are injected into `os.environ` before `build` and `deploy`.

## 2) Deploy with `astris deploy`

Requirements:

- Python environment with Astris installed.
- Node.js installed (`npx` must be available).
- Cloudflare authentication configured for Wrangler (`npx wrangler login`).

Run:

```bash
uv sync
uv run astris deploy --file main.py
```

This command will:

1. Load `[tool.astris]` configuration from `pyproject.toml`.
2. Build your site using configured build options.
3. Run Wrangler under the hood:

```bash
npx wrangler pages deploy dist --project-name your-cloudflare-pages-project
```

## 3) Deploy from Git (Cloudflare-managed builds)

If you prefer automatic deploys from your repository:

1. In Cloudflare Dashboard, go to **Workers & Pages** > **Create** > **Pages**.
2. Connect your Git provider and select the repository.
3. Set build configuration:
   - **Build command**: `uv run astris build --file main.py`
   - **Build output directory**: `dist`
4. In Cloudflare project settings, add any required environment variables.
5. Trigger the first deploy.

### Notes for clean URLs

With `clean_urls = true`, Astris generates files in folder-based format (`about/index.html`) and your links stay extensionless (`/about`). Cloudflare Pages serves these as clean routes.
