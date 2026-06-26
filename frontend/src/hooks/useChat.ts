import { useState } from 'react';
import { chat as chatApi } from '@/services/api';

export interface Message {
  role: 'user' | 'assistant';
  content: string;
  sources?: any[];
}

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async (question: string, topK?: number) => {
    setLoading(true);
    setMessages((prev) => [...prev, { role: 'user', content: question }]);

    try {
      const response = await chatApi(question, topK);
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: response.answer,
          sources: response.sources,
        },
      ]);
    } catch (error) {
      console.error('Chat error:', error);
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: '抱歉，发生了错误，请重试。' },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const clearMessages = () => setMessages([]);

  return { messages, loading, sendMessage, clearMessages };
}
