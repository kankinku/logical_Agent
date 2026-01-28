---
description: "Stage 전이 (Transition) 제어 Workflow - 검증된 Stage만 통과"
---

# Stage Transition Workflow

> **Goal**: 현재 Stage가 완료(VERIFIED)되었는지 물리적으로 검증하고, 다음 Stage를 활성화한다.

## Step 1: Verify Current Stage
현재 Stage의 Completion Record가 물리적으로 `VERIFIED` 상태인지 확인한다.

1.  **Check Gate**:
    ```bash
    # 예: Stage 1 검증
    python C:\Users\hanji\.gemini\.agent\scripts\validate_gate.py --check completion_record --path "c:\Users\hanji\Documents\github\logical_Agent\workspace\reports\agent_completion\INST-001_orchestrator_completion.md"
    ```
    *(실제 실행 시에는 대상 Stage의 Record 경로를 지정)*

    **실패 시**: "이전 Stage가 완료되지 않았습니다." 출력 후 중단.

## Step 2: Enable Next Stage
다음 Stage 상태를 `NOT_STARTED (ENABLED)`로 변경한다.

1.  **Read Log**: `view_file c:\Users\hanji\Documents\github\logical_Agent\workspace\plans\stage_execution_log.md`
2.  **Update Log**: 다음 Stage 상태 업데이트.

## Step 3: Init Next Instruction
다음 Stage를 위한 빈 Instruction 파일을 생성한다.

1.  **Create Instruction**: 다음 Stage용 Instruction 템플릿 생성 (예: `project_config.yaml` 기반)
    *   Objective, Deliverables 섹션 포함 필수.
