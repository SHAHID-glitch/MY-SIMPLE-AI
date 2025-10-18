# Quick Guide: Enable GitHub Pages

## 📋 Steps to Enable GitHub Pages

1. **Go to Your Repository**
   - Navigate to: https://github.com/SHAHID-glitch/MY-SIMPLE-AI

2. **Open Settings**
   - Click the **Settings** tab (⚙️ icon)
   - Scroll down to find "Pages" in the left sidebar

3. **Configure Pages**
   - Under **"Build and deployment"**
   - **Source**: Select "Deploy from a branch"
   - **Branch**: Select `main` (or your default branch)
   - **Folder**: Select `/ (root)`
   - Click **Save**

4. **Wait for Deployment**
   - GitHub will start building your site
   - This takes 1-2 minutes
   - Check the **Actions** tab to see deployment progress

5. **Access Your Site**
   - Once deployed, your site will be at:
   ```
   https://shahid-glitch.github.io/MY-SIMPLE-AI/
   ```
   - The URL will also appear in Settings → Pages

## ✅ What You'll See

The GitHub Pages site will display a professional landing page that:
- Explains this is a Flask backend application
- Shows setup instructions for running locally
- Lists alternative deployment platforms
- Provides links to the repository

## ⚠️ Important Notes

- **Backend functionality won't work** on GitHub Pages
- GitHub Pages only serves static HTML/CSS/JS
- The AI chat requires a Python Flask server
- For full functionality, deploy to Railway, Render, or similar platforms

## 🚀 For Full App Deployment

Use one of these platforms instead:
- **Railway.app** - Free tier, easy Python deployment
- **Render.com** - Free web services for Flask apps
- **Vercel** - Serverless Python functions
- **Heroku** - Classic platform (requires credit card)

## 🔧 Troubleshooting

### Site not loading?
- Wait 2-3 minutes after enabling
- Check Actions tab for build errors
- Clear browser cache and try again

### Still showing 404?
- Verify `index.html` exists in root (lowercase)
- Check branch name matches what you selected
- Make sure the branch has been pushed

### Want to disable?
- Settings → Pages
- Under Source, select "None"
- Click Save

---

**Last Updated:** October 18, 2025
