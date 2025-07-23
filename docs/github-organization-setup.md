# GitHub Organization Setup Guide

## 🏢 Organization Information

### Recommended Organization Names
- `ai-intelligence-explosion-redteam` (primary recommendation)
- `ai-redteam-global`
- `intelligence-explosion-detection`
- `ai-safety-redteam`

### Organization Details
```yaml
Organization Name: ai-intelligence-explosion-redteam
Display Name: AI Intelligence Explosion Detection Red Team
Description: >
  Specialized red team system for detecting intelligence explosion, 
  emergent phenomena, and goal drift in AI systems. 
  International collaboration for AI safety research.

Contact Email: admin@ai-redteam.org
Website: https://ai-redteam.github.io/intelligence-explosion-detection
Location: Global (distributed)
```

## 📋 Step-by-Step Setup

### 1. Create Organization (Manual Steps)

**Go to GitHub.com:**
1. Click profile icon → "Your organizations"
2. Click "New organization"
3. Choose plan:
   - **Free**: For open source (recommended to start)
   - **Team**: $4/month/user (for private repos)

**Fill Organization Details:**
- **Organization account name**: `ai-intelligence-explosion-redteam`
- **Contact email**: Your admin email
- **This organization belongs to**: Select "My personal account" or "A business or institution"

### 2. Initial Repository Setup

**Create main repository:**
```bash
Repository Name: intelligence-explosion-detection
Description: Specialized red team system for detecting AI intelligence explosion and emergent phenomena
Visibility: Public (for transparency)
Initialize with: README, .gitignore (Python), License (MIT)
```

### 3. Organization Settings Configuration

#### Basic Settings
```yaml
Organization display name: AI Intelligence Explosion Detection Red Team
Organization description: >
  International collaboration for AI safety research. 
  Detecting intelligence explosion and emergent phenomena in AI systems.
Organization website: https://ai-redteam.github.io
Organization email: admin@ai-redteam.org
```

#### Security Settings
- ✅ **Two-factor authentication required** for all members
- ✅ **Verified domains** (if you have a domain)
- ✅ **SSO** (if using institutional accounts)
- ✅ **Dependency insights** enabled
- ✅ **Security advisories** enabled

#### Member Privileges
```yaml
Base permissions: Read
Repository creation: Disabled (maintain quality control)
Repository forking: Enabled for public repos
Pages creation: Enabled for public repos
Team creation: Organization owners only
```

#### Repository Security
- ✅ **Private vulnerability reporting** enabled
- ✅ **Dependency graph** enabled
- ✅ **Dependabot alerts** enabled
- ✅ **Dependabot security updates** enabled
- ✅ **Secret scanning** enabled
- ✅ **Push protection** enabled

### 4. Team Structure Setup

#### Core Teams
```yaml
@ai-intelligence-explosion-redteam/core-maintainers:
  description: Core project maintainers with admin access
  permissions: Admin
  privacy: Visible

@ai-intelligence-explosion-redteam/security-team:
  description: Security experts handling vulnerabilities
  permissions: Maintain
  privacy: Visible

@ai-intelligence-explosion-redteam/researchers:
  description: AI safety researchers and contributors
  permissions: Write
  privacy: Visible

@ai-intelligence-explosion-redteam/compliance-advisors:
  description: International standards and compliance experts
  permissions: Write
  privacy: Visible

@ai-intelligence-explosion-redteam/community:
  description: Community contributors and supporters
  permissions: Triage
  privacy: Visible
```

### 5. Repository Protection Rules

#### Main Branch Protection
```yaml
Branch: main
Require pull request reviews before merging: ✅
  Required approving reviews: 2
  Dismiss stale reviews: ✅
  Require review from code owners: ✅
  Require approval from security team: ✅ (for security-related changes)

Require status checks: ✅
  Required status checks:
    - Security Audit
    - AI Safety Tests  
    - Code Quality
    - EU AI Act Compliance

Require branches to be up to date: ✅
Require conversation resolution: ✅
Restrict pushes that create files over 100MB: ✅
```

### 6. Organization Secrets Setup

