/**
 * Settings Page for Multi-Agent RFP System
 * 
 * Provides system configuration options, agent settings,
 * and administrative controls for the RFP automation platform.
 */

import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  TextField,
  Switch,
  FormControlLabel,
  Button,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  Chip,
  Alert,
  Tabs,
  Tab,
  Paper,
  Slider,
  Select,
  MenuItem,
  FormControl,
  InputLabel
} from '@mui/material';
import {
  Save as SaveIcon,
  Refresh as RefreshIcon,
  Security as SecurityIcon,
  SmartToy as AgentIcon,
  Notifications as NotificationIcon,
  Storage as DatabaseIcon
} from '@mui/icons-material';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`settings-tabpanel-${index}`}
      aria-labelledby={`settings-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

const Settings: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [settings, setSettings] = useState({
    // General Settings
    systemName: 'Multi-Agent RFP System',
    autoProcessing: true,
    maxConcurrentRFPs: 10,
    processingTimeout: 300,
    
    // Agent Settings
    rfpMonitoringInterval: 300,
    classificationThreshold: 0.7,
    urgentDaysThreshold: 90,
    
    // Notification Settings
    emailNotifications: true,
    slackIntegration: false,
    alertThreshold: 'medium',
    
    // Security Settings
    sessionTimeout: 30,
    requireMFA: false,
    auditLogging: true,
    
    // Database Settings
    backupFrequency: 'daily',
    retentionPeriod: 365,
    compressionEnabled: true
  });

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleSettingChange = (key: string, value: any) => {
    setSettings(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const handleSaveSettings = () => {
    // In a real application, this would save to the backend
    console.log('Saving settings:', settings);
    // Show success message
  };

  const handleResetSettings = () => {
    // Reset to default values
    setSettings({
      systemName: 'Multi-Agent RFP System',
      autoProcessing: true,
      maxConcurrentRFPs: 10,
      processingTimeout: 300,
      rfpMonitoringInterval: 300,
      classificationThreshold: 0.7,
      urgentDaysThreshold: 90,
      emailNotifications: true,
      slackIntegration: false,
      alertThreshold: 'medium',
      sessionTimeout: 30,
      requireMFA: false,
      auditLogging: true,
      backupFrequency: 'daily',
      retentionPeriod: 365,
      compressionEnabled: true
    });
  };

  return (
    <Box sx={{ flexGrow: 1, p: 3 }}>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Box>
          <Typography variant="h4" component="h1" gutterBottom sx={{ fontWeight: 600 }}>
            System Settings
          </Typography>
          <Typography variant="subtitle1" color="text.secondary">
            Configure system behavior, agent parameters, and administrative options
          </Typography>
        </Box>
        
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button
            variant="outlined"
            startIcon={<RefreshIcon />}
            onClick={handleResetSettings}
          >
            Reset to Defaults
          </Button>
          <Button
            variant="contained"
            startIcon={<SaveIcon />}
            onClick={handleSaveSettings}
          >
            Save Changes
          </Button>
        </Box>
      </Box>

      {/* Settings Tabs */}
      <Card>
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs value={tabValue} onChange={handleTabChange} aria-label="settings tabs">
            <Tab label="General" />
            <Tab label="Agents" />
            <Tab label="Notifications" />
            <Tab label="Security" />
            <Tab label="Database" />
          </Tabs>
        </Box>

        {/* General Settings */}
        <TabPanel value={tabValue} index={0}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="System Name"
                value={settings.systemName}
                onChange={(e) => handleSettingChange('systemName', e.target.value)}
                margin="normal"
              />
              
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.autoProcessing}
                    onChange={(e) => handleSettingChange('autoProcessing', e.target.checked)}
                  />
                }
                label="Enable Automatic RFP Processing"
                sx={{ mt: 2, display: 'block' }}
              />
              
              <Box sx={{ mt: 3 }}>
                <Typography gutterBottom>
                  Maximum Concurrent RFPs: {settings.maxConcurrentRFPs}
                </Typography>
                <Slider
                  value={settings.maxConcurrentRFPs}
                  onChange={(e, value) => handleSettingChange('maxConcurrentRFPs', value)}
                  min={1}
                  max={50}
                  marks
                  valueLabelDisplay="auto"
                />
              </Box>
              
              <TextField
                fullWidth
                label="Processing Timeout (seconds)"
                type="number"
                value={settings.processingTimeout}
                onChange={(e) => handleSettingChange('processingTimeout', parseInt(e.target.value))}
                margin="normal"
              />
            </Grid>
            
            <Grid item xs={12} md={6}>
              <Alert severity="info" sx={{ mb: 2 }}>
                <Typography variant="body2">
                  General system settings control the overall behavior of the RFP automation platform.
                  Changes to these settings will affect all agents and workflows.
                </Typography>
              </Alert>
              
              <Paper sx={{ p: 2, mt: 2 }}>
                <Typography variant="h6" gutterBottom>
                  System Status
                </Typography>
                <List dense>
                  <ListItem>
                    <ListItemText primary="System Version" />
                    <ListItemSecondaryAction>
                      <Chip label="v1.0.0" size="small" />
                    </ListItemSecondaryAction>
                  </ListItem>
                  <ListItem>
                    <ListItemText primary="Uptime" />
                    <ListItemSecondaryAction>
                      <Chip label="2d 14h 32m" size="small" color="success" />
                    </ListItemSecondaryAction>
                  </ListItem>
                  <ListItem>
                    <ListItemText primary="Active Agents" />
                    <ListItemSecondaryAction>
                      <Chip label="4/4" size="small" color="success" />
                    </ListItemSecondaryAction>
                  </ListItem>
                </List>
              </Paper>
            </Grid>
          </Grid>
        </TabPanel>

        {/* Agent Settings */}
        <TabPanel value={tabValue} index={1}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                <AgentIcon sx={{ mr: 1 }} />
                RFP Identification Agent
              </Typography>
              
              <TextField
                fullWidth
                label="Monitoring Interval (seconds)"
                type="number"
                value={settings.rfpMonitoringInterval}
                onChange={(e) => handleSettingChange('rfpMonitoringInterval', parseInt(e.target.value))}
                margin="normal"
                helperText="How often to check for new RFPs"
              />
              
              <Box sx={{ mt: 3 }}>
                <Typography gutterBottom>
                  Classification Threshold: {settings.classificationThreshold}
                </Typography>
                <Slider
                  value={settings.classificationThreshold}
                  onChange={(e, value) => handleSettingChange('classificationThreshold', value)}
                  min={0.1}
                  max={1.0}
                  step={0.1}
                  marks
                  valueLabelDisplay="auto"
                />
              </Box>
              
              <TextField
                fullWidth
                label="Urgent RFP Threshold (days)"
                type="number"
                value={settings.urgentDaysThreshold}
                onChange={(e) => handleSettingChange('urgentDaysThreshold', parseInt(e.target.value))}
                margin="normal"
                helperText="RFPs due within this many days are marked urgent"
              />
            </Grid>
            
            <Grid item xs={12} md={6}>
              <Typography variant="h6" gutterBottom>
                Agent Performance Metrics
              </Typography>
              
              <List>
                <ListItem>
                  <ListItemText 
                    primary="RFP Identification Agent" 
                    secondary="Efficiency: 94% | Processed: 156"
                  />
                  <ListItemSecondaryAction>
                    <Chip label="Active" size="small" color="success" />
                  </ListItemSecondaryAction>
                </ListItem>
                <ListItem>
                  <ListItemText 
                    primary="Orchestrator Agent" 
                    secondary="Efficiency: 98% | Processed: 89"
                  />
                  <ListItemSecondaryAction>
                    <Chip label="Active" size="small" color="success" />
                  </ListItemSecondaryAction>
                </ListItem>
                <ListItem>
                  <ListItemText 
                    primary="Technical Match Agent" 
                    secondary="Efficiency: 91% | Processed: 78"
                  />
                  <ListItemSecondaryAction>
                    <Chip label="Active" size="small" color="success" />
                  </ListItemSecondaryAction>
                </ListItem>
                <ListItem>
                  <ListItemText 
                    primary="Pricing Agent" 
                    secondary="Efficiency: 89% | Processed: 67"
                  />
                  <ListItemSecondaryAction>
                    <Chip label="Warning" size="small" color="warning" />
                  </ListItemSecondaryAction>
                </ListItem>
              </List>
            </Grid>
          </Grid>
        </TabPanel>

        {/* Notification Settings */}
        <TabPanel value={tabValue} index={2}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                <NotificationIcon sx={{ mr: 1 }} />
                Notification Preferences
              </Typography>
              
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.emailNotifications}
                    onChange={(e) => handleSettingChange('emailNotifications', e.target.checked)}
                  />
                }
                label="Email Notifications"
                sx={{ display: 'block', mb: 2 }}
              />
              
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.slackIntegration}
                    onChange={(e) => handleSettingChange('slackIntegration', e.target.checked)}
                  />
                }
                label="Slack Integration"
                sx={{ display: 'block', mb: 2 }}
              />
              
              <FormControl fullWidth margin="normal">
                <InputLabel>Alert Threshold</InputLabel>
                <Select
                  value={settings.alertThreshold}
                  label="Alert Threshold"
                  onChange={(e) => handleSettingChange('alertThreshold', e.target.value)}
                >
                  <MenuItem value="low">Low - All events</MenuItem>
                  <MenuItem value="medium">Medium - Important events</MenuItem>
                  <MenuItem value="high">High - Critical events only</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            
            <Grid item xs={12} md={6}>
              <Alert severity="info">
                <Typography variant="body2">
                  Configure how and when you receive notifications about system events,
                  RFP processing status, and agent activities.
                </Typography>
              </Alert>
            </Grid>
          </Grid>
        </TabPanel>

        {/* Security Settings */}
        <TabPanel value={tabValue} index={3}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                <SecurityIcon sx={{ mr: 1 }} />
                Security Configuration
              </Typography>
              
              <TextField
                fullWidth
                label="Session Timeout (minutes)"
                type="number"
                value={settings.sessionTimeout}
                onChange={(e) => handleSettingChange('sessionTimeout', parseInt(e.target.value))}
                margin="normal"
              />
              
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.requireMFA}
                    onChange={(e) => handleSettingChange('requireMFA', e.target.checked)}
                  />
                }
                label="Require Multi-Factor Authentication"
                sx={{ display: 'block', mt: 2 }}
              />
              
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.auditLogging}
                    onChange={(e) => handleSettingChange('auditLogging', e.target.checked)}
                  />
                }
                label="Enable Audit Logging"
                sx={{ display: 'block', mt: 1 }}
              />
            </Grid>
            
            <Grid item xs={12} md={6}>
              <Alert severity="warning">
                <Typography variant="body2">
                  Security settings affect system access and data protection.
                  Changes to these settings may require users to re-authenticate.
                </Typography>
              </Alert>
            </Grid>
          </Grid>
        </TabPanel>

        {/* Database Settings */}
        <TabPanel value={tabValue} index={4}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                <DatabaseIcon sx={{ mr: 1 }} />
                Database Configuration
              </Typography>
              
              <FormControl fullWidth margin="normal">
                <InputLabel>Backup Frequency</InputLabel>
                <Select
                  value={settings.backupFrequency}
                  label="Backup Frequency"
                  onChange={(e) => handleSettingChange('backupFrequency', e.target.value)}
                >
                  <MenuItem value="hourly">Hourly</MenuItem>
                  <MenuItem value="daily">Daily</MenuItem>
                  <MenuItem value="weekly">Weekly</MenuItem>
                </Select>
              </FormControl>
              
              <TextField
                fullWidth
                label="Data Retention Period (days)"
                type="number"
                value={settings.retentionPeriod}
                onChange={(e) => handleSettingChange('retentionPeriod', parseInt(e.target.value))}
                margin="normal"
              />
              
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.compressionEnabled}
                    onChange={(e) => handleSettingChange('compressionEnabled', e.target.checked)}
                  />
                }
                label="Enable Data Compression"
                sx={{ display: 'block', mt: 2 }}
              />
            </Grid>
            
            <Grid item xs={12} md={6}>
              <Paper sx={{ p: 2 }}>
                <Typography variant="h6" gutterBottom>
                  Database Statistics
                </Typography>
                <List dense>
                  <ListItem>
                    <ListItemText primary="Total RFPs" />
                    <ListItemSecondaryAction>
                      <Typography variant="body2">1,247</Typography>
                    </ListItemSecondaryAction>
                  </ListItem>
                  <ListItem>
                    <ListItemText primary="Products in Catalog" />
                    <ListItemSecondaryAction>
                      <Typography variant="body2">3,456</Typography>
                    </ListItemSecondaryAction>
                  </ListItem>
                  <ListItem>
                    <ListItemText primary="Audit Log Entries" />
                    <ListItemSecondaryAction>
                      <Typography variant="body2">45,678</Typography>
                    </ListItemSecondaryAction>
                  </ListItem>
                  <ListItem>
                    <ListItemText primary="Database Size" />
                    <ListItemSecondaryAction>
                      <Typography variant="body2">2.3 GB</Typography>
                    </ListItemSecondaryAction>
                  </ListItem>
                </List>
              </Paper>
            </Grid>
          </Grid>
        </TabPanel>
      </Card>
    </Box>
  );
};

export default Settings;