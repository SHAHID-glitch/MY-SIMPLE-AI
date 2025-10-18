# ⚠️ IMPORTANT: HOW TO RUN YOUR APP CORRECTLY

## ❌ WRONG WAY (What you're doing now):
- Opening files directly in browser
- Using Live Server on port 5500
- Getting JavaScript errors

## ✅ CORRECT WAY:

### Step 1: Make sure Flask server is running
Open terminal and run:
```bash
python Backend.py
```

You should see:
```
INFO:__main__:Gemini API configured successfully
 * Running on http://127.0.0.1:5000
```

### Step 2: Open the CORRECT URL in your browser
```
http://127.0.0.1:5000
```

⚠️ NOT http://127.0.0.1:5500 (that's Live Server, wrong!)
✅ USE http://127.0.0.1:5000 (Flask server, correct!)

### Step 3: Test the app
- You should see "🟢 API Connected" 
- Type a message and press Enter
- AI should respond

---

## Why Port 5000?

Your Flask app runs on port **5000**
The files only work through Flask because they use:
- `{{ url_for('static', filename='...') }}` (Flask template syntax)
- Flask routes (`/api/chat`, `/api/status`)
- Backend Python code

---

## Quick Fix Right Now:

1. **Close** the port 5500 tab
2. **Stop** Live Server if running
3. **Make sure** `python Backend.py` is running
4. **Open** http://127.0.0.1:5000

That's it! 🚀
