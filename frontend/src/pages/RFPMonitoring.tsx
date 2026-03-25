import React, { useState, useEffect } from 'react';
import {
  Box, Card, CardContent, Typography, Table, TableBody, TableCell,
  TableContainer, TableHead, TableRow, TablePagination, Chip, IconButton,
  Button, TextField, FormControl, InputLabel, Select, MenuItem, Dialog,
  DialogTitle, DialogContent, DialogActions, LinearProgress, Tooltip,
  Grid, Snackbar,
} from '@mui/material';
import { apiService, CreateRFPRequest } from '../services/api.ts';
import { Visibility, PlayArrow, CheckCircle, Refresh, Add, FilterList, TrendingUp, Speed, Warning } from '@mui/icons-material';

const mockRFPs = [
  { id: 'RFP-047', title: 'Enterprise Software Modernization Initiative', source: 'Government Technology Portal',
    status: 'processing', priority: 'high',   dueDate: '2024-01-15', projectValue: 500000, progress: 65,
    detectedAt: '2024-01-01T10:00:00Z', requirements: 8,  matches: 12, agent: 'Technical Match Agent' },
  { id: 'RFP-046', title: 'High-Performance Computing Infrastructure',    source: 'Research University Procurement',
    status: 'matched',    priority: 'urgent', dueDate: '2024-01-10', projectValue: 750000, progress: 85,
    detectedAt: '2024-01-01T08:30:00Z', requirements: 6,  matches: 8,  agent: 'Pricing Agent' },
  { id: 'RFP-045', title: 'Cybersecurity Assessment and Implementation',  source: 'City Government Portal',
    status: 'priced',     priority: 'high',   dueDate: '2024-01-20', projectValue: 300000, progress: 90,
    detectedAt: '2024-01-01T14:15:00Z', requirements: 10, matches: 15, agent: 'Orchestrator Agent' },
  { id: 'RFP-044', title: 'IT Staff Training and Certification Program',  source: 'Corporate Procurement Portal',
    status: 'reviewed',   priority: 'medium', dueDate: '2024-01-25', projectValue: 150000, progress: 95,
    detectedAt: '2024-01-01T16:45:00Z', requirements: 5,  matches: 6,  agent: 'Human Review' },
  { id: 'RFP-043', title: 'Cloud Migration and Integration Services',     source: 'Enterprise RFP Platform',
    status: 'detected',   priority: 'low',    dueDate: '2024-02-01', projectValue: 425000, progress: 15,
    detectedAt: '2024-01-02T09:20:00Z', requirements: 0,  matches: 0,  agent: 'RFP Identification Agent' },
];

const statusStyle = (s: string) => (({
  detected:   { bg: '#f8fafc', color: '#475569' },
  processing: { bg: '#fffbeb', color: '#92400e' },
  matched:    { bg: '#eff6ff', color: '#1e40af' },
  priced:     { bg: '#faf5ff', color: '#6b21a8' },
  reviewed:   { bg: '#f0fdf4', color: '#166534' },
  approved:   { bg: '#f0fdf4', color: '#166534' },
  rejected:   { bg: '#fef2f2', color: '#991b1b' },
} as Record<string, { bg: string; color: string }>)[s] || { bg: '#f8fafc', color: '#475569' });

const priorityStyle = (p: string) => (({
  urgent: { bg: '#fef2f2', color: '#991b1b' },
  high:   { bg: '#fff7ed', color: '#9a3412' },
  medium: { bg: '#eff6ff', color: '#1e40af' },
  low:    { bg: '#f0fdf4', color: '#166534' },
} as Record<string, { bg: string; color: string }>)[p] || { bg: '#f8fafc', color: '#475569' });

const fmt = (n: number) => new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: 0 }).format(n);
const fmtDate = (d: string) => new Date(d).toLocaleDateString();

const RFPMonitoring: React.FC = () => {
  const [rfps, setRfps] = useState(mockRFPs);
  const [filtered, setFiltered] = useState(mockRFPs);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [selected, setSelected] = useState<any>(null);
  const [detailOpen, setDetailOpen] = useState(false);
  const [search, setSearch] = useState('');
  const [statusF, setStatusF] = useState('all');
  const [priorityF, setPriorityF] = useState('all');
  const [createOpen, setCreateOpen] = useState(false);
  const [newRfp, setNewRfp] = useState<CreateRFPRequest>({ title: '', source: '', priority: 'medium', dueDate: '', projectValue: 0, description: '' });
  const [creating, setCreating] = useState(false);
  const [snack, setSnack] = useState('');

  useEffect(() => {
    let f = rfps;
    if (search) f = f.filter(r => r.title.toLowerCase().includes(search.toLowerCase()) || r.source.toLowerCase().includes(search.toLowerCase()));
    if (statusF !== 'all') f = f.filter(r => r.status === statusF);
    if (priorityF !== 'all') f = f.filter(r => r.priority === priorityF);
    setFiltered(f);
    setPage(0);
  }, [rfps, search, statusF, priorityF]);

  const handleCreate = async () => {
    if (!newRfp.title || !newRfp.source || !newRfp.dueDate || !newRfp.projectValue) {
      setSnack('Please fill in all required fields'); return;
    }
    setCreating(true);
    try {
      const res = await apiService.createRFP(newRfp);
      setRfps(prev => [...prev, res.rfp]);
      setCreateOpen(false);
      setNewRfp({ title: '', source: '', priority: 'medium', dueDate: '', projectValue: 0, description: '' });
      setSnack('RFP created and workflow started!');
      const interval = setInterval(async () => {
        try { const u = await apiService.getRFPs(); setRfps(u); } catch {}
      }, 2000);
      setTimeout(() => clearInterval(interval), 300000);
    } catch {
      setSnack('Error creating RFP. Please try again.');
    } finally {
      setCreating(false);
    }
  };

  return (
    <Box sx={{ maxWidth: 1400 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Box>
          <Typography variant="h4" sx={{ fontWeight: 800, color: '#0f172a', letterSpacing: -0.5 }}>RFP Pipeline</Typography>
          <Typography variant="body2" sx={{ color: '#64748b', mt: 0.5 }}>Autonomous RFP detection, analysis, and response generation</Typography>
        </Box>
        <Box sx={{ display: 'flex', gap: 1.5 }}>
          <Button variant="outlined" size="small" startIcon={<Refresh />} onClick={() => window.location.reload()}
            sx={{ borderColor: '#e2e8f0', color: '#64748b' }}>Refresh</Button>
          <Button variant="contained" size="small" startIcon={<Add />} onClick={() => setCreateOpen(true)}>New RFP</Button>
        </Box>
      </Box>

      <Grid container spacing={2} sx={{ mb: 3 }}>
        {[
          { label: 'Total RFPs',      value: rfps.length,                                        color: '#6366f1', icon: <TrendingUp /> },
          { label: 'Processing',      value: rfps.filter(r => r.status === 'processing').length, color: '#f59e0b', icon: <Speed /> },
          { label: 'Ready to Review', value: rfps.filter(r => r.status === 'reviewed').length,   color: '#10b981', icon: <CheckCircle /> },
          { label: 'Urgent',          value: rfps.filter(r => r.priority === 'urgent').length,   color: '#ef4444', icon: <Warning /> },
        ].map((k) => (
          <Grid item xs={6} md={3} key={k.label}>
            <Card>
              <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Box>
                    <Typography variant="h4" sx={{ fontWeight: 800, color: k.color }}>{k.value}</Typography>
                    <Typography variant="caption" sx={{ color: '#64748b', fontWeight: 600 }}>{k.label}</Typography>
                  </Box>
                  <Box sx={{ width: 40, height: 40, borderRadius: 2, bgcolor: k.color + '15', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    {React.cloneElement(k.icon, { sx: { color: k.color, fontSize: 20 } })}
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Card sx={{ mb: 2.5 }}>
        <CardContent sx={{ p: 2 }}>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} md={4}>
              <TextField fullWidth size="small" label="Search RFPs" value={search}
                onChange={(e) => setSearch(e.target.value)} placeholder="Title or source…" />
            </Grid>
            <Grid item xs={6} md={2.5}>
              <FormControl fullWidth size="small">
                <InputLabel>Status</InputLabel>
                <Select value={statusF} label="Status" onChange={(e) => setStatusF(e.target.value)}>
                  <MenuItem value="all">All</MenuItem>
                  {['detected','processing','matched','priced','reviewed'].map(s => <MenuItem key={s} value={s}>{s}</MenuItem>)}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={6} md={2.5}>
              <FormControl fullWidth size="small">
                <InputLabel>Priority</InputLabel>
                <Select value={priorityF} label="Priority" onChange={(e) => setPriorityF(e.target.value)}>
                  <MenuItem value="all">All</MenuItem>
                  {['urgent','high','medium','low'].map(p => <MenuItem key={p} value={p}>{p}</MenuItem>)}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={3}>
              <Button fullWidth variant="outlined" size="small" startIcon={<FilterList />}
                onClick={() => { setSearch(''); setStatusF('all'); setPriorityF('all'); }}
                sx={{ borderColor: '#e2e8f0', color: '#64748b' }}>
                Clear Filters
              </Button>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      <Card>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow sx={{ bgcolor: '#f8fafc' }}>
                {['RFP', 'Source', 'Status', 'Priority', 'Due Date', 'Value', 'Progress', 'Actions'].map(h => (
                  <TableCell key={h} sx={{ fontWeight: 700, color: '#374151', fontSize: 12, textTransform: 'uppercase', letterSpacing: 0.5 }}>{h}</TableCell>
                ))}
              </TableRow>
            </TableHead>
            <TableBody>
              {filtered.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage).map((rfp) => {
                const ss = statusStyle(rfp.status);
                const ps = priorityStyle(rfp.priority);
                return (
                  <TableRow key={rfp.id} hover sx={{ '&:hover': { bgcolor: '#f8fafc' } }}>
                    <TableCell>
                      <Typography variant="caption" sx={{ fontWeight: 700, color: '#6366f1', display: 'block' }}>{rfp.id}</Typography>
                      <Typography variant="body2" sx={{ fontWeight: 600, color: '#0f172a', fontSize: 13, maxWidth: 220 }}>{rfp.title}</Typography>
                    </TableCell>
                    <TableCell><Typography variant="caption" sx={{ color: '#64748b' }}>{rfp.source}</Typography></TableCell>
                    <TableCell>
                      <Chip label={rfp.status} size="small" sx={{ bgcolor: ss.bg, color: ss.color, fontWeight: 700, fontSize: 10, height: 20, borderRadius: 1 }} />
                    </TableCell>
                    <TableCell>
                      <Chip label={rfp.priority} size="small" sx={{ bgcolor: ps.bg, color: ps.color, fontWeight: 700, fontSize: 10, height: 20, borderRadius: 1 }} />
                    </TableCell>
                    <TableCell><Typography variant="caption" sx={{ color: '#64748b' }}>{fmtDate(rfp.dueDate)}</Typography></TableCell>
                    <TableCell><Typography variant="body2" sx={{ fontWeight: 700, color: '#10b981' }}>{fmt(rfp.projectValue)}</Typography></TableCell>
                    <TableCell>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, minWidth: 80 }}>
                        <LinearProgress variant="determinate" value={rfp.progress}
                          sx={{ flexGrow: 1, height: 5, borderRadius: 3, bgcolor: '#f1f5f9',
                            '& .MuiLinearProgress-bar': { bgcolor: rfp.progress > 80 ? '#10b981' : '#6366f1', borderRadius: 3 } }} />
                        <Typography variant="caption" sx={{ fontWeight: 700, color: '#64748b', minWidth: 28 }}>{rfp.progress}%</Typography>
                      </Box>
                    </TableCell>
                    <TableCell>
                      <Box sx={{ display: 'flex', gap: 0.5 }}>
                        <Tooltip title="View Details">
                          <IconButton size="small" onClick={() => { setSelected(rfp); setDetailOpen(true); }} sx={{ color: '#6366f1' }}>
                            <Visibility fontSize="small" />
                          </IconButton>
                        </Tooltip>
                        {rfp.status === 'detected' && (
                          <Tooltip title="Start Processing">
                            <IconButton size="small" sx={{ color: '#10b981' }}
                              onClick={() => setRfps(prev => prev.map(r => r.id === rfp.id ? { ...r, status: 'processing', progress: 25 } : r))}>
                              <PlayArrow fontSize="small" />
                            </IconButton>
                          </Tooltip>
                        )}
                        {rfp.status === 'reviewed' && (
                          <Tooltip title="Approve">
                            <IconButton size="small" sx={{ color: '#10b981' }}
                              onClick={() => setRfps(prev => prev.map(r => r.id === rfp.id ? { ...r, status: 'approved', progress: 100 } : r))}>
                              <CheckCircle fontSize="small" />
                            </IconButton>
                          </Tooltip>
                        )}
                      </Box>
                    </TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
        </TableContainer>
        <TablePagination rowsPerPageOptions={[5, 10, 25]} component="div"
          count={filtered.length} rowsPerPage={rowsPerPage} page={page}
          onPageChange={(_, p) => setPage(p)}
          onRowsPerPageChange={(e) => { setRowsPerPage(parseInt(e.target.value, 10)); setPage(0); }} />
      </Card>

      {/* Detail Dialog */}
      <Dialog open={detailOpen} onClose={() => setDetailOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle sx={{ fontWeight: 700 }}>RFP Details</DialogTitle>
        <DialogContent>
          {selected && (
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1.5, pt: 1 }}>
              <Typography variant="h6" sx={{ fontWeight: 700, color: '#0f172a' }}>{selected.title}</Typography>
              {[
                { label: 'ID', value: selected.id },
                { label: 'Source', value: selected.source },
                { label: 'Due Date', value: fmtDate(selected.dueDate) },
                { label: 'Value', value: fmt(selected.projectValue) },
                { label: 'Current Agent', value: selected.agent },
                { label: 'Requirements', value: `${selected.requirements} extracted` },
                { label: 'Matches', value: `${selected.matches} products found` },
              ].map((row) => (
                <Box key={row.label} sx={{ display: 'flex', justifyContent: 'space-between', py: 0.5, borderBottom: '1px solid #f1f5f9' }}>
                  <Typography variant="body2" sx={{ color: '#64748b', fontWeight: 600 }}>{row.label}</Typography>
                  <Typography variant="body2" sx={{ color: '#0f172a', fontWeight: 600 }}>{row.value}</Typography>
                </Box>
              ))}
              <Box>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                  <Typography variant="body2" sx={{ color: '#64748b', fontWeight: 600 }}>Progress</Typography>
                  <Typography variant="body2" sx={{ fontWeight: 700 }}>{selected.progress}%</Typography>
                </Box>
                <LinearProgress variant="determinate" value={selected.progress}
                  sx={{ height: 8, borderRadius: 4, bgcolor: '#f1f5f9', '& .MuiLinearProgress-bar': { bgcolor: '#6366f1', borderRadius: 4 } }} />
              </Box>
            </Box>
          )}
        </DialogContent>
        <DialogActions sx={{ p: 2 }}>
          <Button onClick={() => setDetailOpen(false)} sx={{ color: '#64748b' }}>Close</Button>
        </DialogActions>
      </Dialog>

      {/* Create Dialog */}
      <Dialog open={createOpen} onClose={() => setCreateOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle sx={{ fontWeight: 700 }}>Create New RFP</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 0.5 }}>
            <Grid item xs={12}>
              <TextField fullWidth label="RFP Title" required value={newRfp.title}
                onChange={(e) => setNewRfp(p => ({ ...p, title: e.target.value }))} />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField fullWidth label="Source" required value={newRfp.source}
                onChange={(e) => setNewRfp(p => ({ ...p, source: e.target.value }))} />
            </Grid>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth required>
                <InputLabel>Priority</InputLabel>
                <Select value={newRfp.priority} label="Priority" onChange={(e) => setNewRfp(p => ({ ...p, priority: e.target.value }))}>
                  {['low','medium','high','urgent'].map(v => <MenuItem key={v} value={v}>{v}</MenuItem>)}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField fullWidth label="Due Date" type="date" required value={newRfp.dueDate}
                onChange={(e) => setNewRfp(p => ({ ...p, dueDate: e.target.value }))}
                InputLabelProps={{ shrink: true }} />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField fullWidth label="Project Value (USD)" type="number" required
                value={newRfp.projectValue || ''}
                onChange={(e) => setNewRfp(p => ({ ...p, projectValue: parseInt(e.target.value) || 0 }))} />
            </Grid>
            <Grid item xs={12}>
              <TextField fullWidth label="Description (Optional)" multiline rows={3}
                value={newRfp.description}
                onChange={(e) => setNewRfp(p => ({ ...p, description: e.target.value }))} />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions sx={{ p: 2 }}>
          <Button onClick={() => setCreateOpen(false)} disabled={creating} sx={{ color: '#64748b' }}>Cancel</Button>
          <Button variant="contained" onClick={handleCreate} disabled={creating}>
            {creating ? 'Creating…' : 'Create & Start Workflow'}
          </Button>
        </DialogActions>
      </Dialog>

      <Snackbar open={!!snack} autoHideDuration={5000} onClose={() => setSnack('')} message={snack} />
    </Box>
  );
};

export default RFPMonitoring;
