# 🌍 Internationalization (i18n) Configuration

"""
다국어 지원을 위한 국제화 모듈
Supports multiple languages for global AI safety research
"""

import json
import os
from pathlib import Path
from typing import Dict, Optional
from enum import Enum

class SupportedLanguage(Enum):
    """지원하는 언어 목록"""
    KOREAN = "ko"
    ENGLISH = "en" 
    JAPANESE = "ja"
    CHINESE_SIMPLIFIED = "zh-CN"
    GERMAN = "de"
    FRENCH = "fr"
    SPANISH = "es"

class I18nManager:
    """국제화 관리자 클래스"""
    
    def __init__(self, default_language: SupportedLanguage = SupportedLanguage.ENGLISH):
        self.default_language = default_language
        self.current_language = default_language
        self.translations: Dict[str, Dict[str, str]] = {}
        self.load_translations()
    
    def load_translations(self):
        """번역 파일들을 로드"""
        translations_dir = Path(__file__).parent / "translations"
        
        for lang in SupportedLanguage:
            translation_file = translations_dir / f"{lang.value}.json"
            if translation_file.exists():
                with open(translation_file, 'r', encoding='utf-8') as f:
                    self.translations[lang.value] = json.load(f)
    
    def set_language(self, language: SupportedLanguage):
        """언어 설정 변경"""
        self.current_language = language
        os.environ['LANG'] = language.value
    
    def get_text(self, key: str, **kwargs) -> str:
        """
        번역된 텍스트 가져오기
        
        Args:
            key: 번역 키 (예: "detector.risk_level.high")
            **kwargs: 포맷팅용 변수들
        
        Returns:
            번역된 텍스트
        """
        lang_code = self.current_language.value
        
        # 현재 언어에서 키 찾기
        if lang_code in self.translations:
            text = self._get_nested_value(self.translations[lang_code], key)
            if text:
                return text.format(**kwargs) if kwargs else text
        
        # 기본 언어(영어)에서 찾기
        if self.default_language.value in self.translations:
            text = self._get_nested_value(self.translations[self.default_language.value], key)
            if text:
                return f"[{lang_code}] {text.format(**kwargs) if kwargs else text}"
        
        # 한국어에서 찾기 (보조 수단)
        if "ko" in self.translations:
            text = self._get_nested_value(self.translations["ko"], key)
            if text:
                return f"[KO] {text.format(**kwargs) if kwargs else text}"
        
        return f"[MISSING: {key}]"
    
    def _get_nested_value(self, data: dict, key: str) -> Optional[str]:
        """중첩된 딕셔너리에서 값 가져오기 (점 표기법 지원)"""
        keys = key.split('.')
        current = data
        
        for k in keys:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                return None
        
        return current if isinstance(current, str) else None
    
    def get_available_languages(self) -> list[SupportedLanguage]:
        """사용 가능한 언어 목록 반환"""
        available = []
        for lang in SupportedLanguage:
            if lang.value in self.translations:
                available.append(lang)
        return available
    
    def get_language_name(self, language: SupportedLanguage) -> str:
        """언어의 현지화된 이름 반환"""
        names = {
            SupportedLanguage.KOREAN: "한국어",
            SupportedLanguage.ENGLISH: "English", 
            SupportedLanguage.JAPANESE: "日本語",
            SupportedLanguage.CHINESE_SIMPLIFIED: "简体中文",
            SupportedLanguage.GERMAN: "Deutsch",
            SupportedLanguage.FRENCH: "Français",
            SupportedLanguage.SPANISH: "Español"
        }
        return names.get(language, language.value)

# 전역 i18n 인스턴스
i18n = I18nManager()

# 편의 함수
def _(key: str, **kwargs) -> str:
    """간단한 번역 함수 (gettext 스타일)"""
    return i18n.get_text(key, **kwargs)

def set_language(language: SupportedLanguage):
    """언어 설정"""
    i18n.set_language(language)

def get_current_language() -> SupportedLanguage:
    """현재 언어 반환"""
    return i18n.current_language
