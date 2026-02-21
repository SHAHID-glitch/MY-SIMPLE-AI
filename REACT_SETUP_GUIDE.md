# React Frontend Setup Guide

## Overview

This guide walks you through setting up the new React frontend for the Groq AI Assistant application.

## Prerequisites

- **Node.js 16+** - [Download here](https://nodejs.org)
- **npm 8+** - Comes with Node.js
- **Python 3.8+** - For the backend (Flask)
- **Groq API Key** - [Get one here](https://console.groq.com)

## Installation Steps

### 1. Backend Setup (if not already done)

```bash
# In the root directory
pip install -r requirements.txt
```

Create a `.env` file in the root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Start the backend:

```bash
python Backend.py
```

The backend will run on `http://localhost:5000`

### 2. Frontend Setup

Navigate to the frontend directory:

```bash
cd frontend
```

#### Option A: Using npm

Install dependencies:

```bash
npm install
```

Create `.env.local` (optional, defaults to localhost:5000):

```bash
cp .env.example .env.local
```

Start the development server:

```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

#### Option B: Using yarn (if you prefer)

```bash
yarn install
yarn dev
```

#### Option C: Using pnpm

```bash
pnpm install
pnpm dev
```

## Vite Development Server

The Vite development server includes:

- ✅ **Hot Module Replacement (HMR)** - Changes reflect instantly
- ✅ **API Proxy** - Automatically forwards `/api/*` requests to backend
- ✅ **TypeScript Support** - Full type checking
- ✅ **Fast Refresh** - Near-instant file updates

### Running Different Environments

**Development** (with HMR):
```bash
npm run dev
```

**Production Build**:
```bash
npm run build
```

**Preview Production Build**:
```bash
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── App.tsx              # Main component
│   │   ├── Header.tsx           # Navigation header
│   │   ├── Sidebar.tsx          # Conversation list
│   │   ├── ChatArea.tsx         # Message display
│   │   ├── InputArea.tsx        # Message input
│   │   ├── Message.tsx          # Message bubble
│   │   └── Settings.tsx         # Settings modal
│   ├── context/
│   │   └── ChatContext.tsx      # Global state
│   ├── hooks/
│   │   └── useChat.ts           # Context hook
│   ├── services/
│   │   └── api.ts               # API client
│   ├── types/
│   │   └── index.ts             # TypeScript types
│   ├── main.tsx                 # Entry point
│   └── index.css                # Global styles
├── public/                       # Static assets
├── vite.config.ts               # Vite configuration
├── tsconfig.json                # TypeScript config
├── tailwind.config.js           # Tailwind CSS config
├── postcss.config.js            # PostCSS config
├── index.html                   # HTML template
└── package.json                 # Dependencies
```

## Key Features

### 🎨 Modern UI

- Built with **Tailwind CSS** for beautiful styling
- **Dark mode support** with theme toggle
- **Responsive design** for all devices
- **Smooth animations** and transitions
- **Glassmorphism effects** in header

### 💬 Chat Management

- Create multiple conversations
- Delete conversations with confirmation
- Auto-title generation from first message
- Message timestamps
- Copy message to clipboard

### 🔄 State Management

- **Context API** for global state
- **LocalStorage** for persistence
- All conversations saved locally
- Theme preference saved
- Current conversation ID tracked

### ⚡ Performance

- Code splitting ready
- Optimized bundle size
- Fast HMR during development
- Lazy component loading

### 🛡️ Error Handling

- API error messages displayed in chat
- User-friendly error notifications
- Graceful fallbacks
- Request timeout handling

## Environment Variables

### Development (.env.local)

```env
VITE_API_BASE_URL=http://localhost:5000
```

### Building for Production

The build process outputs to `../static/dist/`

Configure your production API URL before building:

```bash
# Edit .env.local or use environment variable
VITE_API_BASE_URL=https://your-production-url.com npm run build
```

## Available Scripts

```bash
# Start development server with HMR
npm run dev

# Build optimized production bundle
npm run build

# Preview production build locally
npm run preview

# Run linting (if configured)
npm run lint
```

## Troubleshooting

### Issue: "Cannot find module 'react'"

**Solution:** Run `npm install` to install dependencies

```bash
npm install
```

### Issue: "API_BASE_URL not working"

**Solution:** Check that the backend is running on the correct port:

```bash
# Check backend
curl http://localhost:5000/api/status
```

### Issue: "Port 3000 already in use"

**Solution:** Kill the process or use a different port:

```bash
# Use different port
npm run dev -- --port 3001
```

### Issue: CORS errors

**Solution:** Ensure backend has CORS enabled. The Flask app should have:

```python
from flask_cors import CORS
CORS(app)
```

### Issue: localStorage not persisting

**Solution:** Check browser privacy settings aren't blocking storage

## Browser Support

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

## Performance Tips

1. **Use React DevTools** - Install React DevTools extension to profile components
2. **Check Network Tab** - Monitor API calls in browser DevTools
3. **Enable dark mode** - Slightly better battery life on OLED displays
4. **Clear cache** - If experiencing stale data issues

## Production Deployment

### Building

```bash
npm run build
```

This creates an optimized build in `dist/`

### Serving

The built files can be served by:
- **Flask** - Configure to serve from `templates/` or  `static/dist/`
- **Nginx/Apache** - Configure as static site
- **Vercel/Netlify** - Use built-in deployment
- **Docker** - Create a container with Node.js

### Example Flask Configuration

```python
@app.route('/')
def index():
    return send_file('static/dist/index.html')

@app.route('/<path:path>')
def send_static(path):
    try:
        return send_file(f'static/dist/{path}')
    except:
        return send_file('static/dist/index.html')
```

## Development Workflow

1. **Start Backend**: `python Backend.py` (terminal 1)
2. **Start Frontend**: `npm run dev` (terminal 2)
3. **Edit Code**: Changes auto-reload with HMR
4. **Test Changes**: Open `http://localhost:3000`
5. **Build**: `npm run build` when ready for production

## Next Steps

- Explore component architecture in `src/components/`
- Review state management in `src/context/`
- Customize colors in `tailwind.config.js`
- Add new API endpoints as needed

## Support

For issues or questions:
1. Check error messages in console (F12)
2. Review browser console for CORS errors
3. Ensure backend is running: `curl http://localhost:5000/api/status`
4. Check `.env.local` configuration
