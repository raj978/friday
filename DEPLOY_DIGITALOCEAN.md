# Friday - DigitalOcean Deployment Guide

Deploy your Friday AI assistant to DigitalOcean App Platform in ~10 minutes using your credits.

## 🎯 What You'll Get

- ✅ Friday running 24/7 on DigitalOcean
- ✅ Free subdomain: `friday-yourname.ondigitalocean.app`
- ✅ Automatic HTTPS with SSL certificate
- ✅ Auto-deploys from GitHub on push
- ✅ 1 GB RAM, 1 vCPU
- ✅ **Cost**: ~$12/month (using your DO credits)

## 📋 Prerequisites

1. DigitalOcean account with credits
2. GitHub account
3. Your code pushed to GitHub repo: `raj978/friday`
4. API keys ready (OpenAI, Anthropic, etc.)

## 🚀 Deployment Steps

### Step 1: Push Your Code to GitHub

```bash
# Make sure all changes are committed
git add .
git commit -m "chore: ready for deployment"
git push origin master
```

### Step 2: Create App on DigitalOcean

1. Go to [DigitalOcean Dashboard](https://cloud.digitalocean.com/apps)
2. Click **"Create App"**
3. Select **"GitHub"** as source
4. **Authorize** DigitalOcean to access your GitHub
5. Select repository: **raj978/friday**
6. Select branch: **master**
7. Click **"Next"**

### Step 3: Configure App (Auto-detected)

DigitalOcean will auto-detect the `.do/app.yaml` configuration:

**Verify these settings:**
- ✅ Service name: `web`
- ✅ Region: `New York (NYC)`
- ✅ Instance size: `Professional - $12/month` (1 GB RAM)
- ✅ Build method: `Dockerfile`
- ✅ HTTP Port: `8080`

Click **"Next"**

### Step 4: Set Environment Variables (SECRETS)

You'll need to set the SECRET environment variables that weren't included in the yaml:

1. **WEBUI_SECRET_KEY** (Required)
   ```bash
   # Generate this locally:
   openssl rand -base64 32
   ```
   - Copy the output
   - In DO dashboard, find `WEBUI_SECRET_KEY`
   - Paste the generated key
   - Mark as **SECRET** ✅

2. **OPENAI_API_KEY** (Required if using OpenAI)
   - Paste your OpenAI API key: `sk-proj-...`
   - Mark as **SECRET** ✅

3. **ANTHROPIC_API_KEY** (Required if using Claude)
   - Paste your Anthropic API key: `sk-ant-...`
   - Mark as **SECRET** ✅

Click **"Next"**

### Step 5: Review & Deploy

1. **Review**:
   - App name: `friday-second-brain`
   - Cost: ~$12/month (uses your credits)
   - Environment variables: ✅ All secrets set

2. Click **"Create Resources"**

### Step 6: Wait for Build (5-10 minutes)

DigitalOcean will:
1. ✅ Clone your repository
2. ✅ Build Docker image (this takes ~5-8 minutes)
3. ✅ Download AI models (embeddings, whisper)
4. ✅ Deploy to infrastructure
5. ✅ Assign subdomain
6. ✅ Configure SSL certificate

**Watch the logs** in the DigitalOcean dashboard to see progress.

### Step 7: Access Your App

Once deployed (status shows "Active"):

1. Copy your app URL: `https://friday-second-brain-xxxxx.ondigitalocean.app`
2. Open in browser
3. **Create your admin account** on first visit

**🎉 Friday is live!**

---

## 🔧 Configuration Details

### Environment Variables (All Set in .do/app.yaml)

| Variable | Value | Description |
|----------|-------|-------------|
| `ENABLE_OLLAMA_API` | `false` | Disable local Ollama (using APIs) |
| `ENABLE_OPENAI_API` | `true` | Enable OpenAI integration |
| `OPENAI_API_BASE_URL` | `https://api.openai.com/v1` | OpenAI endpoint |
| `WEBUI_NAME` | `Friday` | App name |
| `PORT` | `8080` | Internal port |
| `WHISPER_MODEL` | `base` | Speech-to-text model |
| `RAG_EMBEDDING_MODEL` | `sentence-transformers/all-MiniLM-L6-v2` | Document embeddings |
| `SCARF_NO_ANALYTICS` | `true` | Disable telemetry |
| `DO_NOT_TRACK` | `true` | Disable tracking |
| `ANONYMIZED_TELEMETRY` | `false` | Disable telemetry |

### Resource Configuration

| Resource | Value |
|----------|-------|
| **Instance Type** | Professional-XS |
| **RAM** | 1 GB |
| **vCPU** | 1 |
| **Storage** | Persistent (for database) |
| **Region** | NYC (New York) |

---

## 📝 Post-Deployment

### Access Your App

Your app will be available at:
```
https://friday-second-brain-[random].ondigitalocean.app
```

### Create Admin Account

1. Open your app URL
2. Click "Sign Up"
3. Create your account (first user is admin)
4. Log in and start using Friday!

### Configure AI Providers

1. Go to **Settings** → **Connections**
2. Verify OpenAI/Anthropic connections
3. Test with a chat

---

## 🔄 Updates & Redeployment

### Auto-Deploy on Git Push

Every time you push to `master` branch:
```bash
git add .
git commit -m "feat: new feature"
git push origin master
```

DigitalOcean will **automatically**:
1. Detect the push
2. Rebuild the Docker image
3. Redeploy with zero downtime

### Manual Redeploy

In DigitalOcean dashboard:
1. Go to your app
2. Click **"Actions"** → **"Force Rebuild and Deploy"**

---

## 💾 Data Persistence

### Database Location

- **Path**: `/app/backend/data/webui.db`
- **Type**: SQLite
- **Persistence**: ✅ Data persists across deploys

### What's Stored

- User accounts
- Chat history
- Documents uploaded to RAG
- Settings and configurations
- Notes and knowledge base

### Backup Your Data

DigitalOcean App Platform automatically backs up persistent storage, but you can also:

```bash
# Get console access in DO dashboard
# Then backup the database
tar -czf friday-backup-$(date +%Y%m%d).tar.gz /app/backend/data
```

---

## 📊 Monitoring

### View Logs

In DigitalOcean dashboard:
1. Go to your app
2. Click **"Runtime Logs"** tab
3. View real-time application logs

### Check Health

- Health endpoint: `https://your-app.ondigitalocean.app/health`
- Should return: `{"status": true}`

### Resource Usage

Monitor in DigitalOcean dashboard:
- CPU usage
- Memory usage
- Request rate
- Response times

---

## 🐛 Troubleshooting

### Build Fails with "Out of Memory"

**Problem**: Instance too small for Docker build

**Solution**: Upgrade to Professional-XS (1GB) or higher
```yaml
instance_size_slug: professional-xs  # Already set in .do/app.yaml
```

### "WEBUI_SECRET_KEY not set" Error

**Problem**: Secret key not configured

**Solution**:
1. Generate key: `openssl rand -base64 32`
2. In DO dashboard → App Settings → Environment Variables
3. Add `WEBUI_SECRET_KEY` with generated value
4. Mark as SECRET
5. Redeploy

### App Not Accessible

**Problem**: Health check failing

**Solutions**:
1. Check logs for errors
2. Verify PORT=8080 is set
3. Wait 90 seconds for initial model download
4. Check Dockerfile builds locally

### Database Connection Error

**Problem**: Can't connect to database

**Solution**:
- Verify `DATA_DIR=/app/backend/data` is set
- Check persistent storage is enabled
- DATABASE_URL should be empty (uses default)

### API Keys Not Working

**Problem**: Can't connect to OpenAI/Anthropic

**Solutions**:
1. Verify keys are set as SECRETS in DO dashboard
2. Check `OPENAI_API_BASE_URL` is correct (no typo!)
3. Test keys with: Settings → Connections

---

## 💰 Cost Management

### Current Configuration Cost

| Service | Cost/Month |
|---------|------------|
| Professional-XS instance | $12 |
| Bandwidth (included) | $0 |
| SSL Certificate | $0 |
| **Total** | **$12/month** |

### Using Your Credits

- DigitalOcean will automatically use your credits
- Monitor usage in Billing section
- Set up billing alerts

### Downgrade Options

If you need to reduce cost (may impact performance):

1. **Basic plan** ($5/month):
   - 512 MB RAM (⚠️ may fail to build)
   - Not recommended for this app

2. **Professional-XS** ($12/month) ← **Recommended**:
   - 1 GB RAM
   - Reliable builds
   - Good performance

---

## 🔒 Security Best Practices

### 1. Protect Your Secrets

- ✅ All API keys stored as SECRETS
- ✅ WEBUI_SECRET_KEY is random and strong
- ✅ Never commit secrets to Git

### 2. Enable Authentication

- ✅ `ENABLE_SIGNUP=true` - Users must sign up
- ✅ First user becomes admin
- ✅ Additional users need approval

### 3. HTTPS Only

- ✅ Automatic SSL via DigitalOcean
- ✅ All traffic encrypted
- ✅ Certificates auto-renewed

### 4. CORS Configuration

```yaml
CORS_ALLOW_ORIGIN: "*"  # Change to your domain for production
```

---

## 🚦 Next Steps

### 1. Set Up Custom Domain (Optional)

Want `friday.yourdomain.com` instead of DO subdomain?

1. In DO dashboard → App Settings → Domains
2. Add custom domain
3. Update DNS records at your registrar
4. SSL certificate auto-configured

### 2. Configure Webhooks

Set up notifications for events:
- New user signups
- System errors
- Deployment status

### 3. Scale Resources

If you need more power:
- Upgrade to Professional or higher
- Add more instances for load balancing

### 4. Set Up Monitoring

Integrate with:
- DigitalOcean Monitoring (built-in)
- External monitoring (UptimeRobot, Pingdom)
- Custom alerts via webhooks

---

## 📖 Additional Resources

- **DigitalOcean Docs**: https://docs.digitalocean.com/products/app-platform/
- **App Spec Reference**: https://docs.digitalocean.com/products/app-platform/reference/app-spec/
- **Pricing**: https://www.digitalocean.com/pricing/app-platform

---

## 🆘 Getting Help

### Check Logs First

```bash
# In DO dashboard:
# 1. Go to your app
# 2. Click "Runtime Logs"
# 3. Look for errors
```

### Common Log Messages

- ✅ `Application startup complete` - Working!
- ⚠️ `Downloading model...` - First start (wait 2-3 min)
- ❌ `WEBUI_SECRET_KEY not set` - Add secret key
- ❌ `Out of memory` - Upgrade instance size

---

**Congratulations! Friday is deployed on DigitalOcean! 🎉**

Access your app at: `https://friday-second-brain-xxxxx.ondigitalocean.app`
