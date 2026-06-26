'use client';

import { useState, useEffect } from 'react';
import { Settings, Database, Cpu, Key, X, RefreshCw } from 'lucide-react';
import { getStats, getModels } from '@/services/api';

interface SettingsPanelProps {
  onClose: () => void;
}

export default function SettingsPanel({ onClose }: SettingsPanelProps) {
  const [stats, setStats] = useState<any>(null);
  const [models, setModels] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([getStats(), getModels()])
      .then(([s, m]) => { setStats(s); setModels(m); })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50" onClick={onClose}>
      <div className="bg-white rounded-xl shadow-xl w-full max-w-lg mx-4" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between px-6 py-4 border-b">
          <div className="flex items-center gap-2">
            <Settings className="w-5 h-5 text-gray-600" />
            <h2 className="text-lg font-semibold">系统设置</h2>
          </div>
          <button onClick={onClose} className="p-2 hover:bg-gray-100 rounded-lg">
            <X className="w-5 h-5 text-gray-500" />
          </button>
        </div>

        <div className="p-6 space-y-6">
          {loading ? (
            <div className="flex items-center justify-center py-8 text-gray-500">
              <RefreshCw className="w-5 h-5 animate-spin mr-2" />
              加载中...
            </div>
          ) : (
            <>
              <div>
                <h3 className="text-sm font-medium text-gray-700 mb-3 flex items-center gap-2">
                  <Database className="w-4 h-4" />
                  知识库统计
                </h3>
                <div className="grid grid-cols-2 gap-3">
                  <div className="bg-gray-50 rounded-lg p-3">
                    <p className="text-2xl font-bold text-blue-600">{stats?.total_knowledge_items || 0}</p>
                    <p className="text-xs text-gray-500">知识条目</p>
                  </div>
                  <div className="bg-gray-50 rounded-lg p-3">
                    <p className="text-2xl font-bold text-green-600">{stats?.vector_db || 'ChromaDB'}</p>
                    <p className="text-xs text-gray-500">向量数据库</p>
                  </div>
                </div>
              </div>

              <div>
                <h3 className="text-sm font-medium text-gray-700 mb-3 flex items-center gap-2">
                  <Cpu className="w-4 h-4" />
                  模型配置
                </h3>
                <div className="space-y-2">
                  <div className="flex items-center justify-between bg-gray-50 rounded-lg p-3">
                    <span className="text-sm text-gray-600">LLM 提供商</span>
                    <span className="text-sm font-medium">{stats?.llm_provider || '未配置'}</span>
                  </div>
                  <div className="flex items-center justify-between bg-gray-50 rounded-lg p-3">
                    <span className="text-sm text-gray-600">LLM 模型</span>
                    <span className="text-sm font-medium">{stats?.llm_model || '未配置'}</span>
                  </div>
                  <div className="flex items-center justify-between bg-gray-50 rounded-lg p-3">
                    <span className="text-sm text-gray-600">嵌入模型</span>
                    <span className="text-sm font-medium">{stats?.embedding_model || '未配置'}</span>
                  </div>
                </div>
              </div>

              {models?.models && (
                <div>
                  <h3 className="text-sm font-medium text-gray-700 mb-3 flex items-center gap-2">
                    <Key className="w-4 h-4" />
                    可用模型
                  </h3>
                  <div className="space-y-1">
                    {models.models.map((m: any) => (
                      <div key={m.id} className="flex items-center justify-between text-sm py-1.5 px-3 rounded hover:bg-gray-50">
                        <span className="text-gray-700">{m.name}</span>
                        <span className="text-xs text-gray-400">{m.provider}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </>
          )}
        </div>

        <div className="px-6 py-3 border-t bg-gray-50 rounded-b-xl text-xs text-gray-400">
          Personal RAG System v1.0
        </div>
      </div>
    </div>
  );
}
