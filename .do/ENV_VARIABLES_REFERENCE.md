# Environment Variables Reference - DigitalOcean Deployment

Complete list of environment variables configured in `.do/app.yaml`

## ✅ Configured in .do/app.yaml

### 🔐 Security & Authentication (7 variables)
| Variable | Value | Type | Description |
|----------|-------|------|-------------|
| `WEBUI_SECRET_KEY` | *(set in DO dashboard)* | SECRET | JWT & session encryption key |
| `WEBUI_AUTH` | `true` | Public | Enable authentication |
| `ENABLE_SIGNUP` | `true` | Public | Allow user signups |
| `DEFAULT_USER_ROLE` | `user` | Public | Default role for new users |
| `ENABLE_SIGNUP_PASSWORD_CONFIRMATION` | `false` | Public | Require password confirmation |
| `WEBUI_SESSION_COOKIE_SAME_SITE` | `lax` | Public | Cookie same-site policy |
| `WEBUI_SESSION_COOKIE_SECURE` | `true` | Public | Require HTTPS for cookies |

### 🤖 AI Provider APIs (8 variables)
| Variable | Value | Type | Description |
|----------|-------|------|-------------|
| `ENABLE_OLLAMA_API` | `false` | Public | Disable local Ollama |
| `ENABLE_OPENAI_API` | `true` | Public | Enable OpenAI integration |
| `OPENAI_API_KEY` | *(set in DO dashboard)* | SECRET | OpenAI API key |
| `OPENAI_API_BASE_URL` | `https://api.openai.com/v1` | Public | OpenAI endpoint |
| `ANTHROPIC_API_KEY` | *(set in DO dashboard)* | SECRET | Anthropic/Claude API key |
| `ANTHROPIC_API_BASE_URL` | *(empty - uses default)* | Public | Anthropic endpoint |
| `GOOGLE_API_KEY` | *(set in DO dashboard)* | SECRET | Google AI/Gemini API key |
| `OLLAMA_BASE_URL` | `/ollama` | Public | Ollama proxy path (disabled) |

### 📊 Database & Storage (2 variables)
| Variable | Value | Type | Description |
|----------|-------|------|-------------|
| `DATABASE_URL` | *(empty - uses default SQLite)* | Public | Database connection string |
| `DATA_DIR` | `/app/backend/data` | Public | Data directory path |

### 🔍 RAG (Document Search) Configuration (6 variables)
| Variable | Value | Type | Description |
|----------|-------|------|-------------|
| `RAG_EMBEDDING_MODEL` | `sentence-transformers/all-MiniLM-L6-v2` | Public | Embedding model for search |
| `RAG_TOP_K` | `5` | Public | Number of search results |
| `RAG_CHUNK_SIZE` | `1000` | Public | Document chunk size |
| `RAG_CHUNK_OVERLAP` | `200` | Public | Overlap between chunks |
| `ENABLE_RAG_HYBRID_SEARCH` | `false` | Public | Enable BM25 + vector search |
| `ENABLE_RAG_WEB_SEARCH` | `true` | Public | Enable web search in RAG |
| `RAG_WEB_SEARCH_ENGINE` | *(empty)* | Public | Web search provider |

### 🎤 Speech & Media (1 variable)
| Variable | Value | Type | Description |
|----------|-------|------|-------------|
| `WHISPER_MODEL` | `base` | Public | Speech-to-text model size |

### 🌐 Network & CORS (4 variables)
| Variable | Value | Type | Description |
|----------|-------|------|-------------|
| `PORT` | `8080` | Public | Application port |
| `CORS_ALLOW_ORIGIN` | `*` | Public | CORS allowed origins |
| `FORWARDED_ALLOW_IPS` | `*` | Public | Trusted proxy IPs |
| `ENABLE_WEBSOCKET_SUPPORT` | `true` | Public | Enable WebSocket |

### 📤 File Upload (1 variable)
| Variable | Value | Type | Description |
|----------|-------|------|-------------|
| `UPLOAD_FILE_SIZE_LIMIT` | `100` | Public | Max upload size in MB |

### 🎨 Application Settings (4 variables)
| Variable | Value | Type | Description |
|----------|-------|------|-------------|
| `WEBUI_NAME` | `Friday` | Public | Application name |
| `ENV` | `prod` | Public | Environment mode |
| `ENABLE_IMAGE_GENERATION` | `false` | Public | Disable image gen |
| `ENABLE_COMMUNITY_SHARING` | `false` | Public | Disable sharing |

