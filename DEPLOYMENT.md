# 🚀 Deployment Guide

Complete guide for deploying the Agentic AI Research Assistant.

## 🐳 Docker Deployment (Recommended)

### Prerequisites
- Docker & Docker Compose installed
- OpenAI API key
- Tavily API key

### Steps

1. **Clone the repository**
```bash
git clone <repo-url>
cd agentic-ai-research-assistant
```

2. **Create environment file**
```bash
cp backend/.env.example .env
```

Edit `.env`:
```env
OPENAI_API_KEY=sk-your-key
TAVILY_API_KEY=tvly-your-key
```

3. **Start all services**
```bash
docker-compose up -d
```

4. **Access the application**
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- Weaviate: `http://localhost:8080`

5. **View logs**
```bash
docker-compose logs -f
```

6. **Stop services**
```bash
docker-compose down
```

## ☁️ Cloud Deployment

### Deploy to Heroku

#### Backend

```bash
cd backend
heroku create your-app-backend
heroku config:set OPENAI_API_KEY=your-key
heroku config:set TAVILY_API_KEY=your-key
heroku config:set WEAVIATE_URL=your-weaviate-cloud-url
git push heroku main
```

#### Frontend

```bash
cd frontend
npm run build
# Deploy dist/ folder to your static hosting service
```

### Deploy to AWS

#### Backend (EC2)

1. Launch EC2 instance (t2.medium recommended)
2. Install Python 3.9+
3. Clone repository
4. Set environment variables
5. Install dependencies
6. Run with systemd or supervisor

#### Frontend (S3 + CloudFront)

1. Build frontend: `npm run build`
2. Upload `dist/` to S3 bucket
3. Configure CloudFront distribution
4. Update API URL in environment

### Deploy to DigitalOcean

#### App Platform

1. Connect GitHub repository
2. Configure components:
   - Backend: Python app on port 8000
   - Frontend: Static site from `frontend/dist`
3. Set environment variables
4. Deploy

#### Droplets

1. Create Ubuntu droplet
2. Install Docker
3. Clone repository
4. Run docker-compose
5. Configure firewall (ports 3000, 8000, 8080)

### Deploy to Vercel (Frontend) + Railway (Backend)

#### Vercel (Frontend)

```bash
cd frontend
vercel --prod
```

Configure:
- Build: `npm run build`
- Output: `dist`
- Environment: `VITE_API_URL`

#### Railway (Backend)

1. Connect GitHub repo
2. Select `backend` directory
3. Add environment variables
4. Deploy

## 🗄️ Weaviate Deployment

### Weaviate Cloud Services (Recommended)

1. Sign up at [Weaviate Cloud](https://console.weaviate.cloud)
2. Create cluster
3. Copy cluster URL
4. Update `WEAVIATE_URL` in environment

### Self-Hosted Weaviate

#### Docker
```bash
docker run -d \
  -p 8080:8080 \
  -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \
  -e PERSISTENCE_DATA_PATH=/var/lib/weaviate \
  -e ENABLE_MODULES=text2vec-openai \
  -e OPENAI_APIKEY=your-key \
  semitechnologies/weaviate:latest
```

#### Kubernetes
```bash
helm repo add weaviate https://weaviate.github.io/weaviate-helm
helm install weaviate weaviate/weaviate
```

## 🔒 Security Checklist

- [ ] Use environment variables for all secrets
- [ ] Enable HTTPS/SSL certificates
- [ ] Configure CORS for production domains
- [ ] Set up rate limiting
- [ ] Enable authentication if needed
- [ ] Regular security updates
- [ ] Monitor API usage and costs
- [ ] Backup Weaviate data

## 📊 Monitoring

### Logs

**Backend:**
```bash
docker-compose logs -f backend
```

**Frontend:**
```bash
docker-compose logs -f frontend
```

### Health Checks

```bash
# Backend health
curl http://localhost:8000/health

# Weaviate health
curl http://localhost:8080/v1/.well-known/ready
```

### Metrics

Consider adding:
- Application Performance Monitoring (APM)
- Error tracking (Sentry)
- Analytics (Plausible, Google Analytics)
- Uptime monitoring (UptimeRobot)

## 🔧 Production Configuration

### Backend Environment

```env
# Production settings
OPENAI_API_KEY=sk-prod-key
TAVILY_API_KEY=tvly-prod-key
WEAVIATE_URL=https://your-cluster.weaviate.network
WEAVIATE_API_KEY=your-api-key

# Optional: Rate limiting
RATE_LIMIT_PER_MINUTE=60

# Optional: Logging
LOG_LEVEL=INFO
```

### Frontend Environment

```env
VITE_API_URL=https://api.yourdomain.com
```

### Nginx Configuration

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        
        # SSE support
        proxy_set_header Connection '';
        proxy_http_version 1.1;
        chunked_transfer_encoding off;
        proxy_buffering off;
        proxy_cache off;
    }
}
```

## 🚦 Scaling

### Horizontal Scaling

1. **Load Balancer**: Distribute traffic across multiple backend instances
2. **Stateless Backend**: All state in Weaviate, not in memory
3. **Cache Layer**: Redis for frequently accessed data
4. **CDN**: CloudFront/Cloudflare for frontend

### Vertical Scaling

- Backend: 2-4 CPU cores, 4-8GB RAM
- Weaviate: 4-8 CPU cores, 16-32GB RAM
- Frontend: CDN + static hosting

### Cost Optimization

- Use API rate limiting
- Cache responses where possible
- Monitor OpenAI token usage
- Use smaller models for simple tasks
- Implement request queuing

## 🐛 Troubleshooting

### Common Issues

**CORS errors:**
- Update CORS settings in `backend/main.py`
- Set allowed origins in production

**SSE not working:**
- Check proxy configuration
- Verify nginx/load balancer settings
- Ensure no response buffering

**High API costs:**
- Implement caching
- Add rate limiting
- Monitor usage in OpenAI dashboard

**Weaviate connection fails:**
- Check network connectivity
- Verify API key if using cloud
- Check firewall rules

## 📈 Performance Tips

1. **Enable compression** (gzip)
2. **Use CDN** for static assets
3. **Implement caching** for common queries
4. **Database indexing** in Weaviate
5. **Connection pooling** for API clients
6. **Async operations** where possible

## 🔄 CI/CD

### GitHub Actions Example

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build and test
        run: |
          cd backend
          pip install -r requirements.txt
          # Run tests
          
      - name: Deploy to production
        run: |
          # Your deployment script
```

## 📝 Maintenance

- **Regular updates**: Keep dependencies current
- **Backup data**: Schedule Weaviate backups
- **Monitor costs**: Track API usage
- **Security patches**: Apply updates promptly
- **Performance monitoring**: Review metrics weekly

## 🆘 Support

For deployment issues:
1. Check logs first
2. Review documentation
3. Open GitHub issue
4. Contact support

---

**Happy Deploying! 🚀**

