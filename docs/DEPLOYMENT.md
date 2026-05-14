# Deployment

CI is configured in `.github/workflows/ci.yml` to install dependencies, run backend tests, run quality checks, and build the frontend.

`.github/workflows/deploy.yml` is a manual deployment placeholder. Add your target provider secrets and replace the placeholder command with the platform-specific deployment step.

## Vercel Deployment (Recommended)

1. **Push to GitHub**: Ensure your latest changes are pushed to your repository.
2. **Import to Vercel**: Connect your GitHub account to Vercel and import the repository.
3. **Framework Preset**: Vercel should automatically detect the configuration via `vercel.json`.
4. **Environment Variables**:
   - Add any keys from `backend/.env.example` (like OpenAI, Google Maps, etc.) in the Vercel Dashboard under **Settings > Environment Variables**.
5. **Deploy**: Click deploy.

*Note: The current `InMemoryStore` will reset data frequently in a serverless environment. Use a persistent database for production.*
