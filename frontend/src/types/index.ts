export interface Message {
  id: string;
  content: string;
  role: 'user' | 'ai';
  timestamp: Date;
}

export interface Conversation {
  id: string;
  title: string;
  messages: Message[];
  createdAt: Date;
  updatedAt: Date;
}

export interface ChatContextType {
  currentConversation: Conversation | null;
  conversations: Conversation[];
  isLoading: boolean;
  error: string | null;
  isDarkMode: boolean;
  apiStatus: 'connected' | 'disconnected' | 'checking';
  
  // Actions
  createNewConversation: () => void;
  loadConversation: (id: string) => void;
  deleteConversation: (id: string) => void;
  sendMessage: (content: string) => Promise<void>;
  clearHistory: () => void;
  toggleTheme: () => void;
  checkAPIStatus: () => Promise<void>;
}
