'use client';

import ReactMarkdown from 'react-markdown';
import { Message } from '@/hooks/useChat';

interface MessageListProps {
  messages: Message[];
}

export default function MessageList({ messages }: MessageListProps) {
  if (messages.length === 0) {
    return (
      <div className="flex-1 flex items-center justify-center text-gray-500">
        <div className="text-center">
          <p className="text-lg mb-2">欢迎使用 RAG 知识库</p>
          <p className="text-sm">输入问题开始对话</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-4">
      {messages.map((msg, i) => (
        <div
          key={i}
          className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
        >
          <div
            className={`max-w-[70%] rounded-lg px-4 py-2 ${
              msg.role === 'user'
                ? 'bg-blue-600 text-white'
                : 'bg-white border shadow-sm'
            }`}
          >
            {msg.role === 'assistant' ? (
              <div className="prose prose-sm max-w-none">
                <ReactMarkdown>{msg.content}</ReactMarkdown>
                {msg.sources && msg.sources.length > 0 && (
                  <div className="mt-2 pt-2 border-t text-xs text-gray-500">
                    <p className="font-medium mb-1">参考来源:</p>
                    {msg.sources.map((src: any, j: number) => (
                      <p key={j} className="truncate">
                        {src.metadata?.title || `来源 ${j + 1}`}
                      </p>
                    ))}
                  </div>
                )}
              </div>
            ) : (
              msg.content
            )}
          </div>
        </div>
      ))}
    </div>
  );
}
