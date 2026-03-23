---
title: MY SIMPLE AI
emoji: 🤖
colorFrom: indigo
colorTo: blue
sdk: docker
pinned: false
---

# Gemini AI Assistant - 3D Experience 🧠✨

A beautiful, modern AI chat application powered by Google Gemini 2.5 Flash with stunning 3D UI effects, glassmorphism design, and smooth animations.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

- 🎨 **3D Animated UI** - Floating particles, rotating logo, animated letters
- 🪟 **Glassmorphism Design** - Modern frosted glass effects with depth
- 🤖 **Google Gemini 2.5 Flash** - Powered by the latest AI model
- 💬 **Real-time Chat** - Fast and responsive AI conversations
- 📱 **Fully Responsive** - Works on desktop, tablet, and mobile
- 🎭 **Avatar-based Messages** - Visual distinction between user and AI
- ⚡ **Smooth Animations** - Beautiful transitions and hover effects
- 🔄 **Session Management** - Maintains conversation history
- 🎯 **Auto-resize Input** - Smart textarea that grows with content

## 🎬 Demo

### 3D Effects
- Floating animated background spheres
- 3D rotating logo (brain/sparkle flip)
- Individual letter animations in title
- Particle system with 50+ floating elements
- Hover effects on avatars and buttons

### Chat Features
- Conversation history support
- Typing indicators
- Message timestamps
- Smooth scrolling
- Error handling with user-friendly messages

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/SHAHID-glitch/MY-SIMPLE-AI.git
   cd MY-SIMPLE-AI
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   GOOGLE_API_KEY=your_api_key_here
   ```

4. **Run the application**
   ```bash
   python Backend.py
   ```

5. **Open your browser**
   
   Navigate to: `http://127.0.0.1:5000`

## 📁 Project Structure

```
MY-SIMPLE-AI/
├── Backend.py              # Flask server with Gemini API integration
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
├── .gitignore             # Git ignore rules
├── README.md              # This file
├── templates/
│   └── index.html         # Main HTML with 3D structure
└── static/
    ├── gemini-style.css   # 3D UI styles with animations
    └── gemini-app.js      # Chat functionality and interactions
```

## 🎨 UI Components

### 3D Background
- **Floating Spheres**: Three animated gradient spheres
- **Particles**: 50 floating particles with random animations
- **Blur Effects**: Dynamic background blur for depth

### Header
- **3D Logo**: Rotating cube with emoji faces
- **Animated Title**: Each letter floats independently
- **Status Indicator**: Real-time API connection status

### Chat Interface
- **Glassmorphism Panels**: Frosted glass effect
- **Avatar System**: User (👤) and AI (🤖) avatars
- **Message Bubbles**: Gradient backgrounds with hover effects
- **Custom Scrollbar**: Styled scrollbar matching theme

### Input Area
- **Glow Effects**: Border glows on focus
- **Auto-resize**: Textarea expands with content
- **3D Button**: Rotating send button with hover animation
- **Keyboard Shortcuts**: Enter to send, Shift+Enter for new line

## 🛠️ Technologies Used

### Backend
- **Flask 2.3.3** - Web framework
- **google-generativeai** - Gemini API client
- **Flask-CORS** - Cross-origin resource sharing
- **python-dotenv** - Environment variable management

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Advanced animations and effects
  - CSS Variables for theming
  - Keyframe animations
  - Transform and perspective 3D
  - Backdrop-filter for glassmorphism
- **Vanilla JavaScript** - No frameworks needed
  - ES6+ syntax
  - Async/await for API calls
  - DOM manipulation

## 🎯 API Endpoints

- `GET /` - Main application page
- `POST /api/chat` - Send message to AI
- `GET /api/status` - Check API health
- `GET /api/models` - List available models
- `POST /api/reset` - Reset conversation session

## 🔧 Configuration

### Gemini Model Settings
Edit `Backend.py` to customize:
```python
generation_config=genai.types.GenerationConfig(
    temperature=0.9,      # Creativity (0.0-1.0)
    top_p=0.95,          # Nucleus sampling
    top_k=64,            # Top-k sampling
    max_output_tokens=2048  # Response length
)
```

### Session Management
- History limit: 12 conversation turns
- Session stored in-memory (non-persistent)
- Cookie-based session tracking

## 📱 Responsive Breakpoints

- **Desktop**: 1200px+ (full 3D effects)
- **Tablet**: 768px-1199px (optimized layout)
- **Mobile**: <768px (simplified animations)

## 🎨 Color Scheme

```css
--primary: #4285f4        /* Google Blue */
--secondary: #34a853      /* Google Green */
--accent: #fbbc04         /* Google Yellow */
--danger: #ea4335         /* Google Red */
```

## 🐛 Troubleshooting

### API Key Issues
- Ensure `.env` file exists with `GOOGLE_API_KEY`
- Verify API key is active in Google AI Studio
- Check API quota limits

### Port Already in Use
```bash
# Change port in Backend.py
app.run(debug=True, port=5001, host='0.0.0.0')
```

### CSS Not Loading
- Hard refresh browser: `Ctrl + Shift + R` (Windows) or `Cmd + Shift + R` (Mac)
- Clear browser cache
- Check browser console for errors

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**SHAHID**
- GitHub: [@SHAHID-glitch](https://github.com/SHAHID-glitch)
- Repository: [MY-SIMPLE-AI](https://github.com/SHAHID-glitch/MY-SIMPLE-AI)

## 🌟 Acknowledgments

- Google Gemini API for AI capabilities
- Flask framework for backend simplicity
- Modern CSS techniques for stunning UI

## 📸 Screenshots

### Desktop View
Beautiful 3D interface with floating particles and glassmorphism effects.

### Mobile View
Fully responsive design optimized for mobile devices.

## 🔮 Future Enhancements

- [ ] Persistent conversation history (database)
- [ ] User authentication system
- [ ] Theme customization
- [ ] Voice input/output
- [ ] Multi-language support
- [ ] Code syntax highlighting
- [ ] File upload support
- [ ] Export chat history

## 🆘 Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/SHAHID-glitch/MY-SIMPLE-AI/issues) page
2. Create a new issue with detailed description
3. Include error messages and screenshots if applicable

---

⭐ **Star this repository** if you found it helpful!

Made with ❤️ by SHAHID
