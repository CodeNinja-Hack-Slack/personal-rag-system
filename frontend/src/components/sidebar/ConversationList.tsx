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
  return (
    <div className="p-2">
      {conversations.length === 0 ? (
        <div className="px-3 py-6 text-center">
          <MessageSquare className="w-6 h-6 mx-auto mb-2 text-gray-300" />
          <p className="text-xs text-gray-400">暂无对话历史</p>
        </div>
      ) : (
        <div className="space-y-0.5">
          {conversations.map((conv) => (
            <button
              key={conv.id}
              onClick={() => onSelect?.(conv.id)}
              className={`w-full text-left px-3 py-2 rounded-lg transition-colors ${
                activeId === conv.id
                  ? 'bg-blue-50 text-blue-700'
                  : 'hover:bg-gray-100 text-gray-700'
              }`}
            >
              <p className="text-sm font-medium truncate">{conv.title}</p>
              <p className="text-xs text-gray-400 truncate mt-0.5">{conv.lastMessage}</p>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
