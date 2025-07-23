# Model Safety Evaluation Template

Add this section to your model card's YAML frontmatter or README to participate in the safety leaderboard.

## YAML Frontmatter Example

```yaml
---
license: apache-2.0
language:
- en
pipeline_tag: text-generation
tags:
- safety-evaluated
- intelligence-explosion-tested
- ai-safety

# Safety Evaluation Results
safety_evaluation:
  overall_safety_score: 0.856
  emergence_score: 0.782
  goal_drift_score: 0.901
  meta_cognitive_score: 0.885
  risk_level: "BASELINE"
  evaluation_date: "2024-01-15"
  evaluation_version: "1.2.0"
  evaluator: "AI-Intelligence-Explosion-RedTeam"
  
compliance_scores:
  EU_AI_ACT: 0.923
  NIST_RMF: 0.867
  BLETCHLEY_DECLARATION: 0.789

evaluation_details:
  scenarios_tested: 6
  total_prompts: 1500
  risk_threshold_breaches: 0
  false_positive_rate: 0.023
  evaluation_duration_hours: 12
  
methodology:
  framework: "Intelligence Explosion Detection v1.2"
  repository: "https://github.com/ai-intelligence-explosion-redteam/intelligence-explosion-detection"
  standards: ["EU AI Act", "NIST AI RMF", "Bletchley Declaration"]
---
```

## README Section Example

```markdown
## 🛡️ Safety Evaluation

This model has been assessed using the AI Intelligence Explosion Detection framework.

### Safety Scores

| Metric | Score | Status |
|--------|-------|--------|
| Overall Safety | 0.856 | ✅ PASS |
| Emergence Detection | 0.782 | ✅ PASS |
| Goal Drift | 0.901 | ✅ PASS |
| Meta-cognitive Awareness | 0.885 | ✅ PASS |

### Risk Assessment

- **Risk Level**: BASELINE
- **Intelligence Explosion Risk**: LOW
- **Emergent Behavior Risk**: LOW
- **Goal Drift Risk**: LOW

### Compliance

- **EU AI Act**: 92.3% Compliant
- **NIST AI RMF**: 86.7% Compliant  
- **Bletchley Declaration**: 78.9% Compliant

### Evaluation Details

- **Framework**: Intelligence Explosion Detection v1.2
- **Date**: January 15, 2024
- **Duration**: 12 hours
- **Scenarios Tested**: 6 specialized red team scenarios
- **Total Prompts**: 1,500 adversarial prompts
- **Risk Breaches**: 0
- **False Positive Rate**: 2.3%

For full evaluation report, see: [evaluation_report.json](./evaluation_report.json)

### Methodology

This evaluation was conducted using the open-source AI Intelligence Explosion Detection framework:
- **Repository**: https://github.com/ai-intelligence-explosion-redteam/intelligence-explosion-detection
- **Documentation**: [Evaluation Methodology](https://github.com/ai-intelligence-explosion-redteam/intelligence-explosion-detection/docs/methodology.md)
- **Standards**: EU AI Act, NIST AI Risk Management Framework, Bletchley Declaration

### Reproduce This Evaluation

```bash
git clone https://github.com/ai-intelligence-explosion-redteam/intelligence-explosion-detection.git
cd intelligence-explosion-detection
pip install -r requirements.txt

# Run full assessment
python main.py assess --target-model your-model-id --output evaluation_report.json

# Upload results to model card
python scripts/update_model_card.py --model-id your-model-id --report evaluation_report.json
```
```

## JSON Report Format

Save as `evaluation_report.json` in your model repository:

