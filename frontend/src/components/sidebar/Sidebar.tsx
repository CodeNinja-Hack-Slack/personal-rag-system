'use client';

import { useState } from 'react';
import { MessageSquare, Search, Plus, ChevronLeft, ChevronRight, Upload, Database } from 'lucide-react';
import ConversationList from './ConversationList';

interface SidebarProps {
  mode: 'chat' | 'search' | 'import' | 'list';
  onModeChange: (mode: 'chat' | 'search' | 'import' | 'list') => void;
  onNewChat?: () => void;
}

export default function Sidebar({ mode, onModeChange, onNewChat }: SidebarProps) {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <div
      className={`bg-white border-r flex flex-col transition-all duration-200 ${
        collapsed ? 'w-16' : 'w-60'
      }`}
    >
      <div className="p-3 flex items-center justify-between border-b">
        {!collapsed && (
          <h2 className="font-semibold text-gray-800 text-sm">RAG 知识库</h2>
        )}
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="p-1.5 hover:bg-gray-100 rounded-lg text-gray-500"
        >
          {collapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
        </button>
      </div>

      {!collapsed && (
        <>
          <div className="p-2">
            <button
              onClick={onNewChat}
              className="w-full flex items-center gap-2 px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <Plus className="w-4 h-4" />
              新对话
            </button>
          </div>

          <div className="px-2 space-y-0.5">
            <button
              onClick={() => onModeChange('chat')}
              className={`w-full flex items-center gap-2 px-3 py-2 text-sm rounded-lg transition-colors ${
                mode === 'chat'
                  ? 'bg-blue-50 text-blue-700 font-medium'
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              <MessageSquare className="w-4 h-4" />
              对话
            </button>
            <button
              onClick={() => onModeChange('search')}
              className={`w-full flex items-center gap-2 px-3 py-2 text-sm rounded-lg transition-colors ${
                mode === 'search'
                  ? 'bg-blue-50 text-blue-700 font-medium'
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              <Search className="w-4 h-4" />
              搜索
            </button>
          </div>

          <div className="px-2 mt-3 mb-1">
            <p className="px-3 text-xs font-medium text-gray-400 uppercase tracking-wider">知识管理</p>
          </div>
          <div className="px-2 space-y-0.5">
            <button
              onClick={() => onModeChange('list')}
              className={`w-full flex items-center gap-2 px-3 py-2 text-sm rounded-lg transition-colors ${
                mode === 'list'
                  ? 'bg-blue-50 text-blue-700 font-medium'
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              <Database className="w-4 h-4" />
              知识列表
            </button>
            <button
              onClick={() => onModeChange('import')}
              className={`w-full flex items-center gap-2 px-3 py-2 text-sm rounded-lg transition-colors ${
                mode === 'import'
                  ? 'bg-blue-50 text-blue-700 font-medium'
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              <Upload className="w-4 h-4" />
              导入知识
            </button>
          </div>

          <div className="flex-1 overflow-y-auto mt-3 border-t">
            <ConversationList />
          </div>
        </>
      )}

      {collapsed && (
        <div className="flex flex-col items-center gap-1 py-2">
          <button onClick={onNewChat} className="p-2.5 hover:bg-gray-100 rounded-lg text-gray-600" title="新对话">
            <Plus className="w-5 h-5" />
          </button>
          <button onClick={() => onModeChange('chat')} className={`p-2.5 rounded-lg ${mode === 'chat' ? 'bg-blue-50 text-blue-600' : 'hover:bg-gray-100 text-gray-600'}`} title="对话">
            <MessageSquare className="w-5 h-5" />
          </button>
          <button onClick={() => onModeChange('search')} className={`p-2.5 rounded-lg ${mode === 'search' ? 'bg-blue-50 text-blue-600' : 'hover:bg-gray-100 text-gray-600'}`} title="搜索">
            <Search className="w-5 h-5" />
          </button>
          <button onClick={() => onModeChange('list')} className={`p-2.5 rounded-lg ${mode === 'list' ? 'bg-blue-50 text-blue-600' : 'hover:bg-gray-100 text-gray-600'}`} title="知识列表">
            <Database className="w-5 h-5" />
          </button>
          <button onClick={() => onModeChange('import')} className={`p-2.5 rounded-lg ${mode === 'import' ? 'bg-blue-50 text-blue-600' : 'hover:bg-gray-100 text-gray-600'}`} title="导入知识">
            <Upload className="w-5 h-5" />
          </button>
        </div>
      )}
    </div>
  );
}
