/**
 * API Service for Multi-Agent RFP System
 * 
 * This service handles all HTTP requests to the backend API,
 * providing a centralized interface for data fetching and mutations.
 */

import axios, { AxiosInstance, AxiosResponse } from 'axios';

// API Configuration
const API_BASE_URL = (window as any).REACT_APP_API_URL || 'http://localhost:8000';

// Create axios instance with default configuration
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for adding auth tokens (if needed)
apiClient.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// Type definitions
export interface RFP {
  id: string;
  title: string;
  source: string;
  status: 'processing' | 'matched' | 'priced' | 'reviewed' | 'submitted';
  priority: 'low' | 'medium' | 'high' | 'urgent';
  dueDate: string;
  projectValue: number;
  progress: number;
  detectedAt: string;
  requirements: number;
  matches: number;
  agent: string;
}

export interface CreateRFPRequest {
  title: string;
  source: string;
  priority: string;
  dueDate: string;
  projectValue: number;
  description?: string;
}

export interface Workflow {
  id: string;
  rfpId: string;
  rfpTitle: string;
  status: 'processing' | 'completed' | 'error';
  progress: number;
  startTime: string;
  estimatedCompletion: string;
  currentStep: number;
  steps: WorkflowStep[];
}

export interface WorkflowStep {
  id: string;
  name: string;
  agent: string;
  status: 'pending' | 'processing' | 'completed' | 'error';
  startTime: string | null;
  endTime: string | null;
  duration: number | null;
  output: string;
}

export interface Agent {
  id: string;
  name: string;
  type: string;
  status: 'active' | 'idle' | 'processing' | 'error';
  health: 'healthy' | 'warning' | 'error';
  uptime: string;
  processed: number;
  efficiency: number;
  currentTask: string;
  lastActivity: string;
}

export interface DashboardMetrics {
  totalRFPs: number;
  activeRFPs: number;
  completedRFPs: number;
  totalValue: number;
  activeAgents: number;
  avgEfficiency: number;
  lastUpdate: string;
}

// API Service Class
class ApiService {
  // Health Check
  async healthCheck(): Promise<any> {
    const response = await apiClient.get('/health');
    return response.data;
  }

  // RFP Endpoints
  async getRFPs(): Promise<RFP[]> {
    const response = await apiClient.get('/api/v1/rfps/');
    return response.data;
  }

  async getRFP(id: string): Promise<RFP> {
    const response = await apiClient.get(`/api/v1/rfps/${id}`);
    return response.data;
  }

  async createRFP(rfpData: CreateRFPRequest): Promise<any> {
    const response = await apiClient.post('/api/v1/rfps/', rfpData);
    return response.data;
  }

  // Workflow Endpoints
  async getWorkflows(): Promise<Workflow[]> {
    const response = await apiClient.get('/api/v1/workflows/');
    return response.data;
  }

  async getWorkflow(id: string): Promise<Workflow> {
    const response = await apiClient.get(`/api/v1/workflows/${id}`);
    return response.data;
  }

  // Agent Endpoints
  async getAgents(): Promise<Agent[]> {
    const response = await apiClient.get('/api/v1/agents/');
    return response.data;
  }

  async getAgent(id: string): Promise<Agent> {
    const response = await apiClient.get(`/api/v1/agents/${id}`);
    return response.data;
  }

  // Dashboard Endpoints
  async getDashboardMetrics(): Promise<DashboardMetrics> {
    const response = await apiClient.get('/api/v1/dashboard/metrics');
    return response.data;
  }

  // System Information
  async getSystemInfo(): Promise<any> {
    const response = await apiClient.get('/');
    return response.data;
  }
}

// Export singleton instance
export const apiService = new ApiService();
export default apiService;