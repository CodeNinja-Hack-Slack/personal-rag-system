const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export async function chat(query: string, topK?: number) {
  const response = await fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, top_k: topK }),
  });
  if (!response.ok) throw new Error('Chat request failed');
  return response.json();
}

export async function searchKnowledge(query: string, topK?: number) {
  const params = new URLSearchParams({ query, top_k: String(topK || 5) });
  const response = await fetch(`${API_BASE}/search?${params}`, {
    method: 'POST',
  });
  if (!response.ok) throw new Error('Search request failed');
  return response.json();
}

export async function getKnowledgeList(skip = 0, limit = 100) {
  const response = await fetch(`${API_BASE}/knowledge?skip=${skip}&limit=${limit}`);
  if (!response.ok) throw new Error('Failed to fetch knowledge list');
  return response.json();
}

export async function getKnowledge(id: string) {
  const response = await fetch(`${API_BASE}/knowledge/${id}`);
  if (!response.ok) throw new Error('Failed to fetch knowledge');
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

export async function updateKnowledge(id: string, data: {
  title?: string;
  content?: string;
  content_type?: string;
  source?: string;
  language?: string;
  tags?: string[];
  category?: string;
}) {
  const response = await fetch(`${API_BASE}/knowledge/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!response.ok) throw new Error('Failed to update knowledge');
  return response.json();
}

export async function deleteKnowledge(id: string) {
  const response = await fetch(`${API_BASE}/knowledge/${id}`, {
    method: 'DELETE',
  });
  if (!response.ok) throw new Error('Failed to delete knowledge');
  return response.json();
}

export async function importKnowledge(items: any[]) {
  const response = await fetch(`${API_BASE}/knowledge/import`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ items }),
  });
  if (!response.ok) throw new Error('Failed to import knowledge');
  return response.json();
}

export async function exportKnowledge() {
  const response = await fetch(`${API_BASE}/knowledge/export`);
  if (!response.ok) throw new Error('Failed to export knowledge');
  return response.json();
}

export async function getChatHistory(skip = 0, limit = 50) {
  const response = await fetch(`${API_BASE}/chat/history?skip=${skip}&limit=${limit}`);
  if (!response.ok) throw new Error('Failed to fetch chat history');
  return response.json();
}

export async function getModels() {
  const response = await fetch(`${API_BASE}/system/models`);
  if (!response.ok) throw new Error('Failed to fetch models');
  return response.json();
}

export async function switchModel(modelId: string) {
  const response = await fetch(`${API_BASE}/system/models/switch`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ model_id: modelId }),
  });
  if (!response.ok) throw new Error('Failed to switch model');
  return response.json();
}

export async function getStats() {
  const response = await fetch(`${API_BASE}/system/stats`);
  if (!response.ok) throw new Error('Failed to fetch stats');
  return response.json();
}
