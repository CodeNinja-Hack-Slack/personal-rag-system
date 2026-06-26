'use client';

import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { Message } from '@/hooks/useChat';
import { User, Bot, BookOpen, ChevronDown, ChevronUp, Copy, Check, ThumbsUp, ThumbsDown } from 'lucide-react';

interface MessageListProps {
  messages: Message[];
  onSourceClick?: (source: any) => void;
}

export default function MessageList({ messages, onSourceClick }: MessageListProps) {
  if (messages.length === 0) return null;

  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-4">
      {messages.map((msg, i) => (
        <MessageBubble key={i} message={msg} onSourceClick={onSourceClick} />
      ))}
    </div>
  );
}

function MessageBubble({ message, onSourceClick }: { message: Message; onSourceClick?: (source: any) => void }) {
  const [showSources, setShowSources] = useState(false);
  const [copied, setCopied] = useState(false);
  const [feedback, setFeedback] = useState<'up' | 'down' | null>(null);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(message.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className={`flex gap-3 ${message.role === 'user' ? 'flex-row-reverse' : ''}`}>
      <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
        message.role === 'user' ? 'bg-blue-600' : 'bg-gray-200'
      }`}>
        {message.role === 'user'
          ? <User className="w-4 h-4 text-white" />
          : <Bot className="w-4 h-4 text-gray-600" />
        }
      </div>
      <div className={`max-w-[75%] ${message.role === 'user' ? 'text-right' : ''}`}>
        <div
          className={`rounded-2xl px-4 py-2.5 ${
            message.role === 'user'
              ? 'bg-blue-600 text-white rounded-tr-md'
              : 'bg-white border shadow-sm rounded-tl-md'
          }`}
        >
          {message.role === 'assistant' ? (
            <div className="markdown-body text-sm">
              <ReactMarkdown>{message.content}</ReactMarkdown>

              {message.sources && message.sources.length > 0 && (
                <div className="mt-3 pt-2 border-t">
                  <button
                    onClick={() => setShowSources(!showSources)}
                    className="flex items-center gap-1 text-xs text-blue-600 hover:text-blue-800"
                  >
                    <BookOpen className="w-3 h-3" />
                    参考来源 ({message.sources.length})
                    {showSources ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
                  </button>
                  {showSources && (
                    <div className="mt-2 space-y-1.5">
                      {message.sources.map((src: any, j: number) => (
                        <button
                          key={j}
                          onClick={() => onSourceClick?.(src)}
                          className="w-full text-left p-2 rounded bg-gray-50 hover:bg-blue-50 transition-colors"
                        >
                          <p className="text-xs font-medium text-gray-700 truncate">
                            {src.metadata?.title || `来源 ${j + 1}`}
                          </p>
                          <p className="text-xs text-gray-500 truncate mt-0.5">
                            {src.content?.slice(0, 80)}...
                          </p>
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
          ) : (
            <p className="text-sm whitespace-pre-wrap">{message.content}</p>
          )}
        </div>

        {message.role === 'assistant' && (
          <div className="flex items-center gap-1 mt-1 px-1">
            <button
              onClick={handleCopy}
              className="p-1 text-gray-400 hover:text-gray-600 rounded"
              title="复制"
            >
              {copied ? <Check className="w-3.5 h-3.5 text-green-500" /> : <Copy className="w-3.5 h-3.5" />}
            </button>
            <button
              onClick={() => setFeedback(feedback === 'up' ? null : 'up')}
              className={`p-1 rounded ${feedback === 'up' ? 'text-green-500' : 'text-gray-400 hover:text-gray-600'}`}
              title="有帮助"
            >
              <ThumbsUp className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={() => setFeedback(feedback === 'down' ? null : 'down')}
              className={`p-1 rounded ${feedback === 'down' ? 'text-red-500' : 'text-gray-400 hover:text-gray-600'}`}
              title="没帮助"
            >
              <ThumbsDown className="w-3.5 h-3.5" />
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
