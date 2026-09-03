# -*- coding: utf-8 -*-
"""生成《OpenAI（Codex）洞察》PPT 右半页：形态演进 + 终局架构。"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.oxml.ns import qn
from pptx.oxml import parse_xml

FONT = "Microsoft YaHei"

RED = RGBColor(0xC7, 0x00, 0x0B)
RED_DK = RGBColor(0x8E, 0x00, 0x08)
RED_LT = RGBColor(0xFB, 0xE8, 0xE9)
NAVY = RGBColor(0x1B, 0x2A, 0x4A)
NAVY_MD = RGBColor(0x33, 0x45, 0x6B)
GRAY = RGBColor(0x6B, 0x74, 0x86)
GRAY_LT = RGBColor(0x9D, 0xA6, 0xB4)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
PANEL = RGBColor(0xF5, 0xF8, 0xFC)
BLUE1 = RGBColor(0xEA, 0xF0, 0xFA)
BLUE2 = RGBColor(0xE1, 0xEA, 0xF7)
BLUE3 = RGBColor(0xD6, 0xE2, 0xF3)
BORDER = RGBColor(0xC4, 0xD3, 0xE8)


def _font(run, size, bold, color):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = FONT
    rPr = run._r.get_or_add_rPr()
    for tag in ("a:ea", "a:cs"):
        el = rPr.find(qn(tag))
        if el is None:
            el = parse_xml('<%s xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>' % tag)
            rPr.append(el)
        el.set("typeface", FONT)


def text(slide, x, y, w, h, lines, align=PP_ALIGN.CENTER,
         anchor=MSO_ANCHOR.MIDDLE, spacing=0.92):
    """lines: (内容, 字号, 加粗, 颜色) 或其列表；内容中的 \n 自动分段。"""
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    if isinstance(lines, tuple):
        lines = [lines]
    flat = []
    for content, size, bold, color in lines:
        for piece in str(content).split("\n"):
            flat.append((piece, size, bold, color))
    for i, (content, size, bold, color) in enumerate(flat):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = spacing
        _font(p.add_run(), size, bold, color)
        p.runs[0].text = content
    return box


def shape(slide, kind, x, y, w, h, fill=None, line=None, lw=0.75, adj=None):
    s = slide.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
    s.shadow.inherit = False
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid()
        s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line
        s.line.width = Pt(lw)
    if adj is not None:
        try:
            s.adjustments[0] = adj
        except Exception:
            pass
    s.text_frame.word_wrap = True
    return s


def line(slide, x1, y1, x2, y2, color=GRAY_LT, lw=1.0, dash=None, arrow=False):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,
                                   Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.color.rgb = color
    c.line.width = Pt(lw)
    if dash is not None:
        c.line.dash_style = dash
    if arrow:
        ln = c.line._get_or_add_ln()
        ln.append(parse_xml(
            '<a:tailEnd xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"'
            ' type="triangle" w="med" len="med"/>'))
    return c


def vertical_text(sh, content, size, color=WHITE, bold=True):
    tf = sh.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf._txBody.bodyPr.set("vert", "vert270")
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.line_spacing = 1.0
    _font(p.add_run(), size, bold, color)
    p.runs[0].text = content


def draw(slide, px, py, pw, ph, fs=1.0, panel_bg=True):
    """在 (px,py,pw,ph) 区域内绘制右半页全部内容；fs 为字号缩放。"""

    def X(u):
        return px + u * pw

    def W(u):
        return u * pw

    def Y(v):
        return py + v * ph

    def H(v):
        return v * ph

    def S(pt):
        return round(pt * fs, 1)

    if panel_bg:
        shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, px, py, pw, ph,
              fill=PANEL, adj=0.018)
        shape(slide, MSO_SHAPE.RECTANGLE, px, py, 0.055, ph, fill=RED)

    CL, CW = 0.036, 0.942          # 内容区
    SL, SW = 0.036, 0.8464         # 架构堆栈区
    AL, AW = 0.894, 0.081          # 右侧“代码”竖轴
    LL, LW = 0.048, 0.130          # 层名区
    ZL, ZW = 0.188, 0.684          # 层内容区

    # ── 标题区 ────────────────────────────────────────────────
    tag = shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, X(CL), Y(0.014), W(0.20), H(0.039),
                fill=RED, adj=0.35)
    text(slide, X(CL), Y(0.014), W(0.20), H(0.039), ("未来 · 终局判断", S(8.5), True, WHITE))
    text(slide, X(CL), Y(0.059), W(CW), H(0.048),
         ("从代码智能体到个人通用智能：一个内核，千人千面", S(18), True, NAVY),
         align=PP_ALIGN.LEFT)
    text(slide, X(CL), Y(0.109), W(CW), H(0.031),
         ("依据：OpenAI Codex 负责人 Tibo 最新访谈（Matthew Berman 专访）　｜　★ 标记为我方推论", S(8.5), False, GRAY),
         align=PP_ALIGN.LEFT)

    # ── 数据锚点条 ────────────────────────────────────────────
    chips = ["Codex 用户 2000 万", "推理速度 3 个月 +60%", "极速模式最高 14 倍",
             "推理成本降约 80%", "单模型并发 100+ 应用"]
    cw, gap = 0.1772, 0.014
    for i, c in enumerate(chips):
        cx = CL + i * (cw + gap)
        shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, X(cx), Y(0.148), W(cw), H(0.036),
              fill=WHITE, line=BORDER, adj=0.3)
        text(slide, X(cx), Y(0.148), W(cw), H(0.036), (c, S(7.5), True, NAVY_MD))

    # ── ① 形态演进 ───────────────────────────────────────────
    def section(v, num, title, note=None):
        shape(slide, MSO_SHAPE.RECTANGLE, X(CL), Y(v) + H(0.006), W(0.010), H(0.016), fill=RED)
        text(slide, X(CL + 0.020), Y(v), W(CW - 0.020), H(0.028),
             ("%s %s" % (num, title), S(11.5), True, NAVY),
             align=PP_ALIGN.LEFT)
        if note:
            text(slide, X(CL + 0.020), Y(v + 0.030), W(CW - 0.020), H(0.026),
                 (note, S(8), True, RED), align=PP_ALIGN.LEFT)

    section(0.196, "①", "形态演进：从工具到内核，最终收敛为一个极简应用")

    stages = [
        ("① 工具", "命令行 · 插件补全\n人管每一步", BLUE1, NAVY, GRAY),
        ("② 任务", "云端沙箱智能体\n按任务交付成果", BLUE2, NAVY, GRAY),
        ("③ 融合", "并入对话产品\n能力向全员开放", BLUE3, NAVY, NAVY_MD),
        ("④ 内核", "个人通用智能\n界面自适应 · 语音优先", RED, WHITE, WHITE),
    ]
    sw, sgap = 0.1865, 0.006
    for i, (name, desc, fill, c1, c2) in enumerate(stages):
        sx = CL + i * (sw + sgap)
        shape(slide, MSO_SHAPE.CHEVRON, X(sx), Y(0.230), W(sw), H(0.078),
              fill=fill, adj=0.26)
        text(slide, X(sx + 0.023), Y(0.234), W(sw - 0.046), H(0.028), (name, S(9), True, c1))
        text(slide, X(sx + 0.023), Y(0.262), W(sw - 0.046), H(0.042), (desc, S(6.5), False, c2))

    # 终局形态：融合为一个极简应用
    ic_h = 0.046
    ic_w = H(ic_h) / pw
    ic_x = 0.899 - ic_w / 2
    app = shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, X(ic_x), Y(0.230), W(ic_w), H(ic_h),
                fill=NAVY, adj=0.22)
    shape(slide, MSO_SHAPE.ROUNDED_RECTANGULAR_CALLOUT, X(ic_x + ic_w * 0.18),
          Y(0.230) + H(ic_h) * 0.24, W(ic_w * 0.64), H(ic_h) * 0.40, fill=WHITE)
    text(slide, X(0.820), Y(0.282), W(0.158), H(0.026),
         ("终局：融合为\n一个极简应用", S(7), True, RED), spacing=1.05)

    # 剪刀差：能力↑ / 界面复杂度↓
    xl, xr = CL + 0.016, 0.560
    ytop, ybot = 0.330, 0.382
    line(slide, X(xl), Y(ybot), X(xr), Y(ytop), color=RED, lw=1.5, arrow=True)
    line(slide, X(xl), Y(ytop), X(xr), Y(ybot), color=GRAY_LT, lw=1.5,
         dash=MSO_LINE_DASH_STYLE.DASH, arrow=True)
    shape(slide, MSO_SHAPE.OVAL, X((xl + xr) / 2 - 0.007), Y(0.351), W(0.014), H(0.010), fill=RED)
    text(slide, X(0.590), Y(0.322), W(0.388), H(0.020),
         ("底层能力（模型 · 内核 · 云端算力）持续上升", S(7.5), True, RED), align=PP_ALIGN.LEFT)
    text(slide, X(0.590), Y(0.372), W(0.388), H(0.020),
         ("用户可见复杂度 / 界面持续做减法", S(7.5), True, GRAY), align=PP_ALIGN.LEFT)

    # ── ② 终局架构 ───────────────────────────────────────────
    section(0.408, "②", "终局架构：一个内核，千人千面",
            "★ 通用智能体不是把办公与编程拼起来，而是共用一套以代码为底层语言的执行内核")

    def layer(v, h, fill, name, sub):
        shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, X(SL), Y(v), W(SW), H(h),
              fill=fill, line=BORDER, adj=0.10)
        text(slide, X(LL), Y(v), W(LW), H(h),
             [(name, S(8.5), True, NAVY), (sub, S(6.5), False, GRAY)], spacing=1.0)
        line(slide, X(LL + LW + 0.006), Y(v) + H(h) * 0.18,
             X(LL + LW + 0.006), Y(v) + H(h) * 0.82, color=BORDER, lw=0.75)

    # L3 自适应界面层
    layer(0.479, 0.101, BLUE1, "自适应界面层", "同一底座\n千人千面")
    roles = [("程序员", "深度开发环境"), ("产品经理", "文档 · 需求看板"),
             ("销售 / 市场", "邮件与客户数据台"), ("普通用户", "一个简洁对话框")]
    rw, rgap = 0.1605, 0.014
    for i, (role, ui) in enumerate(roles):
        rx = ZL + i * (rw + rgap)
        shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, X(rx), Y(0.492), W(rw), H(0.075),
              fill=WHITE, line=BORDER, adj=0.18)
        text(slide, X(rx), Y(0.492), W(rw), H(0.075),
             [(role, S(7.5), True, NAVY), (ui, S(7), False, GRAY)], spacing=1.05)

    # L2 统一智能体内核
    layer(0.585, 0.101, BLUE2, "统一智能体内核", "Agent Harness")
    bx, bw, bh, bv = ZL, 0.290, 0.062, 0.594
    shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, X(bx), Y(bv), W(bw), H(bh),
          fill=WHITE, line=GRAY_LT, adj=0.12)
    tangles = [(0.10, 0.18, 0.78, 0.86), (0.84, 0.16, 0.16, 0.88),
               (0.06, 0.84, 0.94, 0.28), (0.46, 0.08, 0.58, 0.92)]
    for a, b, c, d in tangles:
        line(slide, X(bx + bw * a), Y(bv) + H(bh) * b,
             X(bx + bw * c), Y(bv) + H(bh) * d, color=GRAY_LT, lw=0.75)
    kws = ["技能 Skills", "记忆 Memory", "子智能体"]
    kw_w = 0.084
    for i, k in enumerate(kws):
        kx = bx + 0.0125 + i * (kw_w + 0.009)
        shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, X(kx), Y(bv) + H(bh) * 0.30,
              W(kw_w), H(bh) * 0.40, fill=RGBColor(0xF0, 0xF3, 0xF8), line=BORDER, adj=0.3)
        text(slide, X(kx), Y(bv) + H(bh) * 0.30, W(kw_w), H(bh) * 0.40, (k, S(6.5), False, NAVY_MD))
    text(slide, X(bx), Y(bv + bh + 0.002), W(bw), H(0.024),
         ("今天：用户手工维护，体验被反复打断", S(7), False, GRAY))

    shape(slide, MSO_SHAPE.RIGHT_ARROW, X(bx + bw + 0.016), Y(bv) + H(bh) * 0.30,
          W(0.048), H(bh) * 0.40, fill=RED)
    rbx = bx + bw + 0.080
    shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, X(rbx), Y(bv), W(bw), H(bh),
          fill=NAVY, adj=0.12)
    text(slide, X(rbx), Y(bv), W(bw), H(bh),
         [("模型自主管理，用户不再介入", S(8.5), True, WHITE),
          ("自主决定记什么 · 用什么技能\n是否派出子智能体", S(6.5), False, RGBColor(0xC9, 0xD4, 0xE8))],
         spacing=1.1)
    text(slide, X(rbx), Y(bv + bh + 0.002), W(bw), H(0.024),
         ("明天：模型越强，脚手架越少", S(7), True, RED))

    # L1 原生多模态模型
    layer(0.692, 0.084, BLUE3, "原生多模态模型", "同一套底座\n天然具备")
    caps = [("编程", RED, WHITE, 0.132), ("工具调用", WHITE, NAVY_MD, 0.104),
            ("搜索", WHITE, NAVY_MD, 0.104), ("调研", WHITE, NAVY_MD, 0.104),
            ("语音", WHITE, NAVY_MD, 0.104), ("视觉", WHITE, NAVY_MD, 0.104)]
    cx = ZL
    for name, fill, fc, w in caps:
        shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, X(cx), Y(0.700), W(w), H(0.040),
              fill=fill, line=None if fill == RED else BORDER, adj=0.28)
        text(slide, X(cx), Y(0.700), W(w), H(0.040),
             (name, S(8) if fill == RED else S(7.5), True if fill == RED else False, fc))
        cx += w + 0.006
    text(slide, X(ZL), Y(0.744), W(ZW), H(0.024),
         ("★ 编程是穿透所有场景的核心能力：办公任务的天花板，由代码能力决定", S(7), True, RED),
         align=PP_ALIGN.LEFT)

    # L0 云端执行层
    layer(0.782, 0.076, BLUE2, "云端执行层", "端侧轻交互\n云端重执行")
    infra = [("云端沙箱集群", 0.200), ("百级应用并发", 0.200), ("笔记本成为物理瓶颈 · 终端仅做轻交互", 0.272)]
    cx = ZL
    for name, w in infra:
        shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, X(cx), Y(0.796), W(w), H(0.044),
              fill=WHITE, line=BORDER, adj=0.24)
        text(slide, X(cx), Y(0.796), W(w), H(0.044), (name, S(7.5), False, NAVY_MD))
        cx += w + 0.006

    # 递归自我改进飞轮
    shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, X(SL), Y(0.863), W(SW), H(0.039),
          fill=RGBColor(0xF0, 0xF3, 0xF8), line=BORDER, adj=0.3)
    text(slide, X(SL), Y(0.863), W(SW), H(0.039),
         ("↻ 递归自我改进飞轮：模型优化推理栈与内核 → 运行成本降约 80% → 释放算力 → 训练更强模型", S(7.5), True, NAVY_MD))

    # 右侧“代码”竖轴
    axis = shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, X(AL), Y(0.479), W(AW), H(0.423),
                 fill=RED, adj=0.10)
    vertical_text(axis, "代码 = 人工智能操作数字世界的底层机器语言", 8.5)

    # ── 人群扩散带 ────────────────────────────────────────────
    shape(slide, MSO_SHAPE.PENTAGON, X(CL), Y(0.910), W(CW), H(0.042),
          fill=RED_LT, adj=0.14)
    spread = [("程序员\n首批 · 2000 万", 0.245, 7.0), ("产品 · 设计 · 数据", 0.235, 7.5),
              ("销售 · 市场 · 财务", 0.235, 8.0), ("所有人", 0.180, 9.0)]
    sx = CL + 0.005
    for name, w, size in spread:
        text(slide, X(sx), Y(0.910), W(w), H(0.042), (name, S(size), True, RED_DK), spacing=0.95)
        sx += w
    for u in (CL + 0.245, CL + 0.480, CL + 0.715):
        line(slide, X(u), Y(0.916), X(u), Y(0.946), color=RGBColor(0xEE, 0xC2, 0xC5), lw=0.75)

    # ── 脚注 ─────────────────────────────────────────────────
    text(slide, X(CL), Y(0.958), W(CW), H(0.040),
         [("编码不再是职业技能，而是全员可无感调用的底层能力：程序员只是最早的体验群体。", S(6.5), True, GRAY),
          ("资料来源：Matthew Berman 专访 OpenAI Codex 负责人 Tibo Sottiaux（2026）；★ 为我方推论，非受访者原话。", S(6.5), False, GRAY_LT)],
         align=PP_ALIGN.LEFT, spacing=1.15)


NOTES = """【本页主张】通用智能体的终局是个人通用智能；而通往终局的底座是代码——我们做的正是那个内核。

【上半部分怎么讲】四段形态演进：工具 → 任务 → 融合 → 内核，右端收敛为一个极简应用。交叉曲线是题眼：底层能力持续上升，用户可见的界面持续做减法（对应 Tibo：底层可以极度复杂，暴露给用户的必须极简）。

【下半部分怎么讲】自下而上四层：
- 云端执行层：笔记本按人的节奏设计，是物理瓶颈；端侧只做轻交互，重执行全部上云。
- 原生多模态模型：编程、工具调用、搜索、调研、语音、视觉长在同一套底座上；编程是穿透所有场景的核心能力。
- 统一智能体内核：今天手工维护技能/记忆/子智能体是过渡形态，明天由模型自治——模型越强，脚手架越少。
- 自适应界面层：同一底座，程序员看到开发环境，销售看到客户数据台，普通用户看到一个对话框。
右侧红色竖轴贯穿三层：代码是人工智能操作数字世界的底层机器语言。底部扩散带：程序员只是首批体验群体，最终覆盖所有人。

【对内定位的三句话】
1. 终局是一个产品，但内核只有一个，而内核是从代码侧长出来的。
2. 代码智能体做能力内核与执行引擎，通用/办公侧做入口与场景界面，二者是上下游而不是零和。
3. 办公任务的天花板由代码能力决定：跨系统集成、批处理、自定义逻辑本质都是编程问题；代码侧有编译与测试这类客观验证信号，能力只能由代码侧外溢到办公侧，反向很难。

