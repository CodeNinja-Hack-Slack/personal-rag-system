'use client';

import { Search } from 'lucide-react';
import { useSearch, SearchResult } from '@/hooks/useSearch';
import ResultCard from './ResultCard';
import { useState } from 'react';

export default function SearchResults() {
  const { results, loading, query, search } = useSearch();
  const [input, setInput] = useState('');

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim()) {
      search(input.trim());
    }
  };

  return (
    <div className="flex flex-col h-full">
      <form onSubmit={handleSearch} className="p-4 border-b bg-white">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="搜索知识库..."
            className="flex-1 border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            type="submit"
            disabled={loading || !input.trim()}
            className="bg-blue-600 text-white rounded-lg px-4 py-2 hover:bg-blue-700 disabled:opacity-50"
          >
            <Search className="w-5 h-5" />
          </button>
        </div>
      </form>

      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {loading && (
          <div className="text-center text-gray-500 py-8">搜索中...</div>
        )}

        {!loading && query && results.length === 0 && (
          <div className="text-center text-gray-500 py-8">
            未找到与 "{query}" 相关的结果
          </div>
        )}

        {!loading && !query && (
          <div className="text-center text-gray-500 py-8">
            <Search className="w-12 h-12 mx-auto mb-4 text-gray-400" />
            <p>输入关键词搜索知识库</p>
          </div>
        )}

        {results.map((result, i) => (
          <ResultCard key={i} result={result} index={i} />
        ))}
      </div>
    </div>
  );
}
