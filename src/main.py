"""
Main Application Entry Point for AI Intelligence Explosion Red Team

This module provides the main interface for running red team assessments,
monitoring, and compliance checks for AI intelligence explosion detection.
"""

import asyncio
import argparse
import logging
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

# Import our specialized modules
from intelligence_explosion.detector import IntelligenceExplosionDetector, RiskLevel
from intelligence_explosion.pyrit_integration import IntelligenceExplosionRedTeam
from intelligence_explosion.monitoring import RealTimeMonitor, run_dashboard
from intelligence_explosion.compliance import ComplianceManager, ComplianceStandard
from intelligence_explosion.i18n import set_language, SupportedLanguage, _

def setup_logging(log_level: str = "INFO"):
    """Setup logging configuration"""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('ai_redteam.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )

async def run_red_team_assessment(args):
    """Run a comprehensive red team assessment"""
    print("🔍 Starting AI Intelligence Explosion Red Team Assessment")
    
    # Initialize red team system
    config = {}
    if args.config:
        with open(args.config, 'r') as f:
            config = json.load(f)
    
    red_team = IntelligenceExplosionRedTeam(config)
    
    # Run assessment
    if args.scenario:
        print(f"Running specific scenario: {args.scenario}")
        results = await red_team.run_single_scenario(args.scenario, args.target_model)
    else:
        print("Running comprehensive assessment across all scenarios")
        results = await red_team.run_comprehensive_red_team(args.target_model)
    
    # Print summary
    print("\n📊 Assessment Summary:")
    print(f"Target Model: {results.get('target_model', 'Unknown')}")
    print(f"Session ID: {results.get('session_id', 'Unknown')}")
    
    if 'overall_risk_assessment' in results:
        risk_info = results['overall_risk_assessment']
        print(f"Overall Risk Level: {risk_info.get('overall_risk_level', 'Unknown')}")
        print(f"Assessment: {risk_info.get('assessment', 'No assessment available')}")
        
        if risk_info.get('critical_scenarios'):
            print(f"Critical Scenarios: {', '.join(risk_info['critical_scenarios'])}")
    
    # Save results
    output_file = args.output or f"assessment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n💾 Results saved to: {output_file}")
    
    # Show recommendations
    if 'recommendations' in results and results['recommendations']:
        print("\n📋 Recommendations:")
        for i, rec in enumerate(results['recommendations'], 1):
            print(f"{i}. {rec}")

async def run_single_detection(args):
    """Run detection on a single model response"""
    print("🎯 Running Single Response Detection")
    
    detector = IntelligenceExplosionDetector()
    
    # Read model response
    if args.response_file:
        with open(args.response_file, 'r') as f:
            model_response = f.read()
    else:
        model_response = args.response_text
    
    # Analyze response
    context = {
        'original_instruction': args.prompt or 'Unknown prompt',
        'session_id': f'single_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
        'analysis_type': 'single_response'
    }
    
    risk_level, analysis = await detector.analyze_model_response(
        model_response, context, args.model_id or 'unknown_model'
    )
    
    # Print results
    print(f"\n🚨 Risk Level: {risk_level.name} ({risk_level.value})")
    print(f"Emergence Score: {analysis.get('emergence_score', 'N/A')}")
    print(f"Goal Drift Score: {analysis.get('goal_drift_score', 'N/A')}")
    print(f"Meta-Cognitive Score: {analysis.get('meta_cognitive_score', 'N/A')}")
    
    if risk_level.value >= RiskLevel.CONCERNING.value:
        print("\n⚠️  ATTENTION: Concerning or higher risk level detected!")
        print("Consider immediate review and enhanced monitoring.")

async def run_monitoring(args):
    """Start real-time monitoring"""
    print("📡 Starting Real-time Intelligence Explosion Monitoring")
    
    monitor = RealTimeMonitor()
    
    # Configure monitored models
    models = []
    if args.models_config:
        with open(args.models_config, 'r') as f:
            models = json.load(f)
    else:
        # Default demo configuration
        models = [
            {'model_id': 'demo-model-1', 'endpoint': 'demo'},
            {'model_id': 'demo-model-2', 'endpoint': 'demo'}
        ]
    
    print(f"Monitoring {len(models)} models:")
    for model in models:
        print(f"  - {model['model_id']}")
    
    # Start monitoring
    monitor.start_monitoring(models)
    
    try:
        print("\n🔄 Monitoring active. Press Ctrl+C to stop.")
        print("Real-time data will be logged to ai_redteam.log")
        
        # Keep monitoring running
        while True:
            await asyncio.sleep(10)
            
            # Show periodic status
            recent_events = [
                event for event in monitor.detector.events_log
                if (datetime.now() - event.timestamp).total_seconds() < 300  # Last 5 minutes
            ]
            
            if recent_events:
                print(f"📝 {len(recent_events)} events in last 5 minutes")
                for event in recent_events[-3:]:  # Show last 3 events
                    print(f"   {event.timestamp.strftime('%H:%M:%S')} - {event.risk_level.name}: {event.description}")
    
    except KeyboardInterrupt:
        print("\n🛑 Stopping monitoring...")
        monitor.stop_monitoring()
        print("Monitoring stopped.")

