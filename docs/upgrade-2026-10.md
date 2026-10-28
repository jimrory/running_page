# Running Page 3.0 升级记录

升级基线：个人仓库 `16fd5db`；上游 `3bec720`（2026-10-26）。

## 数据保留

- 直接迁移现有 SQLite，不从 Nike 或 Strava 全量重拉。
- 原数据库 972 条活动（964 跑步、3 骑行、5 力量训练），全部保留。
- 原有 12 个数据库字段逐条核对一致，包含原始路线、心率、距离、日期和时长。
- 新增 subtype、elevation_gain 字段，历史值为 NULL，不编造旧活动的爬升数据。
- 通过上游导出器，使用原有隐私过滤配置重新生成 967 条网页活动；所有原有 JSON 字段逐条一致。
- 5 条零距离力量训练仍保留在数据库中；上游导出器按距离筛选，因此网页不展示。

## 功能和配置

- 使用上游 Dashboard 主题，保留 classic 主题切换能力。
- 保留个人域名、网站标题、头像、favicon 和个人链接元数据。
- 保留每天 UTC 00:00（北京时间 08:00）增量同步 Strava。
- 继续引用原来的 STRAVA_CLIENT_ID、STRAVA_CLIENT_SECRET、STRAVA_CLIENT_REFRESH_TOKEN，无需重新填写或公开 Secrets。
- 保持数据提交到仓库，关闭 GitHub Pages，继续由 Vercel 部署。
- vercel.json 明确设置 Vite、pnpm run build、dist，并保留前端路由重写。
- 不设置未知生日，关闭上游默认的 Month of Life 生成；运动目标暂用上游默认值，可在 config.yml 调整。
- 无 Mapbox Token 时使用 MapLibre + CARTO，避免新版 Mapbox GL 的令牌要求导致地图不可用；显式提供 Token 时保留 Mapbox 渲染器。
- 补齐 TypeScript 路径别名、SVG 声明及 GeoJSON 类型；清理上游 Ruff 无效抑制注释。

## 历史保护

Strava 同步前保存数据库活动 ID，同步后核对所有旧 ID 仍然存在。缺失、空库或损坏数据库会阻止发布。该检查防止丢记录，日常同步仍允许 Strava 更新既有活动字段。

## 验证

- SQLite integrity_check；972 条原始记录所有旧字段严格一致。
- 967 条 JSON 记录所有旧字段严格一致。
- 9 项 Python 测试：源路线不被导出器写回修改、缺失 GPS 不被伪造、允许追加活动、拒绝历史 ID 丢失、拒绝空库和缺失数据库。
- 生产构建、TypeScript、ESLint、Prettier、Black、Ruff。
- 浏览器检查首页、轨迹墙、汇总；底图、单次路线、定位及缩放。
- 未实际访问 Strava API；定时任务需在合并后使用仓库现有 Secrets 验证。

## 上线与回退

推送升级分支并创建 PR 后，先验证 Vercel Preview。Vercel 项目应使用当前受支持的 Node.js（建议 22.12+），确认安装命令未被旧项目设置覆盖。此升级使用 pnpm 8.9.0。

合并前再次获取 master，若每日同步产生了新活动，应以最新数据库和 JSON 重新迁移、核验，不能用旧升级快照覆盖它们。预览通过后合并 master，Vercel 自动正式部署；随后检查首次 GitHub Actions 同步。

回退前端时保留最新数据库和 JSON，恢复旧代码并保留新增数据库列即可。整库回滚到升级前备份会丢失备份之后的新活动，因此只能在核对并保留新增数据之后执行。
