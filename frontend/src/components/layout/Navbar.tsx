import React, { useState, useEffect } from 'react';
import { AppBar, Toolbar, Typography, Box, IconButton, Badge, Chip, Tooltip, Avatar } from '@mui/material';
import { Notifications as NotifIcon, AccountCircle as AccountIcon, AutoAwesome as AIIcon, Circle as CircleIcon } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

interface NavbarProps { sidebarWidth: number; }

const Navbar: React.FC<NavbarProps> = ({ sidebarWidth }) => {
  const navigate = useNavigate();
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const t = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(t);
  }, []);

  return (
    <AppBar
      position="fixed"
      elevation={0}
      sx={{
        zIndex: (theme) => theme.zIndex.drawer + 1,
        width: `calc(100% - ${sidebarWidth}px)`,
        ml: `${sidebarWidth}px`,
        bgcolor: 'rgba(255,255,255,0.92)',
        backdropFilter: 'blur(12px)',
        borderBottom: '1px solid rgba(226,232,240,0.8)',
        color: 'text.primary',
      }}
    >
      <Toolbar sx={{ minHeight: 64, px: 3 }}>
        {/* Brand */}
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5, flexGrow: 1 }}>
          <Box sx={{
            width: 36, height: 36, borderRadius: 2,
            background: 'linear-gradient(135deg, #6366f1 0%, #06b6d4 100%)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
          }}>
            <AIIcon sx={{ color: '#fff', fontSize: 20 }} />
          </Box>
          <Box>
            <Typography variant="subtitle1" sx={{ fontWeight: 700, lineHeight: 1.2, color: '#0f172a' }}>
              AutonomIQ
            </Typography>
            <Typography variant="caption" sx={{ color: '#64748b', lineHeight: 1 }}>
              Agentic Enterprise Workflows
            </Typography>
          </Box>
        </Box>

        {/* Live status */}
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mr: 2 }}>
          <Chip
            icon={<CircleIcon sx={{ fontSize: '10px !important', color: '#10b981 !important' }} />}
            label="4 Agents Live"
            size="small"
            sx={{ bgcolor: '#f0fdf4', color: '#166534', border: '1px solid #bbf7d0', fontWeight: 600 }}
          />
          <Chip
            label="2 Processing"
            size="small"
            sx={{ bgcolor: '#fffbeb', color: '#92400e', border: '1px solid #fde68a', fontWeight: 600 }}
          />
          <Typography variant="caption" sx={{ color: '#94a3b8', fontFamily: 'monospace', fontWeight: 600 }}>
            {time.toLocaleTimeString()}
          </Typography>
        </Box>

        {/* Actions */}
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
          <Tooltip title="Notifications">
            <IconButton size="small" sx={{ color: '#64748b' }}>
              <Badge badgeContent={3} color="error">
                <NotifIcon fontSize="small" />
              </Badge>
            </IconButton>
          </Tooltip>
          <Tooltip title="Account">
            <IconButton size="small" onClick={() => navigate('/settings')} sx={{ color: '#64748b' }}>
              <Avatar sx={{ width: 32, height: 32, bgcolor: '#6366f1', fontSize: 14, fontWeight: 700 }}>
                A
              </Avatar>
            </IconButton>
          </Tooltip>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
