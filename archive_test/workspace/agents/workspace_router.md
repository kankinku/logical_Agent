---
agent_type: router
instance_name: workspace_router
project: logical_agent_project
created: 2026-01-28
---

# Workspace Router

> Task Spec → skill_id 매핑 - **규칙 우선, Registry 보조**

---

## 핵심 책임

1. **Task 분석**: Task Spec의 purpose, acceptance_criteria 파싱
2. **Skill 매핑**: task_tag → skill_id 라우팅
3. **근거 제공**: 라우팅 근거 (routing_rationale) 명시
4. **검증**: 모든 skill_id가 skills_index.json에 존재하는지 확인

---

## 라우팅 알고리즘

### Step 1: Task Spec 파싱
```python
def parse_task_spec(task_spec_path):
    task = load_json(task_spec_path)
    
    return {
        "task_id": task["task_id"],
        "purpose": task["purpose"],
        "acceptance_criteria": task["acceptance_criteria"],
        "task_tags": extract_tags(task["purpose"])  # 키워드 추출
    }
```

### Step 2: 규칙 기반 라우팅 (우선)
```python
def route_by_rules(task_tags, routing_rules):
    """
    project_config.yaml의 routing_rules 우선 적용
    """
    matched_rules = []
    
    for rule in routing_rules:
        if rule["task_tag"] in task_tags:
            matched_rules.append(rule)
    
    if matched_rules:
        return {
            "required_skills": merge_required(matched_rules),
            "recommended_skills": merge_recommended(matched_rules),
            "source": "project_config.yaml routing_rules"
        }
    
    # Fallback to default rule
    return route_default()
```

**예시**:
```yaml
# project_config.yaml
routing_rules:
  - task_tag: "analysis"
    required_skills:
      - "evidence-collection"
      - "evidence-map-builder"
```

### Step 3: Registry 매칭 (보조)
```python
def route_by_registry(task_tags, skills_index):
    """
    skills_index.json에서 tags 매칭
    """
    matches = []
    
    for skill in skills_index:
        # Tag 매칭
        tag_overlap = set(task_tags) & set(skill["tags"])
        
        if tag_overlap:
            relevance = len(tag_overlap) / len(task_tags)
            matches.append({
                "skill_id": skill["id"],
                "relevance": relevance,
                "matched_tags": list(tag_overlap)
            })
    
    # 관련도 순 정렬
    matches.sort(key=lambda x: x["relevance"], reverse=True)
    
    return matches[:5]  # Top 5
```

### Step 4: 결합 및 우선순위
```python
def combine_routing(rule_based, registry_based):
    """
    규칙 기반 우선, Registry는 보조
    """
    result = {
        "skills_required": rule_based["required_skills"],
        "skills_recommended": []
    }
    
    # Registry 결과를 recommended에 추가
    for match in registry_based:
        if match["skill_id"] not in result["skills_required"]:
            result["skills_recommended"].append(match["skill_id"])
    
    # Recommended는 상위 3개만
    result["skills_recommended"] = result["skills_recommended"][:3]
    
    return result
```

---

## 라우팅 출력 포맷

```json
{
  "task_id": "AUTH-001",
  "skills_required": [
    "evidence-collection",
    "evidence-map-builder"
  ],
  "skills_recommended": [
    "scenario-generator",
    "architecture"
  ],
  "routing_rationale": {
    "evidence-collection": "분석 작업은 근거 수집 필수 (rule: analysis)",
    "evidence-map-builder": "시스템 현황 구조화 필요 (rule: analysis)",
    "scenario-generator": "개선 방안 시나리오 생성 (registry: tags=[scenario])",
    "architecture": "아키텍처 검토 권장 (registry: tags=[architecture])"
  },
  "routing_source": {
    "required": "project_config.yaml",
    "recommended": "skills_index.json"
  }
}
```

---

## 검증 로직

