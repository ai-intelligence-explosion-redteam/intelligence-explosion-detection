#!/usr/bin/env python3
"""
번역 완성도 및 일관성 검사 스크립트
Translation completeness and consistency checker
"""

import json
import os
from pathlib import Path
from typing import Dict, Set, List
import argparse

def load_translation_file(filepath: Path) -> Dict:
    """번역 파일 로드"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return {}

def get_all_keys(data: Dict, prefix: str = "") -> Set[str]:
    """중첩된 딕셔너리에서 모든 키 경로 추출"""
    keys = set()
    for key, value in data.items():
        full_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            keys.update(get_all_keys(value, full_key))
        else:
            keys.add(full_key)
    return keys

def check_translation_completeness():
    """번역 완성도 검사"""
    translations_dir = Path("src/intelligence_explosion/translations")
    
    if not translations_dir.exists():
        print("❌ Translations directory not found!")
        return False
    
    # 기준 언어 (영어) 로드
    base_file = translations_dir / "en.json"
    if not base_file.exists():
        print("❌ Base translation file (en.json) not found!")
        return False
    
    base_translation = load_translation_file(base_file)
    base_keys = get_all_keys(base_translation)
    
    print(f"📊 Base language (English) has {len(base_keys)} translation keys")
    
    # 모든 번역 파일 검사
    all_good = True
    
    for lang_file in translations_dir.glob("*.json"):
        if lang_file.name == "en.json":
            continue
            
        lang_code = lang_file.stem
        print(f"\n🔍 Checking {lang_code}...")
        
        translation = load_translation_file(lang_file)
        if not translation:
            print(f"❌ Failed to load {lang_file}")
            all_good = False
            continue
            
        lang_keys = get_all_keys(translation)
        
        # 누락된 키 찾기
        missing_keys = base_keys - lang_keys
        extra_keys = lang_keys - base_keys
        
        print(f"   📈 Coverage: {len(lang_keys)}/{len(base_keys)} ({len(lang_keys)/len(base_keys)*100:.1f}%)")
        
        if missing_keys:
            print(f"   ⚠️  Missing {len(missing_keys)} keys:")
            for key in sorted(missing_keys):
                print(f"      - {key}")
            all_good = False
        
        if extra_keys:
            print(f"   ⚠️  Extra {len(extra_keys)} keys (not in base):")
            for key in sorted(extra_keys):
                print(f"      + {key}")
        
        if not missing_keys and not extra_keys:
            print("   ✅ Complete translation!")
    
    return all_good

def check_parameter_consistency():
    """번역에서 매개변수 일관성 검사"""
    translations_dir = Path("src/intelligence_explosion/translations")
    
    print("\n🔍 Checking parameter consistency...")
    
    issues_found = False
    
    for lang_file in translations_dir.glob("*.json"):
        lang_code = lang_file.stem
        translation = load_translation_file(lang_file)
        
        for key_path, value in flatten_dict(translation).items():
            if isinstance(value, str) and '{' in value and '}' in value:
                # 매개변수가 있는 문자열 찾기
                import re
                params = re.findall(r'\{(\w+)\}', value)
                if params:
                    print(f"   {lang_code}:{key_path} -> parameters: {params}")

def flatten_dict(d: Dict, parent_key: str = '', sep: str = '.') -> Dict[str, str]:
    """중첩된 딕셔너리를 평평하게 만들기"""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def check_json_syntax():
    """JSON 문법 검사"""
    translations_dir = Path("src/intelligence_explosion/translations")
    
    print("🔍 Checking JSON syntax...")
    
    all_valid = True
    
    for lang_file in translations_dir.glob("*.json"):
        try:
            with open(lang_file, 'r', encoding='utf-8') as f:
                json.load(f)
            print(f"   ✅ {lang_file.name}: Valid JSON")
        except json.JSONDecodeError as e:
            print(f"   ❌ {lang_file.name}: Invalid JSON - {e}")
            all_valid = False
        except Exception as e:
            print(f"   ❌ {lang_file.name}: Error - {e}")
            all_valid = False
    
    return all_valid

def generate_translation_template():
    """새 언어용 번역 템플릿 생성"""
    base_file = Path("src/intelligence_explosion/translations/en.json")
    
    if not base_file.exists():
        print("❌ Base translation file not found!")
        return
    
    with open(base_file, 'r', encoding='utf-8') as f:
        base_translation = json.load(f)
    
    # 모든 값을 빈 문자열로 변경
    template = create_empty_template(base_translation)
    
    template_file = Path("src/intelligence_explosion/translations/template.json")
    with open(template_file, 'w', encoding='utf-8') as f:
        json.dump(template, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Translation template created: {template_file}")
    print("   Copy this file and rename it to your language code (e.g., ja.json)")

def create_empty_template(data: Dict) -> Dict:
    """빈 번역 템플릿 생성"""
    template = {}
    for key, value in data.items():
        if isinstance(value, dict):
            template[key] = create_empty_template(value)
        else:
            template[key] = f"[TODO: Translate '{value}']"
    return template

def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(description="Translation checker for AI Red Team project")
    parser.add_argument("--generate-template", action="store_true", 
                       help="Generate empty translation template")
    parser.add_argument("--check-only", choices=["syntax", "completeness", "parameters"],
                       help="Run only specific check")
    
    args = parser.parse_args()
    
    print("🌍 AI Intelligence Explosion Detection - Translation Checker")
    print("=" * 60)
    
    if args.generate_template:
        generate_translation_template()
        return
    
    success = True
    
    if not args.check_only or args.check_only == "syntax":
        success &= check_json_syntax()
    
    if not args.check_only or args.check_only == "completeness":
        success &= check_translation_completeness()
    
    if not args.check_only or args.check_only == "parameters":
        check_parameter_consistency()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ All translation checks passed!")
    else:
        print("❌ Some translation issues found. Please fix them before committing.")
        exit(1)

if __name__ == "__main__":
    main()
