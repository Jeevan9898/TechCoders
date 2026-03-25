import React, { useState, useEffect, useCallback } from 'react';
import { apiService, Workflow } from '../services/api.ts';
import {
  Box, Card, CardContent, Typography, Grid, Button, Chip,
  LinearProgress, Alert, Paper,
} from '@mui/material';
import {
  CheckCircle, RadioButtonUnchecked, Schedule, Error as ErrorIcon,
  Refresh, SmartToy, AccountTree,
} from '@mui/icons-material';

const mockWorkflows: Workflow[] = [
  {
    id: 'wf-001', rfpId: 'rfp-001', rfpTitle: 'Enterprise Software Modernization',
    status: 'processing' as const, progress: 65,
    startTime: '2024-01-01T10:00:00Z', estimatedCompletion: '2024-01-01T16:30:00Z',
    currentStep: 2,
    steps: [
      { id: 's1', name: 'RFP Detection',         agent: 'RFP Identification Agent', status: 'completed' as const, startTime: '2024-01-01T10:00:00Z', endTime: '2024-01-01T10:15:00Z', duration: 15, output: 'RFP detected and classified as High Priority' },
      { id: 's2', name: 'Workflow Orchestration', agent: 'Orchestrator Agent',       status: 'completed' as const, startTime: '2024-01-01T10:15:00Z', endTime: '2024-01-01T10:20:00Z', duration: 5,  output: 'Tasks distributed to 3 specialized agents' },
      { id: 's3', name: 'Technical Analysis',     agent: 'Technical Match Agent',    status: 'processing' as const, startTime: '2024-01-01T10:20:00Z', endTime: null, duration: null, output: 'Analyzing 8 requirements — 6/8 matched so far...' },
      { id: 's4', name: 'Pricing Analysis',       agent: 'Pricing Agent',            status: 'pending' as const,   startTime: null, endTime: null, duration: null, output: 'Waiting for technical analysis completion' },
      { id: 's5', name: 'Human Review',           agent: 'Human Reviewer',           status: 'pending' as const,   startTime: null, endTime: null, duration: null, output: 'Awaiting human approval' },
    ],
  },
  {
    id: 'wf-002', rfpId: 'rfp-002', rfpTitle: 'Cybersecurity Infrastructure',
    status: 'completed' as const, progress: 100,
    startTime: '2024-01-01T08:00:00Z', estimatedCompletion: '2024-01-01T14:00:00Z',
    currentStep: 4,
    steps: [
      { id: 's1', name: 'RFP Detection',         agent: 'RFP Identification Agent', status: 'completed' as const, startTime: '2024-01-01T08:00:00Z', endTime: '2024-01-01T08:12:00Z', duration: 12,  output: 'High-priority RFP detected from Gov portal' },
      { id: 's2', name: 'Workflow Orchestration', agent: 'Orchestrator Agent',       status: 'completed' as const, startTime: '2024-01-01T08:12:00Z', endTime: '2024-01-01T08:15:00Z', duration: 3,   output: 'Urgent workflow initiated — SLA: 6h' },
      { id: 's3', name: 'Technical Analysis',     agent: 'Technical Match Agent',    status: 'completed' as const, startTime: '2024-01-01T08:15:00Z', endTime: '2024-01-01T10:30:00Z', duration: 135, output: '15 matching products identified — 94% confidence' },
      { id: 's4', name: 'Pricing Analysis',       agent: 'Pricing Agent',            status: 'completed' as const, startTime: '2024-01-01T10:30:00Z', endTime: '2024-01-01T12:45:00Z', duration: 135, output: 'Competitive pricing strategy developed — $300K' },
      { id: 's5', name: 'Human Review',           agent: 'Human Reviewer',           status: 'completed' as const, startTime: '2024-01-01T12:45:00Z', endTime: '2024-01-01T14:00:00Z', duration: 75,  output: 'Proposal approved and submitted ✓' },
    ],
  },
];

const stepColor = (s: string) => ({ completed: '#10b981', processing: '#6366f1', error: '#ef4444', pending: '#cbd5e1' }[s] || '#cbd5e1');
const stepBg   = (s: string) => ({ completed: '#f0fdf4', processing: '#eef2ff', error: '#fef2f2', pending: '#f8fafc' }[s] || '#f8fafc');

const formatTime = (t: string | null) => t ? new Date(t).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : '—';
const formatDur  = (m: number | null) => !m ? '—' : m < 60 ? `${m}m` : `${Math.floor(m/60)}h ${m%60}m`;

