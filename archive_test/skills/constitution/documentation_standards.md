# Documentation Standards

> 글로벌 문서 작성 규칙 - LLM 인식 최적화

---

## 핵심 원칙

> [!IMPORTANT]
> **"모든 Constitution 문서는 LLM 인식에 최적화된 형태로 작성한다"**

---

## 1. 이모지 사용 금지

### 1.1 금지 사항
- **절대 금지**: 이모지 사용 (예: ✅, ❌, ⚠️, 📌, 👉, ★)
- **이유**: LLM 토큰화 과정에서 비효율적, 의미 전달 불명확

### 1.2 대체 표현

| 금지 (이모지) | 권장 (텍스트) |
|--------------|--------------|
| ✅ | VALID, APPROVED, CORRECT |
| ❌ | PROHIBITED, INVALID, INCORRECT |
| ⚠️ | WARNING, CAUTION |
| 📌 | NOTE, IMPORTANT |
| 👉 | NOTE, SEE |
| ★★★★★ | Level 5, Rating 5/5 |

---

## 2. 텍스트 기반 강조

### 2.1 승인된 강조 방법
```markdown
**굵게**: 중요 키워드
*기울임*: 용어 정의
`코드`: 식별자, 파일명
> 인용: 원칙 명시
```

### 2.2 GitHub Markdown Alerts (허용)
```markdown
> [!NOTE]
> 일반 정보

> [!TIP]
> 유용한 팁

> [!IMPORTANT]
> 중요 정보

> [!WARNING]
> 주의 사항

> [!CAUTION]
> 위험 경고
```

---

## 3. 구조화된 표현

### 3.1 상태 표시
```
PROHIBITED: 금지됨
VALID: 유효함
REQUIRED: 필수
OPTIONAL: 선택
DEPRECATED: 폐기됨
```

### 3.2 우선순위 표시
```
CRITICAL: 치명적
HIGH: 높음
MEDIUM: 중간
LOW: 낮음
```

### 3.3 신뢰도 표시
```
Level 5: 최고 신뢰도 (Observed Facts)
Level 4: 높은 신뢰도 (Verified Data)
Level 3: 중간 신뢰도 (Expert Opinion)
Level 2: 낮은 신뢰도 (Inferred)
Level 1: 최저 신뢰도 (Assumed)
```

---

## 4. LLM 최적화 가이드라인

### 4.1 명확한 구분자 사용
```
PREFERRED:
- Section 1
- Section 2

AVOID:
• Section 1 (bullets may render differently)
```

### 4.2 일관된 포맷
```
GOOD:
task_id: "AUTH-001"
status: "approved"

AVOID:
Task Id: AUTH-001 (비일관적 키 포맷)
```

### 4.3 코드 블록 언어 명시
```markdown
\`\`\`yaml
key: value
\`\`\`

NOT:
\`\`\`
key: value
\`\`\`
```

---

## 5. 체크리스트 표준

### 5.1 Markdown 체크박스 (허용)
```markdown
- [ ] 미완료 항목
- [x] 완료 항목
- [/] 진행 중 (커스텀, 시스템 내부용)
```

### 5.2 상태 코드 (권장)
```markdown
- PENDING: 대기 중
- IN_PROGRESS: 진행 중
- COMPLETED: 완료
- BLOCKED: 차단됨
```

---

## 6. 표와 다이어그램

### 6.1 ASCII 표 (허용)
```
┌─────────────┐
│   Header    │
├─────────────┤
│   Content   │
└─────────────┘
```

### 6.2 Markdown 표 (권장)
```markdown
| Column 1 | Column 2 |
|----------|----------|
| Value 1  | Value 2  |
```

### 6.3 Mermaid 다이어그램 (허용)
```markdown
\`\`\`mermaid
graph LR
    A --> B
\`\`\`
```

---

## 7. 위반 처리

### 7.1 검증 기준
- Constitution 문서는 이모지 포함 시 **즉시 거부**
- 리뷰어는 문서 표준 준수 확인 필수

### 7.2 예외
- **없음** - 예외 없이 모든 Constitution 문서는 이 표준 준수

---

## 8. 버전 관리

- **Documentation Standards 버전**: v1.0
- **최종 수정일**: 2026-01-28
- **적용 범위**: 모든 Global Constitution 문서

---

> [!NOTE]
> 이 표준은 Constitution Layer에만 적용되며, Workspace 문서는 프로젝트 재량에 따라 결정 가능하다.
> 단, Workspace 문서도 이 표준을 따르는 것을 강력히 권장한다.
