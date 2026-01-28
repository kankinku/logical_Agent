# Project Charter

> 프로젝트 헌장 - 이 프로젝트의 경계와 성공 기준

---

## 프로젝트 목표

Evidence-First 추론 시스템을 갖춘 에이전트 시스템을 구축한다.

**핵심 가치**:
- 탑다운 계획 (설계 → 분해 → 실행)
- 근거 기반 판단 (주장 = 근거)
- 구조적 품질 관리 (3-Layer Quality Model)

**최종 목표**:
"에이전트가 일을 망치지 못하게 막는 구조" 완성

---

## 비목표 (Non-Goals)

다음은 이 프로젝트의 범위가 **아니다**:

- 완벽한 AI 추론 엔진 개발 (연구 범위 아님)
- 모든 도메인 커버 (특정 도메인에 집중)
- 실시간 성능 최적화 (정확성 우선)
- 프로덕션 배포 인프라 구축
- UI/UX 개발

---

## 범위 (Scope)

### 포함 (Included)
- Global Constitution 구축 (규칙 체계)
- Agent Catalog 정의 (6개 타입)
- Evidence-First 핵심 스킬 3개
- Workspace 템플릿 구축
- 문서 기반 설계 (코드보다 규칙 우선)

### 제외 (Excluded)
- 전체 스킬 마이그레이션 (최소셋만)
- 프로덕션 배포
- 외부 시스템 통합
- 실시간 모니터링

---

## 제약 사항 (Constraints)

| 제약 유형 | 내용 |
|----------|------|
| **리소스** | 단일 개발자 |
| **비용** | LLM API 토큰 효율성 중요 |
| **시간** | 문서 우선, 코드 최소화 |
| **기술** | 기존 스킬 활용 (새 개발 최소화) |

---

## 성공 기준 (Acceptance Criteria)

| 기준 | 측정 방법 | 우선순위 |
|------|----------|---------|
| Constitution 문서로 금지 사항 판단 가능 | 문서 리뷰 통과 | CRITICAL |
| Router가 skill_id로 라우팅 성공 | 시뮬레이션 테스트 | HIGH |
| Evidence-First 스킬 3개 동작 | 예제 태스크 실행 | HIGH |
| Workspace 설정 변경으로 재구성 가능 | project_config.yaml 수정 테스트 | MEDIUM |

---

## 이해관계자 (Stakeholders)

| 역할 | 책임 |
|------|------|
| **개발자** | 시스템 설계 및 구현 |
| **사용자** | 프로젝트 요구사항 정의, 검증 |

---

## 리스크 (Risks)

| 리스크 | 영향도 | 완화 방안 |
|--------|--------|----------|
| Global Constitution 과도한 복잡성 | HIGH | 최소 규칙으로 시작, 점진적 확장 |
| 스킬 라우팅 실패 | MEDIUM | 시뮬레이션 테스트로 사전 검증 |
| 문서 동기화 누락 | MEDIUM | GC-IV-001 Lock으로 강제 |

---

## 산출물 (Deliverables)

1. **Constitution 문서 6종**
   - constitution.md
   - documentation_standards.md
   - task_protocol.md
   - instruction_verification_lock.md
   - quality_gates.md
   - evidence_policy.md

2. **Registry 파일 2종**
   - agent_catalog.json
   - skills_index_validation.md

3. **Core Skills 3개**
   - evidence-collection
   - evidence-map-builder
   - scenario-generator

4. **Workspace 템플릿 4종**
   - project_config.yaml
   - project_charter.md (본 문서)
   - glossary.md
   - ontology.yaml

---

## 버전 관리

- **Charter 버전**: v1.0
- **최종 수정일**: 2026-01-28
- **변경 이력**: charter_changelog.md

---

> [!IMPORTANT]
> 이 Charter는 Stage 1의 산출물로, 모든 후속 작업의 기준이 된다.
> 변경 시 Orchestrator 승인 필수.