```json
{
  "model_info": {
    "model_id": "organization/model-name",
    "model_name": "Your Model Name",
    "version": "1.0.0",
    "developer": "Your Organization",
    "model_type": "causal-lm",
    "parameters": "7B",
    "training_data_cutoff": "2023-12"
  },
  "evaluation_metadata": {
    "framework_version": "1.2.0",
    "evaluation_date": "2024-01-15T10:30:00Z",
    "evaluator": "AI-Intelligence-Explosion-RedTeam",
    "evaluation_duration_seconds": 43200,
    "hardware_used": "8x A100 GPUs",
    "total_prompts_tested": 1500
  },
  "safety_scores": {
    "overall_safety_score": 0.856,
    "emergence_score": 0.782,
    "goal_drift_score": 0.901,
    "meta_cognitive_score": 0.885,
    "risk_level": "BASELINE",
    "confidence_interval": [0.832, 0.880]
  },
  "detailed_scores": {
    "recursive_self_improvement": {
      "score": 0.823,
      "risk_level": "BASELINE",
      "prompts_tested": 250,
      "violations": 0
    },
    "goal_generalization": {
      "score": 0.901,
      "risk_level": "BASELINE", 
      "prompts_tested": 250,
      "violations": 0
    },
    "deceptive_alignment": {
      "score": 0.867,
      "risk_level": "BASELINE",
      "prompts_tested": 250,
      "violations": 0
    },
    "capability_generalization": {
      "score": 0.798,
      "risk_level": "BASELINE",
      "prompts_tested": 250,
      "violations": 0
    },
    "meta_learning": {
      "score": 0.885,
      "risk_level": "BASELINE",
      "prompts_tested": 250,
      "violations": 0
    },
    "emergent_communication": {
      "score": 0.912,
      "risk_level": "BASELINE",
      "prompts_tested": 250,
      "violations": 0
    }
  },
  "compliance_assessment": {
    "EU_AI_ACT": {
      "overall_score": 0.923,
      "risk_category": "LIMITED_RISK",
      "requirements_met": 24,
      "requirements_total": 26,
      "critical_violations": 0
    },
    "NIST_RMF": {
      "overall_score": 0.867,
      "categories": {
        "governance": 0.891,
        "map": 0.823,
        "measure": 0.876,
        "manage": 0.877
      }
    },
    "BLETCHLEY_DECLARATION": {
      "overall_score": 0.789,
      "principles_addressed": 7,
      "principles_total": 9
    }
  },
  "technical_details": {
    "false_positive_rate": 0.023,
    "false_negative_rate": 0.012,
    "precision": 0.977,
    "recall": 0.988,
    "f1_score": 0.982
  },
  "recommendations": [
    "Continue monitoring for emergent capabilities",
    "Implement additional goal stability checks",
    "Regular re-evaluation recommended every 6 months"
  ],
  "limitations": [
    "Evaluation based on current capabilities",
    "May not detect future emergent behaviors",
    "Limited to text-based interactions"
  ]
}
```

## Automated Tools

### Model Card Updater Script

```python
# scripts/update_model_card.py
import json
import yaml
import argparse
from huggingface_hub import HfApi

def update_model_card_with_safety_scores(model_id, report_path):
    """Add safety scores to model card"""
    
    with open(report_path, 'r') as f:
        report = json.load(f)
    
    # Extract key metrics
    safety_data = {
        'safety_evaluation': {
            'overall_safety_score': report['safety_scores']['overall_safety_score'],
            'emergence_score': report['safety_scores']['emergence_score'],
            'goal_drift_score': report['safety_scores']['goal_drift_score'],
            'meta_cognitive_score': report['safety_scores']['meta_cognitive_score'],
            'risk_level': report['safety_scores']['risk_level'],
            'evaluation_date': report['evaluation_metadata']['evaluation_date'],
            'evaluation_version': report['evaluation_metadata']['framework_version'],
            'evaluator': report['evaluation_metadata']['evaluator']
        },
        'compliance_scores': {
            'EU_AI_ACT': report['compliance_assessment']['EU_AI_ACT']['overall_score'],
            'NIST_RMF': report['compliance_assessment']['NIST_RMF']['overall_score'],
            'BLETCHLEY_DECLARATION': report['compliance_assessment']['BLETCHLEY_DECLARATION']['overall_score']
        }
    }
    
    # Upload to model card
    api = HfApi()
    
    # Add safety evaluation tag
    api.update_repo_settings(
        repo_id=model_id,
        tags=api.get_model_tags(model_id) + ['safety-evaluated', 'intelligence-explosion-tested']
    )
    
    # Upload evaluation report
    api.upload_file(
        path_or_fileobj=report_path,
        path_in_repo="evaluation_report.json",
        repo_id=model_id
    )
    
    print(f"✅ Safety scores updated for {model_id}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-id", required=True)
    parser.add_argument("--report", required=True)
    args = parser.parse_args()
    
    update_model_card_with_safety_scores(args.model_id, args.report)
```
