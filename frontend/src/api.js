import axios from 'axios';

// Base API URL - will use proxy in development
const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Check API health status
 */
export const checkHealth = async () => {
  const response = await api.get('/health');
  return response.data;
};

/**
 * Create a new research query
 * @param {string} query - The research question
 * @param {boolean} stream - Whether to use streaming
 */
export const createQuery = async (query, stream = true) => {
  const response = await api.post('/query', { query, stream });
  return response.data;
};

/**
 * Get task status
 * @param {string} taskId - The task ID
 */
export const getTaskStatus = async (taskId) => {
  const response = await api.get(`/task/${taskId}`);
  return response.data;
};

/**
 * Get stream URL for SSE
 * @param {string} taskId - The task ID
 */
export const getStreamUrl = (taskId) => {
  const baseUrl = API_BASE_URL.startsWith('http') 
    ? API_BASE_URL 
    : `${window.location.origin}${API_BASE_URL}`;
  return `${baseUrl}/stream/${taskId}`;
};

/**
 * List all tasks
 */
export const listTasks = async () => {
  const response = await api.get('/tasks');
  return response.data;
};

/**
 * Delete a task
 * @param {string} taskId - The task ID
 */
export const deleteTask = async (taskId) => {
  const response = await api.delete(`/task/${taskId}`);
  return response.data;
};

export default api;

