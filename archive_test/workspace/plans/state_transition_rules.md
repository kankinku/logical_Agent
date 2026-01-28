# State Transition Rules

> 상태 전이 규칙 - Completion Record 기반 실행 제어

---

## 핵심 원칙

> [!CAUTION]
> **"Completion Record 없음 = 작업 미완료"**

모든 Stage와 Task는 Completion Record가 VERIFIED 상태여야만 완료로 간주된다.

---

## 1. State Definitions

### 1.1 State Values
```yaml
states:
  NOT_STARTED:
    description: "아직 시작되지 않음"
    next_allowed: [IN_PROGRESS]
  
  IN_PROGRESS:
    description: "작업 진행 중"
    next_allowed: [COMPLETED_SELF]
    requirement: "Instruction Document 존재 (GC-IV-001)"
  
  COMPLETED_SELF:
    description: "에이전트 자체 완료 선언"
    next_allowed: [VERIFIED, REJECTED, NEEDS_REVISION]
    requirement: "Completion Record 생성 필수"
  
  VERIFIED:
    description: "Validator 검증 통과"
    next_allowed: []  # Terminal state
    requirement: "Completion Record VERIFIED 상태"
  
  REJECTED:
    description: "Validator 거부"
    next_allowed: [IN_PROGRESS]  # 재작업
    requirement: "Rejection Report 생성 필수"
  
  NEEDS_REVISION:
    description: "조건부 통과 (minor 수정 필요)"
    next_allowed: [IN_PROGRESS, VERIFIED]
    requirement: "Revision 항목 명시 필수"
```

---

## 2. Transition Rules

### 2.1 NOT_STARTED → IN_PROGRESS

**Trigger**: Orchestrator가 Stage/Task 할당

**Prerequisites**:
- [ ] Instruction Document 존재 (Task Spec or Stage Plan)
- [ ] 이전 Stage/Task가 VERIFIED 상태
- [ ] 의존성 해결됨

**Action**:
```yaml
check_prerequisites:
  - instruction_document: "EXISTS"
  - previous_stage: "VERIFIED"
  - dependencies: "RESOLVED"

if_all_pass:
  state: "IN_PROGRESS"
  log: "Stage Execution Log 업데이트"
else:
  state: "NOT_STARTED"
  error: "GC-IV-001 위반 또는 의존성 미해결"
```

---

### 2.2 IN_PROGRESS → COMPLETED_SELF

**Trigger**: 에이전트가 작업 완료 선언

**Prerequisites**:
- [ ] Completion Record 생성됨
- [ ] 모든 Deliverables 산출됨
- [ ] Self-Assessment 완료

**Action**:
```yaml
generate_completion_record:
  path: "workspace/reports/agent_completion/{InstructionID}_{Agent}_completion.md"
  required_sections:
    - "Execution Details"
    - "Outputs"
    - "Quality Gates"
    - "Acceptance Criteria"
    - "Self-Assessment"

if_record_valid:
  state: "COMPLETED_SELF"
  notify: "Reviewer"
else:
  state: "IN_PROGRESS"
  error: "Completion Record 누락 또는 불완전"
```

---

### 2.3 COMPLETED_SELF → VERIFIED

**Trigger**: Validator가 검증 수행

**Prerequisites**:
- [ ] Completion Record 존재
- [ ] Quality Gates 모두 PASS
- [ ] Acceptance Criteria 충족

**Action**:
```yaml
validator_checks:
  gate_1_logic: "PASS"
  gate_2_premise: "PASS"
  gate_3_reality: "PASS"
  acceptance_criteria: "ALL_MET"

if_all_pass:
  state: "VERIFIED"
  update_completion_record:
    verification_status: "VERIFIED"
    verified_by: "Validator"
    verified_date: "TIMESTAMP"
  update_stage_log:
    stage_status: "COMPLETED"
    next_stage: "ENABLED"
else:
  state: "REJECTED or NEEDS_REVISION"
```

---

### 2.4 COMPLETED_SELF → REJECTED

**Trigger**: Validator가 검증 실패 판정

**Conditions**:
- Quality Gate FAIL (critical)
- Acceptance Criteria 미충족
- 근거 부족 (L5 비율 과다)

