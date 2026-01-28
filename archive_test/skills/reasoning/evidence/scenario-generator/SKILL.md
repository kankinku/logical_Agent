---
name: Scenario Generator
description: Evidence-Constrained Scenario 생성. 관찰/해석/가정을 3층 구조로 분리하여 시나리오 과잉 서사화 방지
use_when: |
  - Evidence Map 완료 후 시나리오 생성 시
  - 여러 설명 후보를 만들어야 할 때
  - 가정을 명시적 비용으로 표시해야 하는 경우
  - Hallucination 최소화가 중요한 분석 작업
tags:
  - scenario
  - generation
  - hypothesis
  - abduction
  - cost-based-ranking
aliases:
  - hypothesis-generator
  - scenario-builder
  - explanation-generator
---

# Evidence-Constrained Scenario Generator

> 출처: `docs/05 - Evidence-Constrained Scenario Generator.md`

## 핵심 원칙

**"시나리오 상한선 = Evidence Map"**

Evidence Map을 벗어나는 시나리오는 생성하지 않는다.

---

## 1. 3층 Scenario 구조

### 1.1 Layer 구조
```yaml
scenario:
  layer_1_observed:
    - "직접 관찰된 사실만"
    - "Evidence Map의 L1, L2 증거"
  
  layer_2_interpretation:
    - "관찰 사실에 대한 해석"
    - "전제 명시 필수"
  
  layer_3_assumptions:
    - "검증되지 않은 가정"
    - "비용으로 표시 (cost=low/medium/high)"
```

### 1.2 비용 계산
```
Scenario Cost = 
  (가정 개수 × 2) + 
  (L4 근거 개수 × 1) + 
  (모순 증거 무시 × 10)

낮을수록 선호됨
```

---

## 2. Scenario 생성 프로토콜

### 2.1 입력
- Evidence Map (완성됨)
- Timeline (정렬됨)
- Topic/Claim

### 2.2 출력
```json
{
  "scenarios": [
    {
      "scenario_id": "S001",
      "title": "시나리오 제목",
      "observed": ["사실1", "사실2"],
      "interpretation": {
        "claim": "해석 내용",
        "premise": ["전제1", "전제2"]
      },
      "assumptions": [
        {
          "assumption": "가정 설명",
          "cost": "low | medium | high",
          "pivotal": true | false
        }
      ],
      "total_cost": 5,
      "supporting_evidence": ["E001", "E002"],
      "contradicting_evidence": []
    }
  ]
}
```

### 2.3 생성 규칙
```
RULE 1: Observed는 Evidence Map의 사실만
RULE 2: Interpretation은 전제 명시 필수
RULE 3: Assumption은 명시적으로 표시
RULE 4: 3~5개 시나리오 생성 (과잉 생성 금지)
RULE 5: 비용 순으로 정렬
```

---

## 3. 가정 비용 계산

### 3.1 비용 등급
| 비용 | 설명 | 예시 | 점수 |
|------|------|------|------|
| **LOW** | 일반적으로 합리적 | "사용자는 편의성 선호" | 1 |
| **MEDIUM** | 검증 필요 | "트래픽이 10배 증가 예상" | 2 |
| **HIGH** | 강한 가정 | "모든 사용자가 모바일 사용" | 3 |

### 3.2 Pivotal Assumption
```yaml
pivotal_assumption:
  definition: "이 가정이 틀리면 시나리오 전체가 무효화됨"
  marking: true
  priority: "검증 우선순위 최상위"
```

---

## 4. 과잉 서사화 방지

### 4.1 금지 사항
```
PROHIBITED:
  - Evidence 없는 세부 사항 추가
  - "아마도...", "...일 것이다" 남발
  - 가정을 사실처럼 서술

REQUIRED:
  - 모든 주장에 근거 표기
  - 가정은 명시적 assumption 섹션에만
  - 비용 계산 명시
```

### 4.2 간결성 원칙
```
GOOD:
  "현재 세션 기반 인증 사용 {L1: auth.ts}"

AVOID:
  "현재 세션 기반 인증을 사용하고 있으며, 
   이는 아마도 초기 개발 속도를 위한 선택이었을 것이고,
   향후 JWT로 전환할 계획일 수 있다..." (추측 과다)
```

---

## 5. 사용 예시

### 예시 1: 인증 시스템 분석
```json
{
  "scenario_id": "S001",
  "title": "JWT 마이그레이션 준비 중",
  "observed": [
    "현재 세션 기반 인증 (L1: auth.ts)",
    "JWT 라이브러리 설치됨 (L1: package.json 2026-01-15)"
  ],
  "interpretation": {
    "claim": "JWT로 전환 준비 중",
    "premise": ["라이브러리 설치 = 사용 의도"]
  },
  "assumptions": [
    {
      "assumption": "마이그레이션 일정이 확정됨",
      "cost": "medium",
      "pivotal": true,
      "if_false": "단순 테스트일 수 있음"
    }
  ],
  "total_cost": 2
}
```

---

## 6. Ranking 알고리즘

### 6.1 우선순위 계산
```python
priority_score = 
  (supporting_evidence_count × 2) - 
  (total_cost) - 
  (contradicting_evidence_count × 10)

# 높을수록 우선
```

### 6.2 필터링
```yaml
filters:
  - name: "비용 임계값"
    rule: "total_cost > 10이면 자동 제외"
  
  - name: "모순 증거"
    rule: "contradicting_evidence > 0이면 경고"
  
  - name: "Pivotal Assumption"
    rule: "pivotal=true인 것 우선 검증"
```

---

## 7. 품질 기준

### 통과 조건
- [ ] 모든 시나리오가 3층 구조 준수
- [ ] Observed가 Evidence Map 내에만 존재
- [ ] Assumption이 명시적으로 표시됨
- [ ] 비용 계산 완료
- [ ] Pivotal Assumption 식별됨

### 실패 시 처리
- Evidence Map으로 돌아가 보완
- 과잉 서사화 부분 삭제
- 가정을 명시적으로 분리

---

## 8. 다음 단계 연결

Scenario Generation 완료 후:
1. Pivotal Assumption Finding (skill: assumption-finder)
2. Targeted Retrieval (skill: targeted-retrieval)
3. Cross-Critique (skill: cross-critique)

---

> [!IMPORTANT]
> Scenario Generator는 "상상력"이 아니라 **"제약 속 해석"**이다.
> 많이 만드는 게 아니라 **덜 만드는 것**이 목표다.
