import React, { createContext, useState, useCallback, useEffect } from 'react';
import { Message, Conversation, ChatContextType } from '../types';
import { chatService } from '../services/api';

const generateId = () => Math.random().toString(36).substr(2, 9);

export const ChatContext = createContext<ChatContextType | undefined>(undefined);

export const ChatProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [conversations, setConversations] = useState<Conversation[]>(() => {
    const saved = localStorage.getItem('conversations');
    if (saved) {
      const parsed = JSON.parse(saved);
      // Convert timestamp strings back to Date objects
      return parsed.map((conv: Conversation) => ({
        ...conv,
        createdAt: new Date(conv.createdAt),
        updatedAt: new Date(conv.updatedAt),
        messages: conv.messages.map((msg: Message) => ({
          ...msg,
          timestamp: new Date(msg.timestamp),
        })),
      }));
    }
    return [];
  });

  const [currentConversationId, setCurrentConversationId] = useState<string | null>(() => {
    const saved = localStorage.getItem('currentConversationId');
    return saved || (conversations[0]?.id ?? null);
  });

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isDarkMode, setIsDarkMode] = useState(() => {
    const saved = localStorage.getItem('darkMode');
    return saved !== null ? JSON.parse(saved) : false;
  });
  const [apiStatus, setApiStatus] = useState<'connected' | 'disconnected' | 'checking'>('checking');

  const currentConversation = conversations.find(c => c.id === currentConversationId) || null;

  // Persist conversations to localStorage
  useEffect(() => {
    localStorage.setItem('conversations', JSON.stringify(conversations));
  }, [conversations]);

  // Persist current conversation ID
  useEffect(() => {
    localStorage.setItem('currentConversationId', currentConversationId || '');
  }, [currentConversationId]);

  // Apply dark mode
  useEffect(() => {
    localStorage.setItem('darkMode', JSON.stringify(isDarkMode));
    if (isDarkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [isDarkMode]);

  const createNewConversation = useCallback(() => {
    const newConversation: Conversation = {
      id: generateId(),
      title: `New Chat - ${new Date().toLocaleDateString()}`,
      messages: [],
      createdAt: new Date(),
      updatedAt: new Date(),
    };
    setConversations(prev => [newConversation, ...prev]);
    setCurrentConversationId(newConversation.id);
  }, []);

  const loadConversation = useCallback((id: string) => {
    setCurrentConversationId(id);
  }, []);

  const deleteConversation = useCallback((id: string) => {
    setConversations(prev => prev.filter(c => c.id !== id));
    if (currentConversationId === id) {
      const remaining = conversations.filter(c => c.id !== id);
      setCurrentConversationId(remaining[0]?.id || null);
      if (remaining.length === 0) {
        createNewConversation();
      }
    }
  }, [currentConversationId, conversations, createNewConversation]);

  const sendMessage = useCallback(async (content: string) => {
    if (!currentConversation) return;

    setIsLoading(true);
    setError(null);

    try {
      // Add user message
      const userMessage: Message = {
        id: generateId(),
        content,
        role: 'user',
        timestamp: new Date(),
      };

      setConversations((prev: Conversation[]) =>
        prev.map(conv =>
          conv.id === currentConversation.id
            ? { ...conv, messages: [...conv.messages, userMessage], updatedAt: new Date() }
            : conv
        )
      );

      // Get AI response
      const response = await chatService.sendMessage(content);

      if (response.success) {
        const aiMessage: Message = {
          id: generateId(),
          content: response.response,
          role: 'ai',
          timestamp: new Date(),
        };

        setConversations((prev: Conversation[]) =>
          prev.map(conv =>
            conv.id === currentConversation.id
              ? {
                  ...conv,
                  messages: [...conv.messages, aiMessage],
                  updatedAt: new Date(),
                  title: conv.title === `New Chat - ${new Date().toLocaleDateString()}` 
                    ? content.substring(0, 50) + (content.length > 50 ? '...' : '')
                    : conv.title,
                }
              : conv
          )
        );
      } else {
        throw new Error(response.error || 'Failed to get response');
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An error occurred';
      setError(errorMessage);

      // Add error message to chat
      if (currentConversation) {
        const errorMsg: Message = {
          id: generateId(),
          content: `Error: ${errorMessage}`,
          role: 'ai',
          timestamp: new Date(),
        };

        setConversations((prev: Conversation[]) =>
          prev.map(conv =>
            conv.id === currentConversation.id
              ? { ...conv, messages: [...conv.messages, errorMsg], updatedAt: new Date() }
              : conv
          )
        );
      }
    } finally {
      setIsLoading(false);
    }
  }, [currentConversation, conversations]);

  const clearHistory = useCallback(() => {
    setConversations([]);
    createNewConversation();
    setError(null);
  }, [createNewConversation]);

  const toggleTheme = useCallback(() => {
    setIsDarkMode((prev: boolean) => !prev);
  }, []);

  const checkAPIStatus = useCallback(async () => {
    setApiStatus('checking');
    try {
      const status = await chatService.checkStatus();
      setApiStatus(status.success ? 'connected' : 'disconnected');
    } catch {
      setApiStatus('disconnected');
    }
  }, []);

  // Initialize conversation on mount
  useEffect(() => {
    if (conversations.length === 0) {
      createNewConversation();
    }
  }, []);

  // Check API status on mount
  useEffect(() => {
    checkAPIStatus();
  }, [checkAPIStatus]);

  const value: ChatContextType = {
    currentConversation,
    conversations,
    isLoading,
    error,
    isDarkMode,
    apiStatus,
    createNewConversation,
    loadConversation,
    deleteConversation,
    sendMessage,
    clearHistory,
    toggleTheme,
    checkAPIStatus,
  };

  return <ChatContext.Provider value={value}>{children}</ChatContext.Provider>;
};
