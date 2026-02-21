import axios, { AxiosInstance } from 'axios';

// Use relative URLs to leverage Vite's proxy in development
// In production, set VITE_API_BASE_URL to your backend URL
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

const api: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

export const chatService = {
  sendMessage: async (message: string) => {
    try {
      const response = await api.post('/api/chat', { message });
      return response.data;
    } catch (error) {
      throw new Error(`Failed to send message: ${error}`);
    }
  },

  checkStatus: async () => {
    try {
      const response = await api.get('/api/status');
      return response.data;
    } catch (error) {
      throw new Error(`Failed to check API status: ${error}`);
    }
  },

  getConversationHistory: async () => {
    try {
      const response = await api.get('/api/history');
      return response.data;
    } catch (error) {
      throw new Error(`Failed to get history: ${error}`);
    }
  },
};

export default api;
