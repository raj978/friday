# Local Testing Guide

Test Friday locally before deploying to production.

## Quick Test

```bash
# 1. Copy environment example
cp .env.production.example .env

# 2. Generate secret key
echo "WEBUI_SECRET_KEY=$(openssl rand -base64 32)" >> .env

# 3. Add your API keys to .env
nano .env

# 4. Test build (without starting)
docker compose -f docker-compose.production.yml build

# 5. Start locally
docker compose -f docker-compose.production.yml up

# 6. Open browser
open http://localhost:3000
```

## Test Checklist

- [ ] Container builds successfully
- [ ] Application starts without errors
- [ ] Can access at http://localhost:3000
- [ ] Can create user account
- [ ] Can chat with AI models
- [ ] Documents upload works
- [ ] Settings save properly

## Stop Testing

```bash
# Stop containers
docker compose -f docker-compose.production.yml down

# Clean up (optional)
docker compose -f docker-compose.production.yml down -v
docker system prune -a
```

## Common Issues

### Build Fails
```bash
# Clear Docker cache
docker builder prune -a
docker compose -f docker-compose.production.yml build --no-cache
```

### Port 3000 Already in Use
```bash
# Use different port
FRIDAY_PORT=3001 docker compose -f docker-compose.production.yml up
```

### Missing API Keys
```bash
# Check .env file
cat .env | grep API_KEY

# Add keys
nano .env
```

## Test HTTPS Locally (Optional)

Not recommended for local testing. Just test HTTP, then use Caddy on production server for HTTPS.

## Ready to Deploy?

If everything works locally, proceed to production deployment:

See [deploy/DEPLOYMENT.md](deploy/DEPLOYMENT.md) for full guide.
