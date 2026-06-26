const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export async function chat(question: string, model?: string) {
  const response = await fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question, model }),
  });
  if (!response.ok) throw new Error('Chat request failed');
  return response.json();
}

export async function searchKnowledge(query: string, topK?: number) {
  const response = await fetch(`${API_BASE}/search`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, top_k: topK }),
  });
  if (!response.ok) throw new Error('Search request failed');
  return response.json();
}

export async function getKnowledgeList(skip = 0, limit = 100) {
  const response = await fetch(`${API_BASE}/knowledge?skip=${skip}&limit=${limit}`);
  if (!response.ok) throw new Error('Failed to fetch knowledge list');
  return response.json();
}

export async function createKnowledge(data: {
  title: string;
  content: string;
  content_type: string;
  source?: string;
  language?: string;
  tags?: string[];
  category?: string;
}) {
  const response = await fetch(`${API_BASE}/knowledge`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!response.ok) throw new Error('Failed to create knowledge');
  return response.json();
}

export async function deleteKnowledge(id: string) {
  const response = await fetch(`${API_BASE}/knowledge/${id}`, {
    method: 'DELETE',
  });
  if (!response.ok) throw new Error('Failed to delete knowledge');
  return response.json();
}

export async function getChatHistory(skip = 0, limit = 50) {
  const response = await fetch(`${API_BASE}/chat/history?skip=${skip}&limit=${limit}`);
  if (!response.ok) throw new Error('Failed to fetch chat history');
  return response.json();
}

export async function getModels() {
  const response = await fetch(`${API_BASE}/models`);
  if (!response.ok) throw new Error('Failed to fetch models');
  return response.json();
}

export async function getStats() {
  const response = await fetch(`${API_BASE}/stats`);
  if (!response.ok) throw new Error('Failed to fetch stats');
  return response.json();
}
