# Domain Glossary

> 프로젝트 용어집 - 도메인 특화 용어 정의

---

## A

### Acceptance Criteria
**정의**: 태스크 완료를 판단하는 측정 가능한 기준  
**예시**: "Unit test 통과율 100%"  
**참조**: task_protocol.md#stage-3

### Agent Catalog
**정의**: Global에서 정의한 에이전트 타입 카탈로그  
**예시**: orchestrator, router, reviewer, validator  
**참조**: registry/agent_catalog.json

### Assumption
**정의**: 검증되지 않은 가정, 비용으로 표시됨  
**레벨**: L5 (가장 낮은 신뢰도)  
**참조**: evidence_policy.md#evidence-계층

---

## C

### Canonical Home
**정의**: 스킬이 속한 단 하나의 경로  
**원칙**: 중복 배치 금지  
**예시**: `reasoning/evidence/`

### Constitution
**정의**: 모든 에이전트가 따라야 하는 최상위 규칙  
**우선순위**: 1순위 (절대 불변)  
**참조**: constitution/constitution.md

---

## E

### Evidence-First
**정의**: 추론/분석 전에 근거를 먼저 수집하는 원칙  
**흐름**: Data Requirements → Evidence Collection → Generate  
**효과**: Hallucination 구조적 차단

### Evidence Map
**정의**: 수집된 증거를 구조화한 맵 (사실, 타임라인, 관계, Gap)  
**참조**: evidence-map-builder 스킬

---

## G

### Gap Detection
**정의**: "알고 있는 것"과 "모르는 것"을 명시하는 과정  
**목적**: 불확실성을 명시하고 Targeted Retrieval 대상 식별

### Global Constitution
**정의**: 프로젝트와 무관한 절대 규칙 계층  
**위치**: `skills/constitution/`

---

## L

### Layer (3-Layer Quality Model)
**정의**: 품질 검증의 3단계 모델  
**구성**:
- Layer 1: 논리 검증 (Logic)
- Layer 2: 전제 신뢰성 (Premise)
- Layer 3: 현실 일관성 (Reality)

---

## P

### Pivotal Assumption
**정의**: 이것이 틀리면 시나리오 전체가 무효화되는 핵심 가정  
**우선순위**: 검증 최상위  
**참조**: scenario-generator 스킬

### Project Overlay
**정의**: Workspace 계층의 프로젝트별 설정  
**위치**: `workspace/project/`  
**특징**: Global을 수정하지 않고 프로젝트 구성

---

## R

### Routing
**정의**: Task를 분석하여 필요한 skill_id를 매핑하는 과정  
**담당**: Router 에이전트  
**기준**: tags, description, task.purpose

---

## S

### Scenario (3층 구조)
**정의**: Evidence-Constrained 시나리오  
**구성**:
- Layer 1: Observed (관찰된 사실)
- Layer 2: Interpretation (해석)
- Layer 3: Assumptions (가정)

### skill_id
**정의**: 스킬을 참조하는 고유 식별자  
**형식**: 문자열  
**예시**: `evidence-collection`, `architecture`  
**금지**: 경로 참조 (path)

### Stage (탑다운 5단계)
**정의**: Task Protocol의 필수 실행 단계  
**순서**:
1. Project Charter 확정
2. WBS 생성
3. Task Spec 표준화
4. Skill Routing
5. 실행 → 리뷰 → 검증

---

## T

### Task Spec
**정의**: 표준화된 태스크 정의서 (JSON)  
**필수 필드**: task_id, purpose, acceptance_criteria, dependencies  
**참조**: task_protocol.md#stage-3

### Taxonomy
**정의**: 스킬 분류 체계  
**구조**: tier1/tier2/skill_name (3레벨)  
**예시**: `reasoning/evidence/evidence-collection`

---

## W

### WBS (Work Breakdown Structure)
**정의**: 프로젝트를 3~4레벨로 분해한 구조  
**레벨**: Workstream → Component → Unit → Task  
**참조**: task_protocol.md#stage-2

### Workspace
**정의**: 프로젝트별 가변 설정 계층  
**위치**: `workspace/`  
**우선순위**: 4순위 (Global 다음)

---

## 약어

| 약어 | 전체 이름 | 설명 |
|------|----------|------|
| **DoD** | Definition of Done | 완료 기준 |
| **GC** | Global Constitution | 글로벌 헌법 |
| **L1~L5** | Level 1~5 | 증거 신뢰도 등급 |
| **WBS** | Work Breakdown Structure | 작업 분해 구조 |

---

> [!NOTE]
> 이 Glossary는 프로젝트 참여자 간 용어 통일을 위한 문서입니다.
> 새로운 용어 추가 시 이 문서를 업데이트하세요.
