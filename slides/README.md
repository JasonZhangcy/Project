# Agent Team 规划 OBP 单页胶片

华为云码道 CodeArts Agent Team 竞争力规划的单页汇报胶片（16:9）。

- **左侧：规划构建架构图**。主链路为 ① 统一入口 → ② 任务复杂度画像 → ③ 编排策略引擎（形态自主路由）→ 分支出单 Agent / 单 Agent+评审 / Agent Team 三种形态（含升配降配双向关系）→ ④ Agent Team 执行结构（Leader 与 Teammate 的层级关系、共享任务池）→ 质量门禁链 → ⑤ 交付件；两侧竖栏为"专家/专家团资产库"与"Agent Team Ops 底座"，以虚线箭头注入主链路，并由交付件经虚线回环沉淀为资产与路由策略。实线表示执行主链路，虚线表示注入与反馈。
- **右侧：关键竞争力特性表**，两列（关键竞争力 / 竞争力描述），"编排形态自主路由"行高亮。

| 文件 | 说明 |
| --- | --- |
| `codearts-agent-team-obp.pptx` | 可编辑胶片，全部为 PowerPoint 原生形状与表格，可直接改字、调色、拆分 |
| `codearts-agent-team-obp.pdf` | 打印/预览版 |
| `codearts-agent-team-obp-preview.png` | 效果预览图（150 dpi） |
| `agent_team_obp_slide.py` | 生成脚本，文案与配色集中在文件顶部常量区 |

## 重新生成

```bash
pip install python-pptx
python3 slides/agent_team_obp_slide.py slides/codearts-agent-team-obp.pptx
```

导出 PDF 与预览图（需 LibreOffice 与 poppler-utils）：

```bash
cd slides
soffice --headless --convert-to pdf codearts-agent-team-obp.pptx
pdftoppm -png -r 150 -singlefile codearts-agent-team-obp.pdf codearts-agent-team-obp-preview
```

## 修改文案

编辑 `agent_team_obp_slide.py` 顶部常量即可：

- `ASSET_CHIPS` / `OPS_CHIPS`：左右两侧竖栏条目
- `FORMS`：三种执行形态（第二个元素为 `True` 表示高亮）
- `TEAMMATES` / `GATES`：团队角色与门禁链节点
- `TABLE_ROWS`：右侧竞争力表（第三个元素为 `True` 表示高亮行）
- `FOOTER_LINES`：页脚度量口径与数据锚点

架构图各节点坐标集中在 `draw_architecture()` 中，按英寸标注，调整位置只需改数值。中文字体由 `EA_FONT` 控制，默认微软雅黑。
