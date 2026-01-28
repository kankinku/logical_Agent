import os
import base64

# 압축할 대상 파일 목록 (상대 경로 매핑)
# Source Path (현재 시스템) -> Target Path (설치될 시스템의 상대 경로)
TARGET_MAP = {
    # 1. Global Constitution
    r"C:\Users\hanji\.gemini\skills\constitution": "skills/constitution",
    
    # 2. Global Registry
    r"C:\Users\hanji\.gemini\skills\registry": "skills/registry",
    
    # 3. Core Skills
    r"C:\Users\hanji\.gemini\skills\skills\reasoning\evidence": "skills/reasoning/evidence",
    
    # 4. Workspace (plans, reports는 빈 디렉토리만 있어도 됨, 하지만 템플릿 포함)
    r"c:\Users\hanji\Documents\github\logical_Agent\workspace\project": "workspace/project",
    r"c:\Users\hanji\Documents\github\logical_Agent\workspace\agents": "workspace/agents",
    r"c:\Users\hanji\Documents\github\logical_Agent\workspace\plans": "workspace/plans",
    r"c:\Users\hanji\Documents\github\logical_Agent\workspace\reports\agent_completion": "workspace/reports/agent_completion",
    
    # 5. Antigravity Agent Configuration
    r"C:\Users\hanji\.gemini\.agent\scripts": ".agent/scripts",
    r"C:\Users\hanji\.gemini\.agent\workflows": ".agent/workflows",
}

INSTALLER_TEMPLATE = """import os
import base64
import sys

def create_file(path, content_b64):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            f.write(base64.b64decode(content_b64))
        print(f"[OK] Created: {path}")
    except Exception as e:
        print(f"[FAIL] Failed to create {path}: {e}")

def main():
    print("=== Logical Agent System Installer ===")
    base_dir = os.getcwd()
    print(f"Installing to: {base_dir}")
    
    files = {FILES_DATA}
    
    for rel_path, content in files.items():
        full_path = os.path.join(base_dir, rel_path)
        create_file(full_path, content)
        
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
                
                # 계산된 상대 경로 (Source root 기준)
                rel_from_src = os.path.relpath(src_path, src_dir)
                # 최종 Target 경로
                target_path = os.path.join(target_rel_dir, rel_from_src)
                
                # Windows 경로 구분자 통일
                target_path = target_path.replace("\\\\", "/")
                
                with open(src_path, 'rb') as f:
                    content = f.read()
                    files_data[target_path] = base64.b64encode(content).decode('utf-8')
                
                print(f"Packed: {target_path}")

    # Generate Output
    output_content = INSTALLER_TEMPLATE.replace("{FILES_DATA}", str(files_data))
    
    output_path = r"c:\Users\hanji\Documents\github\logical_Agent\agent_installer.py"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output_content)
        
    print(f"\nSuccessfully generated installer at: {output_path}")

if __name__ == "__main__":
    generate_installer()
