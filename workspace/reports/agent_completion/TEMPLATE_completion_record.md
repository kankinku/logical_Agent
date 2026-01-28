# Agent Completion Record

> Instruction ID: {INSTRUCTION_ID}  
> Agent: {AGENT_TYPE}  
> Date: {YYYY-MM-DD HH:MM}

---

## Instruction Summary

**Instruction Document**: {path/to/instruction.md}  
**Objective**: {작업 목표}  
**Stage**: {Stage N}

---

## Execution Details

### Input
- **Task Spec**: {task_id or N/A}
- **Dependencies**: {dependency_list}
- **Prerequisites**: {prerequisite_list}

### Skills Used
| Skill ID | Usage | Rationale |
|----------|-------|-----------|
| {skill_id} | {how used} | {why needed} |

**Example**:
| Skill ID | Usage | Rationale |
|----------|-------|-----------|
| evidence-collection | 프로젝트 요구사항 근거 수집 | Evidence-First 원칙 준수 |
| architecture | 시스템 구조 설계 | 아키텍처 결정 필요 |

---

## Outputs

### Deliverables
- **File 1**: {path} - {description}
- **File 2**: {path} - {description}

### Evidence Collected
| Evidence Type | Source | Level | Reference |
|---------------|--------|-------|-----------|
| {type} | {source} | {L1-L5} | {ref} |

**Example**:
| Evidence Type | Source | Level | Reference |
|---------------|--------|-------|-----------|
| Observed Fact | project_charter.md | L1 | "목표: Evidence-First 시스템" |
| Expert Opinion | docs/12 - 최종 정리.md | L3 | "11-stage 추론 시스템" |

---

## Quality Gates

### Gate 1: Logic Verification
- [ ] 추론 과정 타당함
- [ ] 전제 완전함
- [ ] 순환 논증 없음

**Result**: PASS / FAIL  
**Findings**: {findings if any}

### Gate 2: Premise Reliability
- [ ] 모든 출처 명시됨
- [ ] 신뢰도 L3 이상

**Result**: PASS / FAIL  
**L1-L5 Distribution**: {L1: X, L2: Y, L3: Z, L4: A, L5: B}

### Gate 3: Reality Consistency
- [ ] 기술적 실현 가능
- [ ] 자원 확보 가능
- [ ] 타임라인 일관성

**Result**: PASS / FAIL

---

## Acceptance Criteria

| Criterion | Test Method | Result | Evidence |
|-----------|-------------|--------|----------|
| {criterion from Task Spec} | {test method} | PASS/FAIL | {evidence} |

**Example**:
| Criterion | Test Method | Result | Evidence |
|-----------|-------------|--------|----------|
| 규칙 문서로 금지 판단 가능 | 문서 리뷰 | PASS | constitution.md#prohibited |

---

## Self-Assessment

### Completion Status
- **Status**: COMPLETED_SELF
- **Confidence**: {0.0 - 1.0}
- **Issues Encountered**: {list or none}

### Assumptions Made
| Assumption | Cost | Pivotal | Impact if False |
|------------|------|---------|-----------------|
| {assumption} | {low/med/high} | {true/false} | {impact} |

### Gaps Identified
| Gap | Priority | Action |
|-----|----------|--------|
| {gap} | {HIGH/MED/LOW} | {action} |

---

## Review Request

### To Reviewer
- **Focus Areas**: {what to review carefully}
- **Known Limitations**: {what might need improvement}
- **Questions**: {any clarifications needed}

### To Validator
- **Acceptance Criteria**: {reference to Task Spec}
- **Evidence Package**: {list of evidence files}

---

## Verification Section (Filled by Validator)

### Verification Result
- **Status**: VERIFIED / REJECTED / NEEDS_REVISION
- **Verified By**: {Validator Agent}
- **Verified Date**: {YYYY-MM-DD HH:MM}

### Verification Findings
| Finding | Severity | Description | Action Required |
|---------|----------|-------------|-----------------|
| {finding} | {CRITICAL/MAJOR/MINOR} | {desc} | {action} |

### Final Decision
```
IF VERIFIED:
  - Stage Status → COMPLETED
  - Next Stage → ENABLED
  
IF REJECTED:
  - Stage Status → IN_PROGRESS (재작업)
  - Blocking Issues: {list}
  
IF NEEDS_REVISION:
  - Conditional Pass
  - Minor fixes required: {list}
```

---

## Metadata

**Created By**: {Agent Type}  
**Instruction ID**: {INSTRUCTION_ID}  
**Completion Record ID**: {RECORD_ID}  
**Stage**: {Stage N}  
**Project**: {project_name}

---

> [!CAUTION]
> 이 Completion Record가 VERIFIED 상태여야만 다음 Stage로 진행할 수 있습니다.
> Completion Record 없음 = 작업 미완료.
