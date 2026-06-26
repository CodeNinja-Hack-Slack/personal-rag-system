'use client';

import { useState } from 'react';
import { FileText } from 'lucide-react';
import Sidebar from '@/components/sidebar/Sidebar';
import ChatWindow from '@/components/chat/ChatWindow';
import SearchResults from '@/components/search/SearchResults';

export default function Home() {
  const [mode, setMode] = useState<'chat' | 'search'>('chat');

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar mode={mode} onModeChange={setMode} />

      <div className="flex-1 flex flex-col">
        <header className="bg-white border-b px-6 py-4 flex items-center gap-2">
          <FileText className="w-6 h-6 text-blue-600" />
          <h1 className="text-xl font-semibold">RAG Chat</h1>
        </header>

        <main className="flex-1 overflow-hidden">
          {mode === 'chat' ? <ChatWindow /> : <SearchResults />}
        </main>
      </div>
    </div>
  );
}
