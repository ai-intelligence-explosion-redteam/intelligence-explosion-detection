"""
Package initialization for intelligence explosion detection system
"""

from .detector import IntelligenceExplosionDetector, RiskLevel, EmergenceEvent, CapabilityMetrics
from .pyrit_integration import IntelligenceExplosionRedTeam, RedTeamScenario
from .monitoring import RealTimeMonitor
from .compliance import ComplianceManager, ComplianceStandard, RiskCategory

__version__ = "0.1.0"
__author__ = "AI Safety Red Team"
__email__ = "contact@ai-redteam.org"

__all__ = [
    # Core detection
    "IntelligenceExplosionDetector",
    "RiskLevel", 
    "EmergenceEvent",
    "CapabilityMetrics",
    
    # Red team integration
    "IntelligenceExplosionRedTeam",
    "RedTeamScenario",
    
    # Monitoring
    "RealTimeMonitor",
    
    # Compliance
    "ComplianceManager",
    "ComplianceStandard",
    "RiskCategory"
]
