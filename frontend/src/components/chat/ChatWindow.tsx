'use client';

import { useChat } from '@/hooks/useChat';
import MessageList from './MessageList';
import InputBox from './InputBox';

export default function ChatWindow() {
  const { messages, loading, sendMessage } = useChat();

  return (
    <div className="flex flex-col h-full">
      <MessageList messages={messages} />
      <InputBox onSend={sendMessage} loading={loading} />
    </div>
  );
}
