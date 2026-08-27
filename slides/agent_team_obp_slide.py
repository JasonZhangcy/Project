"""生成华为云码道 CodeArts Agent Team 规划 OBP 单页胶片（16:9，原生可编辑形状 + 表格）。

用法：python3 slides/agent_team_obp_slide.py [输出路径.pptx]
"""

import sys

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

LATIN_FONT = "Arial"
EA_FONT = "微软雅黑"

INK = RGBColor(0x14, 0x21, 0x3D)
MUTED = RGBColor(0x5A, 0x66, 0x78)
HAIRLINE = RGBColor(0xD9, 0xE0, 0xEA)
CARD_BG = RGBColor(0xF6, 0xF8, 0xFB)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
ACCENT = RGBColor(0xC7, 0x00, 0x0B)
ACCENT_BG = RGBColor(0xFD, 0xF1, 0xF1)
BAND = RGBColor(0xF6, 0xF8, 0xFB)

SLIDE_W, SLIDE_H = 13.333, 7.5
MARGIN = 0.42
CONTENT_TOP = 1.72
CONTENT_BOTTOM = 6.80
LEFT_X, LEFT_W = MARGIN, 5.66
RIGHT_X = LEFT_X + LEFT_W + 0.33
RIGHT_W = SLIDE_W - MARGIN - RIGHT_X

TITLE = "Agent Team 规划：从多智能体引擎 → 智能体组织生产力平台"
SUBTITLE = (
    "三层跃迁：能力可召唤（专家化）· 编排可复现（资产化）· 形态可自主（路由化）"
    "；底座：团队记忆复利 + 可信治理与成本可控"
)
EYEBROW = "华为云码道 CodeArts · OBP 规划"

# (序号标题, 说明, 标签, 标签宽度, 主色, 是否高亮)
LAYERS = [
    (
        "① 统一入口 One Entry",
        "任务描述单一入口进入，IDE / Agent Space / CLI / 流水线多端接入；发起时不再由人选择单 Agent 或 Agent Team",
        "P0",
        0.44,
        RGBColor(0x2E, 0x6B, 0xE6),
        False,
    ),
    (
        "② 决策层 · 编排形态自主路由",
        "复杂度画像（任务信号 + 仓库耦合信号）→ 策略引擎决策形态·规模·模型档位·预算；升配降配断点续跑、路由可解释与 Pin、预算熔断",
        "P0 · L3 业界空白",
        1.34,
        ACCENT,
        True,
    ),
    (
        "③ 编排层 · 自主编排与团队资产固化",
        "Team Leader 编排 + Teammate 自主执行 + 共享任务池；Blueprint 三态与版本锁定、参数化槽位、拓扑 DSL 可视化组队、Trace→Blueprint 自动萃取",
        "P0 · P1",
        0.78,
        RGBColor(0x7A, 0x3E, 0xBF),
        False,
    ),
    (
        "④ 能力层 · 专家与专家团",
        "Role Profile 契约（人设·方法论·工具·DoD·权限·模型档位）；场景专家团包：存量增量开发 / 鸿蒙适配 / 测试补齐 / 安全整改；专家市场与四级作用域治理",
        "P0",
        0.44,
        RGBColor(0x0F, 0x9B, 0x8E),
        False,
    ),
    (
        "⑤ 底座 · Agent Team Ops",
        "团队记忆与轨迹复盘 ｜ 单线程写入 + worktree 沙箱 ｜ 研发门禁 CodeCheck·CloudTest·流水线 ｜ 审计·配额·熔断 ｜ Codebase 与鸿蒙增训模型",
        "P0 · P1",
        0.78,
        RGBColor(0x4A, 0x55, 0x68),
        False,
    ),
]

