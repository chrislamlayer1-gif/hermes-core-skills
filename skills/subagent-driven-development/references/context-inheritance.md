# Subagent Context Inheritance Pattern

## 問題
每次 delegate_task 都要傳晒所有 context，subagent 各自探索 codebase 浪費 token。

## 解決方案：Context Package

每次 dispatch subagent 前，打包一份結構化 context：

```
## Project Context —— 2-3句 project 簡介
## Task —— 要做咩（from the plan）
## Shared State —— 已做咗咩、決定咗咩
## Files —— 相關檔案
## Constraints —— 限制同注意事項
```

## 多 task 共享狀態

```python
# Task 1 完成後寫 low .hermes/state/task-1-done.json
{
  "files_created": ["src/storage/StorageAdapter.ts"],
  "key_decisions": {"pattern": "adapter pattern"},
  "pending_issues": []
}

# Task 2 讀取呢份 file 做 context
```

## 好處
- Subagent 唔使自己探索 codebase（省 token）
- 避免 subagent 做錯方向
- 唔使次次傳晒所有嘢
