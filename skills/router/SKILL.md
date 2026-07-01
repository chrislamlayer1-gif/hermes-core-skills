---
name: router-learning-system
description: Router Learning System — 越用越聰明嘅任務路由引擎。
 每個 task 有最佳 path，Router 自動記錄經驗、動態調整、跳過爛 path。
version: 1.0
---

# Router Learning System

## 一句總結

Router 係心臟。你俾個任務，Router 自動揀最快最可靠嘅方法執行。
每次使用自動學習，越用越知邊條 path 最快。

## 核心功能

- **五層 Routing**: CLI (T1) → CDP (T2) → Browser (T3) → Cua (T4) → Vision (T5)
- **RouterHistoryDB**: SQLite 自動記錄每次 routing 結果
- **動態排序**: ≥5 samples 後按歷史 performance 排序 paths
- **Fail 跳過**: 連續 3 次 fail 嘅 path 自動 skip
- **冷啟動兼容**: 冇歷史 data 時用 static tier order

## 用法

```python
from router import do, route, history_stats

# 一句搞掂
result = do("create_github_token", args={"note": "my-token"})

# 查學習統計
stats = history_stats("create_github_token")
```

## 技術棧

- Python 3.13+
- SQLite (macOS built-in)
- Zero external dependencies