### 1. Skill ID 존재 확인
```python
def validate_skill_ids(skill_ids, skills_index):
    """
    모든 skill_id가 skills_index.json에 존재하는지 검증
    """
    valid_ids = [skill["id"] for skill in skills_index]
    
    for skill_id in skill_ids:
        if skill_id not in valid_ids:
            raise Error(f"skill_id '{skill_id}' not found in skills_index.json")
    
    return True
```

### 2. 순환 의존성 확인
```python
def check_circular_dependency(task_spec):
    """
    Task dependencies에 순환 참조 없는지 확인
    """
    visited = set()
    path = set()
    
    def dfs(task_id):
        if task_id in path:
            raise Error(f"순환 의존성 발견: {path}")
        
        if task_id in visited:
            return
        
        visited.add(task_id)
        path.add(task_id)
        
        task = load_task_spec(task_id)
        for dep in task["dependencies"]:
            dfs(dep)
        
        path.remove(task_id)
    
    dfs(task_spec["task_id"])
    return True
```

---

## 라우팅 예시

### 예시 1: 분석 태스크

#### 입력
```json
{
  "task_id": "AUTH-ANALYSIS-001",
  "purpose": "현재 인증 시스템 분석 및 개선 방안 제시",
  "acceptance_criteria": [
    {"criterion": "근거 있는 분석 결과"}
  ]
}
```

#### 처리
```python
# Step 1: Tags 추출
task_tags = ["analysis", "authentication", "improvement"]

# Step 2: 규칙 매칭
rule = find_rule(task_tag="analysis")
# → required: [evidence-collection, evidence-map-builder]

# Step 3: Registry 매칭
registry_matches = [
  {"skill_id": "scenario-generator", "relevance": 0.67},
  {"skill_id": "architecture", "relevance": 0.33}
]

# Step 4: 결합
result = {
  "skills_required": ["evidence-collection", "evidence-map-builder"],
  "skills_recommended": ["scenario-generator", "architecture"]
}
```

---

### 예시 2: 코드 리뷰 태스크

#### 입력
```json
{
  "task_id": "CODE-REVIEW-001",
  "purpose": "인증 로직 코드 리뷰",
  "acceptance_criteria": [
    {"criterion": "보안 취약점 없음"}
  ]
}
```

#### 처리
```python
task_tags = ["code-review", "security"]

# 규칙 매칭
rule = find_rule(task_tag="code-review")
# → required: [code-review-checklist, clean-code]

result = {
  "skills_required": ["code-review-checklist", "clean-code"],
  "skills_recommended": ["production-code-audit"]
}
```

---

## 에이전트 통신

### Orchestrator → Router
```yaml
input:
  task_specs: ["workspace/plans/tasks/AUTH-001.json"]
  routing_request: true
```

### Router → Implementer/Researcher
```yaml
output:
  task_id: "AUTH-001"
  assigned_agent: "researcher"
  skills_required: ["evidence-collection"]
  skills_recommended: []
```

---

## 설정 (project_config.yaml 연동)

```yaml
router_config:
  custom_behavior:
    matching_algorithm: "semantic+tag"
    min_confidence: 0.7
```

---

## 라우팅 실패 처리

### Case 1: 규칙 매칭 실패
```python
if no_rule_matched:
    # Fallback to default rule
    return {
        "skills_required": [],
        "skills_recommended": ["architecture"]  # 기본 권장
    }
```

### Case 2: Skill ID 불존재
```python
if skill_id not in skills_index:
    raise Error(f"skill_id '{skill_id}' not found")
    # → Orchestrator에게 에러 전달
```

---

## 체크리스트 (Self-Check)

Router는 매 라우팅 시 다음 확인:

- [ ] Task Spec 유효성 (JSON Schema)
- [ ] task_tags 추출 성공
- [ ] 규칙 매칭 시도 (project_config.yaml)
- [ ] Registry 매칭 (skills_index.json)
- [ ] 모든 skill_id 존재 확인
- [ ] routing_rationale 명시
- [ ] 순환 의존성 없음

---

> [!NOTE]
> Router는 "추측하지 않습니다".
> 규칙이 없으면 default로, skill_id가 없으면 에러로 처리합니다.
