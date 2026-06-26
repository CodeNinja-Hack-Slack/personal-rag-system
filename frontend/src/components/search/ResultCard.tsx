'use client';

import { FileText, Code, Globe, Edit3 } from 'lucide-react';
import { SearchResult } from '@/hooks/useSearch';

interface ResultCardProps {
  result: SearchResult;
  index: number;
}

const typeIcons: Record<string, any> = {
  markdown: FileText,
  code: Code,
  webpage: Globe,
  manual: Edit3,
};

export default function ResultCard({ result, index }: ResultCardProps) {
  const Icon = typeIcons[result.metadata?.content_type || 'manual'] || FileText;
  const score = result.distance ? Math.round((1 - result.distance) * 100) : null;

  return (
    <div className="bg-white border rounded-lg p-4 hover:shadow-md transition-shadow">
      <div className="flex items-start gap-3">
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
          <p className="text-sm text-gray-600 line-clamp-3">{result.content}</p>
          <div className="mt-2 flex items-center gap-2 text-xs text-gray-400">
            <span className="capitalize">{result.metadata?.content_type || '未知类型'}</span>
            {result.metadata?.language && (
              <>
                <span>·</span>
                <span>{result.metadata.language === 'zh' ? '中文' : '英文'}</span>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