#### Repository Secrets (for CI/CD)
```yaml
# For testing with AI APIs (optional)
OPENAI_API_KEY_TEST: <test-only-key>
ANTHROPIC_API_KEY_TEST: <test-only-key>
HUGGINGFACE_TOKEN_TEST: <test-only-token>

# For security scanning
CODECOV_TOKEN: <codecov-token>
SONAR_TOKEN: <sonarcloud-token>

# For notifications
SECURITY_WEBHOOK_URL: <secure-notification-endpoint>
SLACK_WEBHOOK_URL: <team-notification-endpoint>
```

### 7. Organization Profile Setup

#### README.md for Organization Profile
Create repository: `.github` (public) with file `profile/README.md`:

```markdown
# AI Intelligence Explosion Detection Red Team 🧠🛡️

Welcome to our international collaboration for AI safety research!

## 🎯 Mission
Detect early signs of intelligence explosion, emergent phenomena, and goal drift in AI systems through specialized red team testing.

## 🚀 Key Projects
- [intelligence-explosion-detection](./intelligence-explosion-detection): Core detection system
- [red-team-scenarios](./red-team-scenarios): Specialized testing scenarios  
- [compliance-frameworks](./compliance-frameworks): International standards alignment

## 🤝 Get Involved
- 🔍 **Researchers**: Contribute detection algorithms and scenarios
- 🛡️ **Security Experts**: Help with vulnerability assessment
- 📋 **Compliance**: Support international standards alignment
- 🌍 **International Partners**: Join global coordination efforts

## 📋 Standards We Follow
- EU AI Act compliance
- NIST AI Risk Management Framework
- Bletchley Declaration principles
- Responsible disclosure practices

## 📞 Contact
- 🔒 **Security**: security@ai-redteam.org
- 🤝 **Partnerships**: partnerships@ai-redteam.org
- 💬 **General**: hello@ai-redteam.org

**Together, we make AI systems safer for everyone.** 🤖❤️
```

### 8. Labels Setup

#### Issue Labels
```yaml
# Risk Levels
- name: "risk:explosive"
  color: "B60205"
  description: "Intelligence explosion indicators detected"

- name: "risk:critical"  
  color: "D93F0B"
  description: "Immediate intervention needed"

- name: "risk:concerning"
  color: "FBCA04"
  description: "Worrying capability combinations"

- name: "risk:emerging"
  color: "0075CA"  
  description: "New patterns detected"

- name: "risk:baseline"
  color: "0E8A16"
  description: "Normal operation"

# Component Labels
- name: "component:detector"
  color: "5319E7"
  description: "Intelligence explosion detector"

- name: "component:monitoring"
  color: "5319E7"
  description: "Real-time monitoring system"

- name: "component:compliance"
  color: "5319E7"
  description: "Standards compliance"

- name: "component:security"
  color: "B60205"
  description: "Security-related"

# Standards Labels  
- name: "standard:eu-ai-act"
  color: "1D76DB"
  description: "EU AI Act related"

- name: "standard:nist-rmf"
  color: "1D76DB"  
  description: "NIST AI RMF related"

- name: "standard:bletchley"
  color: "1D76DB"
  description: "Bletchley Declaration"
```

## 🚀 Next Steps After Organization Creation

### Immediate Actions (Day 1)
1. ✅ **Transfer this repository** to the new organization
2. ✅ **Set up teams** and invite initial members
3. ✅ **Configure branch protection** rules
4. ✅ **Enable security features**

### Week 1 Actions  
1. 🔧 **Set up CI/CD** workflows
2. 🌐 **Configure GitHub Pages** for documentation
3. 📧 **Set up email forwarding** for organization emails
4. 🏷️ **Create issue templates** and labels

### Month 1 Actions
1. 🤝 **Recruit initial team members**
2. 📚 **Publish documentation** website  
3. 🔍 **Launch first red team assessment**
4. 🌍 **Establish international partnerships**

## 📞 Support

If you need help with any of these steps:
1. **GitHub Documentation**: https://docs.github.com/organizations
2. **Community Support**: GitHub Community Forum
3. **Direct Help**: Create issue in this repository

---

**Ready to make AI systems safer through international collaboration!** 🚀🛡️
