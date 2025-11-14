# Friday - Quick Start Deployment Guide

Deploy your Friday AI assistant to Oracle Cloud Free Tier in ~30 minutes for **$0/month**.

## 🎯 What You'll Get

- ✅ Friday AI assistant running 24/7
- ✅ Free subdomain (e.g., `friday-yourname.duckdns.org`)
- ✅ Optional HTTPS with auto-renewing SSL certificate
- ✅ 12-24 GB RAM, 2-4 ARM CPUs
- ✅ **$0/month forever**

## 🚀 3-Step Deployment

### Step 1: Test Locally (5 minutes)

```bash
# Copy environment template
cp .env.production.example .env

# Add your API keys
nano .env

# Build and test
docker compose -f docker-compose.production.yml up
```

Open http://localhost:3000 to verify it works.

**Stop with:** `Ctrl+C` then `docker compose -f docker-compose.production.yml down`

### Step 2: Create Oracle Cloud Server (10 minutes)

1. Go to [Oracle Cloud Console](https://cloud.oracle.com/)
2. **Create Instance:**
   - Image: Ubuntu 22.04
   - Shape: **Ampere VM.Standard.A1.Flex** (ARM)
   - OCPUs: 2-4, RAM: 12-24 GB
   - Download SSH key
3. **Configure Firewall** (Security List):
   - Add Ingress Rules: TCP ports 80, 443, 3000

See [deploy/DEPLOYMENT.md](deploy/DEPLOYMENT.md) for detailed instructions with screenshots.

### Step 3: Deploy to Server (15 minutes)

```bash
# SSH into your server
ssh -i ~/Downloads/ssh-key.key ubuntu@YOUR_SERVER_IP

# Clone repository
git clone YOUR_REPO_URL
cd open-webui

# Setup server (Docker, firewall, etc.)
bash deploy/setup-server.sh

# Log out and back in
exit
ssh -i ~/Downloads/ssh-key.key ubuntu@YOUR_SERVER_IP
cd open-webui

# Configure environment
cp .env.production.example .env
nano .env  # Add your API keys

# Deploy!
bash deploy/deploy.sh
```

**Access Friday at:** `http://YOUR_SERVER_IP:3000`

## 🌐 Add Custom Domain (Optional, 5 minutes)

### Free Option: DuckDNS

1. Visit [duckdns.org](https://www.duckdns.org/)
2. Sign in with GitHub/Google
3. Create subdomain: `friday-yourname`
4. Point to your server IP

**Access at:** `http://friday-yourname.duckdns.org:3000`

## 🔒 Enable HTTPS (Optional, 5 minutes)

```bash
# Edit Caddyfile with your domain
nano deploy/caddy/Caddyfile

# Replace YOUR_DOMAIN with: friday-yourname.duckdns.org
# Replace email with your email

# Redeploy with Caddy
docker compose -f docker-compose.production.yml down
docker compose -f docker-compose.caddy.yml up -d
```

**Access at:** `https://friday-yourname.duckdns.org` (no port needed!)

## 📁 Files Overview

| File | Purpose |
|------|---------|
| `docker-compose.production.yml` | Production deployment (HTTP) |
| `docker-compose.caddy.yml` | Production with HTTPS |
| `.env.production.example` | Environment variables template |
| `deploy/setup-server.sh` | Server setup script |
| `deploy/deploy.sh` | Deploy/update script |
| `deploy/DEPLOYMENT.md` | Complete guide |
| `TESTING.md` | Local testing guide |

## 🛠️ Common Commands

```bash
# Deploy/Update
bash deploy/deploy.sh

# View logs
docker logs friday -f

# Restart
docker restart friday

# Stop
docker compose -f docker-compose.production.yml down

# Status
docker ps
```

## 🐛 Troubleshooting

**Can't access from browser?**
```bash
# Check Oracle Cloud Security List has ports 80, 443, 3000 open
# Check firewall: sudo ufw status
```

**Container won't start?**
```bash
# Check logs: docker logs friday
# Verify .env has WEBUI_SECRET_KEY set
```

**HTTPS not working?**
```bash
# Check Caddy logs: docker logs friday-caddy
# Ensure ports 80 and 443 are open in Oracle Cloud
```

## 📖 Full Documentation

- **[deploy/DEPLOYMENT.md](deploy/DEPLOYMENT.md)** - Complete deployment guide
- **[deploy/README.md](deploy/README.md)** - Deployment scripts overview
- **[TESTING.md](TESTING.md)** - Local testing guide

## 💰 Cost Breakdown

| Service | Cost |
|---------|------|
| Oracle Cloud ARM (2-4 CPU, 12-24 GB RAM) | $0 |
| DuckDNS Domain | $0 |
| Let's Encrypt SSL | $0 |
| **Total** | **$0/month** ✅ |

## 🎉 Next Steps

1. Create admin account in Friday
2. Connect your AI providers (OpenAI, Anthropic)
3. Upload documents for RAG
4. Start chatting!

## 🆘 Need Help?

- Check logs: `docker logs friday -f`
- Read [deploy/DEPLOYMENT.md](deploy/DEPLOYMENT.md)
- Check `.env` file has all required variables

---

**Ready to deploy? Start with Step 1 above! 🚀**
