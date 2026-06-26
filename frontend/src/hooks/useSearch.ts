import { useState } from 'react';
import { searchKnowledge } from '@/services/api';

export interface SearchResult {
  content: string;
  metadata: {
    title?: string;
    content_type?: string;
    chunk_index?: number;
    language?: string;
  };
  distance?: number;
}

export function useSearch() {
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [query, setQuery] = useState('');

  const search = async (searchQuery: string, topK?: number) => {
    if (!searchQuery.trim()) return;

    setLoading(true);
    setQuery(searchQuery);

    try {
      const response = await searchKnowledge(searchQuery, topK);
      setResults(response.results || []);
    } catch (error) {
      console.error('Search error:', error);
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  const clearResults = () => {
    setResults([]);
    setQuery('');
  };

  return { results, loading, query, search, clearResults };
}
