# -*- coding: utf-8 -*-
"""生成《Agent Team 竞争力构建规划》OBP 单页 PPT。
左侧:逻辑流程架构图(入口→路由→单Agent/Team→固化回流);右侧:竞争力特性规划表。
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.oxml.ns import qn

# ---------- 配色 ----------
HW_RED = RGBColor(0xC7, 0x00, 0x0B)        # 华为红(强调色)
DARK = RGBColor(0x1F, 0x2A, 0x3A)
GRAY = RGBColor(0x5A, 0x64, 0x72)
BLUE = RGBColor(0x2C, 0x5F, 0x9E)          # 专家资产
GREEN = RGBColor(0x1F, 0x7A, 0x6D)         # 编排/Team
BASE = RGBColor(0x4A, 0x55, 0x68)          # 底座
PURPLE = RGBColor(0x6B, 0x4F, 0xA0)        # 入口
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GREEN = RGBColor(0xEE, 0xF6, 0xF4)
TBL_HDR = RGBColor(0x1F, 0x2A, 0x3A)
TBL_ROW_A = RGBColor(0xF5, 0xF7, 0xFA)
TBL_ROW_B = RGBColor(0xEA, 0xEE, 0xF4)
FONT = "微软雅黑"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
slide = prs.slides.add_slide(prs.slide_layouts[6])


def set_font(run, size, color=DARK, bold=False, name=FONT):
    f = run.font
    f.size = Pt(size)
    f.bold = bold
    f.color.rgb = color
    f.name = name
    rPr = run._r.get_or_add_rPr()
    ea = rPr.find(qn('a:ea'))
    if ea is None:
        ea = rPr.makeelement(qn('a:ea'), {})
        rPr.append(ea)
    ea.set('typeface', name)


def add_text(shape, lines, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE):
    tf = shape.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Pt(2)
    tf.margin_top = tf.margin_bottom = Pt(1)
    for i, (text, size, color, bold) in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        r = p.add_run()
        r.text = text
        set_font(r, size, color, bold)
    return shape


def box(x, y, w, h, fill, line=None, shape_type=MSO_SHAPE.ROUNDED_RECTANGLE,
        radius=0.12, line_w=1.0):
    sp = slide.shapes.add_shape(shape_type, Inches(x), Inches(y), Inches(w), Inches(h))
    if shape_type == MSO_SHAPE.ROUNDED_RECTANGLE:
        try:
            sp.adjustments[0] = radius
        except Exception:
            pass
    if fill is None:
        sp.fill.background()
    else:
        sp.fill.solid()
        sp.fill.fore_color.rgb = fill
    if line is None:
        sp.line.fill.background()
    else:
        sp.line.color.rgb = line
        sp.line.width = Pt(line_w)
    sp.shadow.inherit = False
    return sp


def arrow(x1, y1, x2, y2, color=GRAY, dashed=False, width=1.5,
          head=False, tail=True):
    """带箭头连接线。tail=终点箭头,head=起点箭头。"""
    conn = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,
                                      Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    conn.line.color.rgb = color
    conn.line.width = Pt(width)
    conn.shadow.inherit = False
    ln = conn.line._get_or_add_ln()
    if dashed:
        d = ln.makeelement(qn('a:prstDash'), {'val': 'dash'})
        ln.append(d)
    if head:
        he = ln.makeelement(qn('a:headEnd'), {'type': 'triangle', 'w': 'med', 'len': 'med'})
        ln.append(he)
    if tail:
        te = ln.makeelement(qn('a:tailEnd'), {'type': 'triangle', 'w': 'med', 'len': 'med'})
        ln.append(te)
    return conn


def label(x, y, w, text, size=8.5, color=GRAY, bold=False, align=PP_ALIGN.CENTER):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(0.25))
    add_text(tb, [(text, size, color, bold)], align=align)
    return tb


# ================= 标题区 =================
title = slide.shapes.add_textbox(Inches(0.35), Inches(0.14), Inches(12.6), Inches(0.55))
add_text(title, [("Agent Team 竞争力构建规划:从单 Agent 到企业级数字团队", 26, DARK, True)],
         align=PP_ALIGN.LEFT)
subtitle = slide.shapes.add_textbox(Inches(0.38), Inches(0.66), Inches(12.6), Inches(0.34))
add_text(subtitle, [("统一入口 · 自动路由 · 自主编排 · 专家资产化 —— 三层递进能力 + 企业级治理底座,构筑差异化竞争力", 12.5, GRAY, False)],
         align=PP_ALIGN.LEFT)
box(0.38, 0.60, 1.6, 3.0 / 72, HW_RED, shape_type=MSO_SHAPE.RECTANGLE)

TOP = 1.12
LEFT_X = 0.35
LEFT_W = 5.95

# ================= 左侧:逻辑流程架构图 =================
sec1 = slide.shapes.add_textbox(Inches(LEFT_X), Inches(TOP - 0.04), Inches(LEFT_W), Inches(0.3))
add_text(sec1, [("规划构建架构", 15, HW_RED, True)], align=PP_ALIGN.LEFT)

# --- 第1行:用户 → 统一任务入口 ---
user = box(0.50, 1.50, 0.52, 0.48, DARK, shape_type=MSO_SHAPE.OVAL)
add_text(user, [("用户", 9.5, WHITE, True)])
entry = box(2.00, 1.50, 2.70, 0.48, PURPLE)
add_text(entry, [("统一任务入口", 11.5, WHITE, True), ("自然语言描述,免选执行模式", 8, WHITE, False)])
arrow(1.02, 1.74, 2.00, 1.74, color=DARK)

# --- 第2行:路由决策菱形 ---
dia = box(2.45, 2.18, 1.80, 0.88, HW_RED, shape_type=MSO_SHAPE.DIAMOND)
add_text(dia, [("复杂度评估", 10, WHITE, True), ("自动路由", 10, WHITE, True)])
arrow(3.35, 1.98, 3.35, 2.18, color=DARK)

# --- 第3行:分支 ---
# 左分支:单 Agent
arrow(2.45, 2.62, 1.25, 3.30, color=GRAY)
label(0.82, 2.66, 1.0, "简单任务", 8.5, GRAY)
single = box(0.55, 3.30, 1.30, 0.60, BASE)
add_text(single, [("单 Agent", 10.5, WHITE, True), ("直接执行", 8.5, WHITE, False)])

# 右分支:Agent Team 容器
arrow(4.25, 2.62, 4.42, 3.20, color=GRAY)
label(4.42, 2.60, 1.0, "复杂任务", 8.5, GRAY)
team = box(2.60, 3.20, 3.62, 1.85, LIGHT_GREEN, line=GREEN, line_w=1.2)
label(2.72, 3.26, 2.4, "Agent Team · 自主编排", 9.5, GREEN, True, align=PP_ALIGN.LEFT)
lead = box(3.66, 3.52, 1.50, 0.45, GREEN)
add_text(lead, [("Team Lead:递归拆解·组队", 8.5, WHITE, True)])
tm_xs = [2.78, 3.93, 5.08]
tm_names = ["开发专家", "测试专家", "安全专家"]
for tx, tn in zip(tm_xs, tm_names):
    t = box(tx, 4.22, 1.02, 0.42, WHITE, line=GREEN)
    add_text(t, [(tn, 9, DARK, False)])
    arrow(4.41, 3.97, tx + 0.51, 4.22, color=GREEN, width=1.2)
label(2.70, 4.72, 3.4, "共享任务列表 · Teammate 间消息协同", 8, GRAY)

# 单 Agent ↔ Team 动态升降级(双向虚线)
arrow(1.85, 3.60, 2.60, 3.60, color=HW_RED, dashed=True, head=True, tail=True, width=1.5)
label(1.48, 3.10, 1.6, "动态升降级", 8.5, HW_RED, True)

# --- 第4行:资产与交付 ---
expert = box(0.55, 5.45, 1.50, 0.72, BLUE, shape_type=MSO_SHAPE.CAN)
add_text(expert, [("专家/技能", 9, WHITE, True), ("资产库", 9, WHITE, True)])
deliver = box(2.70, 5.50, 1.40, 0.62, WHITE, line=DARK)
add_text(deliver, [("统一交付", 10, DARK, True), ("结果可审计", 8.5, GRAY, False)])
blueprint = box(4.72, 5.45, 1.50, 0.72, GREEN, shape_type=MSO_SHAPE.CAN)
add_text(blueprint, [("团队蓝图库", 9, WHITE, True), ("(版本化)", 8.5, WHITE, False)])

# 交付箭头
arrow(1.20, 3.90, 2.80, 5.50, color=GRAY)                    # 单Agent → 交付
arrow(3.85, 5.05, 3.55, 5.50, color=GREEN)                   # Team → 交付
# 专家库 → Team(虚线:实例化组队)
arrow(1.55, 5.45, 2.95, 5.05, color=BLUE, dashed=True)
label(1.10, 5.12, 1.7, "专家实例化组队", 8, BLUE)
# Team → 蓝图库(虚线:固化)
arrow(5.05, 5.05, 5.35, 5.45, color=GREEN, dashed=True)
label(5.12, 5.12, 1.2, "执行后固化", 8, GREEN)
# 蓝图库 → 入口(虚线回流,沿右缘)
arrow(6.24, 5.60, 6.24, 1.74, color=GREEN, dashed=True, tail=False)
arrow(6.24, 1.74, 4.72, 1.74, color=GREEN, dashed=True)
label(4.62, 2.02, 1.75, "蓝图复用·例行触发", 8, GREEN)

# --- 第5行:治理底座 ---
base = box(0.55, 6.32, 5.69, 0.46, BASE)
add_text(base, [("企业级治理底座:权限审计 · 成本配额 · 效果度量(ROI) · 共享记忆", 10, WHITE, True)])
legend = slide.shapes.add_textbox(Inches(0.55), Inches(6.84), Inches(5.7), Inches(0.3))
add_text(legend, [("实线 = 任务流    虚线 = 资产/反馈流    架构原则:写操作单线程 + 多 Agent 贡献智能", 8.5, GRAY, False)],
         align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP)

# ================= 右侧:竞争力特性规划表 =================
RIGHT_X = 6.55
RIGHT_W = 6.45
sec2 = slide.shapes.add_textbox(Inches(RIGHT_X), Inches(TOP - 0.04), Inches(RIGHT_W), Inches(0.3))
add_text(sec2, [("竞争力特性规划", 15, HW_RED, True)], align=PP_ALIGN.LEFT)

rows_data = [
    ("专家/专家团资产体系",
     "预置研发领域专家库与场景化专家团模板,一句话唤起整团;企业专家工厂支持规范/资产蒸馏定制;专家市场实现共享、版本化与审核治理"),
    ("任务自主编排(自动组队)",
     "递归 Planner 意图理解与任务拆解,按子任务自动合成 Teammate(角色/模型/工具/上下文);共享任务列表 + 依赖图调度,并行推进"),
    ("团队蓝图固化",
     "编队结构、角色分工、执行流程一键沉淀为参数化、版本化蓝图资产,支持重放与回归评测,解决\u201c每次生成不一致\u201d;支持用户自组团队并固化"),
    ("复杂度自适应路由",
     "统一入口免选择,复杂度评估驱动三档路由(单 Agent / 子 Agent / 团队),决策可解释、可覆盖;运行中动态升降级,业界首个显式产品化"),
    ("成本-质量协同治理",
     "团队模式 Token 成本随规模线性增长,路由决策纳入成本预算约束;基于任务级反馈在线学习,持续优化成本-质量帕累托前沿"),
    ("企业级治理与度量底座",
     "统一控制面纳管全部 Agent 资产:权限、审计、配额;路由决策全程留痕可审计;Agent 效果与 ROI 度量看板;跨任务共享记忆空间"),
]

tbl_top = TOP + 0.32
tbl_h = 5.62
gfx = slide.shapes.add_table(len(rows_data) + 1, 2,
                             Inches(RIGHT_X), Inches(tbl_top), Inches(RIGHT_W), Inches(tbl_h))
table = gfx.table
table.columns[0].width = Inches(1.72)
table.columns[1].width = Inches(RIGHT_W - 1.72)
table.rows[0].height = Inches(0.40)
for i in range(1, len(rows_data) + 1):
    table.rows[i].height = Inches((tbl_h - 0.40) / len(rows_data))

hdr = ["关键竞争力", "竞争力描述"]
for c in range(2):
    cell = table.cell(0, c)
    cell.fill.solid()
    cell.fill.fore_color.rgb = TBL_HDR
    cell.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = cell.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = hdr[c]
    set_font(r, 13, WHITE, True)

for i, (k, v) in enumerate(rows_data, start=1):
    fill = TBL_ROW_A if i % 2 == 1 else TBL_ROW_B
    c0 = table.cell(i, 0)
    c0.fill.solid(); c0.fill.fore_color.rgb = fill
    c0.vertical_anchor = MSO_ANCHOR.MIDDLE
    c0.margin_left = Pt(5); c0.margin_right = Pt(3)
    p = c0.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    r = p.add_run(); r.text = k
    accent = HW_RED if "路由" in k else DARK
    set_font(r, 11, accent, True)
    c1 = table.cell(i, 1)
    c1.fill.solid(); c1.fill.fore_color.rgb = fill
    c1.vertical_anchor = MSO_ANCHOR.MIDDLE
    c1.margin_left = Pt(6); c1.margin_right = Pt(5)
    c1.text_frame.word_wrap = True
    p = c1.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    r = p.add_run(); r.text = v
    set_font(r, 10, DARK, False)

foot = slide.shapes.add_textbox(Inches(RIGHT_X), Inches(tbl_top + tbl_h + 0.05), Inches(RIGHT_W), Inches(0.5))
add_text(foot, [("对标:Claude Code Agent Teams / Cursor 递归编排 / Devin Managed Devins / Grok Bot / WorkBuddy 专家团 / GitHub Agent HQ", 9, GRAY, False)],
         align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP)

prs.save("/workspace/Agent_Team_OBP规划.pptx")
print("saved")
