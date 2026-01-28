# skills_index.json 필드 검증

> 기존 skills_index.json 필드 구조 분석 및 필수 필드 확인

---

## 현재 필드 구조

```json
{
  "id": "skill_id",
  "name": "skill_name",
  "path": "skills/category/subcategory/skill_name",
  "tags": ["tag1", "tag2", ...],
  "category": "category/subcategory",
  "source": "source_info",
  "description": "Use when...",
  "risk": "risk_level"
}
```

---

## 필수 필드 검증

| 필드 | 필수 여부 | 현재 상태 | 비고 |
|------|----------|----------|------|
| **id** (skill_id) | REQUIRED | PRESENT | 모든 스킬에 존재 |
| **name** | REQUIRED | PRESENT | 스킬 이름 |
| **path** | REQUIRED | PRESENT | 파일 경로 (참조용만) |
| **tags** | REQUIRED | PRESENT | 라우팅용 태그 |
| **description** | REQUIRED | PRESENT | "Use when" 포함 |
| **use_when** | RECOMMENDED | NOT_PRESENT | description에 포함됨 |
| **aliases** | OPTIONAL | NOT_PRESENT | 별칭 없음 |

---

## 필드 매핑

### use_when 처리
- **현재**: `description` 필드에 "Use when..." 포함
- **권장 방식**: 별도 `use_when` 필드 분리
- **현실**: description으로 충분, 변경 불필요

### aliases 처리
- **현재**: 없음
- **필요성**: 낮음 (`tags`로 대체 가능)
- **결정**: 추가 불필요

---

## 라우팅 알고리즘 검증

Router가 skill_id를 찾는 방법:

```javascript
// Step 1: Parse task
const keywords = extractKeywords(task.purpose);

// Step 2: Query skills_index.json
const matches = skills_index.filter(skill => {
  // Match by tags
  const tagMatch = skill.tags.some(tag => 
    keywords.includes(tag)
  );
  
  // Match by description
  const descMatch = skill.description.toLowerCase()
    .includes(keywords.join(" ").toLowerCase());
  
  return tagMatch || descMatch;
});

// Step 3: Rank by relevance
const ranked = rankByRelevance(matches, task);

// Step 4: Return skill_id only
return {
  skills_required: ranked.slice(0, 3).map(s => s.id),
  skills_recommended: ranked.slice(3, 6).map(s => s.id)
};
```

---

## 검증 결과

### PASS 항목
- [x] skill_id 필드 존재 (id)
- [x] path 필드 존재 (참조용)
- [x] name 필드 존재
- [x] tags 필드 존재 (라우팅 핵심)
- [x] description 필드 존재 (use_when 포함)

### 추가 불필요 항목
- [ ] use_when 별도 필드 - description으로 충분
- [ ] aliases 필드 - tags로 대체 가능

---

## 결론

> [!NOTE]
> 기존 skills_index.json 구조가 Router의 skill_id 기반 라우팅에 **충분**합니다.
> 
> 필드 추가/변경 불필요.

---

## ID 기반 참조 규칙 재확인

### PROHIBITED (금지)
```yaml
# Workspace/Task에서 절대 사용 금지
skill_ref: "skills/coding/architecture/architecture"
skill_ref: "../architecture"
```

### REQUIRED (필수)
```yaml
# skill_id만 사용
skill_id: "architecture"
skill_id: "code-review-checklist"
```

---

## agent_catalog.json 연동

```json
{
  "orchestrator": {
    "core_skills": [
      "architecture",           // skill_id
      "software-architecture",  // skill_id
      "senior-architect"        // skill_id
    ]
  }
}
```

모든 스킬 참조는 `skill_id`만 사용.
