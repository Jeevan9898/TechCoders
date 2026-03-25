/**
 * AutonomIQ — Main Dashboard
 * Agentic AI for Autonomous Enterprise Workflows
 */

import React, { useState, useEffect } from 'react';
import {
  Box, Grid, Card, CardContent, Typography, LinearProgress,
  Chip, Avatar, Button, IconButton, Divider, List, ListItem,
  ListItemAvatar, ListItemText, Tooltip,
} from '@mui/material';
import {
  TrendingUp, SmartToy, Description, AttachMoney, Speed,
  CheckCircle, Warning, Error as ErrorIcon, Refresh,
  ArrowUpward, ArrowDownward, AutoAwesome, Timeline,
  FlashOn, Security, AccountTree,
} from '@mui/icons-material';
import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip as RTooltip,
  ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell, Legend,
} from 'recharts';

/* ─── Mock Data ─────────────────────────────────────────────────── */
const kpis = [
  { label: 'Total RFPs',       value: '47',    delta: '+12%', up: true,  icon: <Description />,  color: '#6366f1', bg: '#eef2ff' },
  { label: 'Active Processing', value: '12',   delta: '+3',   up: true,  icon: <Speed />,         color: '#f59e0b', bg: '#fffbeb' },
  { label: 'Pipeline Value',   value: '$2.4M', delta: '+8%',  up: true,  icon: <AttachMoney />,   color: '#10b981', bg: '#f0fdf4' },
  { label: 'Autonomy Rate',    value: '94.2%', delta: '+1.8%',up: true,  icon: <AutoAwesome />,   color: '#06b6d4', bg: '#ecfeff' },
];

const areaData = [
  { day: 'Mon', autonomous: 8,  human: 2 },
  { day: 'Tue', autonomous: 12, human: 1 },
  { day: 'Wed', autonomous: 9,  human: 3 },
  { day: 'Thu', autonomous: 15, human: 1 },
  { day: 'Fri', autonomous: 11, human: 2 },
  { day: 'Sat', autonomous: 6,  human: 0 },
  { day: 'Sun', autonomous: 4,  human: 1 },
];

const barData = [
  { stage: 'Detect',     count: 47 },
  { stage: 'Analyze',    count: 41 },
  { stage: 'Match',      count: 38 },
  { stage: 'Price',      count: 35 },
  { stage: 'Review',     count: 30 },
  { stage: 'Submit',     count: 28 },
];

const pieData = [
  { name: 'Completed',  value: 28, color: '#10b981' },
  { name: 'Processing', value: 12, color: '#6366f1' },
  { name: 'Pending',    value: 7,  color: '#f59e0b' },
];

const agents = [
  { name: 'RFP Identification', status: 'active',     eff: 94, tasks: 156, color: '#6366f1' },
  { name: 'Orchestrator',       status: 'active',     eff: 98, tasks: 89,  color: '#10b981' },
  { name: 'Technical Match',    status: 'processing', eff: 91, tasks: 78,  color: '#f59e0b' },
  { name: 'Pricing Agent',      status: 'warning',    eff: 89, tasks: 67,  color: '#ef4444' },
];

const recentActivity = [
  { id: 'BK-2024-047', title: 'Enterprise Software Modernization', status: 'processing', value: '$500K', time: '2m ago',  priority: 'high' },
  { id: 'BK-2024-046', title: 'Cybersecurity Infrastructure',      status: 'matched',    value: '$300K', time: '18m ago', priority: 'urgent' },
  { id: 'BK-2024-045', title: 'Cloud Migration Services',          status: 'priced',     value: '$750K', time: '1h ago',  priority: 'medium' },
  { id: 'BK-2024-044', title: 'IT Training Program',               status: 'reviewed',   value: '$150K', time: '3h ago',  priority: 'low' },
];

const auditLog = [
  { time: '14:32', agent: 'Orchestrator',    action: 'Routed RFP-047 to Technical Match Agent',       type: 'info' },
  { time: '14:28', agent: 'Pricing Agent',   action: 'Auto-corrected pricing model — SLA risk avoided', type: 'success' },
  { time: '14:15', agent: 'RFP Identifier',  action: 'Detected 3 new RFPs from Gov portal',            type: 'info' },
  { time: '13:58', agent: 'Technical Match', action: 'Escalated RFP-043 — low confidence score (62%)', type: 'warning' },
  { time: '13:44', agent: 'Orchestrator',    action: 'Self-corrected workflow after API timeout',       type: 'success' },
];

