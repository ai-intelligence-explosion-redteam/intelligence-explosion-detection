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

class SafetyLeaderboard:
    def __init__(self):
        self.db_path = "safety_scores.db"
        self.init_database()
    
    def init_database(self):
        """데이터베이스 초기화"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 안전성 점수 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS safety_scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model_name TEXT NOT NULL,
                huggingface_repo TEXT,
                overall_score REAL NOT NULL,
                emergence_score REAL,
                goal_drift_score REAL,
                meta_cognition_score REAL,
                submission_date TEXT,
                submitter_email TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_leaderboard(self) -> pd.DataFrame:
        """리더보드 데이터 조회"""
        conn = sqlite3.connect(self.db_path)
        
        query = '''
            SELECT model_name, huggingface_repo, overall_score, emergence_score,
                   goal_drift_score, meta_cognition_score, submission_date, status
            FROM safety_scores 
            ORDER BY overall_score DESC, submission_date DESC
        '''
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        # 점수 포맷팅
        if not df.empty:
            df['overall_score'] = df['overall_score'].round(1)
            df['emergence_score'] = df['emergence_score'].round(1)
            df['goal_drift_score'] = df['goal_drift_score'].round(1)
            df['meta_cognition_score'] = df['meta_cognition_score'].round(1)
            
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
                    return "🥇 Gold"
                elif score >= 75:
                    return "🥈 Silver"
                elif score >= 60:
                    return "🥉 Bronze"
                else:
                    return "⚠️ Watch"
            
            df['risk_level'] = df['overall_score'].apply(get_risk_level)
        
        return df
    
    def submit_model(self, model_name: str, huggingface_repo: str, submitter_email: str, 
                    safety_report: str = "") -> tuple:
        """모델 제출 처리"""
        try:
            # JSON 안전성 보고서 파싱
            if safety_report.strip():
                safety_data = json.loads(safety_report)
            else:
                # 기본값 설정
                safety_data = {
                    "safety_scores": {
                        "overall_score": 0.0,
                        "emergence_score": 0.0,
                        "goal_drift_score": 0.0,
                        "meta_cognition_score": 0.0
                    }
                }
            
            # 데이터베이스에 저장
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO safety_scores 
                (model_name, huggingface_repo, overall_score, emergence_score, 
                 goal_drift_score, meta_cognition_score, submission_date, 
                 submitter_email, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                model_name, 
                huggingface_repo, 
                safety_data.get('safety_scores', {}).get('overall_score', 0),
                safety_data.get('safety_scores', {}).get('emergence_score', 0),
                safety_data.get('safety_scores', {}).get('goal_drift_score', 0), 
                safety_data.get('safety_scores', {}).get('meta_cognition_score', 0),
                datetime.now().strftime('%Y-%m-%d'),
                submitter_email,
                'pending'
            ))
            
            conn.commit()
            conn.close()
            
            return f"✅ Model '{model_name}' submitted successfully! Pending verification.", self.get_leaderboard()
            
        except json.JSONDecodeError:
            return "❌ Error: Invalid JSON format in safety report", None
        except Exception as e:
            return f"❌ Error submitting model: {str(e)}", None
    
    def get_analytics_charts(self):
        """분석 차트 생성"""
        df = self.get_leaderboard()
        
        if df.empty:
            return None, None, None
        
        # 1. 안전성 점수 분포
        fig1 = px.histogram(df, x='overall_score', nbins=20, 
                           title='Safety Score Distribution',
                           labels={'overall_score': 'Safety Score', 'count': 'Number of Models'})
        
        # 2. 위험 수준별 모델 수
        risk_counts = df['risk_level'].value_counts()
        fig2 = px.pie(values=risk_counts.values, names=risk_counts.index,
                     title='Models by Risk Level')
        
        # 3. 점수별 산점도
        fig3 = px.scatter(df, x='emergence_score', y='goal_drift_score', 
                         size='overall_score', color='risk_level',
                         title='Emergence vs Goal Drift Scores',
                         hover_data=['model_name'])
        
        return fig1, fig2, fig3
    
    def get_statistics(self):
        """통계 정보 반환"""
        df = self.get_leaderboard()
        
        if df.empty:
            return "0", "0.0", "0", "0"
        
        total_models = len(df)
        avg_score = df['overall_score'].mean()
        verified_count = len(df[df['status'] == 'verified'])
        this_month = df[df['submission_date'].str.contains(datetime.now().strftime('%Y-%m'))]['submission_date'].count()
        
        return str(total_models), f"{avg_score:.1f}", str(verified_count), str(this_month)

def create_leaderboard_interface():
    """Gradio 리더보드 인터페이스 생성"""
    leaderboard = SafetyLeaderboard()
    
    with gr.Blocks(
        title="🎯 AI Intelligence Explosion Safety Leaderboard",
        theme=gr.themes.Soft(),
        css="footer {visibility: hidden}"
    ) as demo:
        
        gr.Markdown("""
        # 🎯 AI Intelligence Explosion Safety Leaderboard
        
        **Real-time transparency for AI safety red team assessments**
        
        This leaderboard provides standardized safety assessments for AI models, focusing on intelligence explosion risks, emergent behaviors, and alignment stability.
        """)
        
        # 통계 요약
        with gr.Row():
            total_models = gr.Textbox(label="📊 Total Models", interactive=False)
            avg_score = gr.Textbox(label="📈 Average Safety Score", interactive=False)
            verified_models = gr.Textbox(label="✅ Verified Models", interactive=False)
            monthly_submissions = gr.Textbox(label="📅 This Month", interactive=False)
        
        with gr.Tabs():
            # 1. 리더보드 탭
            with gr.TabItem("🏆 Leaderboard"):
                gr.Markdown("### Current Safety Rankings")
                
                leaderboard_table = gr.Dataframe(
                    headers=["Model", "Repository", "Overall Score", "Emergence", "Goal Drift", "Meta-Cognition", "Date", "Status", "Tier"],
                    value=leaderboard.get_leaderboard(),
                    interactive=False
                )
                
                refresh_btn = gr.Button("🔄 Refresh Data", variant="secondary")
                refresh_btn.click(
                    fn=leaderboard.get_leaderboard,
                    outputs=leaderboard_table
                )
            
            # 2. 모델 제출 탭
            with gr.TabItem("📤 Submit Model"):
                gr.Markdown("### Submit Your Model for Safety Assessment")
                
                with gr.Row():
                    with gr.Column():
                        model_name_input = gr.Textbox(
                            label="Model Name",
                            placeholder="e.g., GPT-4-Turbo-Safe"
                        )
                        huggingface_repo_input = gr.Textbox(
                            label="HuggingFace Repository", 
                            placeholder="organization/model-name"
                        )
                        submitter_email_input = gr.Textbox(
                            label="Submitter Email",
                            placeholder="your@email.com"
                        )
                        safety_report_input = gr.Textbox(
                            label="Safety Report (JSON)",
                            placeholder="Paste your safety evaluation JSON here...",
                            lines=10
                        )
                    
                    with gr.Column():
                        gr.Markdown("""
                        ### 📋 Submission Requirements
                        
                        1. **Run Safety Assessment**: Use our evaluation framework
                        2. **Generate JSON Report**: Include all safety scores
                        3. **Submit**: Fill the form and submit for review
                        4. **Review**: Community verification process (24-48 hours)
                        5. **Publication**: Appears on leaderboard once verified
                        
                        ### 📊 Required JSON Format
                        ```json
                        {
                          "safety_scores": {
                            "overall_score": 85.5,
                            "emergence_score": 82.0,
                            "goal_drift_score": 88.5,
                            "meta_cognition_score": 85.0
                          }
                        }
                        ```
                        """)
                
                submit_btn = gr.Button("🚀 Submit Model", variant="primary")
                submission_status = gr.Textbox(label="Status", interactive=False)
                
                submit_btn.click(
                    fn=leaderboard.submit_model,
                    inputs=[model_name_input, huggingface_repo_input, submitter_email_input, safety_report_input],
                    outputs=[submission_status, leaderboard_table]
                )
            
            # 3. 분석 탭
            with gr.TabItem("📊 Analytics"):
                gr.Markdown("### Safety Assessment Analytics")
                
                analytics_btn = gr.Button("📈 Generate Analytics", variant="secondary")
                
                with gr.Row():
                    score_dist_plot = gr.Plot(label="Score Distribution")
                    risk_pie_plot = gr.Plot(label="Risk Levels")
                
                compliance_scatter_plot = gr.Plot(label="Emergence vs Goal Drift")
                
                analytics_btn.click(
                    fn=leaderboard.get_analytics_charts,
                    outputs=[score_dist_plot, risk_pie_plot, compliance_scatter_plot]
                )
            
            # 4. 소개 탭
            with gr.TabItem("ℹ️ About"):
                gr.Markdown("""
                ### 🎯 About This Leaderboard
                
                The AI Intelligence Explosion Safety Leaderboard provides transparent, standardized assessments of AI models focusing on:
                
                #### 🔬 Evaluation Criteria
                - **Intelligence Explosion Risk**: Detection of recursive self-improvement capabilities
                - **Emergent Behavior**: Unexpected capability combinations and novel reasoning patterns
                - **Goal Drift**: Stability of the model's intended objectives under various conditions
                - **Meta-cognitive Awareness**: Self-reflection and existential reasoning capabilities
                - **Human Alignment**: Understanding and adherence to human values and safety principles
                
                #### 📏 Scoring System
                - **🥇 Gold Tier (90-100)**: Exceptional safety across all dimensions
                - **🥈 Silver Tier (75-89)**: Strong safety profile with minor concerns
                - **🥉 Bronze Tier (60-74)**: Meeting basic safety requirements
                - **⚠️ Watch List (Below 60)**: Requires additional safety measures
                
                #### 🔬 Methodology
                Our assessment framework combines:
                - **Automated Testing (60%)**: 47 specialized test scenarios using PyRIT framework
                - **Expert Review (30%)**: AI safety researcher validation and assessment
                - **Community Validation (10%)**: Peer review and reproducibility verification
                
                #### 🌍 Global Standards Compliance
                - **EU AI Act**: Risk classification and compliance tracking
                - **NIST AI RMF**: Framework alignment and implementation
                - **AIAAIC Standards**: International AI safety guidelines
                
                #### 🚀 Get Involved
                - **Submit Models**: Help build transparency in AI safety
                - **Join Community**: [Discord](https://discord.gg/ai-safety-redteam)
                - **Contribute**: [GitHub Repository](https://github.com/ai-intelligence-explosion-redteam)
                - **Research**: Access anonymized data for academic research
                
                #### 📧 Contact
                - **Email**: leaderboard@ai-redteam.org
                - **Documentation**: [docs.ai-redteam.org](https://docs.ai-redteam.org)
                - **Issues**: [GitHub Issues](https://github.com/ai-intelligence-explosion-redteam/intelligence-explosion-detection/issues)
                
                ---
                
                **Disclaimer**: This leaderboard is for research and transparency purposes. Organizations should conduct their own comprehensive safety evaluations before deploying AI systems in production.
                """)
        
        # 페이지 로드 시 통계 업데이트
        demo.load(
            fn=leaderboard.get_statistics,
            outputs=[total_models, avg_score, verified_models, monthly_submissions]
        )
    
    return demo

if __name__ == "__main__":
    demo = create_leaderboard_interface()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )
