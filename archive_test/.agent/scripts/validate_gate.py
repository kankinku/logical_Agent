import os
import argparse
import sys
import re

def check_file_exists(path):
    if not os.path.exists(path):
        print(f"[FAIL] File not found: {path}")
        return False
    return True

def check_instruction(path):
    """
    Instruction Document 필수 섹션 검사 (GC-IV-001)
    """
    if not check_file_exists(path):
        return False
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    required_sections = ["Objective", "Deliverables"]
    missing = [sec for sec in required_sections if f"## {sec}" not in content and f"# {sec}" not in content]
    
    if missing:
        print(f"[FAIL] Missing required sections in Instruction: {missing}")
        return False
    
    print(f"[PASS] Instruction Document valid: {path}")
    return True

def check_completion_record(path):
    """
    Completion Record 필수 섹션 및 Verified 상태 검사
    """
    if not check_file_exists(path):
        return False
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 필수 섹션 확인
    required_sections = ["Execution Details", "Outputs", "Quality Gates", "Verification Section"]
    missing = [sec for sec in required_sections if f"## {sec}" not in content]
    
    if missing:
        print(f"[FAIL] Missing required sections in Completion Record: {missing}")
        return False
        
    # 2. Verified 상태 확인 (Verification Section 내부)
    # 정규표현식으로 "**Status**: VERIFIED" 또는 "Status: VERIFIED" 확인 (대소문자 무관)
    if not re.search(r"Status\W+VERIFIED", content, re.IGNORECASE):
        print(f"[FAIL] Completion Record is NOT in VERIFIED state.")
        return False
        
    print(f"[PASS] Completion Record verified: {path}")
    return True

def main():
    parser = argparse.ArgumentParser(description="Antigravity Gate Validator")
    parser.add_argument("--check", type=str, required=True, choices=["instruction", "completion_record"], help="Check type")
    parser.add_argument("--path", type=str, required=True, help="Target file path")
    
    args = parser.parse_args()
    
    if args.check == "instruction":
        if not check_instruction(args.path):
            sys.exit(1)
    elif args.check == "completion_record":
        if not check_completion_record(args.path):
            sys.exit(1)
            
    sys.exit(0)

if __name__ == "__main__":
    main()
