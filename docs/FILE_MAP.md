# 文件对照表

## 目标架构（当前仓库）

| 路径 | 职责 |
|------|------|
| `config/settings.py` | 全局配置 |
| `core/pipeline.py` | Ingest → Transform → Deliver |
| `core/triggers.py` | CLI、定时调度 |
| `plugins/ingest/dongqiudi.py` | 懂球帝 API |
| `plugins/ingest/playwright_web.py` | 浏览器抓取 |
| `plugins/transform/html_to_text.py` | HTML → 文本 + 关键词 |
| `plugins/transform/pandas_clean.py` | 预留 |
| `plugins/deliver/telegram.py` | Telegram 发送 |
| `plugins/deliver/whatsapp.py` | 预留 |
| `jobs/*.yaml` | 业务编排 |
| `scripts/run_job.py` | **主入口** |

## 命令

```powershell
python scripts/run_job.py dongqiudi_schedule
python scripts/run_job.py web_monitor
python scripts/scheduler.py
```

## Legacy（`legacy/`）

旧习惯命令仍可用，内部转发到新入口，见 `legacy/README.md`。

## 不入库

`.env`、`data/*`（除 `.gitkeep`）
