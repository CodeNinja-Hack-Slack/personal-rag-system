'use client';

import { useState, useEffect } from 'react';
import { FileText, Code, Globe, Edit3, Trash2, ChevronRight, Search, Loader2, RefreshCw, Download } from 'lucide-react';
import { getKnowledgeList, deleteKnowledge, exportKnowledge } from '@/services/api';

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

interface KnowledgeListProps {
  onItemSelect: (item: KnowledgeItem) => void;
}

const typeIcons: Record<string, any> = {
  markdown: FileText,
  code: Code,
  webpage: Globe,
  manual: Edit3,
};

export default function KnowledgeList({ onItemSelect }: KnowledgeListProps) {
  const [items, setItems] = useState<KnowledgeItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [deleteConfirm, setDeleteConfirm] = useState<string | null>(null);

  const loadItems = async () => {
    setLoading(true);
    try {
      const res = await getKnowledgeList(0, 200);
      setItems(res.items || []);
    } catch (e) {
      console.error('Failed to load knowledge list:', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { loadItems(); }, []);

  const handleDelete = async (id: string) => {
    try {
      await deleteKnowledge(id);
      setItems(prev => prev.filter(item => item.id !== id));
      setDeleteConfirm(null);
    } catch (e) {
      console.error('Delete failed:', e);
    }
  };

  const handleExport = async () => {
    try {
      const res = await exportKnowledge();
      const blob = new Blob([JSON.stringify(res.items, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `knowledge-export-${new Date().toISOString().slice(0, 10)}.json`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (e) {
      console.error('Export failed:', e);
    }
  };

  const filtered = items.filter(item => {
    if (!search.trim()) return true;
    const q = search.toLowerCase();
    return item.title.toLowerCase().includes(q)
      || (item.category || '').toLowerCase().includes(q)
      || (item.tags || []).some(t => t.toLowerCase().includes(q));
  });

  const categories = [...new Set(items.map(i => i.category).filter(Boolean))] as string[];

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full text-gray-500">
        <Loader2 className="w-5 h-5 animate-spin mr-2" />
        加载中...
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full">
      <div className="p-4 border-b bg-white">
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-lg font-semibold text-gray-800">
            知识库
            <span className="ml-2 text-sm font-normal text-gray-500">共 {items.length} 条</span>
          </h2>
          <div className="flex items-center gap-1">
            <button onClick={handleExport} className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg" title="导出全部">
              <Download className="w-4 h-4" />
            </button>
            <button onClick={loadItems} className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg" title="刷新">
              <RefreshCw className="w-4 h-4" />
            </button>
          </div>
        </div>
        <div className="flex gap-2">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              type="text"
              value={search}
              onChange={e => setSearch(e.target.value)}
              placeholder="搜索标题、分类、标签..."
              className="w-full border rounded-lg pl-9 pr-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
        {categories.length > 0 && (
          <div className="mt-2 flex flex-wrap gap-1">
            <button
              onClick={() => setSearch('')}
              className={`px-2 py-1 text-xs rounded-full ${!search ? 'bg-blue-100 text-blue-700' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'}`}
            >
              全部
            </button>
            {categories.map(cat => (
              <button
                key={cat}
                onClick={() => setSearch(cat!)}
                className={`px-2 py-1 text-xs rounded-full ${search === cat ? 'bg-blue-100 text-blue-700' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'}`}
              >
                {cat}
              </button>
            ))}
          </div>
        )}
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-2">
        {filtered.length === 0 && (
          <div className="text-center text-gray-500 py-8">
            {search ? `未找到与 "${search}" 相关的知识` : '知识库为空'}
          </div>
        )}

        {filtered.map(item => {
          const Icon = typeIcons[item.content_type] || FileText;

          return (
            <div
              key={item.id}
              className="bg-white border rounded-lg flex items-center gap-3 p-3 cursor-pointer hover:bg-gray-50 hover:border-blue-300 transition-colors"
              onClick={() => onItemSelect(item)}
            >
              <div className="p-1.5 bg-blue-50 rounded">
                <Icon className="w-4 h-4 text-blue-600" />
              </div>
              <div className="flex-1 min-w-0">
                <h3 className="text-sm font-medium text-gray-900 truncate">{item.title}</h3>
                <div className="flex items-center gap-2 mt-0.5">
                  {item.category && (
                    <span className="text-xs bg-blue-50 text-blue-700 px-1.5 py-0.5 rounded">{item.category}</span>
                  )}
                  {(item.tags || []).slice(0, 3).map(tag => (
                    <span key={tag} className="text-xs bg-gray-100 text-gray-500 px-1.5 py-0.5 rounded">{tag}</span>
                  ))}
                  {item.tags && item.tags.length > 3 && (
                    <span className="text-xs text-gray-400">+{item.tags.length - 3}</span>
                  )}
                </div>
              </div>
              <div className="flex items-center gap-1">
                {deleteConfirm === item.id ? (
                  <div className="flex items-center gap-1" onClick={e => e.stopPropagation()}>
                    <button
                      onClick={() => handleDelete(item.id)}
                      className="px-2 py-1 text-xs bg-red-500 text-white rounded hover:bg-red-600"
                    >
                      确认
                    </button>
                    <button
                      onClick={() => setDeleteConfirm(null)}
                      className="px-2 py-1 text-xs bg-gray-200 text-gray-600 rounded hover:bg-gray-300"
                    >
                      取消
                    </button>
                  </div>
                ) : (
                  <button
                    onClick={e => { e.stopPropagation(); setDeleteConfirm(item.id); }}
                    className="p-1.5 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded"
                    title="删除"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                )}
                <ChevronRight className="w-4 h-4 text-gray-400" />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
