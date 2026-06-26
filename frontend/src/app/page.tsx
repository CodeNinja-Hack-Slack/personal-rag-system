'use client';

import { useState, useEffect } from 'react';
import { FileText, Database, Settings } from 'lucide-react';
import Sidebar from '@/components/sidebar/Sidebar';
import ChatWindow from '@/components/chat/ChatWindow';
import SearchResults from '@/components/search/SearchResults';
import ImportKnowledge from '@/components/knowledge/ImportKnowledge';
import KnowledgeList from '@/components/knowledge/KnowledgeList';
import KnowledgeDetail from '@/components/knowledge/KnowledgeDetail';
import SettingsPanel from '@/components/settings/SettingsPanel';
import { getStats } from '@/services/api';

interface KnowledgeItem {
  id: string;
  title: string;
  content: string;
  content_type: string;
  category: string | null;
  tags: string[];
  source: string | null;
  language: string;
  created_at: string;
  version: number;
}

export default function Home() {
  const [mode, setMode] = useState<'chat' | 'search' | 'import' | 'list'>('chat');
  const [selectedItem, setSelectedItem] = useState<KnowledgeItem | null>(null);
  const [stats, setStats] = useState<{ total: number } | null>(null);
  const [chatKey, setChatKey] = useState(0);
  const [showSettings, setShowSettings] = useState(false);

  useEffect(() => {
    getStats().then(res => setStats({ total: res.total_knowledge_items })).catch(() => {});
  }, []);

  const handleModeChange = (newMode: 'chat' | 'search' | 'import' | 'list') => {
    setMode(newMode);
    if (newMode !== 'list') setSelectedItem(null);
  };

  const handleNewChat = () => {
    setChatKey(prev => prev + 1);
    setMode('chat');
  };

  const handleDeleteFromDetail = (id: string) => {
    setSelectedItem(null);
  };

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar mode={mode} onModeChange={handleModeChange} onNewChat={handleNewChat} />

      <div className="flex-1 flex flex-col">
        <header className="bg-white border-b px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <FileText className="w-6 h-6 text-blue-600" />
            <h1 className="text-xl font-semibold">RAG Chat</h1>
          </div>
          <div className="flex items-center gap-2">
            {stats && (
              <div className="flex items-center gap-1.5 text-sm text-gray-500 bg-gray-50 px-3 py-1.5 rounded-full">
                <Database className="w-4 h-4" />
                <span>{stats.total} 条知识</span>
              </div>
            )}
            <button
              onClick={() => setShowSettings(true)}
              className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg"
              title="系统设置"
            >
              <Settings className="w-5 h-5" />
            </button>
          </div>
        </header>

        <main className="flex-1 overflow-hidden">
          {mode === 'chat' && <ChatWindow key={chatKey} />}
          {mode === 'search' && <SearchResults />}
          {mode === 'list' && !selectedItem && <KnowledgeList onItemSelect={setSelectedItem} />}
          {mode === 'list' && selectedItem && (
            <KnowledgeDetail
              item={selectedItem}
              onBack={() => setSelectedItem(null)}
              onDelete={handleDeleteFromDetail}
              onUpdate={setSelectedItem}
            />
          )}
          {mode === 'import' && <ImportKnowledge />}
        </main>
      </div>

      {showSettings && <SettingsPanel onClose={() => setShowSettings(false)} />}
    </div>
  );
}
