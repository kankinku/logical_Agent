# Evidence Policy

> 근거/출처 정책 - No Assertion, Evidence Required

---

## 핵심 원칙

> [!CAUTION]
> **"근거 없는 주장은 주장이 아니라 노이즈다"**

모든 주장은 검증 가능한 근거를 동반해야 한다.

---

## 1. Evidence-First 원칙

### 1.1 Retrieve → Structure → Generate

```
INVALID FLOW:
Prompt → Generate → (사후에 근거 찾기)

VALID FLOW:
Data Requirements → Evidence Collection → 
Evidence Map → Generate (근거 기반)
```

> 출처: `docs/12 - 최종 정리.md` (Evidence-First 구조)

### 1.2 효과
- Hallucination 구조적 차단
- 시나리오 상한선이 Evidence Map으로 제한
- "생각의 자유" 대신 "해석의 책임" 부여

---

## 2. Evidence 계층 (5단계)

| 레벨 | 유형 | 신뢰도 | 예시 | 비용 |
|------|------|--------|------|------|
| **L1** | Observed Facts | Level 5 | 실행 로그, 테스트 결과 | 0 |
| **L2** | Verifiable Data | Level 4 | 공식 문서, API 스펙 | 낮음 |
| **L3** | Expert Opinion | Level 3 | 논문, 기술 블로그 | 중간 |
| **L4** | Logical Inference | Level 2 | (전제 명시 필수) | 높음 |
| **L5** | Assumptions | Level 1 | 가정 (명시 필수) | 매우 높음 |

### 2.1 비용 개념
- L4, L5는 "비용"으로 취급
- 비용이 높을수록 시나리오 우선순위 하락
- 가정이 적을수록 선호

> 출처: `docs/05 - Evidence-Constrained Scenario Generator`

---

## 3. Evidence 표기 규칙

### 3.1 기본 포맷
```
[주장] {evidence_type: source}
```

### 3.2 예시
```markdown
"JWT 토큰은 15분 만료가 일반적이다" 
{expert: RFC 7519, Section 4.1.4}

"현재 API 응답 시간은 200ms다" 
{observed: monitoring_dashboard, 2026-01-28}

"사용자 인증이 필요하다" 
{requirement: project_charter.md#security}

"Redis가 성능에 유리할 것이다" 
{inferred: premise="key-value 접근 패턴", cost=medium}
```

### 3.3 가정 명시
```markdown
"마이크로서비스 아키텍처를 채택한다"
{assumed: 
  - "트래픽이 월 100만 이상", 
  - "팀이 5명 이상",
  cost=high
}
```

---

## 4. Evidence Collection 프로토콜

### 4.1 Data Requirements 우선 정의
> 출처: `docs/02 - Data Requirements Spec`

```yaml
data_requirements:
  - category: "authentication"
    required_evidence:
      - "현재 인증 방식"
      - "보안 요구사항"
      - "성능 SLA"
    sources:
      - "project_charter.md"
      - "system_diagram.png"
```

### 4.2 Evidence Collection
> 출처: `docs/03 - Evidence Collection & Curation`

- 출처별로 수집
- 신뢰도 등급 부여
- 모순되는 증거 식별

### 4.3 Evidence Map 구축
> 출처: `docs/04 - Evidence Map, Timeline Builder`

```json
{
  "evidence_map": {
    "topic": "authentication",
    "facts": [
      {
        "fact": "현재 세션 기반 인증 사용",
        "source": "current_codebase/auth.ts",
        "level": "L1"
      }
    ],
    "timeline": [
      {
        "event": "JWT 라이브러리 설치",
        "timestamp": "2026-01-15",
        "evidence": "package.json"
      }
    ]
  }
}
```

---

## 5. 출처 유형 및 신뢰도

### 5.1 코드 기반 증거 (L1)
- 실행 로그
- 테스트 결과
- 커밋 이력
- 성능 프로파일

### 5.2 문서 기반 증거 (L2)
- 공식 문서 (RFC, W3C, MDN)
- API 스펙
- 아키텍처 다이어그램
- Project Charter

### 5.3 전문가 의견 (L3)
- 학술 논문 (peer-reviewed)
- 기술 블로그 (출처 명시)
- 공식 가이드 (예: React 공식 문서)

### 5.4 추론 (L4)
- 논리적 추론 (전제 명시 필수)
- 경험 법칙 (근거 필요)