【风险提示】
- 标★的两处是我方推论，Tibo 原话只说“下一代模型要求 ChatGPT 与 Codex 合并”，未直接断言“代码智能体是通用智能体的核心”，被追问时按上面三句话展开。
- Tibo 把 Codex 近期增长主要归因于 ChatGPT 的既有用户基础做分发，对方可能引用；用“内核 vs 入口”的分层回应，不要否定入口价值。
- 端侧的准确表述是“端侧轻交互 + 云端重执行”，不要说成“端侧智能体成为主流”。
- 数据锚点均出自该访谈：Codex 约 2000 万用户、基础推理速度 3 个月约 +60%、极速模式最高约 14 倍、Luna 运行成本降约 80%、未来单模型可并发上百个应用。"""


def main():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

    # —— 第 1 页：整页（左半区留给已有内容，右半区为本次交付） ——
    s1 = prs.slides.add_slide(blank)
    ph = shape(s1, MSO_SHAPE.ROUNDED_RECTANGLE, 0.35, 0.28, 5.62, 7.04,
               fill=WHITE, line=BORDER, adj=0.02)
    ph.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    text(s1, 0.75, 3.05, 4.82, 1.5,
         [("左半区（保留位）", 14, True, GRAY_LT),
          ("当前：OpenAI 与 Codex 的发展趋势 —— 你已完成的内容", 10, False, GRAY_LT),
          ("直接删除本占位框，粘贴你的原有内容即可", 9, False, GRAY_LT)], spacing=1.5)
    line(s1, 6.14, 0.30, 6.14, 7.20, color=BORDER, lw=0.75, dash=MSO_LINE_DASH_STYLE.DASH)
    seam = s1.shapes.add_textbox(Inches(6.00), Inches(2.20), Inches(0.26), Inches(3.10))
    seam.text_frame.word_wrap = True
    seam.text_frame._txBody.bodyPr.set("vert", "vert270")
    seam.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = seam.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    _font(p.add_run(), 8, True, GRAY_LT)
    p.runs[0].text = "今天：能力融合　→　明天：形态收敛"
    draw(s1, 6.25, 0.18, 6.90, 7.14, fs=1.0)
    s1.notes_slide.notes_text_frame.text = NOTES

    # —— 第 2 页：右半区放大版（便于校对与二次编辑） ——
    s2 = prs.slides.add_slide(blank)
    draw(s2, 0.55, 0.30, 12.23, 6.90, fs=1.12)

    prs.save("/workspace/OpenAI_Codex_洞察_右半页.pptx")
    print("saved")


if __name__ == "__main__":
    main()