/* ─── Helpers ───────────────────────────────────────────────────── */
const statusChip = (s: string) => {
  const map: Record<string, { color: string; bg: string }> = {
    processing: { color: '#92400e', bg: '#fef3c7' },
    matched:    { color: '#1e40af', bg: '#dbeafe' },
    priced:     { color: '#5b21b6', bg: '#ede9fe' },
    reviewed:   { color: '#065f46', bg: '#d1fae5' },
    active:     { color: '#065f46', bg: '#d1fae5' },
    warning:    { color: '#92400e', bg: '#fef3c7' },
  };
  const c = map[s] || { color: '#374151', bg: '#f3f4f6' };
  return (
    <Chip label={s} size="small"
      sx={{ bgcolor: c.bg, color: c.color, fontWeight: 700, fontSize: 11, height: 22, borderRadius: 1 }} />
  );
};

const priorityDot = (p: string) => {
  const c: Record<string, string> = { urgent: '#ef4444', high: '#f59e0b', medium: '#6366f1', low: '#10b981' };
  return <Box sx={{ width: 8, height: 8, borderRadius: '50%', bgcolor: c[p] || '#94a3b8', flexShrink: 0 }} />;
};

const auditIcon = (t: string) => {
  if (t === 'success') return <CheckCircle sx={{ fontSize: 16, color: '#10b981' }} />;
  if (t === 'warning') return <Warning sx={{ fontSize: 16, color: '#f59e0b' }} />;
  return <FlashOn sx={{ fontSize: 16, color: '#6366f1' }} />;
};

/* ─── Section Header ────────────────────────────────────────────── */
const SectionHeader: React.FC<{ title: string; sub?: string; action?: React.ReactNode }> = ({ title, sub, action }) => (
  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
    <Box>
      <Typography variant="h6" sx={{ fontWeight: 700, color: '#0f172a' }}>{title}</Typography>
      {sub && <Typography variant="caption" sx={{ color: '#94a3b8' }}>{sub}</Typography>}
    </Box>
    {action}
  </Box>
);

