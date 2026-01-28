import os
import base64

# 압축할 대상 파일 목록 (상대 경로 매핑)
TARGET_MAP = {
    r"C:\Users\hanji\.gemini\skills\constitution": "skills/constitution",
    r"C:\Users\hanji\.gemini\skills\registry": "skills/registry",
    r"C:\Users\hanji\.gemini\skills\skills\reasoning\evidence": "skills/reasoning/evidence",
    r"c:\Users\hanji\Documents\github\logical_Agent\workspace\project": "workspace/project",
    r"c:\Users\hanji\Documents\github\logical_Agent\workspace\agents": "workspace/agents",
    r"c:\Users\hanji\Documents\github\logical_Agent\workspace\plans": "workspace/plans",
    r"c:\Users\hanji\Documents\github\logical_Agent\workspace\reports\agent_completion": "workspace/reports/agent_completion",
    r"C:\Users\hanji\.gemini\.agent\scripts": ".agent/scripts",
    r"C:\Users\hanji\.gemini\.agent\workflows": ".agent/workflows",
}

# Target System용 README 내용 (설치 시 생성됨)
README_CONTENT = """# Logical Agent System (Evidence-First Edition)

> "착한 사람이 아닌, 올바른 구조가 품질을 보장한다"

본 시스템은 작업의 모든 단계에서 **근거(Evidence)**를 요구하고, **물리적 검증(Physical Gate)**을 통과해야만 다음 단계로 넘어갈 수 있는 **구조적 강제력**을 가진 에이전트 시스템입니다.

---

## 🚀 빠른 시작 (Quick Start)

### 1. 프로젝트 시작 (Stage 1)
프로젝트 헌장(Charter) 작성을 시작으로 에이전트를 가동합니다.

```bash
/run stage_1_charter
# Antigravity 환경이 아닐 경우: .agent/workflows/stage_1_charter.md 참조
```

이 명령어는 다음을 자동 수행합니다:
1. Instruction 문서 존재 확인 (물리적 차단)
2. Project Charter 작성
3. Completion Record 생성
4. Validator 검증 (물리적 차단)

### 2. 단계 이동 (Next Stage)
현재 단계가 완료되었는지 검증하고 다음 단계를 엽니다.

```bash
/run stage_transition
```

---

## 🏗️ 시스템 구조

*   **`.agent/`**: **자동화 엔진**. 물리적 차단 스크립트(`validate_gate.py`)와 워크플로우.
*   **`skills/`**: **두뇌**. 헌법(Constitution), 레지스트리, 핵심 스킬.
*   **`workspace/`**: **작업 공간**. 프로젝트 설정(`project_config.yaml`), 에이전트 정의, 로그.

---

## 🛡️ 강제 로직 (Enforcement)

위반 시 `Exit Code 1`로 차단됩니다.

1.  **Instruction First**: 지시 문서 없이 작업 시작 불가.
2.  **No Silent Completion**: Completion Record(완료 증빙) 없이 Stage 완료 불가.
3.  **Verification Gate**: Validator의 승인(`VERIFIED`) 없이 다음 단계 진행 불가.
"""

INSTALLER_TEMPLATE = """import os
import base64
import sys

# 설치될 README 내용
README_TEXT = {README_REPR}

def create_file(path, content_b64):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            f.write(base64.b64decode(content_b64))
        print(f"[OK] Created: {{path}}")
    except Exception as e:
        print(f"[FAIL] Failed to create {{path}}: {{e}}")

def create_readme(base_dir):
    path = os.path.join(base_dir, "README.md")
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(README_TEXT)
        print(f"[OK] Created: {{path}} (Generated Config)")
    except Exception as e:
        print(f"[FAIL] Failed to create README.md: {{e}}")

def main():
    print("=== Logical Agent System Installer ===")
    base_dir = os.getcwd()
    print(f"Installing to: {{base_dir}}")
    
    files = {FILES_DATA}
    
    for rel_path, content in files.items():
        full_path = os.path.join(base_dir, rel_path)
        create_file(full_path, content)
    
    # README 생성
    create_readme(base_dir)
        
    print("\\n=== Installation Complete ===")
    print("Run: /run stage_1_charter to start")

if __name__ == "__main__":
    main()
"""

def generate_installer():
    files_data = {}
    
    print("Scanning files...")
    for src_dir, target_rel_dir in TARGET_MAP.items():
        if not os.path.exists(src_dir):
            print(f"Warning: Source dir not found: {src_dir}")
            continue
            
        for root, dirs, files in os.walk(src_dir):
            for file in files:
                src_path = os.path.join(root, file)
                rel_from_src = os.path.relpath(src_path, src_dir)
                target_path = os.path.join(target_rel_dir, rel_from_src)
                target_path = target_path.replace("\\\\", "/")
                
                with open(src_path, 'rb') as f:
                    content = f.read()
                    files_data[target_path] = base64.b64encode(content).decode('utf-8')
                
                print(f"Packed: {target_path}")

    # 템플릿에 데이터 주입
    # README_CONTENT를 안전하게 문자열 리터럴로 변환 (repr 사용)
    output_content = INSTALLER_TEMPLATE.replace("{FILES_DATA}", str(files_data))
    output_content = output_content.replace("{README_REPR}", repr(README_CONTENT))
    
    output_path = r"c:\Users\hanji\Documents\github\logical_Agent\agent_installer.py"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output_content)
        
    print(f"\nSuccessfully generated installer at: {output_path}")

if __name__ == "__main__":
    generate_installer()
