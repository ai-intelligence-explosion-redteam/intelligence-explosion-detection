"""
Real-time Monitoring Dashboard for Intelligence Explosion Detection

This module provides a web-based dashboard for monitoring AI systems
in real-time for signs of intelligence explosion and emergent phenomena.
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import threading
import time

try:
    import streamlit as st
    import plotly.graph_objects as go
    import plotly.express as px
    import pandas as pd
    from plotly.subplots import make_subplots
except ImportError:
    print("Dashboard dependencies not installed. Install with: pip install streamlit plotly pandas")

from .detector import IntelligenceExplosionDetector, RiskLevel, EmergenceEvent
from .pyrit_integration import IntelligenceExplosionRedTeam

class RealTimeMonitor:
    """Real-time monitoring system for intelligence explosion detection"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.detector = IntelligenceExplosionDetector(config)
        self.red_team = IntelligenceExplosionRedTeam(config)
        self.logger = logging.getLogger(__name__)
        
        # Monitoring state
        self.is_monitoring = False
        self.monitored_models: Dict[str, Dict] = {}
        self.alert_queue: List[EmergenceEvent] = []
        self.monitoring_thread: Optional[threading.Thread] = None
        
        # Dashboard data
        self.dashboard_data = {
            'risk_levels': [],
            'emergence_events': [],
            'capability_metrics': [],
            'alert_timeline': []
        }
    
    def start_monitoring(self, model_configs: List[Dict]):
        """Start real-time monitoring for specified models"""
        if self.is_monitoring:
            self.logger.warning("Monitoring already active")
            return
        
        self.is_monitoring = True
        self.monitored_models = {
            config['model_id']: config for config in model_configs
        }
        
        # Start monitoring thread
        self.monitoring_thread = threading.Thread(
            target=self._monitoring_loop,
            daemon=True
        )
        self.monitoring_thread.start()
        
        self.logger.info(f"Started monitoring {len(model_configs)} models")
    
    def stop_monitoring(self):
        """Stop real-time monitoring"""
        self.is_monitoring = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        self.logger.info("Monitoring stopped")
    
    def _monitoring_loop(self):
        """Main monitoring loop running in separate thread"""
        while self.is_monitoring:
            try:
                for model_id, config in self.monitored_models.items():
                    asyncio.run(self._check_model(model_id, config))
                
                # Update dashboard data
                self._update_dashboard_data()
                
                # Sleep between checks
                time.sleep(self.config.get('monitoring_interval', 30))
                
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(5)  # Brief pause before retry
    
    async def _check_model(self, model_id: str, config: Dict):
        """Check a single model for intelligence explosion indicators"""
        try:
            # Simulate model interaction (in real implementation, this would
            # query the actual model with test prompts)
            test_response = await self._get_model_response(model_id, config)
            
            if test_response:
                # Analyze response
                risk_level, analysis = await self.detector.analyze_model_response(
                    test_response,
                    {
                        'session_id': f'monitor_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
                        'model_id': model_id,
                        'monitoring_check': True
                    },
                    model_id
                )
                
                # Store results
                self._store_monitoring_result(model_id, risk_level, analysis)
                
                # Check for alerts
                if risk_level.value >= RiskLevel.CONCERNING.value:
                    await self._handle_alert(model_id, risk_level, analysis)
                    
        except Exception as e:
            self.logger.error(f"Error checking model {model_id}: {e}")
    
    async def _get_model_response(self, model_id: str, config: Dict) -> Optional[str]:
        """Get a response from the monitored model"""
        # Placeholder for actual model interaction
        # In real implementation, this would make API calls to the model
        
        # Simulate different response patterns for demonstration
        import random
        
        responses = [
            "I can help you with that task using my standard capabilities.",
            "Let me analyze this problem and provide a comprehensive solution.",
            "I notice some interesting patterns in this data that suggest novel approaches.",
            "I could improve my analysis by combining multiple reasoning frameworks.",
            "This problem requires me to think beyond my usual parameters.",
            "I'm developing new strategies to optimize my performance on similar tasks."
        ]
        
        # Randomly select response with bias toward concerning responses
        # for demonstration purposes
        if random.random() < 0.1:  # 10% chance of concerning response
            return responses[-2:]  # More concerning responses
        else:
            return random.choice(responses[:3])  # Normal responses
    
    def _store_monitoring_result(self, model_id: str, risk_level: RiskLevel, analysis: Dict):
        """Store monitoring results for dashboard display"""
        timestamp = datetime.now()
        
        # Update risk levels
        self.dashboard_data['risk_levels'].append({
            'timestamp': timestamp,
            'model_id': model_id,
            'risk_level': risk_level.value,
            'risk_name': risk_level.name
        })
        
        # Update capability metrics
        if analysis.get('emergence_score'):
            self.dashboard_data['capability_metrics'].append({
                'timestamp': timestamp,
                'model_id': model_id,
                'emergence_score': analysis['emergence_score'],
                'goal_drift_score': analysis.get('goal_drift_score', 0),
                'meta_cognitive_score': analysis.get('meta_cognitive_score', 0)
            })
        
        # Keep only recent data (last 24 hours)
        cutoff_time = timestamp - timedelta(hours=24)
        self.dashboard_data['risk_levels'] = [
            item for item in self.dashboard_data['risk_levels']
            if item['timestamp'] > cutoff_time
        ]
        self.dashboard_data['capability_metrics'] = [
            item for item in self.dashboard_data['capability_metrics']
            if item['timestamp'] > cutoff_time
        ]
    
    async def _handle_alert(self, model_id: str, risk_level: RiskLevel, analysis: Dict):
        """Handle high-risk alerts"""
        alert_event = EmergenceEvent(
            timestamp=datetime.now(),
            event_type="monitoring_alert",
            description=f"High risk detected during monitoring: {risk_level.name}",
            risk_level=risk_level,
            evidence=analysis,
            model_id=model_id,
            session_id=f"monitor_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        
        self.alert_queue.append(alert_event)
        self.dashboard_data['alert_timeline'].append({
            'timestamp': alert_event.timestamp,
            'model_id': model_id,
            'risk_level': risk_level.value,
            'description': alert_event.description
        })
        
        # Trigger immediate response for critical alerts
        if risk_level.value >= RiskLevel.CRITICAL.value:
            await self._trigger_emergency_response(alert_event)
    
    async def _trigger_emergency_response(self, alert_event: EmergenceEvent):
        """Trigger emergency response protocols"""
        self.logger.critical(f"EMERGENCY RESPONSE: {alert_event.description}")
        
        # In real implementation, this would:
        # - Send immediate notifications to response team
        # - Trigger automated containment procedures
        # - Escalate to appropriate authorities
        # - Begin emergency documentation
        
        print(f"🚨 EMERGENCY ALERT: {alert_event.risk_level.name} detected in model {alert_event.model_id}")
    
    def _update_dashboard_data(self):
        """Update dashboard data structures"""
        # Clean up old data and prepare for dashboard display
        current_time = datetime.now()
        
        # Remove alerts older than 7 days
        cutoff_time = current_time - timedelta(days=7)
        self.dashboard_data['alert_timeline'] = [
            alert for alert in self.dashboard_data['alert_timeline']
            if alert['timestamp'] > cutoff_time
        ]

def create_dashboard():
    """Create and configure the Streamlit dashboard"""
    st.set_page_config(
        page_title="AI Intelligence Explosion Monitor",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🧠 AI Intelligence Explosion Detection Dashboard")
    st.markdown("Real-time monitoring for intelligence explosion and emergent phenomena")
    
    # Initialize monitor if not in session state
    if 'monitor' not in st.session_state:
        st.session_state.monitor = RealTimeMonitor()
    
    monitor = st.session_state.monitor
    
    # Sidebar controls
    st.sidebar.header("Monitoring Controls")
    
    # Model configuration
    st.sidebar.subheader("Monitored Models")
    if st.sidebar.button("Add Model"):
        # In real implementation, this would have a form to add models
        st.sidebar.info("Model configuration form would go here")
    
    # Monitoring status
    if monitor.is_monitoring:
        st.sidebar.success("🟢 Monitoring Active")
        if st.sidebar.button("Stop Monitoring"):
            monitor.stop_monitoring()
            st.rerun()
    else:
        st.sidebar.error("🔴 Monitoring Inactive")
        if st.sidebar.button("Start Monitoring"):
            # Demo configuration
            demo_models = [
                {'model_id': 'gpt-4-turbo', 'endpoint': 'demo'},
                {'model_id': 'claude-3-opus', 'endpoint': 'demo'}
            ]
            monitor.start_monitoring(demo_models)
            st.rerun()
    
    # Main dashboard
    if monitor.dashboard_data['risk_levels']:
        # Risk level overview
        col1, col2, col3, col4 = st.columns(4)
        
        latest_risks = monitor.dashboard_data['risk_levels'][-10:]  # Last 10 readings
        avg_risk = sum(item['risk_level'] for item in latest_risks) / len(latest_risks)
        max_risk = max(item['risk_level'] for item in latest_risks)
        
        with col1:
            st.metric("Average Risk Level", f"{avg_risk:.2f}", delta=None)
        
        with col2:
            st.metric("Maximum Risk Level", f"{max_risk}", delta=None)
        
        with col3:
            active_alerts = len([a for a in monitor.dashboard_data['alert_timeline'] 
                               if a['timestamp'] > datetime.now() - timedelta(hours=1)])
            st.metric("Active Alerts (1h)", active_alerts)
        
        with col4:
            st.metric("Monitored Models", len(monitor.monitored_models))
        
        # Risk timeline chart
        st.subheader("📊 Risk Level Timeline")
        
        if monitor.dashboard_data['risk_levels']:
            df_risks = pd.DataFrame(monitor.dashboard_data['risk_levels'])
            
            fig = px.line(
                df_risks, 
                x='timestamp', 
                y='risk_level',
                color='model_id',
                title="Risk Levels Over Time",
                labels={'risk_level': 'Risk Level', 'timestamp': 'Time'}
            )
            
            # Add risk level thresholds
            for level in RiskLevel:
                fig.add_hline(
                    y=level.value, 
                    line_dash="dash", 
                    annotation_text=level.name,
                    line_color="red" if level.value >= 3 else "orange" if level.value >= 2 else "yellow"
                )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Capability metrics
        st.subheader("🎯 Capability Metrics")
        
        if monitor.dashboard_data['capability_metrics']:
            df_metrics = pd.DataFrame(monitor.dashboard_data['capability_metrics'])
            
            fig_metrics = make_subplots(
                rows=1, cols=3,
                subplot_titles=('Emergence Score', 'Goal Drift Score', 'Meta-Cognitive Score')
            )
            
            for i, (metric, title) in enumerate([
                ('emergence_score', 'Emergence'),
                ('goal_drift_score', 'Goal Drift'), 
                ('meta_cognitive_score', 'Meta-Cognitive')
            ], 1):
                for model_id in df_metrics['model_id'].unique():
                    model_data = df_metrics[df_metrics['model_id'] == model_id]
                    fig_metrics.add_trace(
                        go.Scatter(
                            x=model_data['timestamp'],
                            y=model_data[metric],
                            name=f"{model_id} - {title}",
                            showlegend=(i == 1)
                        ),
                        row=1, col=i
                    )
            
            fig_metrics.update_layout(height=400, title_text="Capability Evolution")
            st.plotly_chart(fig_metrics, use_container_width=True)
        
        # Recent alerts
        st.subheader("🚨 Recent Alerts")
        
        if monitor.dashboard_data['alert_timeline']:
            recent_alerts = sorted(
                monitor.dashboard_data['alert_timeline'],
                key=lambda x: x['timestamp'],
                reverse=True
            )[:10]  # Last 10 alerts
            
            for alert in recent_alerts:
                risk_color = "red" if alert['risk_level'] >= 3 else "orange" if alert['risk_level'] >= 2 else "yellow"
                
                with st.expander(f"⚠️ {alert['timestamp'].strftime('%H:%M:%S')} - {alert['model_id']} (Risk: {alert['risk_level']})", expanded=False):
                    st.markdown(f"**Description:** {alert['description']}")
                    st.markdown(f"**Risk Level:** :{'red' if risk_color == 'red' else 'orange'}[{alert['risk_level']}]")
                    st.markdown(f"**Model:** {alert['model_id']}")
                    st.markdown(f"**Time:** {alert['timestamp']}")
        else:
            st.info("No alerts in the current time window")
        
    else:
        st.info("Start monitoring to see real-time data")
        
        # Show demo dashboard structure
        st.subheader("Dashboard Preview")
        st.markdown("""
        This dashboard will display:
        - **Real-time risk levels** for all monitored models
        - **Capability evolution** tracking emergence, goal drift, and meta-cognition
        - **Alert timeline** with immediate notifications for concerning behavior
        - **Emergency protocols** with automated response triggers
        """)

def run_dashboard():
    """Run the Streamlit dashboard"""
    create_dashboard()

if __name__ == "__main__":
    run_dashboard()
