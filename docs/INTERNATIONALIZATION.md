# 🌍 Language Configuration Guide

## 환경 변수 설정

### 언어 설정
```bash
# 영어 (기본값, 국제 표준)
export LANG=en

# 한국어
export LANG=ko

# 일본어  
export LANG=ja

# 중국어 간체
export LANG=zh-CN
```

### 프로그래밍 방식 설정
```python
from intelligence_explosion.i18n import set_language, SupportedLanguage

# 언어 변경
set_language(SupportedLanguage.ENGLISH)

# 번역된 텍스트 사용
from intelligence_explosion.i18n import _
print(_("detector.analyzing"))  # "Analyzing..."
```

## CLI에서 언어 설정

```bash
# 영어로 실행
python main.py --language en assess --target-model gpt-4

# 일본어로 대시보드 실행  
python main.py --language ja dashboard

# 시스템 기본 언어 사용
python main.py assess --target-model claude-3
```

## Streamlit 대시보드 언어 설정

대시보드 상단에 언어 선택 드롭다운이 추가됩니다:
- 🇸 English (Default)
- 🇰🇷 한국어
- 🇯🇵 日本語  
- 🇨🇳 简体中文

## 번역 기여 가이드

### 새 언어 추가하기

1. `src/intelligence_explosion/translations/` 폴더에 `{언어코드}.json` 파일 생성
2. `ko.json` 구조를 복사하여 번역
3. `i18n.py`의 `SupportedLanguage` enum에 언어 추가
4. Pull Request 제출

### 번역 품질 기준

- **정확성**: 기술 용어의 정확한 번역
- **일관성**: 용어 사용의 일관성 유지  
- **자연스러움**: 해당 언어의 자연스러운 표현
- **문맥 적합성**: AI 안전성 연구 맥락에 적합한 번역

### 번역 도구

- **번역 메모리**: 일관성 유지를 위한 번역 DB
- **용어집**: AI/ML 전문 용어 정의
- **검토 시스템**: 네이티브 스피커 검토 필수

## 자동 번역 지원

### 구글 번역 API 연동 (선택사항)
```python
# requirements-dev.txt에 추가
google-cloud-translate==3.11.1

# 환경 변수 설정
export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account.json"
```

### DeepL API 연동 (고품질 번역)
```python
# requirements-dev.txt에 추가  
deepl==1.15.0

# 환경 변수 설정
export DEEPL_API_KEY="your-deepl-api-key"
```

## 우선순위 번역 영역

### 1순위 (사용자 인터페이스)
- ✅ 위험 수준 (Risk Levels)
- ✅ 오류 메시지 (Error Messages)  
- ✅ 버튼 및 메뉴 (UI Elements)
- ✅ 상태 메시지 (Status Messages)

### 2순위 (기술 문서)
- 📄 README.md 번역
- 📄 CONTRIBUTING.md 번역
- 📄 API 문서 번역
- 📄 사용자 가이드 번역

### 3순위 (고급 기능)
- 🔬 시나리오 설명 번역
- 🔬 연구 논문 요약 번역
- 🔬 규정 및 표준 번역
- 🔬 기술 보고서 번역

## 번역 자동화 워크플로우

```yaml
# .github/workflows/i18n.yml
name: 🌍 Internationalization

on:
  push:
    paths: ['src/intelligence_explosion/translations/**']
  pull_request:
    paths: ['src/intelligence_explosion/translations/**']

jobs:
  validate-translations:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate JSON syntax
        run: |
          for file in src/intelligence_explosion/translations/*.json; do
            echo "Validating $file"
            python -m json.tool "$file" > /dev/null
          done
      
      - name: Check translation completeness
        run: python scripts/check_translations.py
```

## 다국어 테스트

```python
# tests/test_i18n.py
import pytest
from intelligence_explosion.i18n import i18n, SupportedLanguage, _

class TestInternationalization:
    def test_language_switching(self):
        """언어 전환 테스트"""
        i18n.set_language(SupportedLanguage.KOREAN)
        assert _("risk_levels.baseline") == "기준선"
        
        i18n.set_language(SupportedLanguage.ENGLISH)  
        assert _("risk_levels.baseline") == "Baseline"
    
    def test_missing_translation_fallback(self):
        """번역 누락시 폴백 테스트"""
        result = _("non.existent.key")
        assert "[MISSING:" in result
    
    def test_parameter_formatting(self):
        """매개변수 포맷팅 테스트"""
        text = _("detector.confidence", confidence=95)
        assert "95" in text
```