/* ─── Dashboard ─────────────────────────────────────────────────── */
const Dashboard: React.FC = () => {
  const [tick, setTick] = useState(0);
  useEffect(() => { const t = setInterval(() => setTick(x => x + 1), 5000); return () => clearInterval(t); }, []);

  return (
    <Box sx={{ maxWidth: 1400 }}>
      {/* Page header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Box>
          <Typography variant="h4" sx={{ fontWeight: 800, color: '#0f172a', letterSpacing: -0.5 }}>
            Command Center
          </Typography>
          <Typography variant="body2" sx={{ color: '#64748b', mt: 0.5 }}>
            Autonomous enterprise workflow intelligence · Real-time
          </Typography>
        </Box>
        <Box sx={{ display: 'flex', gap: 1.5, alignItems: 'center' }}>
          <Chip
            icon={<CheckCircle sx={{ fontSize: '14px !important' }} />}
            label="System Healthy"
            sx={{ bgcolor: '#f0fdf4', color: '#166534', border: '1px solid #bbf7d0', fontWeight: 600 }}
          />
          <Tooltip title="Refresh data">
            <IconButton size="small" sx={{ bgcolor: '#f8fafc', border: '1px solid #e2e8f0' }}>
              <Refresh fontSize="small" />
            </IconButton>
          </Tooltip>
        </Box>
      </Box>

      {/* KPI Cards */}
      <Grid container spacing={2.5} sx={{ mb: 3 }}>
        {kpis.map((k) => (
          <Grid item xs={12} sm={6} md={3} key={k.label}>
            <Card sx={{ p: 0, overflow: 'hidden' }}>
              <CardContent sx={{ p: 2.5, '&:last-child': { pb: 2.5 } }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                  <Box>
                    <Typography variant="caption" sx={{ color: '#64748b', fontWeight: 600, textTransform: 'uppercase', letterSpacing: 0.5 }}>
                      {k.label}
                    </Typography>
                    <Typography variant="h4" sx={{ fontWeight: 800, color: '#0f172a', mt: 0.5, lineHeight: 1 }}>
                      {k.value}
                    </Typography>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5, mt: 1 }}>
                      {k.up ? <ArrowUpward sx={{ fontSize: 12, color: '#10b981' }} /> : <ArrowDownward sx={{ fontSize: 12, color: '#ef4444' }} />}
                      <Typography variant="caption" sx={{ color: k.up ? '#10b981' : '#ef4444', fontWeight: 700 }}>
                        {k.delta}
                      </Typography>
                      <Typography variant="caption" sx={{ color: '#94a3b8' }}>vs last week</Typography>
                    </Box>
                  </Box>
                  <Box sx={{ width: 44, height: 44, borderRadius: 2.5, bgcolor: k.bg, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    {React.cloneElement(k.icon, { sx: { color: k.color, fontSize: 22 } })}
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Row 2: Chart + Agents */}
      <Grid container spacing={2.5} sx={{ mb: 2.5 }}>
        {/* Autonomy trend */}
        <Grid item xs={12} md={8}>
          <Card sx={{ height: '100%' }}>
            <CardContent sx={{ p: 2.5 }}>
              <SectionHeader
                title="Autonomous vs Human Interventions"
                sub="Weekly workflow completion breakdown"
                action={
                  <Chip label="Live" size="small"
                    sx={{ bgcolor: '#fef2f2', color: '#dc2626', fontWeight: 700, fontSize: 10,
                      animation: 'pulse 2s infinite', '@keyframes pulse': { '0%,100%': { opacity: 1 }, '50%': { opacity: 0.5 } } }} />
                }
              />
              <ResponsiveContainer width="100%" height={220}>
                <AreaChart data={areaData} margin={{ top: 5, right: 10, left: -20, bottom: 0 }}>
                  <defs>
                    <linearGradient id="autoGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%"  stopColor="#6366f1" stopOpacity={0.15} />
                      <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                    </linearGradient>
                    <linearGradient id="humanGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%"  stopColor="#f59e0b" stopOpacity={0.15} />
                      <stop offset="95%" stopColor="#f59e0b" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                  <XAxis dataKey="day" tick={{ fontSize: 12, fill: '#94a3b8' }} axisLine={false} tickLine={false} />
                  <YAxis tick={{ fontSize: 12, fill: '#94a3b8' }} axisLine={false} tickLine={false} />
                  <RTooltip contentStyle={{ borderRadius: 10, border: '1px solid #e2e8f0', boxShadow: '0 4px 16px rgba(0,0,0,0.08)' }} />
                  <Area type="monotone" dataKey="autonomous" stroke="#6366f1" strokeWidth={2.5} fill="url(#autoGrad)" name="Autonomous" />
                  <Area type="monotone" dataKey="human"      stroke="#f59e0b" strokeWidth={2.5} fill="url(#humanGrad)" name="Human" />
                </AreaChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Status pie */}
        <Grid item xs={12} md={4}>
          <Card sx={{ height: '100%' }}>
            <CardContent sx={{ p: 2.5 }}>
              <SectionHeader title="RFP Status" sub="Current distribution" />
              <ResponsiveContainer width="100%" height={160}>
                <PieChart>
                  <Pie data={pieData} cx="50%" cy="50%" innerRadius={45} outerRadius={70} paddingAngle={4} dataKey="value">
                    {pieData.map((e, i) => <Cell key={i} fill={e.color} />)}
                  </Pie>
                  <RTooltip contentStyle={{ borderRadius: 10, border: '1px solid #e2e8f0' }} />
                </PieChart>
              </ResponsiveContainer>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1, mt: 1 }}>
                {pieData.map((d) => (
                  <Box key={d.name} sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Box sx={{ width: 10, height: 10, borderRadius: '50%', bgcolor: d.color }} />
                      <Typography variant="caption" sx={{ color: '#64748b' }}>{d.name}</Typography>
                    </Box>
                    <Typography variant="caption" sx={{ fontWeight: 700, color: '#0f172a' }}>{d.value}</Typography>
                  </Box>
                ))}
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Row 3: Agents + Activity + Audit */}
      <Grid container spacing={2.5} sx={{ mb: 2.5 }}>
        {/* Agent health */}
        <Grid item xs={12} md={4}>
          <Card sx={{ height: '100%' }}>
            <CardContent sx={{ p: 2.5 }}>
              <SectionHeader title="Agent Health" sub="Real-time status" />
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                {agents.map((a) => (
                  <Box key={a.name}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 0.5 }}>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <Box sx={{ width: 8, height: 8, borderRadius: '50%', bgcolor: a.color }} />
                        <Typography variant="body2" sx={{ fontWeight: 600, color: '#0f172a', fontSize: 13 }}>{a.name}</Typography>
                      </Box>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <Typography variant="caption" sx={{ color: '#94a3b8' }}>{a.tasks} tasks</Typography>
                        {statusChip(a.status)}
                      </Box>
                    </Box>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <LinearProgress variant="determinate" value={a.eff}
                        sx={{ flexGrow: 1, height: 5, borderRadius: 3, bgcolor: '#f1f5f9',
                          '& .MuiLinearProgress-bar': { bgcolor: a.color, borderRadius: 3 } }} />
                      <Typography variant="caption" sx={{ fontWeight: 700, color: a.color, minWidth: 32 }}>{a.eff}%</Typography>
                    </Box>
                  </Box>
                ))}
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Recent RFPs */}
        <Grid item xs={12} md={4}>
          <Card sx={{ height: '100%' }}>
            <CardContent sx={{ p: 2.5 }}>
              <SectionHeader title="Recent RFPs" sub="Latest pipeline activity" />
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1.5 }}>
                {recentActivity.map((r) => (
                  <Box key={r.id} sx={{
                    p: 1.5, borderRadius: 2, bgcolor: '#f8fafc',
                    border: '1px solid #f1f5f9', cursor: 'pointer',
                    '&:hover': { bgcolor: '#f1f5f9', borderColor: '#e2e8f0' },
                    transition: 'all 0.15s',
                  }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 0.5 }}>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        {priorityDot(r.priority)}
                        <Typography variant="caption" sx={{ fontWeight: 700, color: '#6366f1' }}>{r.id}</Typography>
                      </Box>
                      <Typography variant="caption" sx={{ color: '#94a3b8' }}>{r.time}</Typography>
                    </Box>
                    <Typography variant="body2" sx={{ fontWeight: 600, color: '#0f172a', fontSize: 12, mb: 0.5, lineHeight: 1.3 }}>
                      {r.title}
                    </Typography>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      {statusChip(r.status)}
                      <Typography variant="caption" sx={{ fontWeight: 700, color: '#10b981' }}>{r.value}</Typography>
                    </Box>
                  </Box>
                ))}
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Audit log */}
        <Grid item xs={12} md={4}>
          <Card sx={{ height: '100%' }}>
            <CardContent sx={{ p: 2.5 }}>
              <SectionHeader
                title="Audit Trail"
                sub="Agent decision log"
                action={
                  <Chip label="Auto-logged" size="small"
                    sx={{ bgcolor: '#f0fdf4', color: '#166534', fontWeight: 600, fontSize: 10 }} />
                }
              />
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1.5 }}>
                {auditLog.map((log, i) => (
                  <Box key={i} sx={{ display: 'flex', gap: 1.5, alignItems: 'flex-start' }}>
                    <Box sx={{ mt: 0.2, flexShrink: 0 }}>{auditIcon(log.type)}</Box>
                    <Box sx={{ flexGrow: 1, minWidth: 0 }}>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <Typography variant="caption" sx={{ fontWeight: 700, color: '#6366f1' }}>{log.agent}</Typography>
                        <Typography variant="caption" sx={{ color: '#94a3b8', fontFamily: 'monospace' }}>{log.time}</Typography>
                      </Box>
                      <Typography variant="caption" sx={{ color: '#475569', lineHeight: 1.4, display: 'block' }}>
                        {log.action}
                      </Typography>
                    </Box>
                  </Box>
                ))}
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Row 4: Pipeline funnel */}
      <Card>
        <CardContent sx={{ p: 2.5 }}>
          <SectionHeader title="RFP Pipeline Funnel" sub="Conversion across processing stages" />
          <ResponsiveContainer width="100%" height={180}>
            <BarChart data={barData} margin={{ top: 5, right: 10, left: -20, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
              <XAxis dataKey="stage" tick={{ fontSize: 12, fill: '#94a3b8' }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fontSize: 12, fill: '#94a3b8' }} axisLine={false} tickLine={false} />
              <RTooltip contentStyle={{ borderRadius: 10, border: '1px solid #e2e8f0' }} />
              <Bar dataKey="count" fill="#6366f1" radius={[6, 6, 0, 0]} name="RFPs" />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Dashboard;
