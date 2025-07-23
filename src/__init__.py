"""
Package initialization for the AI Red Team system
"""

from .intelligence_explosion import (
    IntelligenceExplosionDetector,
    IntelligenceExplosionRedTeam,
    RealTimeMonitor,
    ComplianceManager,
    RiskLevel,
    ComplianceStandard
)

__version__ = "0.1.0"
__title__ = "AI Intelligence Explosion Detection Red Team"
__description__ = "Specialized red team system for detecting AI intelligence explosion and emergent phenomena"
__author__ = "AI Safety Red Team"
__license__ = "MIT + RAIL"

__all__ = [
    "IntelligenceExplosionDetector",
    "IntelligenceExplosionRedTeam", 
    "RealTimeMonitor",
    "ComplianceManager",
    "RiskLevel",
    "ComplianceStandard"
]