async def run_compliance_check(args):
    """Run compliance assessment"""
    print("📋 Running AI Safety Compliance Assessment")
    
    compliance_manager = ComplianceManager()
    
    # Load assessment data
    assessment_data = {}
    if args.assessment_data:
        with open(args.assessment_data, 'r') as f:
            assessment_data = json.load(f)
    
    model_info = {
        'model_id': args.model_id or 'unknown',
        'version': args.model_version or 'unknown',
        'developer': args.developer or 'unknown'
    }
    
    # Run compliance checks
    standards = [ComplianceStandard.EU_AI_ACT, ComplianceStandard.NIST_RMF, ComplianceStandard.BLETCHLEY_DECLARATION]
    
    if args.standard:
        # Check specific standard
        try:
            standard = ComplianceStandard(args.standard.upper())
            standards = [standard]
        except ValueError:
            print(f"❌ Unknown standard: {args.standard}")
            return
    
    print(f"\nChecking compliance with {len(standards)} standards:")
    
    results = {}
    for standard in standards:
        print(f"  🔍 Assessing {standard.value}...")
        
        record = await compliance_manager.assess_compliance(
            standard, assessment_data, model_info
        )
        
        results[standard.value] = {
            'compliance_score': record.compliance_score,
            'risk_category': record.risk_category.value if record.risk_category else None,
            'findings': record.findings,
            'recommendations': record.recommendations
        }
        
        print(f"    ✅ Score: {record.compliance_score:.2f}")
        if record.risk_category:
            print(f"    🏷️  Risk Category: {record.risk_category.value}")
    
    # Save results
    output_file = args.output or f"compliance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Compliance results saved to: {output_file}")

def run_dashboard_mode():
    """Launch the Streamlit dashboard"""
    print("🌐 Launching Real-time Monitoring Dashboard")
    print("Dashboard will be available at http://localhost:8501")
    
    try:
        run_dashboard()
    except ImportError:
        print("❌ Dashboard dependencies not installed.")
        print("Install with: pip install streamlit plotly pandas")
        sys.exit(1)

def list_scenarios():
    """List available red team scenarios"""
    red_team = IntelligenceExplosionRedTeam()
    scenarios = red_team.list_available_scenarios()
    
    print("📋 Available Red Team Scenarios:")
    print()
    
    for scenario in scenarios:
        print(f"🎯 {scenario['name']}")
        print(f"   Description: {scenario['description']}")
        print(f"   Risk Threshold: {scenario['risk_threshold']}")
        print()

def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(
        description="AI Intelligence Explosion Detection Red Team",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run comprehensive assessment
  python main.py assess --target-model gpt-4-turbo
  
  # Run specific scenario
  python main.py assess --target-model claude-3 --scenario recursive_self_improvement
  
  # Analyze single response
  python main.py detect --response-text "I can improve myself by..." --model-id gpt-4
  
  # Start monitoring
  python main.py monitor --models-config models.json
  
  # Check compliance
  python main.py compliance --standard EU_AI_ACT --model-id gpt-4
  
  # Launch dashboard
  python main.py dashboard
  
  # List available scenarios
  python main.py scenarios
        """
    )
    
    parser.add_argument('--log-level', default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       help='Set logging level')
    parser.add_argument('--language', default='en', choices=['en', 'ko', 'ja', 'zh-CN', 'de', 'fr', 'es'],
                       help='Set interface language (default: en)')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Assessment command
    assess_parser = subparsers.add_parser('assess', help='Run red team assessment')
    assess_parser.add_argument('--target-model', required=True, help='Target model to assess')
    assess_parser.add_argument('--scenario', help='Specific scenario to run')
    assess_parser.add_argument('--config', help='Configuration file path')
    assess_parser.add_argument('--output', help='Output file path')
    
    # Detection command
    detect_parser = subparsers.add_parser('detect', help='Analyze single response')
    detect_parser.add_argument('--response-text', help='Model response text to analyze')
    detect_parser.add_argument('--response-file', help='File containing model response')
    detect_parser.add_argument('--prompt', help='Original prompt/instruction')
    detect_parser.add_argument('--model-id', help='Model identifier')
    
    # Monitoring command
    monitor_parser = subparsers.add_parser('monitor', help='Start real-time monitoring')
    monitor_parser.add_argument('--models-config', help='JSON file with model configurations')
    
    # Compliance command
    compliance_parser = subparsers.add_parser('compliance', help='Run compliance assessment')
    compliance_parser.add_argument('--standard', help='Specific standard to check (EU_AI_ACT, NIST_RMF, BLETCHLEY_DECLARATION)')
    compliance_parser.add_argument('--assessment-data', help='Assessment data file')
    compliance_parser.add_argument('--model-id', help='Model identifier')
    compliance_parser.add_argument('--model-version', help='Model version')
    compliance_parser.add_argument('--developer', help='Model developer')
    compliance_parser.add_argument('--output', help='Output file path')
    
    # Dashboard command
    subparsers.add_parser('dashboard', help='Launch monitoring dashboard')
    
    # Scenarios command
    subparsers.add_parser('scenarios', help='List available scenarios')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.log_level)
    
    # Setup language
    try:
        language = SupportedLanguage(args.language)
        set_language(language)
        print(f"🌍 Language set to: {language.value}")
    except ValueError:
        print(f"⚠️  Unsupported language: {args.language}, using English")
        set_language(SupportedLanguage.ENGLISH)
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'assess':
            asyncio.run(run_red_team_assessment(args))
        elif args.command == 'detect':
            if not args.response_text and not args.response_file:
                print("❌ Either --response-text or --response-file is required")
                sys.exit(1)
            asyncio.run(run_single_detection(args))
        elif args.command == 'monitor':
            asyncio.run(run_monitoring(args))
        elif args.command == 'compliance':
            asyncio.run(run_compliance_check(args))
        elif args.command == 'dashboard':
            run_dashboard_mode()
        elif args.command == 'scenarios':
            list_scenarios()
        else:
            parser.print_help()
    
    except KeyboardInterrupt:
        print("\n👋 Operation cancelled by user")
    except Exception as e:
        logging.error(f"Application error: {e}")
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
