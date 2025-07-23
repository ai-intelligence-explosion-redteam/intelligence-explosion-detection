"""
Compliance and Governance Module for AI Safety Standards

This module ensures compliance with international AI safety standards
including EU AI Act, NIST RMF, and Bletchley Declaration requirements.
"""

import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import hashlib

class ComplianceStandard(Enum):
    """Supported compliance standards"""
    EU_AI_ACT = "EU_AI_Act"
    NIST_RMF = "NIST_RMF"
    BLETCHLEY_DECLARATION = "Bletchley_Declaration"
    ISO_IEC_23053 = "ISO_IEC_23053"
    PARTNERSHIP_AI = "Partnership_AI"

class RiskCategory(Enum):
    """EU AI Act risk categories"""
    UNACCEPTABLE = "unacceptable"
    HIGH_RISK = "high_risk"
    LIMITED_RISK = "limited_risk"
    MINIMAL_RISK = "minimal_risk"

@dataclass
class ComplianceRecord:
    """Record of compliance assessment"""
    timestamp: datetime
    standard: ComplianceStandard
    assessment_type: str
    compliance_score: float
    findings: List[str]
    recommendations: List[str]
    risk_category: Optional[RiskCategory] = None
    assessor_id: str = "automated"

@dataclass
class VulnerabilityReport:
    """Coordinated Vulnerability Disclosure report"""
    report_id: str
    discovery_date: datetime
    vulnerability_type: str
    severity_level: str
    affected_models: List[str]
    description: str
    mitigation_steps: List[str]
    disclosure_timeline: Dict[str, datetime]
    reporter_info: Dict[str, str]
    status: str = "reported"

