/**
 * AutonomIQ - Agentic AI for Autonomous Enterprise Workflows
 * Main Application Entry Point
 */

import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { CssBaseline, Box } from '@mui/material';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

import Sidebar from './components/layout/Sidebar.tsx';
import Navbar from './components/layout/Navbar.tsx';
import Dashboard from './pages/Dashboard.tsx';
import RFPMonitoring from './pages/RFPMonitoring.tsx';
import AgentStatus from './pages/AgentStatus.tsx';
import WorkflowVisualization from './pages/WorkflowVisualization.tsx';
import Settings from './pages/Settings.tsx';
import { WebSocketProvider } from './services/websocket.tsx';

const queryClient = new QueryClient({
  defaultOptions: { queries: { refetchOnWindowFocus: false, retry: 1, staleTime: 30000 } },
});

const theme = createTheme({
  palette: {
    mode: 'light',
    primary:   { main: '#6366f1', light: '#818cf8', dark: '#4f46e5' },
    secondary: { main: '#06b6d4', light: '#22d3ee', dark: '#0891b2' },
    success:   { main: '#10b981' },
    warning:   { main: '#f59e0b' },
    error:     { main: '#ef4444' },
    background:{ default: '#f1f5f9', paper: '#ffffff' },
    text:      { primary: '#0f172a', secondary: '#64748b' },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", sans-serif',
    h4: { fontWeight: 700 },
    h5: { fontWeight: 600 },
    h6: { fontWeight: 600 },
  },
  shape: { borderRadius: 12 },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          boxShadow: '0 1px 3px rgba(0,0,0,0.07), 0 4px 16px rgba(0,0,0,0.05)',
          borderRadius: 16,
          border: '1px solid rgba(226,232,240,0.8)',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: { textTransform: 'none', borderRadius: 10, fontWeight: 600 },
        containedPrimary: {
          background: 'linear-gradient(135deg, #6366f1 0%, #4f46e5 100%)',
          boxShadow: '0 4px 14px rgba(99,102,241,0.35)',
          '&:hover': { boxShadow: '0 6px 20px rgba(99,102,241,0.45)' },
        },
      },
    },
    MuiChip: {
      styleOverrides: { root: { fontWeight: 600, borderRadius: 8 } },
    },
  },
});

const SIDEBAR_WIDTH = 260;
const NAVBAR_HEIGHT = 64;

const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <WebSocketProvider>
          <Router>
            <Box sx={{ display: 'flex', minHeight: '100vh', bgcolor: 'background.default' }}>
              <Navbar sidebarWidth={SIDEBAR_WIDTH} />
              <Sidebar width={SIDEBAR_WIDTH} navbarHeight={NAVBAR_HEIGHT} />
              <Box
                component="main"
                sx={{
                  flexGrow: 1,
                  mt: `${NAVBAR_HEIGHT}px`,
                  ml: `${SIDEBAR_WIDTH}px`,
                  p: 3,
                  minHeight: `calc(100vh - ${NAVBAR_HEIGHT}px)`,
                  bgcolor: 'background.default',
                }}
              >
                <Routes>
                  <Route path="/" element={<Dashboard />} />
                  <Route path="/rfps" element={<RFPMonitoring />} />
                  <Route path="/agents" element={<AgentStatus />} />
                  <Route path="/workflows" element={<WorkflowVisualization />} />
                  <Route path="/settings" element={<Settings />} />
                  <Route path="*" element={<Navigate to="/" replace />} />
                </Routes>
              </Box>
            </Box>
          </Router>
        </WebSocketProvider>
      </ThemeProvider>
    </QueryClientProvider>
  );
};

export default App;
