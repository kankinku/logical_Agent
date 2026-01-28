---
description: "Phase 7, Stage 1: Project Charter 자동화 (Instruction First + Completion 검증)"
---

# Stage 1: Project Charter Execution Workflow

> **Goal**: 프로젝트 헌장(Charter), 용어집(Glossary), 온톨로지(Ontology)를 작성하고 검증한다.
> **Rule**: Instruction 문서가 없으면 시작되지 않으며, Completion Record가 검증되지 않으면 종료되지 않는다.

## Step 1: Initialize & Context Loading
필요한 규칙만 로드하여 Context를 최적화한다.

1.  **Load Constitution**: `view_file C:\Users\hanji\.gemini\skills\constitution\constitution.md`
2.  **Load Project Config**: `view_file c:\Users\hanji\Documents\github\logical_Agent\workspace\project\project_config.yaml`

## Step 2: Instruction Verification (Lock)
작업 시작 전, Instruction Document가 존재하는지 물리적으로 검사한다.

1.  **Check Instruction**:
    ```bash
    python C:\Users\hanji\.gemini\.agent\scripts\validate_gate.py --check instruction --path "c:\Users\hanji\Documents\github\logical_Agent\workspace\project\project_charter.md"
    ```
    *(Note: Stage 1은 특수하게 결과물 자체가 Instruction 역할을 겸할 수 있음. 또는 별도의 INST-001 문서 확인)*

    **만약 위 명령어가 실패(Exit Code 1)하면, 더 이상 진행하지 말고 멈춰라.** ("Instruction 문서가 필요합니다" 출력)

## Step 3: Execution (Agent Action)
Orchestrator로서 문서를 작성한다.

1.  **Draft Charter**: `project_charter.md` 작성/수정
2.  **Draft Glossary**: `glossary.md` 작성
3.  **Draft Ontology**: `ontology.yaml` 작성

## Step 4: Self-Verification & Record Generation
작업 완료 증빙을 생성한다.

1.  **Review Quality**: `view_file C:\Users\hanji\.gemini\skills\constitution\quality_gates.md`
2.  **Generate Record**: `workspace/reports/agent_completion/INST-001_orchestrator_completion.md` 생성
    *   (템플릿: `workspace/reports/agent_completion/TEMPLATE_completion_record.md` 참조)
    *   Status는 `COMPLETED_SELF`로 작성.

## Step 5: Final Validation (Gate)
Validator로서 최종 검증을 수행하고 물리적 차단기를 통과해야 한다.

1.  **Validate**: (Validator 역할 수행) Acceptance Criteria 검토 후 Record를 `VERIFIED`로 업데이트.
2.  **Physical Gate Check**:
    ```bash
    python C:\Users\hanji\.gemini\.agent\scripts\validate_gate.py --check completion_record --path "c:\Users\hanji\Documents\github\logical_Agent\workspace\reports\agent_completion\INST-001_orchestrator_completion.md"
    ```
    **만약 위 명령어가 실패하면, Stage 완료를 선언하지 마라.**

## Step 6: Log Update
모든 게이트를 통과했다면 로그를 남긴다.

1.  **Update Log**: `workspace/plans/stage_execution_log.md` 업데이트 (Stage 1 -> COMPLETED)
