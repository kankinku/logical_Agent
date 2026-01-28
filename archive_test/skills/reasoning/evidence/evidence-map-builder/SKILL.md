---
name: Evidence Map Builder
description: 수집된 증거를 구조화하여 Evidence Map과 Timeline 생성. 시간 순서, 인과 관계, 사실 간 연결 명시
use_when: |
  - Evidence Collection 완료 후 구조화 필요 시
  - 타임라인 오류 방지가 필요한 경우
  - 인과 관계 파악을 위한 사실 매핑 시
  - "알고 있는 것"과 "모르는 것"을 명확히 구분해야 할 때
tags:
  - evidence-map
  - timeline
  - fact-structuring
  - causal-analysis
  - temporal-ordering
aliases:
  - timeline-builder
  - fact-mapper
  - evidence-structuring
---

# Evidence Map & Timeline Builder

> 출처: `docs/04 - Evidence Map, Timeline Builder.md`

## 핵심 원칙

**"인과를 만들 수 없는 상태에서만 다음 단계로"**

타임라인 오류로 인한 가짜 인과 관계를 구조적으로 차단한다.

---

## 1. Evidence Map 구조

### 1.1 기본 포맷
```json
{
  "topic": "주제",
  "facts": [
    {
      "fact_id": "F001",
      "fact": "사실 설명",
      "source": "출처",
      "level": "L1 | L2 | L3",
      "timestamp": "ISO 8601",
      "category": "기술 | 비즈니스 | 요구사항"
    }
  ],
  "timeline": [
    {
      "event_id": "E001",
      "event": "이벤트 설명",
      "timestamp": "ISO 8601",
      "related_facts": ["F001", "F002"],
      "evidence": "근거"
    }
  ],
  "relationships": [
    {
      "type": "temporal | causal | dependency",
      "from": "E001",
      "to": "E002",
      "confidence": "high | medium | low"
    }
  ],
  "gaps": [
    {
      "gap_id": "G001",
      "question": "확인 필요한 사항",
      "impact": "이것을 모르면 어떤 판단이 불가능한가"
    }
  ]
}
```

---

## 2. Timeline 구축 프로토콜

### 2.1 시간 순서 정렬
```yaml
step_1: "모든 증거에서 timestamp 추출"
step_2: "시간순 정렬 (earliest to latest)"
step_3: "시간 간격 확인 (누락 기간 식별)"
step_4: "동시 발생 이벤트 그룹핑"
```

### 2.2 인과 관계 검증
```
PROHIBITED:
  "A → B" (단순 시간 순서만으로 인과 추론)

REQUIRED:
  "A → B" {evidence: "B의 원인이 A임을 보여주는 증거"}
```

### 2.3 타임라인 무결성 체크
```yaml
checks:
  - name: "순환 참조 없음"
    validation: "A → B → C → A 불가"
  
  - name: "시간 순서 일관성"
    validation: "Earlier event cannot depend on later event"
  
  - name: "Gap 명시"
    validation: "시간 공백 구간 표시"
```

---

## 3. 사실 간 관계 유형

### 3.1 Temporal (시간적)
```
E001: "JWT 라이브러리 설치" (2026-01-15)
  → E002: "인증 로직 수정" (2026-01-20)
관계: "E002는 E001 이후에 발생"
```

### 3.2 Causal (인과적)
```
E001: "성능 저하 발생" (2026-01-18)
  ← E002: "DB 인덱스 누락" (발견: 2026-01-19)
관계: "E002가 E001의 원인" {evidence: 인덱스 추가 후 성능 회복}
```

### 3.3 Dependency (의존성)
```
F001: "React 18 사용"
  ← F002: "Concurrent Mode 활성화"
관계: "F002는 F001에 의존"
```

---

## 4. Gap Detection

### 4.1 정보 Gap 유형
| Gap 유형 | 설명 | 우선순위 |
|---------|------|---------|
| **Critical Gap** | 핵심 판단에 필수 | HIGH |
| **Contextual Gap** | 맥락 이해에 도움 | MEDIUM |
| **Nice-to-have Gap** | 추가 정보 | LOW |

### 4.2 Gap 명시 포맷
```yaml
gap:
  id: "G001"
  question: "현재 트래픽이 얼마인가?"
  impact: "캐싱 전략 결정 불가"
  priority: "CRITICAL"
  action: "모니터링 대시보드 확인 요청"
```

---

## 5. 사용 예시

### 예시 1: 인증 시스템 Evidence Map
```json
{
  "topic": "authentication_migration",
  "facts": [
    {
      "fact_id": "F001",
      "fact": "현재 세션 기반 인증",
      "source": "auth.ts",
      "level": "L1"
    },
    {
      "fact_id": "F002",
      "fact": "JWT 라이브러리 설치됨",
      "source": "package.json",
      "level": "L1",
      "timestamp": "2026-01-15"
    }
  ],
  "timeline": [
    {
      "event_id": "E001",
      "event": "JWT 라이브러리 추가",
      "timestamp": "2026-01-15",
      "related_facts": ["F002"]
    }
  ],
  "gaps": [
    {
      "gap_id": "G001",
      "question": "마이그레이션 계획이 있는가?",
      "impact": "실제 전환 여부 불확실"
    }
  ]
}
```

---

## 6. 품질 기준

### 통과 조건
- [ ] 모든 이벤트가 시간순 정렬됨
- [ ] 인과 관계에 증거 명시됨
- [ ] 순환 참조 없음
- [ ] Gap 목록 완성
- [ ] 사실과 추론이 명확히 구분됨

### 실패 시 처리
- 타임라인 재정렬
- 인과 관계 증거 보완
- Gap을 Targeted Retrieval 대상으로 표시

---

## 7. 다음 단계 연결

Evidence Map 완료 후:
1. Scenario Generation (skill: scenario-generator)
2. Pivotal Assumption Finding (skill: assumption-finder)
3. Gap 해결을 위한 Targeted Retrieval (skill: targeted-retrieval)

---

> [!IMPORTANT]
> Evidence Map은 "예쁜 다이어그램"이 아니라 **"인과 오류 방지 도구"**다.
> 시간 순서 ≠ 인과 관계. 증거 없는 인과는 금지.
