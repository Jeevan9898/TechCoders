import React, { useState, useEffect } from 'react';
import {
  Box, Grid, Card, CardContent, Typography, LinearProgress,
  Chip, Avatar, Button, IconButton, Switch, Tooltip,
} from '@mui/material';
import { Refresh, CheckCircle, Warning, Settings } from '@mui/icons-material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as RTooltip, ResponsiveContainer, Legend } from 'recharts';

const initialAgents = [
  { id: 'rfp-id', name: 'RFP Identification', role: 'Scans portals & classifies RFPs',
    status: 'active', health: 'healthy', uptime: '2d 14h', processed: 156,
    efficiency: 94, cpu: 23, mem: 45, errors: 2, avgTime: 1.2, enabled: true, color: '#6366f1',
    currentTask: 'Scanning Gov Contracts Portal — 3 new RFPs queued' },
  { id: 'orch', name: 'Orchestrator', role: 'Routes tasks & manages SLA compliance',
    status: 'active', health: 'healthy', uptime: '2d 14h', processed: 89,
    efficiency: 98, cpu: 15, mem: 38, errors: 0, avgTime: 0.8, enabled: true, color: '#10b981',
    currentTask: 'Coordinating workflow RFP-2024-047 — step 3/5' },
  { id: 'tech', name: 'Technical Match', role: 'Extracts requirements & matches products',
    status: 'processing', health: 'healthy', uptime: '2d 14h', processed: 78,
    efficiency: 91, cpu: 45, mem: 67, errors: 3, avgTime: 3.4, enabled: true, color: '#f59e0b',
    currentTask: 'Analyzing 8 requirements for Enterprise Software RFP' },
  { id: 'price', name: 'Pricing Agent', role: 'Builds competitive pricing strategies',
    status: 'idle', health: 'warning', uptime: '2d 14h', processed: 67,
    efficiency: 89, cpu: 8, mem: 32, errors: 5, avgTime: 2.1, enabled: true, color: '#ef4444',
    currentTask: 'Waiting for market data feed — retry in 2m' },
];

const perfData = [
  { t: '00:00', rfp: 8,  orch: 12, tech: 6,  price: 9  },
  { t: '04:00', rfp: 12, orch: 15, tech: 8,  price: 11 },
  { t: '08:00', rfp: 15, orch: 18, tech: 12, price: 14 },
  { t: '12:00', rfp: 18, orch: 20, tech: 15, price: 16 },
  { t: '16:00', rfp: 14, orch: 16, tech: 11, price: 13 },
  { t: '20:00', rfp: 10, orch: 12, tech: 8,  price: 10 },
];

const statusStyle = (s: string) => ({
  active:     { bg: '#f0fdf4', color: '#166534' },
  processing: { bg: '#fffbeb', color: '#92400e' },
  idle:       { bg: '#f8fafc', color: '#475569' },
  stopped:    { bg: '#fef2f2', color: '#991b1b' },
}[s] || { bg: '#f8fafc', color: '#475569' });

