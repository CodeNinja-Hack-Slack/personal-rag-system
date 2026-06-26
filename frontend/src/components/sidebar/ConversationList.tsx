'use client';

import { MessageSquare } from 'lucide-react';

interface Conversation {
  id: string;
  title: string;
  lastMessage: string;
  timestamp: string;
}

interface ConversationListProps {
  conversations?: Conversation[];
  onSelect?: (id: string) => void;
  activeId?: string;
}

export default function ConversationList({
  conversations = [],
  onSelect,
  activeId,
}: ConversationListProps) {
  if (conversations.length === 0) {
    return (
      <div className="p-4 text-center text-gray-500 text-sm">
        <MessageSquare className="w-8 h-8 mx-auto mb-2 text-gray-400" />
        <p>暂无对话历史</p>
      </div>
    );
  }

  return (
    <div className="space-y-1 p-2">
      {conversations.map((conv) => (
        <button
          key={conv.id}
          onClick={() => onSelect?.(conv.id)}
          className={`w-full text-left p-3 rounded-lg transition-colors ${
            activeId === conv.id
              ? 'bg-blue-50 text-blue-700'
              : 'hover:bg-gray-100 text-gray-700'
          }`}
        >
          <p className="font-medium text-sm truncate">{conv.title}</p>
          <p className="text-xs text-gray-500 truncate mt-1">{conv.lastMessage}</p>
        </button>
      ))}
    </div>
  );
}
