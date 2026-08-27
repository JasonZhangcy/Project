# Agent Team 规划 OBP 单页胶片

华为云码道 CodeArts Agent Team 竞争力规划的单页汇报胶片（16:9）。左侧为规划构建架构图（五层：统一入口 / 决策层 / 编排层 / 能力层 / 底座），右侧为关键竞争力特性表。

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

编辑 `agent_team_obp_slide.py` 顶部的 `LAYERS`（左侧架构层）、`TABLE_ROWS`（右侧竞争力表，`True` 表示高亮行）、`FOOTER_LINES`（页脚度量与数据锚点）即可。中文字体在 `EA_FONT` 中设置，默认微软雅黑。
