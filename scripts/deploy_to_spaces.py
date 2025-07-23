#!/usr/bin/env python3
"""
HuggingFace Spaces 자동 배포 스크립트
Automatic deployment script for HuggingFace Spaces
"""

import os
import shutil
from pathlib import Path
from huggingface_hub import HfApi, Repository
import tempfile

def deploy_to_huggingface_spaces():
    """HuggingFace Spaces에 리더보드 배포"""
    
    # 환경 변수 확인
    hf_token = os.getenv('HF_TOKEN')
    if not hf_token:
        print("❌ HF_TOKEN environment variable not set")
        return False
    
    # HuggingFace API 초기화
    api = HfApi(token=hf_token)
    
    # Space 정보
    space_id = "ai-intelligence-explosion-redteam/safety-leaderboard"
    
    try:
        # Space가 존재하는지 확인, 없으면 생성
        try:
            space_info = api.space_info(space_id)
            print(f"✅ Space {space_id} already exists")
        except Exception:
            print(f"🆕 Creating new Space: {space_id}")
            api.create_repo(
                repo_id=space_id,
                repo_type="space",
                space_sdk="gradio",
                private=False
            )
        
        # 임시 디렉토리에서 작업
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Space 클론
            repo = Repository(
                local_dir=temp_path,
                clone_from=f"https://huggingface.co/spaces/{space_id}",
                token=hf_token
            )
            
            # 기존 파일 정리 (README.md 제외)
            for item in temp_path.iterdir():
                if item.name not in ['.git', 'README.md']:
                    if item.is_file():
                        item.unlink()
                    elif item.is_dir():
                        shutil.rmtree(item)
            
            # 새 파일들 복사
            spaces_dir = Path("huggingface_spaces")
            
            # 주요 파일들 복사
            shutil.copy2(spaces_dir / "app.py", temp_path / "app.py")
            shutil.copy2(spaces_dir / "requirements.txt", temp_path / "requirements.txt")
            
            # README.md 업데이트 (덮어쓰기)
            shutil.copy2(spaces_dir / "README.md", temp_path / "README.md")
            
            # 데이터베이스 초기화 (비어있는 DB)
            db_path = temp_path / "safety_scores.db"
            if not db_path.exists():
                # 빈 데이터베이스 파일 생성
                with open(db_path, 'w') as f:
                    pass
            
            # Git 설정
            repo.git_config_username_and_email(
                username="AI Red Team Bot",
                email="bot@ai-redteam.org"
            )
            
            # 변경사항 커밋 및 푸시
            repo.git_add(auto_lfs_track=True)
            
            # 변경사항이 있는지 확인
            if repo.git_status():
                commit_message = f"🚀 Deploy leaderboard update - {os.getenv('GITHUB_SHA', 'manual')[:8]}"
                repo.git_commit(commit_message)
                repo.git_push()
                print(f"✅ Successfully deployed to {space_id}")
            else:
                print("ℹ️  No changes to deploy")
        
        # Space URL 출력
        space_url = f"https://huggingface.co/spaces/{space_id}"
        print(f"🔗 Leaderboard URL: {space_url}")
        
        return True
        
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        return False

def setup_space_settings(space_id: str, api: HfApi):
    """Space 설정 구성"""
    try:
        # Space 메타데이터 업데이트
        api.update_repo_settings(
            repo_id=space_id,
            repo_type="space",
            description="Real-time leaderboard for AI safety red team assessments",
            website="https://github.com/ai-intelligence-explosion-redteam/intelligence-explosion-detection",
            tags=[
                "ai-safety", 
                "red-team", 
                "intelligence-explosion", 
                "leaderboard", 
                "evaluation",
                "gradio"
            ]
        )
        print("✅ Space settings updated")
        
    except Exception as e:
        print(f"⚠️  Could not update space settings: {e}")

def validate_deployment(space_id: str):
    """배포 검증"""
    import requests
    import time
    
    # Space가 시작될 때까지 대기
    space_url = f"https://{space_id.replace('/', '-')}.hf.space"
    
    print("🔄 Waiting for Space to start...")
    for attempt in range(12):  # 2분 대기
        try:
            response = requests.get(space_url, timeout=10)
            if response.status_code == 200:
                print(f"✅ Space is live at {space_url}")
                return True
        except:
            pass
        
        time.sleep(10)
        print(f"⏳ Attempt {attempt + 1}/12...")
    
    print("⚠️  Could not verify Space deployment")
    return False

if __name__ == "__main__":
    print("🚀 Starting HuggingFace Spaces deployment...")
    
    success = deploy_to_huggingface_spaces()
    
    if success:
        print("\n🎉 Deployment completed successfully!")
        
        # 배포 검증
        validate_deployment("ai-intelligence-explosion-redteam/safety-leaderboard")
        
        print("\n📝 Next steps:")
        print("1. Test the leaderboard interface")
        print("2. Submit a test model")
        print("3. Announce to the community")
        print("4. Share on social media")
        
    else:
        print("\n❌ Deployment failed!")
        exit(1)