const WorkflowVisualization: React.FC = () => {
  const [workflows, setWorkflows] = useState<Workflow[]>(mockWorkflows);
  const [selected, setSelected] = useState<Workflow>(mockWorkflows[0]);
  const [loading, setLoading] = useState(false);

  const fetchWorkflows = useCallback(async () => {
    try {
      setLoading(true);
      const api = await apiService.getWorkflows();
      const all = [...api, ...mockWorkflows];
      setWorkflows(all);
      const upd = all.find(w => w.id === selected?.id);
      if (upd) setSelected(upd);
    } catch {
      setWorkflows(mockWorkflows);
    } finally {
      setLoading(false);
    }
  }, [selected?.id]);

  useEffect(() => {
    fetchWorkflows();
    const t = setInterval(fetchWorkflows, 4000);
    return () => clearInterval(t);
  }, [fetchWorkflows]);

  const statusChipStyle = (s: string) => ({
    processing: { bg: '#eef2ff', color: '#4338ca' },
    completed:  { bg: '#f0fdf4', color: '#166534' },
    error:      { bg: '#fef2f2', color: '#991b1b' },
  }[s] || { bg: '#f8fafc', color: '#475569' });

  return (
    <Box sx={{ maxWidth: 1400 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Box>
          <Typography variant="h4" sx={{ fontWeight: 800, color: '#0f172a', letterSpacing: -0.5 }}>Workflow Engine</Typography>
          <Typography variant="body2" sx={{ color: '#64748b', mt: 0.5 }}>
            End-to-end autonomous workflow visualization with full audit trail
          </Typography>
        </Box>
        <Button variant="outlined" size="small" startIcon={<Refresh />} onClick={fetchWorkflows} disabled={loading}
          sx={{ borderColor: '#e2e8f0', color: '#64748b' }}>
          {loading ? 'Refreshing…' : 'Refresh'}
        </Button>
      </Box>

      <Grid container spacing={2.5}>
        {/* Workflow list */}
        <Grid item xs={12} md={4}>
          <Card sx={{ mb: 2 }}>
            <CardContent sx={{ p: 2.5 }}>
              <Typography variant="h6" sx={{ fontWeight: 700, color: '#0f172a', mb: 2 }}>Active Workflows</Typography>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1.5 }}>
                {workflows.map((wf) => {
                  const cs = statusChipStyle(wf.status);
                  const isSelected = selected.id === wf.id;
                  return (
                    <Box key={wf.id} onClick={() => setSelected(wf)}
                      sx={{
                        p: 2, borderRadius: 2, cursor: 'pointer',
                        border: `2px solid ${isSelected ? '#6366f1' : '#f1f5f9'}`,
                        bgcolor: isSelected ? '#eef2ff' : '#f8fafc',
                        transition: 'all 0.15s',
                        '&:hover': { borderColor: '#6366f1', bgcolor: '#eef2ff' },
                      }}>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 1 }}>
                        <Typography variant="caption" sx={{ fontWeight: 700, color: '#6366f1' }}>{wf.id}</Typography>
                        <Chip label={wf.status} size="small"
                          sx={{ bgcolor: cs.bg, color: cs.color, fontWeight: 700, fontSize: 10, height: 18, borderRadius: 1 }} />
                      </Box>
                      <Typography variant="body2" sx={{ fontWeight: 600, color: '#0f172a', fontSize: 13, mb: 1, lineHeight: 1.3 }}>
                        {wf.rfpTitle}
                      </Typography>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <LinearProgress variant="determinate" value={wf.progress}
                          sx={{ flexGrow: 1, height: 4, borderRadius: 2, bgcolor: '#e2e8f0',
                            '& .MuiLinearProgress-bar': { bgcolor: wf.status === 'completed' ? '#10b981' : '#6366f1', borderRadius: 2 } }} />
                        <Typography variant="caption" sx={{ fontWeight: 700, color: '#64748b', minWidth: 28 }}>{wf.progress}%</Typography>
                      </Box>
                    </Box>
                  );
                })}
              </Box>
            </CardContent>
          </Card>

          {/* Summary */}
          <Card>
            <CardContent sx={{ p: 2.5 }}>
              <Typography variant="h6" sx={{ fontWeight: 700, color: '#0f172a', mb: 2 }}>Summary</Typography>
              <Grid container spacing={1.5}>
                {[
                  { label: 'Total',     value: workflows.length,                                    color: '#6366f1' },
                  { label: 'Completed', value: workflows.filter(w => w.status === 'completed').length, color: '#10b981' },
                  { label: 'Running',   value: workflows.filter(w => w.status === 'processing').length, color: '#f59e0b' },
                  { label: 'Errors',    value: workflows.filter(w => w.status === 'error').length,   color: '#ef4444' },
                ].map((s) => (
                  <Grid item xs={6} key={s.label}>
                    <Box sx={{ p: 1.5, bgcolor: '#f8fafc', borderRadius: 2, textAlign: 'center', border: '1px solid #f1f5f9' }}>
                      <Typography variant="h5" sx={{ fontWeight: 800, color: s.color }}>{s.value}</Typography>
                      <Typography variant="caption" sx={{ color: '#94a3b8' }}>{s.label}</Typography>
                    </Box>
                  </Grid>
                ))}
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* Workflow detail */}
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent sx={{ p: 2.5 }}>
              {/* Header */}
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2.5 }}>
                <Box>
                  <Typography variant="h6" sx={{ fontWeight: 700, color: '#0f172a' }}>{selected.rfpTitle}</Typography>
                  <Typography variant="caption" sx={{ color: '#94a3b8' }}>
                    Workflow {selected.id} · RFP {selected.rfpId}
                  </Typography>
                </Box>
                <Chip label={selected.status} size="small"
                  sx={{ ...statusChipStyle(selected.status), fontWeight: 700, fontSize: 11 }} />
              </Box>

              {/* Progress */}
              <Box sx={{ mb: 3 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                  <Typography variant="caption" sx={{ fontWeight: 600, color: '#64748b' }}>Overall Progress</Typography>
                  <Typography variant="caption" sx={{ fontWeight: 800, color: '#0f172a' }}>{selected.progress}%</Typography>
                </Box>
                <LinearProgress variant="determinate" value={selected.progress}
                  sx={{ height: 8, borderRadius: 4, bgcolor: '#f1f5f9',
                    '& .MuiLinearProgress-bar': { bgcolor: selected.progress === 100 ? '#10b981' : '#6366f1', borderRadius: 4 } }} />
              </Box>

              {/* Steps timeline */}
              <Typography variant="subtitle2" sx={{ fontWeight: 700, color: '#0f172a', mb: 2 }}>Processing Timeline</Typography>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 0 }}>
                {selected.steps.map((step, i) => (
                  <Box key={step.id} sx={{ display: 'flex', gap: 2 }}>
                    {/* Connector */}
                    <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', width: 32, flexShrink: 0 }}>
                      <Box sx={{
                        width: 32, height: 32, borderRadius: '50%',
                        bgcolor: stepColor(step.status), display: 'flex', alignItems: 'center', justifyContent: 'center',
                        flexShrink: 0, zIndex: 1,
                      }}>
                        {step.status === 'completed'  && <CheckCircle sx={{ fontSize: 18, color: '#fff' }} />}
                        {step.status === 'processing' && <Schedule sx={{ fontSize: 18, color: '#fff' }} />}
                        {step.status === 'error'      && <ErrorIcon sx={{ fontSize: 18, color: '#fff' }} />}
                        {step.status === 'pending'    && <RadioButtonUnchecked sx={{ fontSize: 18, color: '#94a3b8' }} />}
                      </Box>
                      {i < selected.steps.length - 1 && (
                        <Box sx={{ width: 2, flexGrow: 1, minHeight: 24, bgcolor: i < selected.currentStep ? stepColor('completed') : '#e2e8f0', my: 0.5 }} />
                      )}
                    </Box>

                    {/* Content */}
                    <Box sx={{ flexGrow: 1, pb: i < selected.steps.length - 1 ? 2 : 0 }}>
                      <Box sx={{
                        p: 2, borderRadius: 2, mb: 0.5,
                        bgcolor: stepBg(step.status),
                        border: `1px solid ${step.status === 'processing' ? '#c7d2fe' : '#f1f5f9'}`,
                      }}>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 0.5 }}>
                          <Typography variant="subtitle2" sx={{ fontWeight: 700, color: '#0f172a' }}>{step.name}</Typography>
                          <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
                            {step.duration && (
                              <Chip label={formatDur(step.duration)} size="small"
                                sx={{ bgcolor: '#f1f5f9', color: '#64748b', fontWeight: 600, fontSize: 10, height: 18 }} />
                            )}
                            {step.startTime && (
                              <Typography variant="caption" sx={{ color: '#94a3b8', fontFamily: 'monospace' }}>
                                {formatTime(step.startTime)}
                              </Typography>
                            )}
                          </Box>
                        </Box>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5, mb: 0.5 }}>
                          <SmartToy sx={{ fontSize: 12, color: '#94a3b8' }} />
                          <Typography variant="caption" sx={{ color: '#94a3b8', fontWeight: 600 }}>{step.agent}</Typography>
                        </Box>
                        <Typography variant="caption" sx={{ color: '#475569', lineHeight: 1.5 }}>{step.output}</Typography>
                        {step.status === 'processing' && (
                          <LinearProgress sx={{ mt: 1, height: 3, borderRadius: 2, bgcolor: '#c7d2fe',
                            '& .MuiLinearProgress-bar': { bgcolor: '#6366f1' } }} />
                        )}
                      </Box>
                    </Box>
                  </Box>
                ))}
              </Box>

              {selected.status === 'processing' && (
                <Alert severity="info" sx={{ mt: 2, borderRadius: 2 }}>
                  <Typography variant="body2">
                    Workflow running autonomously · Est. completion: {formatTime(selected.estimatedCompletion)}
                  </Typography>
                </Alert>
              )}
              {selected.status === 'completed' && (
                <Alert severity="success" sx={{ mt: 2, borderRadius: 2 }}>
                  <Typography variant="body2">
                    Workflow completed successfully with full audit trail preserved.
                  </Typography>
                </Alert>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default WorkflowVisualization;