TABLE_HEADER = ("关键竞争力", "竞争力描述")
TABLE_ROWS = [
    (
        "专家化封装\n零门槛召唤",
        "Role Profile 契约化 + 场景专家团预置包，以\u201c专家 / 专家团\u201d形态交付多智能体能力；"
        "对标 WorkBuddy 三层心智，叠加码道 Skills 与 Codebase",
        False,
    ),
    (
        "团队资产固化\n与版本治理",
        "Blueprint 三态（Draft→Blueprint→Certified）+ 引用版本锁定 + 参数化槽位，"
        "破解\u201c每次拆解都不一样\u201d，上线拆解一致性指标；对标 Qoder 与 Copilot 的版本锁定实践",
        False,
    ),
    (
        "自主编排\n与自主组队",
        "Leader 自动识别任务、动态拆解并按需建组；拓扑 DSL 与可视化编辑支持用户自建团队并一键固化；"
        "Trace→Blueprint 自动萃取，把成功轨迹沉淀为组织级资产",
        False,
    ),
    (
        "编排形态自主路由\n（战略高地）",
        "统一入口下由 Harness 判定单体 / 单体+评审 / 小团队 / 全量团队；"
        "业界仅到子 Agent 自动委派（L2），形态级路由（L3）尚无产品化闭环，学术已验证降本至多 52%",
        True,
    ),
    (
        "升配降配\n与成本护栏",
        "默认单体起步，触发条件下 checkpoint 移交团队续跑而非重启，收敛后自动降配；"
        "任务与租户级预算、递归深度与并发上限、异常熔断，支撑大客户成本可承诺",
        False,
    ),
    (
        "团队记忆\n与经验复利",
        "Teammate 持续化上下文 + 执行轨迹复盘 + 失败模式库反哺路由与拆解；"
        "Codebase 与企业知识按角色定向注入，形成\u201c越用越强\u201d，区别于竞品一次性构造的团队",
        False,
    ),
    (
        "企业级可信\n与门禁闭环",
        "单线程写入 + worktree 沙箱隔离；产出必过 CodeCheck / CloudTest / 流水线门禁；"
        "最小权限、全链路审计、四级作用域治理与私有化合规——纯 IDE 类竞品的结构性短板",
        False,
    ),
    (
        "场景化\n差异化资产",
        "鸿蒙适配迁移专家团 + 存量代码 Codebase 深度理解 + 华为研发体系 Skills 沉淀，"
        "构筑竞品不可迁移的场景护城河",
        False,
    ),
]

FOOTER_LINES = [
    "度量口径：拆解一致性 · 蓝图复用率 · 路由准确率 · Token/任务 · 人工干预次数 · 一次通过率 · 并行加速比",
    "数据锚点：多智能体 ≈ 15× Chat Token（Anthropic）· 多智能体轨迹失败率 41%~87%（NeurIPS'25）· "
    "编排形态路由降本至多 52%（MasRouter, ACL'25）",
]


def style_run(run, size, bold=False, color=INK, space=None):
    font = run.font
    font.size = Pt(size)
    font.bold = bold
    font.color.rgb = color
    font.name = LATIN_FONT
    rPr = run._r.get_or_add_rPr()
    if space is not None:
        rPr.set("spc", str(int(space * 100)))
    ea = rPr.find(qn("a:ea"))
    if ea is None:
        ea = rPr.makeelement(qn("a:ea"), {})
        rPr.append(ea)
    ea.set("typeface", EA_FONT)


def textbox(slide, x, y, w, h, text, size, bold=False, color=INK,
            align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, line=0.95, space=None):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = box.text_frame
    frame.word_wrap = True
    frame.margin_left = frame.margin_right = 0
    frame.margin_top = frame.margin_bottom = 0
    frame.vertical_anchor = anchor
    para = frame.paragraphs[0]
    para.alignment = align
    para.line_spacing = line
    style_run(para.add_run(), 1)  # placeholder replaced below
    para.runs[0].text = text
    style_run(para.runs[0], size, bold, color, space)
    return box


def rect(slide, x, y, w, h, fill, line=None, shape=MSO_SHAPE.RECTANGLE, radius=None):
    box = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    box.shadow.inherit = False
    if fill is None:
        box.fill.background()
    else:
        box.fill.solid()
        box.fill.fore_color.rgb = fill
    if line is None:
        box.line.fill.background()
    else:
        box.line.color.rgb = line
        box.line.width = Pt(0.75)
    if radius is not None and box.adjustments:
        box.adjustments[0] = radius
    box.text_frame.word_wrap = True
    return box


def set_cell(cell, text, size, bold=False, color=INK, fill=WHITE,
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE, line=1.06):
    cell.fill.solid()
    cell.fill.fore_color.rgb = fill
    cell.margin_left = Inches(0.075)
    cell.margin_right = Inches(0.075)
    cell.margin_top = Inches(0.045)
    cell.margin_bottom = Inches(0.045)
    cell.vertical_anchor = anchor
    frame = cell.text_frame
    frame.word_wrap = True
    para = frame.paragraphs[0]
    para.alignment = align
    para.line_spacing = line
    run = para.add_run()
    run.text = text
    style_run(run, size, bold, color)


