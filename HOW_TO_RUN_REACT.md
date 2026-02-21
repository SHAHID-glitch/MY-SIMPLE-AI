# How to Run the React-Enhanced Application

## Quick Start (30 seconds)

### Prerequisites
- Node.js 16+ installed
- Python 3.8+ installed
- Groq API key (get one at https://console.groq.com)

### Step 1: Create .env file
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### Step 2: Install Dependencies
```bash
# Install backend dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd frontend && npm install
```

### Step 3: Run Both Services

**Option A: Two Terminals (Recommended)**

Terminal 1 - Backend:
```bash
python Backend.py
```

Terminal 2 - Frontend:
```bash
cd frontend && npm run dev
```

**Option B: One Terminal with Background Process**
```bash
python Backend.py &
sleep 2
cd frontend && npm run dev
```

### Step 4: Open Browser
- **Frontend (React App)**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **API Status**: http://localhost:5000/api/status

## Detailed Setup Guide

### Backend Setup

**Install Python dependencies:**
```bash
pip install -r requirements.txt
```

**Required packages:**
- Flask - Web framework
- flask-cors - Cross-origin support
- groq - Groq API client
- python-dotenv - Environment variables

**Environment Configuration:**

Create `.env` in root:
```env
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxx
```

Get your API key from: https://console.groq.com/keys

**Start Backend:**
```bash
python Backend.py
```

Expected output:
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

### Frontend Setup

**Install Node dependencies:**
```bash
cd frontend
npm install
```

This installs:
- React 18
- Vite
- TypeScript
- Tailwind CSS
- Axios
- Lucide React

**Environment Configuration (Optional):**

Create `frontend/.env.local` (defaults to localhost:5000):
```env
VITE_API_BASE_URL=http://localhost:5000
```

**Start Development Server:**
```bash
npm run dev
```

Expected output:
```
  ➜  Local:   http://localhost:3000/
  ➜  press h to show help
```

## Development Workflow

### 1. Hot Module Replacement (HMR)
React app auto-refreshes when you edit files. No manual refresh needed!

### 2. Backend Restart
If you modify Backend.py:
```bash
# Stop the server (Ctrl+C)
# Restart with:
python Backend.py
```

### 3. Debugging
- **Frontend**: Open DevTools (F12) → Console/Network tabs
- **Backend**: Check terminal output for logs
- **API**: Test endpoints at http://localhost:5000/api/status

## What Each Component Does

### Backend (Flask)
- **POST /api/chat** - Sends message to Groq API
- **GET /api/status** - Returns API connection status
- **GET /api/models** - Lists available models
- **POST /api/reset** - Clears conversation

### Frontend (React + Vite)
- **Port 3000** - React development server with HMR
- **Vite Dev Server** - Handles module bundling and loading
- **API Proxy** - Redirects /api/* calls to http://localhost:5000

## Testing the Setup

### 1. Verify Backend is Running
```bash
curl http://localhost:5000/api/status
```

Should return:
```json
{
  "success": true,
  "groq_configured": true,
  "service": "Groq",
  "timestamp": 1234567890
}
```

### 2. Verify Frontend is Running
Open browser to http://localhost:3000
You should see:
- Header with "Groq AI Assistant" title
- Sidebar with "New Chat" button
- Main chat area
- Input box at bottom

### 3. Test Chat
1. Type a message in the input box
2. Click Send or press Enter
3. Wait for AI response
4. See message appear in chat

## Troubleshooting

### Issue: Backend fails to start
**Error**: `Address already in use`
**Solution**: Kill existing process
```bash
lsof -i :5000
kill -9 <PID>
```

### Issue: Frontend fails to start
**Error**: `Port 3000 already in use`
**Solution**: Use different port
```bash
npm run dev -- --port 3001
```

### Issue: Cannot connect to API
**Error**: CORS error or 404
**Solutions**:
1. Verify backend is running: `curl http://localhost:5000/api/status`
2. Check .env.local has correct API_BASE_URL
3. Restart both servers

### Issue: "Module not found"
**Error**: `Cannot find module 'react'`
**Solution**: Install dependencies
```bash
cd frontend && npm install
```

### Issue: "API key not configured"
**Error**: Appears in chat
**Solutions**:
1. Create .env file with GROQ_API_KEY
2. Restart backend
3. Verify key is valid at https://console.groq.com

### Issue: Styling looks broken
**Solutions**:
1. Clear browser cache (Ctrl+Shift+Delete)
2. Restart dev server (Ctrl+C, then npm run dev)
3. Check CSS file sizes loaded in DevTools

## Production Build

### Build Frontend
```bash
cd frontend
npm run build
```

Creates optimized bundle in `static/dist/`:
- `assets/index-*.js` - JavaScript bundle (65KB gzipped)
- `assets/index-*.css` - CSS bundle (3.7KB gzipped)
- `index.html` - HTML template

### Serve with Flask
Backend can serve the built files:

```python
from flask import send_file

@app.route('/')
def index():
    return send_file('static/dist/index.html')

@app.route('/<path:path>')
def static_files(path):
    try:
        return send_file(f'static/dist/{path}')
    except:
        return send_file('static/dist/index.html')
```

## Environment Variables Reference

### Backend (.env)
```env
GROQ_API_KEY=              # Required: Your Groq API key
FLASK_ENV=development      # Optional: development or production
DEBUG=True                 # Optional: Enable debug mode
```

### Frontend (.env.local)  
```env
VITE_API_BASE_URL=         # Optional: Backend URL (defaults to http://localhost:5000)
```

## File Structure After Setup

```
MY-SIMPLE-AI/
├── Backend.py                    # Flask server
├── requirements.txt              # Python dependencies
├── .env                         # Environment variables
├── frontend/                    # React + Vite app
│   ├── node_modules/           # Dependencies (npm install)
│   ├── src/                     # React source code
│   ├── dist/                    # Built files (npm run build)
│   ├── package.json             # Frontend dependencies
│   └── ...
├── static/
│   └── dist/                    # Production build output
├── templates/                   # HTML templates
└── ...
```

## Next Steps

1. ✅ **Get API Key** - Visit https://console.groq.com
2. ✅ **Create .env** - Add your Groq API key
3. ✅ **Install Dependencies** - Run `pip install -r requirements.txt` and `cd frontend && npm install`
4. ✅ **Start Servers** - `python Backend.py` and `cd frontend && npm run dev`
5. ✅ **Open Browser** - Go to http://localhost:3000
6. ✅ **Start Chatting** - Type a message and enjoy!

## Additional Resources

- [REACT_ENHANCEMENT_SUMMARY.md](REACT_ENHANCEMENT_SUMMARY.md) - What's new in React version
- [REACT_SETUP_GUIDE.md](REACT_SETUP_GUIDE.md) - Detailed React setup
- [frontend/README.md](frontend/README.md) - Frontend documentation
- [Groq API Docs](https://console.groq.com/docs)
- [React Docs](https://react.dev)
- [Vite Docs](https://vitejs.dev)

## Support

### Check Logs
```bash
# Backend logs (in terminal window)
# Frontend logs (in browser DevTools - F12)
# DevTools Network tab - check API calls
```

### Test API Endpoint
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
```

## Tips & Tricks

- **Dark Mode**: Click moon icon in header
- **New Chat**: Click "New Chat" button in sidebar
- **Copy Message**: Hover over AI message and click copy icon
- **Clear History**: Click trash icon in header
- **View Settings**: Click gear icon in header

## Performance Tips

- Use dark mode for slightly faster rendering
- Close unused tabs/extensions
- Keep browser DevTools closed when not debugging
- Clear browser cache periodically

---

**Ready to chat with AI?** Start the servers and enjoy! 🚀
