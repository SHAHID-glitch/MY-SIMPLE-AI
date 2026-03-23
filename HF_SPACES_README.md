# 🧠 Gemini AI Assistant on Hugging Face Spaces

A stunning AI chat application with 3D UI effects powered by **Groq Llama 3.3 70B**

![Demo](https://img.shields.io/badge/Status-Live-green)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Framework-Flask%2BReact-brightgreen)

## 🚀 Features

- ✨ **3D Animated UI** - Modern glassmorphism design with smooth animations
- 🤖 **Google Gemini 2.5 Flash** - State-of-the-art AI model
- 💬 **Real-time Chat** - Fast and responsive conversations
- 📱 **Fully Responsive** - Works on all devices
- ⚡ **Optimized Performance** - React + Vite frontend

## 🔧 Configuration

### Required: Set Hugging Face Secrets

Add your **Groq API key** to Hugging Face Spaces secrets:

1. Go to your Space settings
2. Click **"Repository secrets"**
3. Add:
   - **Name**: `GROQ_API_KEY`
   - **Value**: Your Groq API key
   
   Get your API key: https://console.groq.com/keys

## 📁 Deployment Structure

```
frontend/          # React + Vite frontend (built to static/dist)
static/dist/       # Built React frontend (production build)
templates/         # Flask templates
app.py             # Main Flask application
requirements_hf.txt # Python dependencies
```

## 🌐 Accessing Your App

Once deployed on Hugging Face Spaces, your app will be available at:
`https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME`

## 💡 How It Works

1. **Frontend**: React SPA served from `static/dist`
2. **Backend**: Flask API at `/api/chat`
3. **AI Engine**: Groq Llama 3.3 70B

## 🔗 Links

- [Hugging Face Spaces](https://huggingface.co/spaces)
- [Google Generative AI](https://ai.google.dev/)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

**Made with ❤️ for AI enthusiasts**
