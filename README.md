# Datalane

**Datalane**（数据车道）— 可扩展的数据采集 · 清洗 · 推送流水线。

## 架构

```text
Trigger (定时/CLI) → Ingest → Transform → Deliver
                         ↑          ↑          ↑
                    plugins/   plugins/   plugins/
```

业务配置在 `jobs/*.yaml`，代码扩展在 `plugins/`。

## 快速开始

```powershell
pip install -r requirements.txt
playwright install
copy .env.example .env
# 编辑 .env（Token 须为完整格式：数字:密钥）

python run_job.py --list
python run_job.py dongqiudi
python scripts/test_setup.py
```

## 任务

| Job ID | 说明 |
|--------|------|
| `dongqiudi` | 懂球帝赛程 → CSV/TXT → Telegram |
| `web_monitor` | 网页监控 → 关键词告警 → Telegram |

## 定时（每天 00:00）

```powershell
setup_windows_task.bat
# 或
python scripts/scheduler.py
```

## 目录

```text
config/       全局配置
core/         流水线引擎
plugins/      可插拔模块
jobs/         业务 YAML
scripts/      工具脚本
data/         输出（不提交 Git）
```
