# React Frontend for Groq AI Assistant

A modern React application built with Vite, TypeScript, Tailwind CSS, and Context API for state management.

## Features

✨ **Modern React Architecture**
- React 18 with TypeScript
- Vite for lightning-fast builds
- Context API for state management
- Custom hooks for logic separation

🎨 **Beautiful UI**
- Tailwind CSS for styling
- Dark mode support
- Responsive design
- Smooth animations
- Glassmorphism effects

💬 **Enhanced Chat Experience**
- Multi-conversation support
- Persistent chat history (localStorage)
- Real-time message status
- Copy message to clipboard
- AI response loading state
- Error handling

⚙️ **Features**
- Create/delete conversations
- Theme toggle (Light/Dark)
- Conversation statistics
- API status indicator
- Clear chat history
- Auto-saving conversations

## Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Environment Variables

Create a `.env.local` file in the `frontend` directory:

```env
VITE_API_BASE_URL=http://localhost:5000
```

### 3. Run Development Server

```bash
npm run dev
```

The app will be available at `http://localhost:3000`

### 4. Build for Production

```bash
npm run build
```

This creates a production build optimized for performance.

## Project Structure

```
frontend/
├── src/
│   ├── components/          # React components
│   │   ├── App.tsx         # Main app component
│   │   ├── Header.tsx      # Header with theme toggle
│   │   ├── Sidebar.tsx     # Chat list sidebar
│   │   ├── ChatArea.tsx    # Message display
│   │   ├── InputArea.tsx   # Message input
│   │   ├── Message.tsx     # Message bubble
│   │   └── Settings.tsx    # Settings modal
│   ├── context/
│   │   └── ChatContext.tsx # Global state management
│   ├── hooks/
│   │   └── useChat.ts      # Chat context hook
│   ├── services/
│   │   └── api.ts          # API client
│   ├── types/
│   │   └── index.ts        # TypeScript types
│   ├── main.tsx            # Entry point
│   └── index.css           # Global styles
├── vite.config.ts          # Vite configuration
├── tailwind.config.js      # Tailwind configuration
├── tsconfig.json           # TypeScript configuration
├── package.json            # Dependencies
└── index.html              # HTML template
```

## Technologies Used

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Axios** - HTTP client
- **Lucide React** - Icons

## Key Components

### ChatContext
Manages global state including:
- Conversations and messages
- Current conversation
- Loading and error states
- Theme preference
- API status

### Custom Hooks
- `useChat()` - Access chat context with error handling

### Components
- **Header** - Navigation and controls
- **Sidebar** - Conversation management
- **ChatArea** - Message display with auto-scroll
- **InputArea** - Message input with auto-resize
- **Message** - Individual message with copy feature
- **Settings** - App settings and statistics

## Features Detail

### LocalStorage Persistence
- Conversations automatically saved to browser storage
- Theme preference persisted
- Current conversation ID saved

### Error Handling
- API error messages displayed in chat
- Graceful degradation
- User-friendly error messages

### Performance
- Optimized re-renders with Context
- Lazy message scrolling
- Code splitting ready

## Development

Run the development server:
```bash
npm run dev
```

The app auto-refreshes on file changes thanks to Vite's HMR.

## Building

Create an optimized production build:
```bash
npm run build
```

outputs to `../static/dist/`