def build(path):
    prs = Presentation()
    prs.slide_width = Inches(SLIDE_W)
    prs.slide_height = Inches(SLIDE_H)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # ---------- 标题区 ----------
    rect(slide, MARGIN, 0.30, 0.075, 0.52, ACCENT)
    textbox(slide, MARGIN + 0.20, 0.29, 10.4, 0.5, TITLE, 23, True, INK, space=0.4)
    textbox(slide, MARGIN + 0.20, 0.86, 11.6, 0.32, SUBTITLE, 11, False, MUTED)
    textbox(slide, SLIDE_W - MARGIN - 3.2, 0.34, 3.2, 0.26, EYEBROW, 10, False,
            MUTED, align=PP_ALIGN.RIGHT)
    rect(slide, MARGIN, 1.26, SLIDE_W - 2 * MARGIN, 0.012, HAIRLINE)

    # ---------- 栏目标题 ----------
    textbox(slide, LEFT_X, 1.36, LEFT_W, 0.3, "规划构建架构", 14, True, INK)
    rect(slide, LEFT_X, 1.655, 1.05, 0.032, ACCENT)
    textbox(slide, RIGHT_X, 1.36, RIGHT_W, 0.3, "竞争力特性规划", 14, True, INK)
    rect(slide, RIGHT_X, 1.655, 1.05, 0.032, ACCENT)

    # ---------- 左：架构图 ----------
    card_h = 0.88
    gap = (CONTENT_BOTTOM - CONTENT_TOP - len(LAYERS) * card_h) / (len(LAYERS) - 1)
    for idx, (title, detail, tag, tag_w, color, highlight) in enumerate(LAYERS):
        y = CONTENT_TOP + idx * (card_h + gap)
        rect(slide, LEFT_X, y, LEFT_W, card_h,
             ACCENT_BG if highlight else CARD_BG,
             ACCENT if highlight else HAIRLINE,
             shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.055)
        rect(slide, LEFT_X + 0.055, y + 0.075, 0.075, card_h - 0.15, color)
        textbox(slide, LEFT_X + 0.24, y + 0.10, LEFT_W - 0.44 - tag_w, 0.26,
                title, 11.5, True, color if highlight else INK)
        rect(slide, LEFT_X + LEFT_W - 0.14 - tag_w, y + 0.115, tag_w, 0.215,
             color, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.28)
        textbox(slide, LEFT_X + LEFT_W - 0.14 - tag_w, y + 0.145, tag_w, 0.18,
                tag, 8, True, WHITE, align=PP_ALIGN.CENTER)
        textbox(slide, LEFT_X + 0.24, y + 0.40, LEFT_W - 0.46, card_h - 0.46,
                detail, 8.5, False, MUTED, line=1.16)
        if idx < len(LAYERS) - 1:
            arrow = rect(slide, LEFT_X + LEFT_W / 2 - 0.14, y + card_h + gap / 2 - 0.075,
                         0.28, 0.15, RGBColor(0x8C, 0x9A, 0xAD),
                         shape=MSO_SHAPE.ISOSCELES_TRIANGLE)
            arrow.rotation = 180

    # ---------- 右：竞争力表格 ----------
    header_h = 0.36
    row_h = (CONTENT_BOTTOM - CONTENT_TOP - header_h) / len(TABLE_ROWS)
    frame = slide.shapes.add_table(
        len(TABLE_ROWS) + 1, 2, Inches(RIGHT_X), Inches(CONTENT_TOP),
        Inches(RIGHT_W), Inches(CONTENT_BOTTOM - CONTENT_TOP))
    table = frame.table
    tbl_pr = table._tbl.tblPr
    tbl_pr.set("firstRow", "0")
    tbl_pr.set("bandRow", "0")
    for style_id in tbl_pr.findall(qn("a:tableStyleId")):
        tbl_pr.remove(style_id)
    style_el = tbl_pr.makeelement(qn("a:tableStyleId"), {})
    style_el.text = "{2D5ABB26-0587-4C30-8999-92F81FD0307C}"
    tbl_pr.append(style_el)

    table.columns[0].width = Inches(1.58)
    table.columns[1].width = Inches(RIGHT_W - 1.58)
    table.rows[0].height = Inches(header_h)
    for row in list(table.rows)[1:]:
        row.height = Inches(row_h)

    set_cell(table.cell(0, 0), TABLE_HEADER[0], 10.5, True, WHITE, INK,
             align=PP_ALIGN.CENTER)
    set_cell(table.cell(0, 1), TABLE_HEADER[1], 10.5, True, WHITE, INK)
    for i, (key, desc, highlight) in enumerate(TABLE_ROWS, start=1):
        if highlight:
            fill, key_color = ACCENT_BG, ACCENT
        else:
            fill, key_color = (WHITE if i % 2 else BAND), INK
        set_cell(table.cell(i, 0), key, 9.5, True, key_color, fill,
                 align=PP_ALIGN.CENTER)
        set_cell(table.cell(i, 1), desc, 8.5, False,
                 INK if highlight else MUTED, fill)

    # ---------- 页脚 ----------
    rect(slide, MARGIN, CONTENT_BOTTOM + 0.14, SLIDE_W - 2 * MARGIN, 0.012, HAIRLINE)
    footer = textbox(slide, MARGIN, CONTENT_BOTTOM + 0.23, SLIDE_W - 2 * MARGIN, 0.40,
                     FOOTER_LINES[0], 8.5, False, MUTED, line=1.25)
    second = footer.text_frame.add_paragraph()
    second.line_spacing = 1.25
    run = second.add_run()
    run.text = FOOTER_LINES[1]
    style_run(run, 8.5, False, MUTED)

    prs.save(path)
    return path


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "slides/codearts-agent-team-obp.pptx"
    print(build(out))
