---
name: Evidence Collection
description: Evidence-First 정보 수집 및 큐레이션. 출처별 수집, 신뢰도 등급 부여, 모순 증거 식별
use_when: |
  - 프로젝트 분석 전 근거 자료 수집 필요 시
  - Data Requirements 정의 후 실제 증거 수집 단계
  - Hallucination 방지를 위한 사실 기반 구축 시
  - 추론 전 Evidence Base 확보가 필요한 경우
tags:
  - evidence
  - collection
  - research
  - fact-checking
  - source-evaluation
  - data-curation
aliases:
  - evidence-gathering
  - fact-collection
  - source-research
---

# Evidence Collection & Curation

> 출처: `docs/03 - Evidence Collection & Curation.md`

## 핵심 원칙

**"Generate 전에 Collect"**

모든 추론/분석은 Evidence Collection 이후에만 시작한다.

---

## 1. Evidence Collection 프로세스

### 1.1 입력
- Data Requirements (Stage 0)
- Topic/Claim Decomposition 결과

### 1.2 출력
- Evidence Map
- 신뢰도 등급별 증거 목록
- 모순 증거 리스트

---

## 2. 수집 프로토콜

### 2.1 출처별 수집
```yaml
sources:
  - type: "codebase"
    reliability: "L1"
    examples:
      - "실행 로그"
      - "테스트 결과"
      - "커밋 이력"
  
  - type: "documentation"
    reliability: "L2"
    examples:
      - "공식 문서"
      - "API 스펙"
      - "아키텍처 다이어그램"
  
  - type: "expert_opinion"
    reliability: "L3"
    examples:
      - "학술 논문"
      - "기술 블로그 (출처 명시)"
      - "공식 가이드"
```

### 2.2 신뢰도 등급 부여
| Level | 유형 | 예시 |
|-------|------|------|
| L1 | Observed Facts | 실행 결과, 테스트 로그 |
| L2 | Verified Data | 공식 문서, API 스펙 |
| L3 | Expert Opinion | 논문, 기술 블로그 |
| L4 | Inferred | 논리적 추론 (전제 명시 필수) |
| L5 | Assumed | 가정 (비용으로 표시) |

### 2.3 모순 증거 식별
```yaml
contradiction_check:
  - source_a: "토큰 만료 15분" {L2: RFC 7519}
  - source_b: "토큰 만료 1시간" {L1: config.yaml}
  resolution: "현재 설정과 표준의 차이 명시, 보안 강화 권장"
```

---

## 3. Evidence Curation

### 3.1 Out-of-date 처리
- 발행일 확인
- 현재 버전과 비교
- 오래된 증거 폐기 또는 표시

### 3.2 Duplicate 제거
- 동일 사실의 중복 출처
- 가장 신뢰도 높은 출처만 유지

### 3.3 Evidence Map 구축
```json
{
  "topic": "authentication",
  "facts": [
    {
      "fact": "현재 세션 기반 인증 사용",
      "source": "current_codebase/auth.ts",
      "level": "L1",
      "timestamp": "2026-01-28"
    }
  ],
  "contradictions": [],
  "gaps": [
    "JWT 라이브러리 성능 데이터 부족"
  ]
}
```

---

## 4. 사용 예시

### 예시 1: 인증 시스템 분석
```yaml
task: "인증 시스템 개선 방안 제시"

evidence_collection:
  step_1: "현재 코드베이스에서 인증 로직 추출" (L1)
  step_2: "보안 요구사항 문서 확인" (L2)
  step_3: "JWT vs Session 비교 논문 수집" (L3)
  
result:
  - "현재 세션 기반 (L1: auth.ts)"
  - "보안 요구사항: 2FA 필요 (L2: charter.md)"
  - "JWT 장점: Stateless (L3: RFC 7519)"
```

### 예시 2: 성능 최적화
```yaml
task: "API 응답 속도 개선"

evidence_collection:
  step_1: "현재 응답 시간 측정" (L1)
  step_2: "병목 구간 프로파일링" (L1)
  step_3: "캐싱 전략 베스트 프랙티스" (L3)
```

---

## 5. 품질 기준

### 통과 조건
- [ ] 모든 증거에 출처 명시
- [ ] 신뢰도 등급 부여됨
- [ ] 모순 증거 식별 완료
- [ ] Gap 목록 작성됨
- [ ] L3 이상 증거 비율 70% 이상

### 실패 시 처리
- 추가 조사 수행
- Gap을 명시적으로 표시
- 불확실성으로 표시하고 진행

---

## 6. 다음 단계 연결

Evidence Collection 완료 후:
1. Evidence Map 생성 (skill: evidence-map-builder)
2. Timeline 구축 (skill: timeline-builder)
3. Scenario 생성 (skill: scenario-generator)

---

> [!IMPORTANT]
> Evidence Collection은 "많이 모으기"가 아니라 **"신뢰할 수 있게 모으기"**다.
> L5 (Assumed) 증거는 최소화하고, L1~L3을 우선한다.
