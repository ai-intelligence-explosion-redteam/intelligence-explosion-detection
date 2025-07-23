#!/usr/bin/env python3
"""
HuggingFace Spaces 업데이트 스크립트
샘플 데이터가 추가된 리더보드를 배포합니다.
"""

import os
from huggingface_hub import HfApi

def update_spaces():
    """HuggingFace Spaces 업데이트"""
    api = HfApi()
    
    # 토큰은 환경변수에서 가져오거나 직접 입력
    token = os.getenv("HUGGINGFACE_TOKEN")  # 환경변수에서 토큰 가져오기
    if not token:
        print("❌ HUGGINGFACE_TOKEN 환경변수를 설정해주세요")
        return
    
    try:
        # app.py 업데이트
        api.upload_file(
            path_or_fileobj="huggingface_spaces/app.py",
            path_in_repo="app.py",
            repo_id="makarismov/ai-safety-leaderboard",
            repo_type="space",
            token=token
        )
        print("✅ app.py 업데이트 완료")
        
        print("🚀 리더보드 업데이트 성공!")
        print("🔗 URL: https://huggingface.co/spaces/makarismov/ai-safety-leaderboard")
        
    except Exception as e:
        print(f"❌ 업데이트 실패: {e}")

if __name__ == "__main__":
    update_spaces()
