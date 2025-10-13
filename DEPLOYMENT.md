# 🚀 BuyBlack City Guide - Deployment Guide

## Quick Start Options

### 1. 🌐 **Local Web Interface** (Easiest)
```bash
# Install Gradio (if not already installed)
pip install gradio

# Run the web interface
python web_app.py
```
- Opens at: http://localhost:7860
- Perfect for testing and local use
- No external dependencies

### 2. 🐳 **Docker Deployment** (Recommended for Production)
```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build manually
docker build -t buyblack-city-guide .
docker run -p 7860:7860 -e OPENAI_API_KEY=your_key -e GOOGLE_PLACES_API_KEY=your_key buyblack-city-guide
```

### 3. ☁️ **Railway Deployment** (Cloud Platform)
1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```

2. **Deploy:**
   ```bash
   railway login
   railway init
   railway up
   ```

3. **Set Environment Variables:**
   ```bash
   railway variables set OPENAI_API_KEY=your_openai_key
   railway variables set GOOGLE_PLACES_API_KEY=your_google_key
   ```

### 4. 🌊 **Streamlit Alternative** (If you prefer Streamlit)
```bash
pip install streamlit
streamlit run streamlit_app.py
```

### 5. 🔧 **Custom Server Deployment**
```bash
# Using Gunicorn (production WSGI server)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:7860 web_app:app
```

## Environment Variables Required

Create a `.env` file or set these environment variables:

```env
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_PLACES_API_KEY=your_google_places_api_key_here
```

## Platform-Specific Instructions

### Railway.app
- **File:** `deploy_railway.py` (ready to use)
- **Config:** `railway.json` (deployment settings)
- **Cost:** Free tier available, then pay-as-you-go

### Heroku
- **File:** `Procfile` (create this):
  ```
  web: python web_app.py
  ```
- **Requirements:** `requirements_deploy.txt`

### Google Cloud Run
- **File:** `Dockerfile` (already configured)
- **Deploy:** `gcloud run deploy --source .`

### AWS EC2/ECS
- **File:** `Dockerfile` + `docker-compose.yml`
- **Deploy:** Use AWS CLI or console

### DigitalOcean App Platform
- **File:** `Dockerfile` (ready to use)
- **Deploy:** Connect GitHub repo to DigitalOcean

## Performance Considerations

### For Production:
1. **Use Gunicorn** instead of Gradio's built-in server
2. **Add caching** for Google Places API calls
3. **Implement rate limiting** to prevent API abuse
4. **Add monitoring** (logging, health checks)
5. **Use a database** for storing user interactions (optional)

### Scaling:
- **Horizontal:** Run multiple instances behind a load balancer
- **Vertical:** Increase server resources
- **Caching:** Redis for API response caching
- **CDN:** For static assets

## Security Considerations

1. **API Keys:** Never commit to version control
2. **Rate Limiting:** Implement to prevent abuse
3. **Input Validation:** Sanitize user inputs
4. **HTTPS:** Always use SSL in production
5. **CORS:** Configure for your domain

## Monitoring & Maintenance

### Health Checks:
- **Endpoint:** `/health` (add to web_app.py)
- **Monitoring:** Uptime monitoring services
- **Logs:** Structured logging with timestamps

### Updates:
- **Code:** Regular updates for security
- **Data:** Update CSV files with new businesses
- **APIs:** Monitor API rate limits and costs

## Cost Estimation

### API Costs (Monthly):
- **OpenAI:** ~$20-100 (depending on usage)
- **Google Places:** ~$10-50 (depending on searches)
- **Hosting:** $5-50 (depending on platform and traffic)

### Free Tiers:
- **Railway:** 500 hours/month free
- **Heroku:** 550-1000 hours/month free
- **Google Cloud:** $300 credit for new users

## Troubleshooting

### Common Issues:
1. **Port conflicts:** Change port in `web_app.py`
2. **API limits:** Check your API quotas
3. **Memory issues:** Increase server resources
4. **Slow responses:** Add caching or optimize queries

### Debug Mode:
```python
# In web_app.py, change:
demo.launch(debug=True)
```

## Next Steps

1. **Choose your deployment method**
2. **Set up environment variables**
3. **Test locally first**
4. **Deploy to your chosen platform**
5. **Monitor and optimize**

Need help? Check the logs and ensure all API keys are properly set!