**Action**:
```yaml
generate_rejection_report:
  path: "workspace/reports/rejection/{InstructionID}_rejection.md"
  required_sections:
    - "Rejection Reason"
    - "Failed Gate"
    - "Required Actions"

rollback:
  state: "IN_PROGRESS"
  stage_status: "IN_PROGRESS"
  blocking_issues: [list]
  next_stage: "BLOCKED"
```

---

### 2.5 REJECTED → IN_PROGRESS

**Trigger**: 에이전트가 재작업 시작

**Prerequisites**:
- [ ] Rejection Report 확인
- [ ] 재작업 계획 수립

**Action**:
```yaml
restart:
  state: "IN_PROGRESS"
  preserve_completion_record: true  # 버전 관리용
  create_new_record: true  # 재작업용
```

---

## 3. Stage-Level Transition

### 3.1 Stage Completion Rule
```
Stage N이 COMPLETED (VERIFIED)가 되려면:

1. Instruction Document 존재
2. Completion Record 생성
3. Completion Record Status = VERIFIED
4. Stage Execution Log 업데이트
```

### 3.2 Next Stage Enable Rule
```
Stage N+1이 시작 가능하려면:

1. Stage N Status = VERIFIED
2. Stage N Completion Record 존재
3. Stage N+1 Instruction Document 존재
```

---

## 4. Task-Level Transition

### 4.1 Task Completion Rule
```
Task가 COMPLETED가 되려면:

1. Task Spec 존재 (GC-IV-001)
2. Completion Record 생성
3. Acceptance Criteria 100% 충족
4. Completion Record Status = VERIFIED
```

### 4.2 Dependent Task Rule
```
Task B가 Task A에 의존할 때:

Task A Status != VERIFIED:
  THEN Task B Status = NOT_STARTED (BLOCKED)

Task A Status = VERIFIED:
  THEN Task B Status = NOT_STARTED (ENABLED)
```

---

## 5. Enforcement Mechanisms

### 5.1 GC-IV-001 Integration
```yaml
instruction_verification_lock:
  rule: "문서 없으면 작업 무효"
  enforcement:
    - "NOT_STARTED → IN_PROGRESS: Instruction 필수"
    - "IN_PROGRESS → COMPLETED_SELF: Completion Record 필수"
```

### 5.2 Quality Gates Integration
```yaml
quality_gates:
  gate_1: "Logic Verification"
  gate_2: "Premise Reliability"
  gate_3: "Reality Consistency"
  enforcement:
    - "COMPLETED_SELF → VERIFIED: 모든 Gate PASS 필수"
    - "FAIL → REJECTED"
```

---

## 6. State Transition Diagram

```
┌─────────────┐
│ NOT_STARTED │
└──────┬──────┘
       │ Instruction Document 존재
       ↓
┌─────────────┐
│ IN_PROGRESS │←──────────────┐
└──────┬──────┘               │
       │ Completion Record    │
       ↓                      │
┌────────────────┐            │
│ COMPLETED_SELF │            │
└───────┬────────┘            │
        │                     │
    ┌───┴───┐                 │
    ↓       ↓                 │
┌──────┐ ┌──────────┐         │
│VERIFIED REJECTED  │─────────┘
└──────┘ └──────────┘
   │
   ↓
(Stage 완료, Next Stage ENABLED)
```

---

## 7. 예외 처리

### 7.1 긴급 상황 (Emergency)
```yaml
emergency_override:
  condition: "시스템 장애, 보안 이슈"
  action:
    - "작업 우선 실행"
    - "24시간 이내 사후 Completion Record 생성"
    - "emergency_log.md 기록"
```

### 7.2 Exploration (탐색 작업)
```yaml
exploration_permit:
  condition: "기술 검증, POC"
  action:
    - "exploration_permit.md 작성"
    - "범위/기간 명시"
    - "결과 Completion Record로 변환"
```

---

> [!IMPORTANT]
> State Transition Rules는 **자동화 가능한 수준으로 명확하게** 정의되었습니다.
> 향후 State Machine으로 구현 가능합니다.
