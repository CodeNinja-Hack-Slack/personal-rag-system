'use client';

import { useChat } from '@/hooks/useChat';
import MessageList from './MessageList';
import InputBox from './InputBox';
import { Lightbulb } from 'lucide-react';

const SUGGESTIONS = [
  'Java 集合框架有哪些常用实现？',
  'Spring Boot 自动配置的原理是什么？',
  'MySQL 索引优化有哪些技巧？',
  'Redis 有哪些数据结构？',
  '如何设计一个秒杀系统？',
  'JVM 垃圾回收算法有哪些？',
  'React Hooks 怎么使用？',
  'Docker 常用命令有哪些？',
];

export default function ChatWindow() {
  const { messages, loading, sendMessage } = useChat();

  if (messages.length === 0) {
    return (
      <div className="flex flex-col h-full">
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center max-w-2xl px-4">
            <div className="w-16 h-16 bg-blue-50 rounded-2xl flex items-center justify-center mx-auto mb-4">
              <Lightbulb className="w-8 h-8 text-blue-500" />
            </div>
            <h2 className="text-xl font-semibold text-gray-800 mb-2">有什么想了解的？</h2>
            <p className="text-sm text-gray-500 mb-6">基于知识库回答你的问题，试试下面的示例</p>
            <div className="grid grid-cols-2 gap-2">
              {SUGGESTIONS.map((q, i) => (
                <button
                  key={i}
                  onClick={() => sendMessage(q)}
                  className="text-left text-sm text-gray-600 bg-white border rounded-lg px-4 py-2.5 hover:bg-blue-50 hover:border-blue-300 hover:text-blue-700 transition-colors"
                >
                  {q}
                </button>
              ))}
            </div>
          </div>
        </div>
        <InputBox onSend={sendMessage} loading={loading} />
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full">
      <MessageList messages={messages} />
      <InputBox onSend={sendMessage} loading={loading} />
    </div>
  );
}
