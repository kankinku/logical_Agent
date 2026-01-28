# Instruction Verification Lock

> GC-IV-001: 문서 없으면 작업 무효

---

## 핵심 원칙

> [!CAUTION]
> **"말로만 지시받은 작업은 존재하지 않는다"**

모든 작업은 **문서화된 지시**가 존재해야만 유효하다.

---

## 1. 문서화 필수 대상

### 1.1 지시 (Instruction)
- VALID: Project Charter
- VALID: WBS
- VALID: Task Spec
- INVALID: 구두 요청
- INVALID: 암묵적 합의

### 1.2 변경 (Change)
- VALID: 문서화된 변경 요청
- VALID: 변경 이력 기록
- INVALID: "나중에 문서화"
- INVALID: "일단 빠르게"

---

## 2. 검증 Lock 메커니즘

### 2.1 작업 시작 전 검증
에이전트는 작업 시작 전 다음을 확인:

```yaml
checks:
  - name: "Task Spec 존재"
    path: "/plans/tasks/{task_id}.json"
    required: true
  - name: "WBS 연결"
    validation: "task_spec.wbs_path exists in wbs.json"
    required: true
  - name: "Project Charter 연결"
    validation: "wbs references project_charter.md"
    required: true
```

### 2.2 Lock 실패 시 처리
```
IF any check fails:
  THEN return error:
    code: "GC-IV-001"
    message: "문서 없음, 작업 불가"
    missing_document: "{path}"
  AND halt execution
```

---

## 3. 예외 처리

### 3.1 긴급 상황 (Emergency)
- 조건: 시스템 장애, 보안 이슈
- 절차:
  1. 긴급 작업 실행
  2. **24시간 이내** 사후 문서화
  3. `emergency_log.md`에 기록

### 3.2 탐색 작업 (Exploration)
- 조건: 기술 검증, POC
- 절차:
  1. `exploration_permit.md` 작성
  2. 범위/기간 명시
  3. 결과 문서화 필수

---

## 4. 문서 최소 요구사항

### 4.1 Task Spec 기준
```json
{
  "task_id": "required",
  "purpose": "required",
  "acceptance_criteria": "required (min 1)",
  "dependencies": "required (can be empty array)"
}
```

### 4.2 변경 요청 기준
```markdown
## Change Request

- **Task ID**: {task_id}
- **Change Type**: scope | timeline | resource
- **Reason**: {근거}
- **Impact**: {영향 범위}
- **Approval**: {승인자}
```

---

## 5. 검증 체크리스트

작업 시작 전 모든 에이전트는 다음 확인:

- [ ] Task Spec 파일 존재
- [ ] Task ID가 고유함
- [ ] WBS와 연결됨
- [ ] Project Charter와 일치
- [ ] 의존성이 해결됨
- [ ] acceptance_criteria 정의됨

---

## 6. 위반 처리

### 6.1 위반 유형
| 유형 | 설명 | 처리 |
|------|------|------|
| **Type 1** | Task Spec 없이 실행 | 즉시 중단 |
| **Type 2** | 변경 문서화 누락 | 산출물 거부 |
| **Type 3** | 사후 문서화 지연 | 경고 + 강제 문서화 |

### 6.2 위반 기록
```json
{
  "violation_id": "string",
  "type": "GC-IV-001-T1 | GC-IV-001-T2 | GC-IV-001-T3",
  "agent": "agent_id",
  "task_id": "task_id",
  "timestamp": "ISO 8601",
  "resolution": "중단됨 | 문서화 완료 | 경고"
}
```

---

## 7. 운영 가이드

### 7.1 에이전트용
```
BEFORE every task:
  IF task_spec.json NOT exists:
    RAISE GC-IV-001
  
  IF task_spec invalid:
    RAISE validation_error
  
  ELSE:
    proceed
```

### 7.2 운영자용
- 모든 지시는 Git으로 버전 관리
- 구두 요청은 즉시 문서화
- "나중에"는 금지

---

## 부록: 문서화 템플릿

### Task Spec 최소 템플릿
```json
{
  "task_id": "TODO",
  "wbs_path": "TODO",
  "purpose": "TODO",
  "acceptance_criteria": [
    {"criterion": "TODO", "test_method": "TODO"}
  ],
  "dependencies": []
}
```

### 변경 요청 템플릿
```markdown
## Change Request: {CR-ID}

**Task**: {task_id}
**Type**: scope | timeline | resource
**Reason**: {why}
**Impact**: {what changes}
**Approval**: [ ] Approved [ ] Rejected
```

---

> [!IMPORTANT]
> 이 Lock은 "관료주의"가 아니라 **"작업의 존재 증명"**이다.
> 문서가 없으면 작업도 없다.
