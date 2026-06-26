'use client';

import { useState } from 'react';
import { MessageSquare, Search, Plus, ChevronLeft, ChevronRight } from 'lucide-react';
import ConversationList from './ConversationList';

interface SidebarProps {
  mode: 'chat' | 'search';
  onModeChange: (mode: 'chat' | 'search') => void;
  onNewChat?: () => void;
}

export default function Sidebar({ mode, onModeChange, onNewChat }: SidebarProps) {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <div
      className={`bg-gray-50 border-r flex flex-col transition-all ${
        collapsed ? 'w-16' : 'w-64'
      }`}
    >
      <div className="p-4 flex items-center justify-between">
        {!collapsed && (
          <h2 className="font-semibold text-gray-700">RAG 知识库</h2>
        )}
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="p-1 hover:bg-gray-200 rounded"
        >
          {collapsed ? (
            <ChevronRight className="w-4 h-4" />
          ) : (
            <ChevronLeft className="w-4 h-4" />
          )}
        </button>
      </div>

      {!collapsed && (
        <>
          <div className="px-2 mb-2">
            <button
              onClick={onNewChat}
              className="w-full flex items-center gap-2 p-2 text-sm text-gray-600 hover:bg-gray-200 rounded-lg"
            >
              <Plus className="w-4 h-4" />
              新对话
            </button>
          </div>

          <div className="px-2 mb-2 flex gap-1">
            <button
              onClick={() => onModeChange('chat')}
              className={`flex-1 flex items-center justify-center gap-1 p-2 text-sm rounded-lg ${
                mode === 'chat'
                  ? 'bg-blue-100 text-blue-700'
                  : 'text-gray-600 hover:bg-gray-200'
              }`}
            >
              <MessageSquare className="w-4 h-4" />
              对话
            </button>
            <button
              onClick={() => onModeChange('search')}
              className={`flex-1 flex items-center justify-center gap-1 p-2 text-sm rounded-lg ${
                mode === 'search'
                  ? 'bg-blue-100 text-blue-700'
                  : 'text-gray-600 hover:bg-gray-200'
              }`}
            >
              <Search className="w-4 h-4" />
              搜索
            </button>
          </div>

          <div className="flex-1 overflow-y-auto">
            <ConversationList />
          </div>
        </>
      )}
    </div>
  );
}
