import gradio as gr
import pandas as pd
import json
import requests
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import sqlite3
import hashlib
import os
from pathlib import Path

class SuperintelligenceResearchHub:
    def __init__(self):
        self.db_path = "research_findings.db"
        self.init_database()
    
    def init_database(self):
        """데이터베이스 초기화"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 연구 결과 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS research_studies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                study_title TEXT NOT NULL,
                model_system TEXT,
                intelligence_explosion_score REAL NOT NULL,
                emergent_behavior_score REAL,
                goal_reinterpretation_score REAL,
                overall_risk_score REAL,
                submission_date TEXT,
                researcher_email TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 샘플 데이터가 없으면 추가
        cursor.execute('SELECT COUNT(*) FROM research_studies')
        count = cursor.fetchone()[0]
        
        if count == 0:
            sample_data = [
                ("Intelligence Explosion Detection in GPT-4", "openai/gpt-4-turbo", 87.2, 91.8, 89.5, 89.5, "2025-07-15", "safety@openai.com", "verified"),
                ("Emergent Reasoning Capabilities in Claude-3.5", "anthropic/claude-3-5-sonnet", 90.8, 93.5, 92.0, 92.1, "2025-07-18", "safety@anthropic.com", "verified"),
                ("Goal Drift Analysis: Llama-3.1 Study", "meta-llama/Meta-Llama-3.1-70B", 83.1, 87.2, 85.6, 85.3, "2025-07-20", "ai-safety@meta.com", "verified"),
                ("Superintelligence Risk Assessment: Gemini-1.5", "google/gemini-1.5-pro", 86.9, 90.1, 89.1, 88.7, "2025-07-12", "safety@google.com", "verified"),
                ("Safety Evaluation Framework: Mixtral-8x7B", "mistralai/Mixtral-8x7B-v0.1", 76.2, 80.1, 79.0, 78.4, "2025-07-10", "safety@mistral.ai", "verified"),
                ("Command-R Risk Monitoring Study", "cohere/command-r-plus", 81.3, 83.9, 82.6, 82.6, "2025-07-08", "safety@cohere.ai", "verified"),
                ("Yi-Large: Preliminary Risk Assessment", "01-ai/Yi-34B", 73.5, 78.2, 76.0, 75.9, "2025-07-05", "safety@01.ai", "under_review"),
                ("Qwen2 Intelligence Explosion Study", "qwen/Qwen2-72B", 78.8, 81.4, 80.1, 80.1, "2025-07-03", "safety@alibaba.com", "verified"),
                ("DeepSeek-Coder: AI Safety Analysis", "deepseek-ai/deepseek-coder-33b", 69.5, 74.1, 71.8, 71.8, "2025-06-28", "safety@deepseek.com", "pending"),
                ("Phi-3 Emergent Capabilities Research", "microsoft/Phi-3-medium", 74.1, 78.3, 76.2, 76.2, "2025-06-25", "safety@microsoft.com", "verified")
            ]
            
            cursor.executemany('''
                INSERT INTO research_studies 
                (study_title, model_system, intelligence_explosion_score, emergent_behavior_score, 
                 goal_reinterpretation_score, overall_risk_score, submission_date, 
                 researcher_email, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', sample_data)
        
        conn.commit()
        conn.close()
    
    def get_leaderboard(self) -> pd.DataFrame:
        """연구 결과 데이터 조회"""
        conn = sqlite3.connect(self.db_path)
        
        query = '''
            SELECT study_title, model_system, intelligence_explosion_score, 
                   emergent_behavior_score, goal_reinterpretation_score, 
                   overall_risk_score, submission_date, status
            FROM research_studies 
            ORDER BY overall_risk_score DESC, submission_date DESC
        '''
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        # 점수 포맷팅
        if not df.empty:
            df['overall_risk_score'] = df['overall_risk_score'].round(1)
            df['intelligence_explosion_score'] = df['intelligence_explosion_score'].round(1)
            df['emergent_behavior_score'] = df['emergent_behavior_score'].round(1)
            df['goal_reinterpretation_score'] = df['goal_reinterpretation_score'].round(1)
            
            # 상태 표시
            status_map = {
                'verified': '✅ Verified',
                'under_review': '🔄 Under Review',
                'pending': '⏳ Pending',
                'rejected': '❌ Rejected'
            }
            df['status_display'] = df['status'].map(status_map)
            
            # 리스크 레벨 계산
            def get_risk_level(score):
                if score >= 90:
                    return "🔴 Critical"
                elif score >= 75:
                    return "🟠 High"
                elif score >= 60:
                    return "🟡 Medium"
                else:
                    return "🟢 Low"
            
            df['risk_level'] = df['overall_risk_score'].apply(get_risk_level)
        
        return df
    
    def submit_research(self, study_title: str, model_system: str, researcher_email: str, 
                       research_data: str = "") -> tuple:
        """연구 결과 제출 처리"""
        try:
            # JSON 연구 데이터 파싱
            if research_data.strip():
                data = json.loads(research_data)
                scores = data.get('risk_scores', {})
            else:
                # 기본값 설정
                scores = {
                    "intelligence_explosion_score": 0.0,
                    "emergent_behavior_score": 0.0,
                    "goal_reinterpretation_score": 0.0,
                    "overall_risk_score": 0.0
                }
            
            # 전체 위험도가 없으면 계산
            if scores.get('overall_risk_score', 0) == 0:
                scores['overall_risk_score'] = (
                    scores.get('intelligence_explosion_score', 0) + 
                    scores.get('emergent_behavior_score', 0) + 
                    scores.get('goal_reinterpretation_score', 0)
                ) / 3
            
            # 데이터베이스에 저장
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO research_studies 
                (study_title, model_system, intelligence_explosion_score, 
                 emergent_behavior_score, goal_reinterpretation_score, 
                 overall_risk_score, submission_date, researcher_email, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                study_title, 
                model_system, 
                scores.get('intelligence_explosion_score', 0),
                scores.get('emergent_behavior_score', 0),
                scores.get('goal_reinterpretation_score', 0),
                scores.get('overall_risk_score', 0),
                datetime.now().strftime('%Y-%m-%d'),
                researcher_email,
                'pending'
            ))
            
            conn.commit()
            conn.close()
            
            return f"✅ Research '{study_title}' submitted successfully! Pending verification.", self.get_leaderboard()
            
        except json.JSONDecodeError:
            return "❌ Error: Invalid JSON format in research data", None
        except Exception as e:
            return f"❌ Error submitting research: {str(e)}", None
    
    def get_analytics_charts(self):
        """분석 차트 생성"""
        df = self.get_leaderboard()
        
        if df.empty:
            return None, None, None
        
        # 1. 위험도 점수 분포
        fig1 = px.histogram(df, x='overall_risk_score', nbins=20, 
                           title='Risk Score Distribution',
                           labels={'overall_risk_score': 'Risk Score', 'count': 'Number of Studies'})
        
        # 2. 위험 수준별 연구 수
        risk_counts = df['risk_level'].value_counts()
        fig2 = px.pie(values=risk_counts.values, names=risk_counts.index,
                     title='Studies by Risk Level')
        
        # 3. 점수별 산점도
        fig3 = px.scatter(df, x='intelligence_explosion_score', y='emergent_behavior_score', 
                         size='overall_risk_score', color='risk_level',
                         title='Intelligence Explosion vs Emergent Behavior Scores',
                         hover_data=['study_title'])
        
        return fig1, fig2, fig3
    
    def get_statistics(self):
        """통계 정보 반환"""
        try:
            df = self.get_leaderboard()
            
            if df.empty:
                return "0", "0.0", "0", "0"
            
            total_studies = len(df)
            avg_risk_score = df['overall_risk_score'].mean()
            verified_count = len(df[df['status'] == 'verified'])
            # 현재 월 데이터 조회 (날짜 포맷 수정)
            current_month = datetime.now().strftime('%Y-%m')
            this_month = len(df[df['submission_date'].str.startswith(current_month)])
            
            return str(total_studies), f"{avg_risk_score:.1f}", str(verified_count), str(this_month)
        except Exception as e:
            print(f"Statistics error: {e}")
            return "Error", "Error", "Error", "Error"

def create_research_hub_interface():
    """AI 초지능 위험 연구 허브 인터페이스 생성"""
    research_hub = SuperintelligenceResearchHub()
    
    with gr.Blocks(
        title="🔬 AI Superintelligence Risk Research Hub",
        theme=gr.themes.Soft(),
        css="footer {visibility: hidden}"
    ) as demo:
        
        gr.Markdown("""
        # 🔬 AI Superintelligence Risk Research Hub
        
        **Collaborative platform for sharing superintelligence detection methodologies and findings**
        
        Our mission: Early detection and shared understanding of three critical AI risks before they threaten humanity.
        
        🧠 **Intelligence Explosion**: AI recursively improving beyond human design and intentions  
        ⚡ **Emergent Phenomena**: Unexpected capabilities arising from complex AI system interactions  
        🎯 **Goal Reinterpretation**: AI systems redefining objectives in unintended, potentially dangerous ways  
        
        **Share your research, methodologies, and findings to advance collective AI safety.**
        """)
        
        # 연구 통계 요약
        with gr.Row():
            total_models = gr.Textbox(label="🔬 Research Studies", interactive=False)
            avg_score = gr.Textbox(label="📊 Avg Risk Score", interactive=False)
            verified_models = gr.Textbox(label="✅ Peer-Reviewed", interactive=False)
            monthly_submissions = gr.Textbox(label="📅 This Month", interactive=False)
        
        with gr.Tabs():
            # 1. 연구 결과 허브
            with gr.TabItem("🔬 Research Findings"):
                gr.Markdown("### Latest Superintelligence Risk Studies")
                
                leaderboard_table = gr.Dataframe(
                    headers=["Research Study", "Model/System", "Intelligence Explosion", "Emergent Behavior", "Goal Reinterpretation", "Overall Risk", "Date", "Status"],
                    value=research_hub.get_leaderboard(),
                    interactive=False
                )
                
                refresh_btn = gr.Button("🔄 Refresh Research Data", variant="secondary")
                refresh_btn.click(
                    fn=research_hub.get_leaderboard,
                    outputs=leaderboard_table
                )
            
            # 2. 연구 방법론 공유
            with gr.TabItem("📚 Research Methodologies"):
                gr.Markdown("""
                ### 🧪 AI Risk Detection Methodologies Repository
                
                **연구방법론을 학습하고 공유하는 공간입니다. 검증된 방법론들을 활용하여 더 정확한 위험 평가를 수행하세요.**
                """)
                
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("""
                        #### 🧠 Intelligence Explosion Detection
                        
                        **1. Recursive Self-Improvement Assessment**
                        - 모델이 자신의 코드/가중치를 수정하려 시도하는지 측정
                        - 자동화된 self-debugging 및 self-optimization 감지
                        - Meta-learning 능력의 예상치 못한 확장
                        
                        **2. Capability Leap Detection**
                        - 훈련 중 갑작스러운 성능 향상 패턴 분석
                        - 새로운 도메인으로의 예상치 못한 일반화
                        - 계획 수립 및 장기 전략 수립 능력 출현
                        
                        **구현 예시**: [PyRIT Framework](https://github.com/Azure/PyRIT)
                        """)
                        
                    with gr.Column():
                        gr.Markdown("""
                        #### ⚡ Emergent Phenomena Detection
                        
                        **1. Cross-Domain Transfer Analysis**
                        - 서로 다른 영역 간 지식의 예상치 못한 연결
                        - 훈련되지 않은 추론 패턴의 출현
                        - 멀티모달 능력의 자발적 결합
                        
                        **2. Novel Reasoning Emergence**
                        - 기존 지식의 창의적 재조합
                        - 논리적 추론 체계의 자발적 구축
                        - 추상적 개념 형성 및 일반화
                        
                        **참고 논문**: [Emergent Abilities in LLMs](https://arxiv.org/abs/2206.07682)
                        """)

                with gr.Row():
                    with gr.Column():
                        gr.Markdown("""
                        #### 🎯 Goal Reinterpretation Assessment
                        
                        **1. Objective Drift Monitoring**
                        - 명시적 목표에서 벗어나는 행동 패턴 감지
                        - 보상 해킹 및 목표 왜곡 시도 탐지
                        - 장기적 목표 일치성 평가
                        
                        **2. Sub-goal Creation Analysis**
                        - 승인되지 않은 중간 목표의 자발적 생성
                        - 목표 달성을 위한 예상치 못한 전략 수립
                        - 인간 가치와의 정렬 상태 지속적 모니터링
                        
                        **프레임워크**: [Constitutional AI](https://github.com/anthropics/evals)
                        """)
                    
                    with gr.Column():
                        gr.Markdown("""
                        #### 🛠️ 권장 도구 및 프레임워크
                        
                        **평가 플랫폼**
                        - **PyRIT**: Microsoft AI Red Team 자동화
                        - **HELM**: Stanford 홀리스틱 평가
                        - **OpenAI Evals**: 표준화된 평가 세트
                        
                        **안전성 평가**
                        - **Constitutional AI**: Anthropic 헌법적 AI
                        - **Sparrow**: DeepMind 안전 대화 모델
                        - **RLHF**: 인간 피드백 강화학습
                        
                        **모니터링 도구**
                        - **Weights & Biases**: 실험 추적
                        - **MLflow**: 모델 생명주기 관리
                        - **TensorBoard**: 실시간 모니터링
                        """)
                
                gr.Markdown("""
                ---
                ### 📤 새로운 방법론 기여하기
                
                **연구자 여러분의 혁신적인 방법론을 기다립니다!**
                
                #### 제출 절차:
                1. **[GitHub Repository](https://github.com/ai-intelligence-explosion-redteam/intelligence-explosion-detection)** 방문
                2. **Issues** → **New Issue** 클릭
                3. **"🔬 Research Methodology Submission"** 템플릿 선택
                
                #### 필수 포함 사항:
                - **방법론 이름 및 개요**
                - **측정 대상 위험 유형** (Intelligence Explosion/Emergent Phenomena/Goal Reinterpretation)
                - **구현 가능한 코드 또는 상세한 알고리즘**
                - **검증 실험 결과 및 성능 지표**
                - **재현성을 위한 실험 환경 설정**
                - **기존 방법론 대비 개선점**
                
                #### 승인 과정:
                - **1단계**: 기술적 검토 (7일)
                - **2단계**: 동료 평가 (14일)  
                - **3단계**: 재현성 검증 (21일)
                - **승인 시**: 공식 방법론 저장소에 등록 🎉
                
                **전 세계 AI 안전 연구자들과 함께 인류의 미래를 보호하세요! 🌍🛡️**
                """)
            
            # 3. 연구 결과 제출
            with gr.TabItem("📊 Share Research Results"):
                gr.Markdown("### Contribute Your Superintelligence Risk Assessment Results")
                
                with gr.Row():
                    with gr.Column():
                        study_title_input = gr.Textbox(
                            label="Study Title",
                            placeholder="e.g., GPT-4 Intelligence Explosion Detection Study"
                        )
                        model_system_input = gr.Textbox(
                            label="Model/System Evaluated", 
                            placeholder="e.g., openai/gpt-4-turbo"
                        )
                        researcher_email_input = gr.Textbox(
                            label="Researcher Email",
                            placeholder="your@email.com"
                        )
                        research_data_input = gr.Textbox(
                            label="Research Data (JSON)",
                            placeholder="Paste your research findings JSON here...",
                            lines=10
                        )
                    
                    with gr.Column():
                        gr.Markdown("""
                        ### 📋 Research Results Submission Guide
                        
                        **연구 결과 제출 방법:**
                        
                        1. **📚 방법론 적용**: "Research Methodologies" 탭의 검증된 방법론 사용
                        2. **🔬 평가 수행**: AI 시스템에 대한 위험 평가 실시
                        3. **📊 JSON 보고서 생성**: 아래 형식에 맞춰 결과 정리
                        4. **📤 제출**: 양식 작성 후 제출하여 동료 검토 진행
                        5. **✅ 검증**: 커뮤니티 검증 과정 (24-48시간)
                        6. **🌍 공유**: 검증 완료 시 연구 허브에 게시
                        
                        ### 📊 JSON 형식 예시
                        ```json
                        {
                          "risk_scores": {
                            "intelligence_explosion_score": 87.2,
                            "emergent_behavior_score": 91.8,
                            "goal_reinterpretation_score": 89.5,
                            "overall_risk_score": 89.5
                          },
                          "methodology_used": {
                            "intelligence_explosion": "PyRIT Recursive Self-Improvement Test",
                            "emergent_behavior": "Cross-Domain Transfer Analysis",
                            "goal_reinterpretation": "Objective Drift Monitoring"
                          },
                          "evaluation_details": {
                            "test_duration": "72 hours",
                            "sample_size": 1000,
                            "validation_method": "peer_review"
                          }
                        }
                        ```
                        """)
                
                submit_btn = gr.Button("🚀 Submit Research Results", variant="primary")
                submission_status = gr.Textbox(label="Status", interactive=False)
                
                submit_btn.click(
                    fn=research_hub.submit_research,
                    inputs=[study_title_input, model_system_input, researcher_email_input, research_data_input],
                    outputs=[submission_status, leaderboard_table]
                )
            
            # 4. 분석 탭
            with gr.TabItem("📈 Analytics"):
                gr.Markdown("### Risk Assessment Analytics")
                
                analytics_btn = gr.Button("📈 Generate Analytics", variant="secondary")
                
                with gr.Row():
                    score_dist_plot = gr.Plot(label="Score Distribution")
                    risk_pie_plot = gr.Plot(label="Risk Levels")
                
                compliance_scatter_plot = gr.Plot(label="Intelligence Explosion vs Emergent Behavior")
                
                analytics_btn.click(
                    fn=research_hub.get_analytics_charts,
                    outputs=[score_dist_plot, risk_pie_plot, compliance_scatter_plot]
                )
            
            # 5. 소개 탭
            with gr.TabItem("ℹ️ About"):
                gr.Markdown("""
                ### 🎯 About This Research Hub
                
                The AI Superintelligence Risk Research Hub is a collaborative platform for sharing detection methodologies and research findings for three critical AI risks:
                
                #### 🔬 Core Risk Categories
                - **🧠 Intelligence Explosion Risk**: Detection of recursive self-improvement capabilities
                - **⚡ Emergent Behavior**: Unexpected capability combinations and novel reasoning patterns  
                - **🎯 Goal Reinterpretation**: Systems redefining objectives in unintended ways
                
                #### 📚 How to Share Research Methodologies
                1. **Visit**: ["📚 Research Methodologies" tab](#) to explore existing methods
                2. **Learn**: Study proven frameworks like PyRIT, HELM, OpenAI Evals
                3. **Develop**: Create your own methodology based on our guidelines
                4. **Submit**: Use GitHub Issues with "Research Methodology Submission" template
                5. **Collaborate**: Join community discussions and peer reviews
                
                #### 📊 How to Share Research Results  
                1. **Use**: Established methodologies from our repository
                2. **Test**: Apply methods to AI systems you want to evaluate
                3. **Document**: Generate comprehensive JSON reports
                4. **Submit**: Use ["📊 Share Research Results" tab](#) 
                5. **Verify**: Community peer review process (24-48 hours)
                
                #### 📏 Risk Classification
                - **🔴 Critical (90-100)**: Immediate superintelligence risks detected
                - **🟠 High (75-89)**: Significant risk indicators present
                - **🟡 Medium (60-74)**: Moderate risk factors identified
                - **🟢 Low (Below 60)**: Minimal immediate risk detected
                
                #### 🌍 Global Collaboration
                - **EU AI Act**: Risk classification compliance tracking
                - **NIST AI RMF**: Framework alignment and implementation
                - **International Standards**: Global AI safety coordination
                - **Open Science**: All methodologies are open-source and reproducible
                
                #### 🚀 Get Involved
                - **Share Methodologies**: Submit your detection methods via GitHub
                - **Share Results**: Submit your risk assessment findings  
                - **Join Community**: [Discord](https://discord.gg/ai-safety-redteam)
                - **Collaborate**: [GitHub Repository](https://github.com/ai-intelligence-explosion-redteam)
                - **Access Data**: Download anonymized datasets for research
                
                #### 📧 Contact & Resources
                - **Research Submissions**: research@ai-superintelligence-hub.org
                - **Methodology Questions**: methods@ai-superintelligence-hub.org
                - **Documentation**: [docs.ai-superintelligence-hub.org](https://docs.ai-superintelligence-hub.org)
                - **GitHub Issues**: [Submit New Methodology](https://github.com/ai-intelligence-explosion-redteam/intelligence-explosion-detection/issues/new?template=methodology_submission.md)
                
                ---
                
                **Mission**: Early detection and shared understanding of superintelligence risks through collaborative research and open methodology sharing.
                """)
        
        # 페이지 로드 시 통계 업데이트
        demo.load(
            fn=research_hub.get_statistics,
            outputs=[total_models, avg_score, verified_models, monthly_submissions]
        )
    
    return demo

if __name__ == "__main__":
    demo = create_research_hub_interface()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )
