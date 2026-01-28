# Agent Completion Reports

This directory contains completion reports from agent executions.

## Directory Structure

```
/reports/
├── agent_completion/        # Agent 완료 보고서
│   ├── YYYYMMDD_TaskID_AgentType.md
│   └── ...
├── rejection_reports/       # 거부 보고서  
│   ├── YYYYMMDD_TaskID_Reason.md
│   └── ...
└── validation_results/      # 검증 결과
    ├── YYYYMMDD_TaskID_Result.json
    └── ...
```

## Report Templates

Reports follow the templates defined in `project_config.yaml`.

## Retention Policy

- Reports are kept for project duration
- Archive after project completion
