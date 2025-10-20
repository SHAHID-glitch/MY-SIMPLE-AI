from api.index import app

# This file exists so Vercel detects a top-level Flask entrypoint named `index.py`
# Vercel will import `app` from this module as the WSGI app.

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
