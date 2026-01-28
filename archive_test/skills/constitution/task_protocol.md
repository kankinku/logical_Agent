# Task Protocol

> 탑다운 Stage 1~5 규정 및 Task Spec 표준

---

## Stage 1. Project Charter 확정

### 목적
프로젝트의 경계와 성공 기준을 명문화

### 필수 산출물
`project_charter.md` (다음 포함)

### 필수 항목
```yaml
goal: "프로젝트 목표"
non_goals: ["비목표 1", "비목표 2"]
scope:
  included: ["범위 내 항목"]
  excluded: ["범위 외 항목"]
constraints: ["제약사항"]
success_criteria:
  - criterion: "성공 기준 1"
    measurement: "측정 방법"
```

### 통과 조건
- [ ] 목표/비목표 명확히 구분
- [ ] 성공 기준이 측정 가능
- [ ] Validator 승인

---

## Stage 2. WBS 생성

### 목적
프로젝트를 3~4레벨로 분해하고 의존성 명시

### 필수 산출물
`wbs.json`

### WBS 구조
```json
{
  "workstream_1": {
    "components": {
      "component_1_1": {
        "units": ["unit_1_1_1", "unit_1_1_2"]
      }
    },
    "dependencies": ["workstream_2"]
  }
}
```

### 레벨 정의
1. **Workstream** (워크스트림) - 큰 작업 영역
2. **Component** (구성요소) - 독립적인 기능 모듈
3. **Unit** (구현단위) - 실제 구현 작업
4. **Task** (태스크) - 최소 실행 단위 (Stage 3에서 생성)

### 통과 조건
- [ ] 모든 말단이 1주일 이내 구현 가능 크기
- [ ] 의존성이 DAG (순환 참조 없음)
- [ ] Reviewer 승인

---

## Stage 3. Task Spec 표준화

### 목적
모든 WBS 말단을 표준화된 태스크로 변환

### 필수 산출물
`/plans/tasks/{task_id}.json`

### Task Spec JSON Schema
```json
{
  "task_id": "string",
  "wbs_path": "workstream.component.unit",
  "purpose": "목적 설명",
  "inputs": [
    {
      "name": "입력명",
      "source": "출처"
    }
  ],
  "outputs": [
    {
      "name": "출력명",
      "format": "포맷"
    }
  ],
  "acceptance_criteria": [
    {
      "criterion": "검증 기준",
      "test_method": "테스트 방법"
    }
  ],
  "dependencies": ["task_id_1", "task_id_2"],
  "risks": [
    {
      "risk": "리스크 설명",
      "mitigation": "완화 방안"
    }
  ],
  "estimated_effort": "2h | 1d | 3d",
  "assigned_to": "agent_type"
}
```

### 필수 필드 검증
- REQUIRED: `task_id` - 고유해야 함
- REQUIRED: `purpose` - 빈 문자열 불가
- REQUIRED: `acceptance_criteria` - 1개 이상 필수
- REQUIRED: `dependencies` - 순환 참조 없어야 함

### 통과 조건
- [ ] JSON Schema 검증 통과
- [ ] 모든 dependency 존재
- [ ] acceptance_criteria 측정 가능
- [ ] Reviewer 승인

---

## Stage 4. Skill Routing

### 목적
태스크에 필요한 스킬을 `skill_id` 기준으로 매핑

### 입력
- `task_spec.json` (Stage 3 산출물)
- `skills_index.json` (Global Registry)
- `workspace_router.md` (라우팅 규칙)

### 출력
```json
{
  "task_id": "task_001",
  "skills_required": ["architecture", "code-review-checklist"],
  "skills_recommended": ["production-code-audit"],
  "routing_rationale": {
    "architecture": "시스템 설계 필요",
    "code-review-checklist": "품질 검토 필요"
  }
}
```

### 라우팅 규칙
1. Task의 `purpose` 분석
2. `skills_index.json`의 `tags`, `description`과 매칭
3. Workspace 라우팅 규칙 적용
4. 필수/권장 구분

### 통과 조건
- [ ] 모든 `skill_id`가 `skills_index.json`에 존재
- [ ] `routing_rationale` 명시
- [ ] Router 승인

---

## Stage 5. 실행 → 리뷰 → 검증

### 5.1 실행 (Execution)

#### 책임 에이전트
- Implementer / Researcher (태스크별 생성)

#### 필수 입력
- Task Spec
- 라우팅된 Skill IDs
- 의존 태스크 산출물

#### 필수 출력
- 산출물 (코드/문서/데이터)
- 실행 로그
- 사용된 근거 목록

---

### 5.2 리뷰 (Review)

#### 책임 에이전트
- Reviewer

#### 검토 항목
- [ ] 구조: 아키텍처 원칙 준수
- [ ] 논리: 추론 과정 타당성
- [ ] 품질: `quality_gates.md` 기준 충족
- [ ] 근거: `evidence_policy.md` 준수

#### 리뷰 결과 포맷
```json
{
  "review_id": "string",
  "task_id": "string",
  "status": "approved | rejected | needs_revision",
  "findings": [
    {
      "category": "structure | logic | quality | evidence",
      "severity": "critical | major | minor",
      "description": "설명",
      "suggestion": "개선 제안"
    }
  ],
  "reviewer": "agent_id",
  "timestamp": "ISO 8601"
}
```

---

### 5.3 검증 (Validation)

#### 책임 에이전트
- Validator

#### 검증 대상
- Task Spec의 `acceptance_criteria` 충족 여부

#### 검증 결과 포맷
```json
{
  "validation_id": "string",
  "task_id": "string",
  "status": "passed | failed",
  "criteria_results": [
    {
      "criterion": "acceptance_criteria[0]",
      "result": "pass | fail",
      "evidence": "검증 근거"
    }
  ],
  "validator": "agent_id",
  "timestamp": "ISO 8601"
}
```

#### 실패 시 처리
- `status: failed` → **계획 단계로 롤백** (Stage 1 or 2 or 3)
- 롤백 사유 문서화 필수

---

## 운영 원칙

### 원칙 1: 순차 진행
- Stage N 미완료 시 Stage N+1 차단

### 원칙 2: 근거 필수
- 모든 단계에서 의사결정 근거 명시

### 원칙 3: 문서 동기화
- 계획 변경 시 모든 관련 문서 즉시 업데이트

### 원칙 4: 실패 허용
- 실패는 정상, 은폐는 위반

---

## 부록: Task Spec 예시

```json
{
  "task_id": "AUTH-001",
  "wbs_path": "backend.authentication.jwt_implementation",
  "purpose": "JWT 기반 인증 시스템 구현",
  "inputs": [
    {
      "name": "project_charter",
      "source": "project_charter.md#security"
    }
  ],
  "outputs": [
    {
      "name": "auth_service.ts",
      "format": "TypeScript"
    }
  ],
  "acceptance_criteria": [
    {
      "criterion": "토큰 발급/검증 정상 동작",
      "test_method": "Unit test 통과율 100%"
    }
  ],
  "dependencies": [],
  "risks": [
    {
      "risk": "토큰 만료 처리 누락",
      "mitigation": "엣지 케이스 테스트 추가"
    }
  ],
  "estimated_effort": "1d",
  "assigned_to": "implementer"
}
```
