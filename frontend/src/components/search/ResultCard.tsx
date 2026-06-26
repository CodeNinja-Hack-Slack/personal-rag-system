'use client';

import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { FileText, Code, Globe, Edit3, ChevronDown, ChevronUp, Copy, Check } from 'lucide-react';
import { SearchResult } from '@/hooks/useSearch';

interface ResultCardProps {
  result: SearchResult;
  index: number;
  query?: string;
}

const typeIcons: Record<string, any> = {
  markdown: FileText,
  code: Code,
  webpage: Globe,
  manual: Edit3,
};

function highlightText(text: string, query: string) {
  if (!query.trim()) return text;
  const parts = text.split(new RegExp(`(${query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi'));
  return parts.map((part, i) =>
    part.toLowerCase() === query.toLowerCase()
      ? `<mark class="bg-yellow-200 rounded px-0.5">${part}</mark>`
      : part
  ).join('');
}

export default function ResultCard({ result, index, query = '' }: ResultCardProps) {
  const [expanded, setExpanded] = useState(false);
  const [copied, setCopied] = useState(false);
  const Icon = typeIcons[result.metadata?.content_type || 'manual'] || FileText;
  const score = result.distance ? Math.round((1 - result.distance) * 100) : null;

  const handleCopy = async (e: React.MouseEvent) => {
    e.stopPropagation();
    await navigator.clipboard.writeText(result.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div
      className="bg-white border rounded-lg hover:shadow-md transition-shadow cursor-pointer"
      onClick={() => setExpanded(!expanded)}
    >
      <div className="flex items-start gap-3 p-4">
        <div className="p-2 bg-blue-50 rounded-lg">
          <Icon className="w-5 h-5 text-blue-600" />
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between mb-1">
            <h3 className="font-medium text-gray-900 truncate">
              {result.metadata?.title || `结果 ${index + 1}`}
            </h3>
            {score !== null && (
              <span className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded-full">
                {score}% 相关
              </span>
            )}
          </div>
          {expanded ? (
            <div className="markdown-body mt-2">
              <ReactMarkdown>{result.content}</ReactMarkdown>
            </div>
          ) : (
            <p
              className="text-sm text-gray-600 line-clamp-3"
              dangerouslySetInnerHTML={{ __html: highlightText(result.content, query) }}
            />
          )}
          <div className="mt-2 flex items-center gap-2 text-xs text-gray-400">
            <span className="capitalize">{result.metadata?.content_type || '未知类型'}</span>
            {result.metadata?.language && (
              <>
                <span>·</span>
                <span>{result.metadata.language === 'zh' ? '中文' : '英文'}</span>
              </>
            )}
            {expanded && (
              <button
                onClick={handleCopy}
                className="ml-auto flex items-center gap-1 text-blue-600 hover:text-blue-800"
              >
                {copied ? <Check className="w-3 h-3" /> : <Copy className="w-3 h-3" />}
                {copied ? '已复制' : '复制'}
              </button>
            )}
            <span className="ml-auto flex items-center gap-1">
              {expanded ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
              {expanded ? '收起' : '展开'}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