### 🔕 Privacy & Telemetry (4 variables)
| Variable | Value | Type | Description |
|----------|-------|------|-------------|
| `SCARF_NO_ANALYTICS` | `true` | Public | Disable Scarf analytics |
| `DO_NOT_TRACK` | `true` | Public | Enable Do Not Track |
| `ANONYMIZED_TELEMETRY` | `false` | Public | Disable telemetry |
| `ENABLE_VERSION_UPDATE_CHECK` | `false` | Public | Disable update checks |

### 🚫 Disabled Features (2 variables)
| Variable | Value | Type | Description |
|----------|-------|------|-------------|
| `ENABLE_CHANNELS` | `false` | Public | Disable chat channels |
| `ENABLE_COMMUNITY_SHARING` | `false` | Public | Disable sharing |

### ⚙️ Performance & Caching (2 variables)
| Variable | Value | Type | Description |
|----------|-------|------|-------------|
| `MODELS_CACHE_TTL` | `1` | Public | Model cache TTL in seconds |
| `ENABLE_COMPRESSION_MIDDLEWARE` | `true` | Public | Enable gzip compression |

---

## 📝 Total: 41 Environment Variables Configured

### Secrets You Must Set in DigitalOcean Dashboard:
1. ✅ `WEBUI_SECRET_KEY` - Generate with `openssl rand -base64 32`
2. ✅ `OPENAI_API_KEY` - Your OpenAI API key
3. ✅ `ANTHROPIC_API_KEY` - Your Anthropic API key
4. ⚠️ `GOOGLE_API_KEY` - Optional, only if using Gemini

---

## ❌ NOT Included (By Design)

These are either auto-configured by the Dockerfile or not needed for DigitalOcean App Platform:

### Build-Time Only (Handled by Dockerfile)
- `NODE_OPTIONS` - Set in Dockerfile
- `APP_BUILD_HASH` - Auto-generated during build
- `DOCKER` - Auto-set to `true` in Dockerfile
- `USE_CUDA_DOCKER` - Not needed (CPU-only deployment)
- `USE_OLLAMA_DOCKER` - Not needed (API-only)
- `TIKTOKEN_ENCODING_NAME` - Default in Dockerfile
- `HF_HOME` - Default in Dockerfile
- `WEBUI_BUILD_VERSION` - Auto-set during build

### Advanced/Optional (Not Needed for Basic Deployment)
- `REDIS_URL` - Not using Redis
- `REDIS_CLUSTER` - Not using Redis
- `DATABASE_POOL_SIZE` - Using SQLite (not relevant)
- `DATABASE_POOL_MAX_OVERFLOW` - Using SQLite
- `UVICORN_WORKERS` - App Platform manages this
- `ENABLE_OTEL` - OpenTelemetry (advanced monitoring)
- `OTEL_*` - OpenTelemetry config (not needed)
- `SCIM_ENABLED` - Enterprise SCIM provisioning
- `LICENSE_KEY` - Not using enterprise features
- `SMTP_*` - Email configuration (optional)
- `OAUTH_*` - OAuth configuration (optional)
- `ENABLE_FORWARD_USER_INFO_HEADERS` - Reverse proxy headers (optional)
- `AUDIT_LOG_*` - Audit logging (optional)

### Development Only (Not for Production)
- `GLOBAL_LOG_LEVEL` - Use default
- `*_LOG_LEVEL` - Individual component log levels
- `ENABLE_REALTIME_CHAT_SAVE` - Development feature
- `RESET_CONFIG_ON_START` - Development feature
- `SAFE_MODE` - Troubleshooting mode

---

## 🔄 How to Update Environment Variables

### In DigitalOcean Dashboard:

1. Go to your app
2. Click **"Settings"** tab
3. Scroll to **"Environment Variables"**
4. Click **"Edit"**
5. Modify values
6. Click **"Save"**
7. App will automatically redeploy

### Common Updates:

**Add a new SECRET:**
```
Click "Add Variable"
Key: YOUR_API_KEY_NAME
Value: your-secret-value
☑️ Encrypt (mark as secret)
```

**Change a public value:**
```
Find the variable
Update the value
Click Save
```

---

## 📖 Reference

For complete documentation of all available environment variables, see:
- Backend config: `backend/friday/env.py`
- Production template: `.env.production.example`
- DigitalOcean config: `.do/app.yaml`

---

**Last Updated**: Based on codebase analysis
**Total Variables in .do/app.yaml**: 41
**Required Secrets**: 3-4 (WEBUI_SECRET_KEY, OPENAI_API_KEY, ANTHROPIC_API_KEY, optionally GOOGLE_API_KEY)
