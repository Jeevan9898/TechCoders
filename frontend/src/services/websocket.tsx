/**
 * WebSocket Service for Multi-Agent RFP System
 * 
 * Provides real-time communication between the frontend and backend
 * for live updates on RFP processing, agent status, and system events.
 */

import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { io, Socket } from 'socket.io-client';

interface WebSocketContextType {
  socket: Socket | null;
  isConnected: boolean;
  lastMessage: any;
  sendMessage: (event: string, data: any) => void;
}

const WebSocketContext = createContext<WebSocketContextType>({
  socket: null,
  isConnected: false,
  lastMessage: null,
  sendMessage: () => {},
});

export const useWebSocket = () => {
  const context = useContext(WebSocketContext);
  if (!context) {
    throw new Error('useWebSocket must be used within a WebSocketProvider');
  }
  return context;
};

interface WebSocketProviderProps {
  children: ReactNode;
}

export const WebSocketProvider: React.FC<WebSocketProviderProps> = ({ children }) => {
  const [socket, setSocket] = useState<Socket | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState<any>(null);

  useEffect(() => {
    // Initialize WebSocket connection
    const newSocket = io(process.env.REACT_APP_WS_URL || 'ws://localhost:8000', {
      transports: ['websocket'],
      autoConnect: true,
    });

    // Connection event handlers
    newSocket.on('connect', () => {
      console.log('WebSocket connected');
      setIsConnected(true);
    });

    newSocket.on('disconnect', () => {
      console.log('WebSocket disconnected');
      setIsConnected(false);
    });

    newSocket.on('connect_error', (error) => {
      console.error('WebSocket connection error:', error);
      setIsConnected(false);
    });

    // System event handlers
    newSocket.on('rfp_detected', (data) => {
      console.log('New RFP detected:', data);
      setLastMessage({ type: 'rfp_detected', data, timestamp: new Date() });
    });

    newSocket.on('rfp_status_update', (data) => {
      console.log('RFP status updated:', data);
      setLastMessage({ type: 'rfp_status_update', data, timestamp: new Date() });
    });

    newSocket.on('agent_status_update', (data) => {
      console.log('Agent status updated:', data);
      setLastMessage({ type: 'agent_status_update', data, timestamp: new Date() });
    });

    newSocket.on('workflow_progress', (data) => {
      console.log('Workflow progress:', data);
      setLastMessage({ type: 'workflow_progress', data, timestamp: new Date() });
    });

    newSocket.on('system_alert', (data) => {
      console.log('System alert:', data);
      setLastMessage({ type: 'system_alert', data, timestamp: new Date() });
    });

    newSocket.on('pricing_update', (data) => {
      console.log('Pricing update:', data);
      setLastMessage({ type: 'pricing_update', data, timestamp: new Date() });
    });

    newSocket.on('technical_match_complete', (data) => {
      console.log('Technical match complete:', data);
      setLastMessage({ type: 'technical_match_complete', data, timestamp: new Date() });
    });

    setSocket(newSocket);

    // Cleanup on unmount
    return () => {
      newSocket.close();
    };
  }, []);

  const sendMessage = (event: string, data: any) => {
    if (socket && isConnected) {
      socket.emit(event, data);
    } else {
      console.warn('WebSocket not connected. Cannot send message:', event, data);
    }
  };

  const contextValue: WebSocketContextType = {
    socket,
    isConnected,
    lastMessage,
    sendMessage,
  };

  return (
    <WebSocketContext.Provider value={contextValue}>
      {children}
    </WebSocketContext.Provider>
  );
};

// Custom hooks for specific event types
export const useRFPUpdates = () => {
  const { lastMessage } = useWebSocket();
  const [rfpUpdates, setRfpUpdates] = useState<any[]>([]);

  useEffect(() => {
    if (lastMessage && (lastMessage.type === 'rfp_detected' || lastMessage.type === 'rfp_status_update')) {
      setRfpUpdates(prev => [lastMessage, ...prev.slice(0, 9)]); // Keep last 10 updates
    }
  }, [lastMessage]);

  return rfpUpdates;
};

export const useAgentUpdates = () => {
  const { lastMessage } = useWebSocket();
  const [agentUpdates, setAgentUpdates] = useState<any[]>([]);

  useEffect(() => {
    if (lastMessage && lastMessage.type === 'agent_status_update') {
      setAgentUpdates(prev => [lastMessage, ...prev.slice(0, 9)]); // Keep last 10 updates
    }
  }, [lastMessage]);

  return agentUpdates;
};

export const useWorkflowUpdates = () => {
  const { lastMessage } = useWebSocket();
  const [workflowUpdates, setWorkflowUpdates] = useState<any[]>([]);

  useEffect(() => {
    if (lastMessage && lastMessage.type === 'workflow_progress') {
      setWorkflowUpdates(prev => [lastMessage, ...prev.slice(0, 9)]); // Keep last 10 updates
    }
  }, [lastMessage]);

  return workflowUpdates;
};

export const useSystemAlerts = () => {
  const { lastMessage } = useWebSocket();
  const [alerts, setAlerts] = useState<any[]>([]);

  useEffect(() => {
    if (lastMessage && lastMessage.type === 'system_alert') {
      setAlerts(prev => [lastMessage, ...prev.slice(0, 4)]); // Keep last 5 alerts
    }
  }, [lastMessage]);

  return alerts;
};