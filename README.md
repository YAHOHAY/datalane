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
run_job.py          ★ 推荐统一入口
daily_job.py        每日赛程（等同 run_job dongqiudi）
fetch_matches.py    赛程抓取（可选 --telegram）
main.py             网页监控
test_setup.py       配置自检
config/             全局配置
core/               流水线引擎
plugins/            可插拔模块
jobs/               业务 YAML
scripts/            定时、自检实现
data/               输出（仅 .gitkeep 入库，数据文件忽略）
docs/FILE_MAP.md    旧文件 → 新位置对照
```

> 若 GitHub 上「少了很多 .py」：旧逻辑已迁入 `plugins/`，见 [docs/FILE_MAP.md](docs/FILE_MAP.md)。