### 5.5 가정 (L5)
- 명시적 가정만 허용
- 비용 계산 필수

---

## 6. 금지 사항

### 6.1 출처 누락
PROHIBITED: "일반적으로 알려져 있다"
PROHIBITED: "경험상 그렇다"
PROHIBITED: "보통 이렇게 한다"

VALID: "Stack Overflow Survey 2023에 따르면 78%가 사용한다 {L3: survey}"
VALID: "현재 코드베이스에서 사용 중이다 {L1: src/auth.ts:L15}"

### 6.2 검증 불가능한 주장
PROHIBITED: "더 빠를 것이다" (측정 없음)
PROHIBITED: "사용자가 선호할 것이다" (조사 없음)

VALID: "벤치마크 결과 30% 빨랐다 {L1: benchmark_result.md}"
VALID: "A/B 테스트에서 CVR 12% 증가 {L1: ab_test_report.md}"

### 6.3 암묵적 가정
PROHIBITED: "확장성을 위해 마이크로서비스를 선택한다" (가정 숨김)

VALID: "확장성을 위해 마이크로서비스를 선택한다 
     {assumed: '트래픽이 향후 10배 증가', cost=high}"

---

## 7. Evidence Curation (근거 큐레이션)

### 7.1 모순 처리
```yaml
contradiction:
  - source_a: "토큰 만료는 15분" {L2: RFC 7519}
  - source_b: "토큰 만료는 1시간" {L1: current_config.yaml}
  resolution: "현재 설정이 1시간이나, 표준은 15분. 보안 강화 필요"
```

### 7.2 Out-of-date 처리
```yaml
outdated:
  - evidence: "React 16 사용 권장" {L3: blog_2019}
  - current: "React 18이 현재 stable" {L2: react_docs}
  action: "이전 증거 폐기"
```

---

## 8. Pivotal Assumption 관리

> 출처: `docs/06 - Pivotal Assumption Finder + Gap Detector`

### 8.1 정의
- **Pivotal Assumption**: 판결을 뒤집을 수 있는 핵심 가정

### 8.2 식별
```yaml
scenario: "Redis를 캐시로 사용"
pivotal_assumptions:
  - assumption: "트래픽이 초당 1000 req 이상"
    if_false: "In-memory cache로 충분, Redis 불필요"
  - assumption: "캐시 히트율 70% 이상"
    if_false: "캐시 효과 미미, DB 최적화 우선"
```

### 8.3 Gap Detection
```yaml
gaps:
  - question: "현재 트래픽이 얼마인가?"
    action: "monitoring_dashboard 확인 요청"
  - question: "캐시 히트율 예측 근거는?"
    action: "로그 분석 또는 가정으로 명시"
```

---

## 9. Targeted Retrieval Loop

> 출처: `docs/07 - Targeted Retrieval Loop`

### 9.1 검색 트리거
- Pivotal Assumption 해결 필요 시
- Critical Gap 발견 시

### 9.2 검색 범위 제한
```
PROHIBITED: "캐시에 대해 모든 자료 검색"
VALID: "현재 트래픽 수치만 검색" (pivotal assumption 해결용)
```

### 9.3 종료 조건
- Assumption 해결됨
- 3회 검색 후에도 미해결 → "불확실성으로 명시하고 종료"

---

## 10. 검증 프로세스

### 10.1 Evidence 검증 체크리스트
- [ ] 모든 주장에 출처 표기
- [ ] 출처가 신뢰도 L3 이상
- [ ] 가정이 명시적으로 표시됨
- [ ] Pivotal Assumption 식별됨
- [ ] Gap이 해결되거나 명시됨

### 10.2 위반 시 처리
```yaml
violation_type: "출처 누락"
action: "산출물 거부 + 출처 보완 요구"
```

---

## 11. 부록: Evidence 템플릿

### 주장 + 근거 템플릿
```markdown
**주장**: {claim}
**근거 유형**: L1 | L2 | L3 | L4 | L5
**출처**: {source}
**신뢰도**: {reliability_justification}
```

### 가정 명시 템플릿
```yaml
assumption:
  description: "{what is assumed}"
  impact: "if false, {consequence}"
  cost: low | medium | high
  pivotal: true | false
```

---

> [!IMPORTANT]
> Evidence Policy는 "완벽한 근거"를 요구하지 않는다.
> **"무엇을 모르는지 알고 명시하는 것"**을 요구한다.
