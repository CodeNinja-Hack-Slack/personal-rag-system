'use client';

import ReactMarkdown from 'react-markdown';
import { ArrowLeft, Copy, Check, FileText, Code, Globe, Edit3, Trash2, List, Save, X } from 'lucide-react';
import { useState, useMemo } from 'react';
import { updateKnowledge } from '@/services/api';

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

interface KnowledgeDetailProps {
  item: KnowledgeItem;
  onBack: () => void;
  onDelete: (id: string) => void;
  onUpdate?: (item: KnowledgeItem) => void;
}

const typeIcons: Record<string, any> = {
  markdown: FileText,
  code: Code,
  webpage: Globe,
  manual: Edit3,
};

export default function KnowledgeDetail({ item, onBack, onDelete, onUpdate }: KnowledgeDetailProps) {
  const [copied, setCopied] = useState(false);
  const [deleteConfirm, setDeleteConfirm] = useState(false);
  const [showToc, setShowToc] = useState(false);
  const [editing, setEditing] = useState(false);
  const [editData, setEditData] = useState({ title: item.title, content: item.content, category: item.category || '', tags: (item.tags || []).join(', ') });
  const [saving, setSaving] = useState(false);
  const Icon = typeIcons[item.content_type] || FileText;

  const headings = useMemo(() => {
    const source = editing ? editData.content : item.content;
    const regex = /^(#{1,4})\s+(.+)$/gm;
    const result: { level: number; text: string; id: string }[] = [];
    let match;
    while ((match = regex.exec(source)) !== null) {
      const text = match[2].trim();
      const id = text.toLowerCase().replace(/[^\w\u4e00-\u9fff]+/g, '-');
      result.push({ level: match[1].length, text, id });
    }
    return result;
  }, [item.content, editing, editData.content]);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(editing ? editData.content : item.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDelete = () => {
    onDelete(item.id);
    onBack();
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      await updateKnowledge(item.id, {
        title: editData.title,
        content: editData.content,
        category: editData.category || undefined,
        tags: editData.tags ? editData.tags.split(',').map(t => t.trim()) : undefined,
      });
      const updated = {
        ...item,
        title: editData.title,
        content: editData.content,
        category: editData.category || null,
        tags: editData.tags ? editData.tags.split(',').map(t => t.trim()) : [],
        version: item.version + 1,
      };
      onUpdate?.(updated);
      setEditing(false);
    } catch (e) {
      console.error('Save failed:', e);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="flex h-full bg-white">
      <div className="flex-1 flex flex-col min-w-0">
        <div className="border-b px-6 py-3 flex items-center gap-3">
          <button onClick={onBack} className="p-2 hover:bg-gray-100 rounded-lg" title="返回列表">
            <ArrowLeft className="w-5 h-5 text-gray-600" />
          </button>
          <div className="p-1.5 bg-blue-50 rounded">
            <Icon className="w-5 h-5 text-blue-600" />
          </div>
          <div className="flex-1 min-w-0">
            {editing ? (
              <input
                value={editData.title}
                onChange={e => setEditData({ ...editData, title: e.target.value })}
                className="text-lg font-semibold text-gray-900 w-full border-b border-blue-300 focus:outline-none pb-0.5"
              />
            ) : (
              <h1 className="text-lg font-semibold text-gray-900 truncate">{item.title}</h1>
            )}
            <div className="flex items-center gap-2 mt-0.5">
              {editing ? (
                <>
                  <input
                    value={editData.category}
                    onChange={e => setEditData({ ...editData, category: e.target.value })}
                    placeholder="分类"
                    className="text-xs border rounded px-2 py-0.5 w-20 focus:outline-none focus:ring-1 focus:ring-blue-500"
                  />
                  <input
                    value={editData.tags}
                    onChange={e => setEditData({ ...editData, tags: e.target.value })}
                    placeholder="标签(逗号分隔)"
                    className="text-xs border rounded px-2 py-0.5 flex-1 focus:outline-none focus:ring-1 focus:ring-blue-500"
                  />
                </>
              ) : (
                <>
                  {item.category && (
                    <span className="text-xs bg-blue-50 text-blue-700 px-2 py-0.5 rounded">{item.category}</span>
                  )}
                  {(item.tags || []).map(tag => (
                    <span key={tag} className="text-xs bg-gray-100 text-gray-500 px-2 py-0.5 rounded">{tag}</span>
                  ))}
                </>
              )}
            </div>
          </div>
          <div className="flex items-center gap-1">
            {editing ? (
              <>
                <button onClick={handleSave} disabled={saving} className="flex items-center gap-1 px-3 py-1.5 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50">
                  <Save className="w-4 h-4" />
                  {saving ? '保存中...' : '保存'}
                </button>
                <button onClick={() => setEditing(false)} className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg">
                  <X className="w-4 h-4" />
                </button>
              </>
            ) : (
              <>
                <button onClick={() => setEditing(true)} className="flex items-center gap-1 px-3 py-1.5 text-sm text-gray-600 hover:bg-gray-100 rounded-lg">
                  <Edit3 className="w-4 h-4" />
                  编辑
                </button>
                {headings.length > 0 && (
                  <button
                    onClick={() => setShowToc(!showToc)}
                    className={`flex items-center gap-1 px-3 py-1.5 text-sm rounded-lg ${showToc ? 'bg-blue-50 text-blue-700' : 'text-gray-600 hover:bg-gray-100'}`}
                  >
                    <List className="w-4 h-4" />
                    目录
                  </button>
                )}
                <button onClick={handleCopy} className="flex items-center gap-1 px-3 py-1.5 text-sm text-gray-600 hover:bg-gray-100 rounded-lg">
                  {copied ? <Check className="w-4 h-4 text-green-600" /> : <Copy className="w-4 h-4" />}
                  {copied ? '已复制' : '复制'}
                </button>
                {deleteConfirm ? (
                  <div className="flex items-center gap-1 ml-1">
                    <button onClick={handleDelete} className="px-3 py-1.5 text-sm bg-red-500 text-white rounded-lg hover:bg-red-600">
                      确认删除
                    </button>
                    <button onClick={() => setDeleteConfirm(false)} className="px-3 py-1.5 text-sm bg-gray-200 text-gray-600 rounded-lg hover:bg-gray-300">
                      取消
                    </button>
                  </div>
                ) : (
                  <button onClick={() => setDeleteConfirm(true)} className="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-lg" title="删除">
                    <Trash2 className="w-4 h-4" />
                  </button>
                )}
              </>
            )}
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-6">
          {editing ? (
            <textarea
              value={editData.content}
              onChange={e => setEditData({ ...editData, content: e.target.value })}
              className="w-full h-full border rounded-lg p-4 font-mono text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
            />
          ) : (
            <div className="max-w-4xl mx-auto markdown-body">
              <ReactMarkdown>{item.content}</ReactMarkdown>
            </div>
          )}
        </div>

        <div className="border-t px-6 py-2 flex items-center gap-4 text-xs text-gray-400">
          <span>类型: {item.content_type}</span>
          <span>语言: {item.language === 'zh' ? '中文' : '英文'}</span>
          {item.source && <span>来源: {item.source}</span>}
          <span>版本: v{item.version}</span>
          {item.created_at && <span className="ml-auto">创建于: {new Date(item.created_at).toLocaleString('zh-CN')}</span>}
        </div>
      </div>

      {showToc && headings.length > 0 && (
        <div className="w-56 border-l overflow-y-auto p-4 bg-gray-50 flex-shrink-0">
          <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">目录</h3>
          <nav className="space-y-1">
            {headings.map((h, i) => (
              <a
                key={i}
                href={`#${h.id}`}
                onClick={e => {
                  e.preventDefault();
                  const el = document.getElementById(h.id);
                  el?.scrollIntoView({ behavior: 'smooth' });
                }}
                className={`block text-sm text-gray-600 hover:text-blue-600 truncate ${
                  h.level === 1 ? 'font-medium' : h.level === 2 ? 'pl-3' : 'pl-6'
                }`}
              >
                {h.text}
              </a>
            ))}
          </nav>
        </div>
      )}
    </div>
  );
}
