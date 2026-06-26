'use client';

import { useState } from 'react';
import { Upload, FileText, Plus, Trash2, Check, AlertCircle, Loader2 } from 'lucide-react';
import { createKnowledge, importKnowledge } from '@/services/api';

interface KnowledgeItem {
  title: string;
  content: string;
  content_type: string;
  category: string;
  tags: string;
  source: string;
}

const emptyItem: KnowledgeItem = {
  title: '',
  content: '',
  content_type: 'markdown',
  category: '',
  tags: '',
  source: '',
};

export default function ImportKnowledge() {
  const [mode, setMode] = useState<'single' | 'batch'>('single');
  const [item, setItem] = useState<KnowledgeItem>({ ...emptyItem });
  const [batchJson, setBatchJson] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<{ type: 'success' | 'error'; message: string } | null>(null);

  const handleSubmitSingle = async () => {
    if (!item.title.trim() || !item.content.trim()) {
      setResult({ type: 'error', message: '标题和内容不能为空' });
      return;
    }
    setLoading(true);
    setResult(null);
    try {
      await createKnowledge({
        title: item.title,
        content: item.content,
        content_type: item.content_type,
        category: item.category || undefined,
        tags: item.tags ? item.tags.split(',').map(t => t.trim()) : undefined,
        source: item.source || undefined,
      });
      setResult({ type: 'success', message: '导入成功！' });
      setItem({ ...emptyItem });
    } catch (e: any) {
      setResult({ type: 'error', message: e.message || '导入失败' });
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitBatch = async () => {
    if (!batchJson.trim()) {
      setResult({ type: 'error', message: 'JSON 内容不能为空' });
      return;
    }
    setLoading(true);
    setResult(null);
    try {
      let items: any[];
      try {
        const parsed = JSON.parse(batchJson);
        items = Array.isArray(parsed) ? parsed : [parsed];
      } catch {
        throw new Error('JSON 格式不正确');
      }
      const res = await importKnowledge(items);
      setResult({ type: 'success', message: `成功导入 ${res.count || items.length} 条知识` });
      setBatchJson('');
    } catch (e: any) {
      setResult({ type: 'error', message: e.message || '导入失败' });
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files) return;

    Array.from(files).forEach(file => {
      const reader = new FileReader();
      reader.onload = (ev) => {
        const content = ev.target?.result as string;
        if (mode === 'single') {
          setItem(prev => ({
            ...prev,
            title: prev.title || file.name.replace(/\.\w+$/, ''),
            content: content,
          }));
        } else {
          setBatchJson(content);
        }
      };
      reader.readAsText(file);
    });
    e.target.value = '';
  };

  return (
    <div className="flex flex-col h-full">
      <div className="p-4 border-b bg-white">
        <h2 className="text-lg font-semibold text-gray-800 mb-3">导入知识</h2>
        <div className="flex gap-2">
          <button
            onClick={() => { setMode('single'); setResult(null); }}
            className={`flex-1 flex items-center justify-center gap-1 p-2 text-sm rounded-lg ${
              mode === 'single' ? 'bg-blue-100 text-blue-700' : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            <Plus className="w-4 h-4" />
            单条添加
          </button>
          <button
            onClick={() => { setMode('batch'); setResult(null); }}
            className={`flex-1 flex items-center justify-center gap-1 p-2 text-sm rounded-lg ${
              mode === 'batch' ? 'bg-blue-100 text-blue-700' : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            <Upload className="w-4 h-4" />
            批量导入
          </button>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-4">
        {result && (
          <div className={`mb-4 p-3 rounded-lg flex items-center gap-2 text-sm ${
            result.type === 'success' ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'
          }`}>
            {result.type === 'success' ? <Check className="w-4 h-4" /> : <AlertCircle className="w-4 h-4" />}
            {result.message}
          </div>
        )}

        {mode === 'single' ? (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">标题 *</label>
              <input
                type="text"
                value={item.title}
                onChange={e => setItem({ ...item, title: e.target.value })}
                placeholder="知识标题"
                className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">分类</label>
                <input
                  type="text"
                  value={item.category}
                  onChange={e => setItem({ ...item, category: e.target.value })}
                  placeholder="如: Java、前端"
                  className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">类型</label>
                <select
                  value={item.content_type}
                  onChange={e => setItem({ ...item, content_type: e.target.value })}
                  className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="markdown">Markdown</option>
                  <option value="code">代码</option>
                  <option value="manual">手动输入</option>
                </select>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">标签</label>
                <input
                  type="text"
                  value={item.tags}
                  onChange={e => setItem({ ...item, tags: e.target.value })}
                  placeholder="逗号分隔，如: java,spring"
                  className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">来源</label>
                <input
                  type="text"
                  value={item.source}
                  onChange={e => setItem({ ...item, source: e.target.value })}
                  placeholder="URL 或书名"
                  className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between mb-1">
                <label className="block text-sm font-medium text-gray-700">内容 *</label>
                <label className="text-xs text-blue-600 hover:text-blue-800 cursor-pointer flex items-center gap-1">
                  <Upload className="w-3 h-3" />
                  从文件导入
                  <input type="file" accept=".md,.txt,.json" onChange={handleFileUpload} className="hidden" />
                </label>
              </div>
              <textarea
                value={item.content}
                onChange={e => setItem({ ...item, content: e.target.value })}
                placeholder="支持 Markdown 格式..."
                rows={12}
                className="w-full border rounded-lg px-3 py-2 text-sm font-mono focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <button
              onClick={handleSubmitSingle}
              disabled={loading || !item.title.trim() || !item.content.trim()}
              className="w-full bg-blue-600 text-white rounded-lg py-2 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Plus className="w-4 h-4" />}
              {loading ? '导入中...' : '导入'}
            </button>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="bg-gray-50 rounded-lg p-3 text-xs text-gray-600">
              <p className="font-medium mb-1">JSON 格式示例：</p>
              <pre className="overflow-x-auto">{`[
  {
    "title": "知识标题",
    "content": "Markdown 内容...",
    "content_type": "markdown",
    "category": "Java",
    "tags": ["tag1", "tag2"]
  }
]`}</pre>
            </div>

            <div>
              <div className="flex items-center justify-between mb-1">
                <label className="block text-sm font-medium text-gray-700">JSON 内容</label>
                <label className="text-xs text-blue-600 hover:text-blue-800 cursor-pointer flex items-center gap-1">
                  <Upload className="w-3 h-3" />
                  从文件导入
                  <input type="file" accept=".json,.txt" onChange={handleFileUpload} className="hidden" />
                </label>
              </div>
              <textarea
                value={batchJson}
                onChange={e => setBatchJson(e.target.value)}
                placeholder='粘贴 JSON 数组...'
                rows={16}
                className="w-full border rounded-lg px-3 py-2 text-sm font-mono focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <button
              onClick={handleSubmitBatch}
              disabled={loading || !batchJson.trim()}
              className="w-full bg-blue-600 text-white rounded-lg py-2 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Upload className="w-4 h-4" />}
              {loading ? '导入中...' : '批量导入'}
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
