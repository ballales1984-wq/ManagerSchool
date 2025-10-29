/**
 * API Configuration - ManagerSchool Mobile
 */

// Configurazione base URL
export const API_BASE_URL = 'http://localhost:5000/api';

// Endpoints API
export const API_ENDPOINTS = {
  // Authentication
  login: '/auth/login',
  logout: '/auth/logout',
  
  // Students
  studenti: '/studenti',
  studenteById: (id) => `/studenti/${id}`,
  
  // Grades
  voti: '/voti',
  votiStudente: (id) => `/voti/studente/${id}`,
  
  // Reports
  report: '/report',
  pagelle: '/pagelle',
  
  // Dashboard
  dashboardStats: '/dashboard/stats',
  dashboardCharts: '/dashboard/charts',
  
  // Communication
  comunicazioni: '/comunicazioni',
  
  // Quick Insert
  inserimentoRapido: '/inserimento-rapido/voto',
};

// Headers default
export const getDefaultHeaders = (token) => ({
  'Content-Type': 'application/json',
  'Authorization': `Bearer ${token}`
});

// API Client
export class APIClient {
  constructor(baseURL = API_BASE_URL) {
    this.baseURL = baseURL;
    this.token = null;
  }
  
  setToken(token) {
    this.token = token;
  }
  
  async get(endpoint, params = {}) {
    const url = new URL(`${this.baseURL}${endpoint}`);
    Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));
    
    const response = await fetch(url, {
      headers: getDefaultHeaders(this.token)
    });
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    return response.json();
  }
  
  async post(endpoint, data = {}) {
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      method: 'POST',
      headers: getDefaultHeaders(this.token),
      body: JSON.stringify(data)
    });
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    return response.json();
  }
  
  async put(endpoint, data = {}) {
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      method: 'PUT',
      headers: getDefaultHeaders(this.token),
      body: JSON.stringify(data)
    });
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    return response.json();
  }
  
  async delete(endpoint) {
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      method: 'DELETE',
      headers: getDefaultHeaders(this.token)
    });
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    return response.json();
  }
}

// Istanza singleton
export const apiClient = new APIClient();

