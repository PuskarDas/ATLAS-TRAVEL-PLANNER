# Deployment

CI is configured in `.github/workflows/ci.yml` to install dependencies, run backend tests, run quality checks, and build the frontend.

`.github/workflows/deploy.yml` is a manual deployment placeholder. Add your target provider secrets and replace the placeholder command with the platform-specific deployment step.

## Vercel Deployment (Recommended)

1. **Push to GitHub**: Ensure your latest changes are pushed to your repository.
2. **Import to Vercel**: Connect your GitHub account to Vercel and import the repository.
3. **Framework Preset**: Vercel should automatically detect the configuration via `vercel.json`.
4. **Environment Variables**:
   - Add any keys from `backend/.env.example` in the Vercel Dashboard.
   - **Critical**: Ensure `TRAVEL_CORS_ORIGINS` includes your Vercel deployment URL.
   - Set `TRAVEL_ENVIRONMENT` to `production`.
5. **Deploy**: Click deploy.

### Important Notes for Vercel:
- **Statelessness**: The `InMemoryStore` resets on cold starts. For persistence, use a remote MongoDB or MySQL instance and update `TRAVEL_DATABASE_URL`.
- **WebSockets**: Vercel Serverless Functions **do not support WebSockets**. The real-time features in `/ws/` will not function as expected; consider using a dedicated server (EC2/DigitalOcean) or a service like Pusher if real-time updates are critical.
