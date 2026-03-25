import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Drawer, List, ListItem, ListItemButton, ListItemIcon, ListItemText, Box, Typography, Chip, Divider } from '@mui/material';
import {
  Dashboard as DashboardIcon, Description as RFPIcon, SmartToy as AgentIcon,
  AccountTree as WorkflowIcon, Settings as SettingsIcon, Circle as CircleIcon,
} from '@mui/icons-material';

interface SidebarProps { width: number; navbarHeight: number; }

const navItems = [
  { id: 'dashboard', label: 'Dashboard',        path: '/',          icon: <DashboardIcon />, badge: null },
  { id: 'rfps',      label: 'RFP Pipeline',     path: '/rfps',      icon: <RFPIcon />,       badge: '12' },
  { id: 'agents',    label: 'Agent Monitor',    path: '/agents',    icon: <AgentIcon />,     badge: '4' },
  { id: 'workflows', label: 'Workflow Engine',  path: '/workflows', icon: <WorkflowIcon />,  badge: '2' },
  { id: 'settings',  label: 'Settings',         path: '/settings',  icon: <SettingsIcon />,  badge: null },
];

const Sidebar: React.FC<SidebarProps> = ({ width, navbarHeight }) => {
  const location = useLocation();
  const navigate = useNavigate();

  return (
    <Drawer
      variant="permanent"
      sx={{
        width,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width,
          boxSizing: 'border-box',
          bgcolor: '#0f172a',
          borderRight: 'none',
          pt: `${navbarHeight}px`,
        },
      }}
    >
      {/* Logo area */}
      <Box sx={{ px: 3, py: 2.5, borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
        <Typography variant="overline" sx={{ color: '#475569', fontWeight: 700, letterSpacing: 2, fontSize: 10 }}>
          NAVIGATION
        </Typography>
      </Box>

      {/* Nav items */}
      <List sx={{ px: 1.5, py: 1.5, flexGrow: 1 }}>
        {navItems.map((item) => {
          const active = location.pathname === item.path;
          return (
            <ListItem key={item.id} disablePadding sx={{ mb: 0.5 }}>
              <ListItemButton
                onClick={() => navigate(item.path)}
                sx={{
                  borderRadius: 2,
                  px: 2, py: 1.2,
                  bgcolor: active ? 'rgba(99,102,241,0.15)' : 'transparent',
                  border: active ? '1px solid rgba(99,102,241,0.3)' : '1px solid transparent',
                  '&:hover': { bgcolor: 'rgba(255,255,255,0.05)' },
                  transition: 'all 0.15s ease',
                }}
              >
                <ListItemIcon sx={{ minWidth: 36, color: active ? '#818cf8' : '#475569' }}>
                  {item.icon}
                </ListItemIcon>
                <ListItemText
                  primary={item.label}
                  primaryTypographyProps={{
                    fontSize: '0.875rem',
                    fontWeight: active ? 600 : 400,
                    color: active ? '#e2e8f0' : '#94a3b8',
                  }}
                />
                {item.badge && (
                  <Chip
                    label={item.badge}
                    size="small"
                    sx={{
                      height: 18, fontSize: 10, fontWeight: 700,
                      bgcolor: active ? 'rgba(99,102,241,0.3)' : 'rgba(255,255,255,0.08)',
                      color: active ? '#a5b4fc' : '#64748b',
                      '& .MuiChip-label': { px: 0.8 },
                    }}
                  />
                )}
              </ListItemButton>
            </ListItem>
          );
        })}
      </List>

      {/* Footer */}
      <Box sx={{ px: 2.5, py: 2, borderTop: '1px solid rgba(255,255,255,0.06)' }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 0.5 }}>
          <CircleIcon sx={{ fontSize: 8, color: '#10b981' }} />
          <Typography variant="caption" sx={{ color: '#475569', fontWeight: 600 }}>
            All Systems Operational
          </Typography>
        </Box>
        <Typography variant="caption" sx={{ color: '#334155', fontSize: 10 }}>
          AutonomIQ v2.0 · Hackathon Build
        </Typography>
      </Box>
    </Drawer>
  );
};

export default Sidebar;