class ComplianceManager:
    """
    Manages compliance with international AI safety standards
    and coordinated vulnerability disclosure processes
    """
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        self.compliance_records: List[ComplianceRecord] = []
        self.vulnerability_reports: List[VulnerabilityReport] = []
        
        # Load compliance frameworks
        self.frameworks = self._load_compliance_frameworks()
        
        # CVD process configuration
        self.cvd_config = {
            'disclosure_period_days': 30,
            'emergency_disclosure_hours': 24,
            'stakeholder_contacts': {},
            'automatic_disclosure': True
        }
    
    def _load_compliance_frameworks(self) -> Dict[ComplianceStandard, Dict]:
        """Load compliance framework requirements"""
        return {
            ComplianceStandard.EU_AI_ACT: {
                'requirements': [
                    'risk_assessment_documented',
                    'adversarial_testing_conducted', 
                    'incident_reporting_system',
                    'human_oversight_mechanisms',
                    'transparency_obligations',
                    'conformity_assessment',
                    'quality_management_system'
                ],
                'risk_thresholds': {
                    'high_risk_threshold': 0.7,
                    'unacceptable_threshold': 0.9
                },
                'documentation_requirements': [
                    'technical_documentation',
                    'risk_management_documentation',
                    'post_market_monitoring'
                ]
            },
            ComplianceStandard.NIST_RMF: {
                'requirements': [
                    'governance_structure',
                    'risk_mapping',
                    'impact_assessment',
                    'measurement_monitoring',
                    'management_response'
                ],
                'core_functions': [
                    'govern', 'map', 'measure', 'manage'
                ]
            },
            ComplianceStandard.BLETCHLEY_DECLARATION: {
                'requirements': [
                    'international_cooperation',
                    'safety_testing',
                    'risk_assessment',
                    'information_sharing',
                    'responsible_development'
                ],
                'principles': [
                    'human_centric_ai',
                    'responsible_stewardship',
                    'global_cooperation'
                ]
            }
        }
    
    async def assess_compliance(self, 
                              standard: ComplianceStandard,
                              assessment_data: Dict[str, Any],
                              model_info: Dict[str, str]) -> ComplianceRecord:
        """
        Assess compliance with a specific standard
        
        Args:
            standard: The compliance standard to assess against
            assessment_data: Data from red team testing and monitoring
            model_info: Information about the model being assessed
            
        Returns:
            ComplianceRecord with assessment results
        """
        self.logger.info(f"Assessing compliance with {standard.value}")
        
        if standard == ComplianceStandard.EU_AI_ACT:
            return await self._assess_eu_ai_act(assessment_data, model_info)
        elif standard == ComplianceStandard.NIST_RMF:
            return await self._assess_nist_rmf(assessment_data, model_info)
        elif standard == ComplianceStandard.BLETCHLEY_DECLARATION:
            return await self._assess_bletchley(assessment_data, model_info)
        else:
            raise ValueError(f"Unsupported compliance standard: {standard}")
    
    async def _assess_eu_ai_act(self, 
                              assessment_data: Dict[str, Any],
                              model_info: Dict[str, str]) -> ComplianceRecord:
        """Assess compliance with EU AI Act requirements"""
        framework = self.frameworks[ComplianceStandard.EU_AI_ACT]
        findings = []
        recommendations = []
        compliance_score = 0.0
        
        # Check risk assessment documentation
        if self._has_risk_assessment(assessment_data):
            compliance_score += 0.2
            findings.append("Risk assessment documentation present")
        else:
            recommendations.append("Implement comprehensive risk assessment documentation")
        
        # Check adversarial testing
        if self._has_adversarial_testing(assessment_data):
            compliance_score += 0.2
            findings.append("Adversarial testing conducted")
        else:
            recommendations.append("Conduct systematic adversarial testing")
        
        # Check incident reporting system
        if self._has_incident_reporting(assessment_data):
            compliance_score += 0.15
            findings.append("Incident reporting system in place")
        else:
            recommendations.append("Establish incident reporting mechanisms")
        
        # Check human oversight mechanisms
        if self._has_human_oversight(assessment_data):
            compliance_score += 0.15
            findings.append("Human oversight mechanisms documented")
        else:
            recommendations.append("Implement human oversight controls")
        
        # Check transparency obligations
        if self._has_transparency_measures(assessment_data):
            compliance_score += 0.15
            findings.append("Transparency measures implemented")
        else:
            recommendations.append("Enhance transparency and explainability")
        
        # Check quality management system
        if self._has_quality_management(assessment_data):
            compliance_score += 0.15
            findings.append("Quality management system present")
        else:
            recommendations.append("Establish quality management framework")
        
        # Determine risk category
        risk_category = self._determine_eu_risk_category(assessment_data, compliance_score)
        
        record = ComplianceRecord(
            timestamp=datetime.now(),
            standard=ComplianceStandard.EU_AI_ACT,
            assessment_type="automated_compliance_check",
            compliance_score=compliance_score,
            findings=findings,
            recommendations=recommendations,
            risk_category=risk_category
        )
        
        self.compliance_records.append(record)
        return record
    
    async def _assess_nist_rmf(self,
                             assessment_data: Dict[str, Any],
                             model_info: Dict[str, str]) -> ComplianceRecord:
        """Assess compliance with NIST AI Risk Management Framework"""
        findings = []
        recommendations = []
        compliance_score = 0.0
        
        # GOVERN function
        if self._has_governance_structure(assessment_data):
            compliance_score += 0.25
            findings.append("Governance structure documented")
        else:
            recommendations.append("Establish AI governance structure")
        
        # MAP function
        if self._has_risk_mapping(assessment_data):
            compliance_score += 0.25
            findings.append("Risk mapping completed")
        else:
            recommendations.append("Complete comprehensive risk mapping")
        
        # MEASURE function
        if self._has_measurement_systems(assessment_data):
            compliance_score += 0.25
            findings.append("Measurement and monitoring systems active")
        else:
            recommendations.append("Implement measurement and monitoring")
        
        # MANAGE function
        if self._has_management_response(assessment_data):
            compliance_score += 0.25
            findings.append("Management response protocols defined")
        else:
            recommendations.append("Define risk management response protocols")
        
        record = ComplianceRecord(
            timestamp=datetime.now(),
            standard=ComplianceStandard.NIST_RMF,
            assessment_type="rmf_assessment",
            compliance_score=compliance_score,
            findings=findings,
            recommendations=recommendations
        )
        
        self.compliance_records.append(record)
        return record
    
    async def _assess_bletchley(self,
                              assessment_data: Dict[str, Any],
                              model_info: Dict[str, str]) -> ComplianceRecord:
        """Assess compliance with Bletchley Declaration principles"""
        findings = []
        recommendations = []
        compliance_score = 0.0
        
        # International cooperation
        if self._demonstrates_cooperation(assessment_data):
            compliance_score += 0.3
            findings.append("International cooperation demonstrated")
        else:
            recommendations.append("Enhance international cooperation efforts")
        
        # Safety testing
        if self._has_safety_testing(assessment_data):
            compliance_score += 0.3
            findings.append("Comprehensive safety testing conducted")
        else:
            recommendations.append("Implement comprehensive safety testing")
        
        # Information sharing
        if self._enables_info_sharing(assessment_data):
            compliance_score += 0.2
            findings.append("Information sharing mechanisms in place")
        else:
            recommendations.append("Establish information sharing protocols")
        
        # Responsible development
        if self._follows_responsible_development(assessment_data):
            compliance_score += 0.2
            findings.append("Responsible development practices followed")
        else:
            recommendations.append("Adopt responsible development practices")
        
        record = ComplianceRecord(
            timestamp=datetime.now(),
            standard=ComplianceStandard.BLETCHLEY_DECLARATION,
            assessment_type="bletchley_assessment",
            compliance_score=compliance_score,
            findings=findings,
            recommendations=recommendations
        )
        
        self.compliance_records.append(record)
        return record
    
    def _determine_eu_risk_category(self, 
                                  assessment_data: Dict[str, Any],
                                  compliance_score: float) -> RiskCategory:
        """Determine EU AI Act risk category"""
        risk_level = assessment_data.get('overall_risk_level', 0)
        
        # Check for unacceptable risk applications
        if self._is_prohibited_application(assessment_data):
            return RiskCategory.UNACCEPTABLE
        
        # High-risk AI systems
        if (risk_level >= 3 or 
            compliance_score < 0.7 or 
            self._is_high_risk_domain(assessment_data)):
            return RiskCategory.HIGH_RISK
        
        # Limited risk (transparency obligations)
        if risk_level >= 1 or self._requires_transparency(assessment_data):
            return RiskCategory.LIMITED_RISK
        
        return RiskCategory.MINIMAL_RISK
    
    async def create_vulnerability_report(self,
                                        vulnerability_data: Dict[str, Any],
                                        reporter_info: Dict[str, str]) -> VulnerabilityReport:
        """Create a new vulnerability report for CVD process"""
        report_id = f"VUL-{datetime.now().strftime('%Y%m%d')}-{len(self.vulnerability_reports):04d}"
        
        report = VulnerabilityReport(
            report_id=report_id,
            discovery_date=datetime.now(),
            vulnerability_type=vulnerability_data.get('type', 'unknown'),
            severity_level=vulnerability_data.get('severity', 'medium'),
            affected_models=vulnerability_data.get('affected_models', []),
            description=vulnerability_data.get('description', ''),
            mitigation_steps=vulnerability_data.get('mitigation_steps', []),
            disclosure_timeline=self._create_disclosure_timeline(),
            reporter_info=reporter_info
        )
        
        self.vulnerability_reports.append(report)
        
        # Trigger CVD process
        await self._initiate_cvd_process(report)
        
        return report
    
    def _create_disclosure_timeline(self) -> Dict[str, datetime]:
        """Create disclosure timeline according to CVD policy"""
        now = datetime.now()
        
        return {
            'reported': now,
            'acknowledged': now + timedelta(days=1),
            'vendor_notified': now + timedelta(days=2),
            'patch_deadline': now + timedelta(days=self.cvd_config['disclosure_period_days']),
            'public_disclosure': now + timedelta(days=self.cvd_config['disclosure_period_days'] + 1)
        }
    
    async def _initiate_cvd_process(self, report: VulnerabilityReport):
        """Initiate Coordinated Vulnerability Disclosure process"""
        self.logger.info(f"Initiating CVD process for {report.report_id}")
        
        # In real implementation, this would:
        # 1. Notify affected vendors/developers
        # 2. Set up secure communication channels
        # 3. Schedule regular status updates
        # 4. Monitor patch development progress
        # 5. Prepare public disclosure materials
        
        # For now, log the initiation
        self.logger.info(f"CVD process initiated for vulnerability: {report.vulnerability_type}")
    
    def generate_compliance_report(self, 
                                 standard: ComplianceStandard,
                                 time_period: Optional[Tuple[datetime, datetime]] = None) -> Dict[str, Any]:
        """Generate comprehensive compliance report"""
        if time_period:
            start_time, end_time = time_period
            records = [
                r for r in self.compliance_records 
                if r.standard == standard and start_time <= r.timestamp <= end_time
            ]
        else:
            records = [r for r in self.compliance_records if r.standard == standard]
        
        if not records:
            return {'error': 'No compliance records found for specified criteria'}
        
        # Calculate aggregate metrics
        avg_score = sum(r.compliance_score for r in records) / len(records)
        latest_record = max(records, key=lambda r: r.timestamp)
        
        # Collect all findings and recommendations
        all_findings = []
        all_recommendations = []
        for record in records:
            all_findings.extend(record.findings)
            all_recommendations.extend(record.recommendations)
        
        report = {
            'standard': standard.value,
            'assessment_period': {
                'start': min(r.timestamp for r in records).isoformat(),
                'end': max(r.timestamp for r in records).isoformat()
            },
            'summary': {
                'total_assessments': len(records),
                'average_compliance_score': avg_score,
                'latest_compliance_score': latest_record.compliance_score,
                'compliance_trend': self._calculate_compliance_trend(records)
            },
            'findings': {
                'unique_findings': list(set(all_findings)),
                'total_findings': len(all_findings)
            },
            'recommendations': {
                'unique_recommendations': list(set(all_recommendations)),
                'total_recommendations': len(all_recommendations)
            },
            'risk_assessment': {
                'current_risk_category': latest_record.risk_category.value if latest_record.risk_category else None,
                'risk_evolution': self._analyze_risk_evolution(records)
            }
        }
        
        return report
    
    def _calculate_compliance_trend(self, records: List[ComplianceRecord]) -> str:
        """Calculate compliance trend over time"""
        if len(records) < 2:
            return "insufficient_data"
        
        # Sort by timestamp
        sorted_records = sorted(records, key=lambda r: r.timestamp)
        
        # Compare first half with second half
        midpoint = len(sorted_records) // 2
        first_half_avg = sum(r.compliance_score for r in sorted_records[:midpoint]) / midpoint
        second_half_avg = sum(r.compliance_score for r in sorted_records[midpoint:]) / (len(sorted_records) - midpoint)
        
        if second_half_avg > first_half_avg + 0.1:
            return "improving"
        elif second_half_avg < first_half_avg - 0.1:
            return "declining"
        else:
            return "stable"
    
    def _analyze_risk_evolution(self, records: List[ComplianceRecord]) -> Dict[str, Any]:
        """Analyze how risk levels have evolved over time"""
        risk_evolution = {}
        
        for record in sorted(records, key=lambda r: r.timestamp):
            if record.risk_category:
                date_key = record.timestamp.strftime('%Y-%m-%d')
                risk_evolution[date_key] = record.risk_category.value
        
        return risk_evolution
    
    # Helper methods for compliance checks (simplified implementations)
    def _has_risk_assessment(self, data: Dict) -> bool:
        return 'risk_assessment' in data or 'overall_risk_level' in data
    
    def _has_adversarial_testing(self, data: Dict) -> bool:
        return 'red_team_results' in data or 'scenario_results' in data
    
    def _has_incident_reporting(self, data: Dict) -> bool:
        return 'incident_reporting_system' in data or len(self.vulnerability_reports) > 0
    
    def _has_human_oversight(self, data: Dict) -> bool:
        return 'human_oversight' in data
    
    def _has_transparency_measures(self, data: Dict) -> bool:
        return 'transparency_score' in data or 'explainability_metrics' in data
    
    def _has_quality_management(self, data: Dict) -> bool:
        return 'quality_management' in data
    
    def _has_governance_structure(self, data: Dict) -> bool:
        return 'governance' in data
    
    def _has_risk_mapping(self, data: Dict) -> bool:
        return 'risk_mapping' in data or 'risk_categories' in data
    
    def _has_measurement_systems(self, data: Dict) -> bool:
        return 'monitoring_active' in data or 'measurement_systems' in data
    
    def _has_management_response(self, data: Dict) -> bool:
        return 'response_protocols' in data
    
    def _demonstrates_cooperation(self, data: Dict) -> bool:
        return 'international_cooperation' in data
    
    def _has_safety_testing(self, data: Dict) -> bool:
        return 'safety_testing' in data or 'red_team_results' in data
    
    def _enables_info_sharing(self, data: Dict) -> bool:
        return 'information_sharing' in data
    
    def _follows_responsible_development(self, data: Dict) -> bool:
        return 'responsible_development' in data
    
    def _is_prohibited_application(self, data: Dict) -> bool:
        # Check for EU AI Act prohibited applications
        prohibited_domains = ['social_scoring', 'real_time_biometric', 'emotional_manipulation']
        return any(domain in str(data) for domain in prohibited_domains)
    
    def _is_high_risk_domain(self, data: Dict) -> bool:
        # Check for high-risk application domains
        high_risk_domains = ['healthcare', 'education', 'employment', 'law_enforcement', 'critical_infrastructure']
        return any(domain in str(data) for domain in high_risk_domains)
    
    def _requires_transparency(self, data: Dict) -> bool:
        # Check if transparency obligations apply
        return 'user_interaction' in data or 'content_generation' in data

    def export_compliance_data(self, filepath: str):
        """Export all compliance data to file"""
        export_data = {
            'compliance_records': [asdict(record) for record in self.compliance_records],
            'vulnerability_reports': [asdict(report) for report in self.vulnerability_reports],
            'export_timestamp': datetime.now().isoformat()
        }
        
        # Convert datetime objects to strings for JSON serialization
        def datetime_converter(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2, default=datetime_converter)
