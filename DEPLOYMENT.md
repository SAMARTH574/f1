# Deployment Guide

## GitHub Repository Setup

### Step 1: Create GitHub Repository
1. Go to [GitHub](https://github.com) and sign in
2. Click the "+" icon and select "New repository"
3. Name your repository (e.g., `financial-advisor-ai`)
4. Add description: "AI-powered financial planning application with calculators"
5. Make it public or private based on your preference
6. Check "Add a README file" (we'll replace it with our custom one)
7. Choose "MIT License"
8. Click "Create repository"

### Step 2: Upload Project Files
You have several options to upload your project:

#### Option A: Using GitHub Web Interface
1. Click "uploading an existing file" on your new repository page
2. Drag and drop all these files:
   - `app.py`
   - `chatbot.py`
   - `calculators.py`
   - `utils.py`
   - `README.md`
   - `project_requirements.txt` (rename to `requirements.txt`)
   - `LICENSE`
   - `.gitignore`
   - `.streamlit/config.toml`
   - `replit.md`

#### Option B: Using Git Commands (if you have Git installed)
```bash
git clone https://github.com/yourusername/financial-advisor-ai.git
cd financial-advisor-ai

# Copy all your project files to this directory
# Then:
git add .
git commit -m "Initial commit: Financial Advisor AI application"
git push origin main
```

## Deployment Options

### 1. Streamlit Cloud (Recommended - Free)
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Connect your repository
5. Set main file path: `app.py`
6. Add environment variable: `GEMINI_API_KEY` = your_api_key
7. Click "Deploy"

### 2. Replit (Current Platform)
- Your app is already running on Replit
- To share: Click "Share" button and copy the URL
- For custom domain: Use Replit's deployment features

### 3. Heroku
1. Create a `Procfile`:
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```
2. Create account on [Heroku](https://heroku.com)
3. Create new app and connect to GitHub repository
4. Add environment variable `GEMINI_API_KEY`
5. Deploy from GitHub

### 4. Railway
1. Go to [Railway](https://railway.app)
2. Connect GitHub repository
3. Add environment variable `GEMINI_API_KEY`
4. Railway will auto-detect Streamlit app
5. Deploy automatically

## Environment Variables Required

For any deployment platform, make sure to set:
- `GEMINI_API_KEY`: Your Google Gemini API key

## Post-Deployment Steps

1. Test all calculators with sample data
2. Verify AI chatbot is responding correctly
3. Check that all charts and visualizations load properly
4. Test on mobile devices for responsiveness
5. Share the URL with friends/colleagues for feedback

## Troubleshooting

### Common Issues:
- **API Key Error**: Ensure `GEMINI_API_KEY` is set correctly
- **Module Not Found**: Check `requirements.txt` has all dependencies
- **Port Issues**: Use platform-specific port configuration
- **Memory Errors**: Some free tiers have memory limits

### Getting Help:
- Check platform-specific documentation
- Review error logs in deployment dashboard
- Test locally first before deploying

## Maintenance

- Keep dependencies updated regularly
- Monitor API usage and costs
- Back up your code regularly
- Consider adding automated testing
- Monitor application performance and user feedback