const AgentStatus: React.FC = () => {
  const [agents, setAgents] = useState(initialAgents);
  const [lastUpdate, setLastUpdate] = useState(new Date());

  useEffect(() => {
    const t = setInterval(() => {
      setLastUpdate(new Date());
      setAgents(prev => prev.map(a => ({
        ...a,
        cpu: Math.max(5, Math.min(85, a.cpu + (Math.random() - 0.5) * 8)),
        mem: Math.max(20, Math.min(90, a.mem + (Math.random() - 0.5) * 4)),
      })));
    }, 4000);
    return () => clearInterval(t);
  }, []);

  const handleToggle = (id: string) =>
    setAgents(prev => prev.map(a => a.id === id ? { ...a, enabled: !a.enabled, status: a.enabled ? 'stopped' : 'active' } : a));

  const handleRestart = (id: string) => {
    setAgents(prev => prev.map(a => a.id === id ? { ...a, status: 'processing', uptime: '0m' } : a));
    setTimeout(() => setAgents(prev => prev.map(a => a.id === id ? { ...a, status: 'active' } : a)), 2500);
  };

  const totalProcessed = agents.reduce((s, a) => s + a.processed, 0);
  const avgEff = (agents.reduce((s, a) => s + a.efficiency, 0) / agents.length).toFixed(1);
  const activeCount = agents.filter(a => a.status === 'active').length;
  const totalErrors = agents.reduce((s, a) => s + a.errors, 0);

  return (
    <Box sx={{ maxWidth: 1400 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Box>
          <Typography variant="h4" sx={{ fontWeight: 800, color: '#0f172a', letterSpacing: -0.5 }}>Agent Monitor</Typography>
          <Typography variant="body2" sx={{ color: '#64748b', mt: 0.5 }}>Real-time control and observability for all autonomous agents</Typography>
        </Box>
        <Button variant="outlined" size="small" startIcon={<Refresh />} onClick={() => setLastUpdate(new Date())}
          sx={{ borderColor: '#e2e8f0', color: '#64748b' }}>
          Refresh
        </Button>
      </Box>

      <Grid container spacing={2} sx={{ mb: 3 }}>
        {[
          { label: 'Active Agents',   value: activeCount,    color: '#10b981' },
          { label: 'Total Processed', value: totalProcessed, color: '#6366f1' },
          { label: 'Avg Efficiency',  value: `${avgEff}%`,   color: '#f59e0b' },
          { label: 'Total Errors',    value: totalErrors,    color: '#ef4444' },
        ].map((k) => (
          <Grid item xs={6} md={3} key={k.label}>
            <Card>
              <CardContent sx={{ p: 2, '&:last-child': { pb: 2 }, textAlign: 'center' }}>
                <Typography variant="h4" sx={{ fontWeight: 800, color: k.color }}>{k.value}</Typography>
                <Typography variant="caption" sx={{ color: '#64748b', fontWeight: 600 }}>{k.label}</Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Grid container spacing={2.5} sx={{ mb: 3 }}>
        {agents.map((agent) => {
          const ss = statusStyle(agent.status);
          return (
            <Grid item xs={12} md={6} key={agent.id}>
              <Card sx={{ position: 'relative', overflow: 'visible' }}>
                <Box sx={{ position: 'absolute', top: 0, left: 0, right: 0, height: 3, bgcolor: agent.color, borderRadius: '16px 16px 0 0' }} />
                <CardContent sx={{ p: 2.5, pt: 3 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5 }}>
                      <Avatar sx={{ width: 40, height: 40, bgcolor: agent.color + '20', color: agent.color, fontWeight: 800, fontSize: 14 }}>
                        {agent.name.charAt(0)}
                      </Avatar>
                      <Box>
                        <Typography variant="subtitle2" sx={{ fontWeight: 700, color: '#0f172a' }}>{agent.name}</Typography>
                        <Typography variant="caption" sx={{ color: '#94a3b8' }}>{agent.role}</Typography>
                      </Box>
                    </Box>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      {agent.health === 'healthy'
                        ? <CheckCircle sx={{ fontSize: 16, color: '#10b981' }} />
                        : <Warning sx={{ fontSize: 16, color: '#f59e0b' }} />}
                      <Chip label={agent.status} size="small"
                        sx={{ bgcolor: ss.bg, color: ss.color, fontWeight: 700, fontSize: 10, height: 20, borderRadius: 1 }} />
                    </Box>
                  </Box>

                  <Box sx={{ p: 1.5, bgcolor: '#f8fafc', borderRadius: 2, mb: 2, border: '1px solid #f1f5f9' }}>
                    <Typography variant="caption" sx={{ fontWeight: 700, color: agent.color, textTransform: 'uppercase', letterSpacing: 0.5, display: 'block', mb: 0.5 }}>
                      Current Task
                    </Typography>
                    <Typography variant="caption" sx={{ color: '#475569' }}>{agent.currentTask}</Typography>
                  </Box>

                  <Box sx={{ mb: 2 }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                      <Typography variant="caption" sx={{ color: '#64748b', fontWeight: 600 }}>Efficiency</Typography>
                      <Typography variant="caption" sx={{ fontWeight: 800, color: agent.color }}>{agent.efficiency}%</Typography>
                    </Box>
                    <LinearProgress variant="determinate" value={agent.efficiency}
                      sx={{ height: 6, borderRadius: 3, bgcolor: '#f1f5f9', '& .MuiLinearProgress-bar': { bgcolor: agent.color, borderRadius: 3 } }} />
                  </Box>

                  <Grid container spacing={1} sx={{ mb: 2 }}>
                    {[
                      { label: 'Processed', value: agent.processed },
                      { label: 'Errors',    value: agent.errors },
                      { label: 'Avg Time',  value: `${agent.avgTime}s` },
                      { label: 'Uptime',    value: agent.uptime },
                    ].map((s) => (
                      <Grid item xs={3} key={s.label}>
                        <Box sx={{ textAlign: 'center', p: 1, bgcolor: '#f8fafc', borderRadius: 1.5 }}>
                          <Typography variant="body2" sx={{ fontWeight: 800, color: '#0f172a', fontSize: 13 }}>{s.value}</Typography>
                          <Typography variant="caption" sx={{ color: '#94a3b8', fontSize: 10 }}>{s.label}</Typography>
                        </Box>
                      </Grid>
                    ))}
                  </Grid>

                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                      <Switch checked={agent.enabled} onChange={() => handleToggle(agent.id)} size="small" />
                      <Typography variant="caption" sx={{ color: '#64748b' }}>{agent.enabled ? 'Enabled' : 'Disabled'}</Typography>
                    </Box>
                    <Box sx={{ display: 'flex', gap: 0.5 }}>
                      <Tooltip title="Restart">
                        <IconButton size="small" onClick={() => handleRestart(agent.id)} sx={{ color: '#6366f1' }}>
                          <Refresh fontSize="small" />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Configure">
                        <IconButton size="small" sx={{ color: '#94a3b8' }}>
                          <Settings fontSize="small" />
                        </IconButton>
                      </Tooltip>
                    </Box>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          );
        })}
      </Grid>

      <Card>
        <CardContent sx={{ p: 2.5 }}>
          <Typography variant="h6" sx={{ fontWeight: 700, color: '#0f172a', mb: 0.5 }}>Agent Performance Over Time</Typography>
          <Typography variant="caption" sx={{ color: '#94a3b8', display: 'block', mb: 2 }}>Tasks completed per 4-hour window</Typography>
          <ResponsiveContainer width="100%" height={260}>
            <LineChart data={perfData} margin={{ top: 5, right: 10, left: -20, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
              <XAxis dataKey="t" tick={{ fontSize: 12, fill: '#94a3b8' }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fontSize: 12, fill: '#94a3b8' }} axisLine={false} tickLine={false} />
              <RTooltip contentStyle={{ borderRadius: 10, border: '1px solid #e2e8f0' }} />
              <Legend wrapperStyle={{ fontSize: 12 }} />
              <Line type="monotone" dataKey="rfp"   stroke="#6366f1" strokeWidth={2.5} dot={false} name="RFP Identification" />
              <Line type="monotone" dataKey="orch"  stroke="#10b981" strokeWidth={2.5} dot={false} name="Orchestrator" />
              <Line type="monotone" dataKey="tech"  stroke="#f59e0b" strokeWidth={2.5} dot={false} name="Technical Match" />
              <Line type="monotone" dataKey="price" stroke="#ef4444" strokeWidth={2.5} dot={false} name="Pricing" />
            </LineChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </Box>
  );
};

export default AgentStatus;
