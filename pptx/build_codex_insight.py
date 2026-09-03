#!/usr/bin/env python3
"""OpenAI Codex 洞察 PPT：一页「当前 | 未来」+ 一页未来全幅。"""

from lxml import etree
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)
FONT = "微软雅黑"

NAVY = RGBColor(0x0B, 0x1F, 0x3A)
NAVY2 = RGBColor(0x14, 0x36, 0x5C)
BLUE = RGBColor(0x1B, 0x6C, 0xA8)
TEAL = RGBColor(0x0F, 0x7A, 0x78)
AMBER = RGBColor(0xC4, 0x6B, 0x14)
AMBER_DK = RGBColor(0x8A, 0x48, 0x0A)
CLOUD = RGBColor(0x1A, 0x3A, 0x5C)
BG = RGBColor(0xF2, 0xF4, 0xF7)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
TEXT = RGBColor(0x1A, 0x23, 0x32)
MUTED = RGBColor(0x5A, 0x68, 0x78)
LINE = RGBColor(0xD0, 0xD7, 0xE0)
SOFT = RGBColor(0xE8, 0xED, 0xF3)
RED_SOFT = RGBColor(0xB5, 0x4A, 0x3C)
GOLD = RGBColor(0xF0, 0xD0, 0x6A)
PILL = [
    RGBColor(0x1B, 0x6C, 0xA8),
    RGBColor(0x2B, 0x7A, 0x8A),
    RGBColor(0x3D, 0x6B, 0x8A),
    RGBColor(0x4A, 0x6A, 0x7C),
    RGBColor(0x5C, 0x6E, 0x7A),
]


def _solid(shape, color):
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()


def _line(shape, color, width_pt=1.0):
    shape.line.color.rgb = color
    shape.line.width = Pt(width_pt)


def _ea(run, name=FONT):
    rPr = run._r.get_or_add_rPr()
    for tag in ("a:latin", "a:ea", "a:cs"):
        el = rPr.find(qn(tag))
        if el is None:
            el = etree.SubElement(rPr, qn(tag))
        el.set("typeface", name)


def set_text(shape, lines, anchor=MSO_ANCHOR.MIDDLE, margin=0.05):
    tf = shape.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.auto_size = None
    tf.anchor = anchor
    m = Inches(margin)
    tf.margin_left = m
    tf.margin_right = m
    tf.margin_top = Inches(max(0.02, margin * 0.55))
    tf.margin_bottom = Inches(max(0.02, margin * 0.55))
    first = True
    for item in lines:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.alignment = item.get("align", PP_ALIGN.LEFT)
        p.space_before = Pt(item.get("before", 0))
        p.space_after = Pt(item.get("after", 0))
        run = p.add_run()
        run.text = item["text"]
        run.font.size = Pt(item.get("size", 10))
        run.font.bold = item.get("bold", False)
        run.font.color.rgb = item.get("color", TEXT)
        run.font.name = FONT
        _ea(run)
    return tf


def rect(slide, x, y, w, h, fill, line=None, line_w=1.0, roundness=0.08):
    s = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
    _solid(s, fill)
    if line is not None:
        _line(s, line, line_w)
    try:
        s.adjustments[0] = roundness
    except Exception:
        pass
    return s


def box(slide, x, y, w, h, fill, line=None, line_w=1.0):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    _solid(s, fill)
    if line is not None:
        _line(s, line, line_w)
    return s


def tbox(slide, x, y, w, h):
    """Transparent text box — does not cover rounded corners."""
    s = slide.shapes.add_textbox(x, y, w, h)
    return s


def oval(slide, x, y, w, h, fill):
    s = slide.shapes.add_shape(MSO_SHAPE.OVAL, x, y, w, h)
    _solid(s, fill)
    return s


def arrow_right(slide, x, y, w, h, fill):
    s = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, x, y, w, h)
    _solid(s, fill)
    return s


def down_arrow(slide, x, y, w, h, fill):
    s = slide.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, x, y, w, h)
    _solid(s, fill)
    return s


def header_bar(slide, right_tag):
    box(slide, 0, 0, SLIDE_W, SLIDE_H, BG)
    box(slide, 0, 0, SLIDE_W, Inches(0.72), NAVY)
    box(slide, 0, Inches(0.72), SLIDE_W, Inches(0.06), AMBER)

    t = tbox(slide, Inches(0.28), Inches(0.06), Inches(11.2), Inches(0.38))
    set_text(
        t,
        [{"text": "OpenAI（Codex）洞察：走向个人通用智能，代码智能体是执行内核",
          "size": 18, "bold": True, "color": WHITE}],
        MSO_ANCHOR.MIDDLE, 0.02,
    )
    s = tbox(slide, Inches(0.28), Inches(0.40), Inches(11.2), Inches(0.28))
    set_text(
        s,
        [{"text": "基于 Codex 负责人 Tibo 访谈  ·  形态越来越简单，底座越来越像一台能写代码的云端操作系统",
          "size": 10, "color": RGBColor(0xC5, 0xD0, 0xDC)}],
        MSO_ANCHOR.TOP, 0.02,
    )
    tag = rect(slide, Inches(11.55), Inches(0.18), Inches(1.52), Inches(0.36), AMBER, roundness=0.16)
    set_text(tag, [{"text": right_tag, "size": 11, "bold": True, "color": WHITE, "align": PP_ALIGN.CENTER}], MSO_ANCHOR.MIDDLE, 0.02)


def footer(slide):
    f = tbox(slide, Inches(0.22), Inches(7.22), Inches(12.9), Inches(0.22))
    set_text(
        f,
        [{"text": "来源：OpenAI Codex 负责人 Tibo Sottiaux × Matthew Berman 访谈（2026.08）  ·  「个人通用智能」指统一入口与长期适应的产品形态，并非宣称 AGI 已经实现",
          "size": 8, "color": MUTED}],
        MSO_ANCHOR.MIDDLE, 0.01,
    )


def col_header(slide, x, y, w, text, fill):
    h = rect(slide, x, y, w, Inches(0.34), fill, roundness=0.10)
    set_text(h, [{"text": text, "size": 12, "bold": True, "color": WHITE, "align": PP_ALIGN.LEFT}], MSO_ANCHOR.MIDDLE, 0.08)
    return h


def build_left(slide):
    x, w = Inches(0.22), Inches(4.78)

    strip = rect(slide, x, Inches(1.30), w, Inches(0.40), RGBColor(0xF7, 0xE9, 0xDC), AMBER, 1.15, 0.10)
    set_text(
        strip,
        [{"text": "今天的 Codex 很快会显得原始：人还在替智能体管理系统。",
          "size": 10, "bold": True, "color": AMBER_DK}],
        MSO_ANCHOR.MIDDLE, 0.08,
    )

    y = Inches(1.80)
    pw, gap = Inches(1.50), Inches(0.14)
    products = [
        ("ChatGPT", "负责理解你", RGBColor(0x2C, 0x5A, 0x86)),
        ("Codex", "负责动手执行", RGBColor(0x1E, 0x6E, 0x6A)),
        ("办公类入口", "邮件 / 文档 / 流程", RGBColor(0x6A, 0x6F, 0x78)),
    ]
    for i, (name, desc, color) in enumerate(products):
        px = x + i * (pw + gap)
        s = rect(slide, px, y, pw, Inches(0.70), WHITE, color, 1.35, 0.12)
        set_text(
            s,
            [
                {"text": name, "size": 11, "bold": True, "color": color, "align": PP_ALIGN.CENTER, "after": 2},
                {"text": desc, "size": 8, "color": MUTED, "align": PP_ALIGN.CENTER},
            ],
            MSO_ANCHOR.MIDDLE, 0.04,
        )
        down_arrow(slide, px + Inches(0.64), Inches(2.52), Inches(0.22), Inches(0.18), LINE)

    human = rect(slide, x, Inches(2.74), w, Inches(1.18), WHITE, RED_SOFT, 1.6, 0.08)
    box(slide, x, Inches(2.74), Inches(0.08), Inches(1.18), RED_SOFT)
    tb = tbox(slide, x + Inches(0.16), Inches(2.80), w - Inches(0.24), Inches(1.06))
    set_text(
        tb,
        [
            {"text": "人  =  智能体的系统管理员", "size": 12, "bold": True, "color": RED_SOFT, "after": 5},
            {"text": "手动维护  Skills  ·  记忆  ·  子智能体  ·  工具权限  ·  并行任务", "size": 9, "color": TEXT, "after": 4},
            {"text": "接缝一断，「它真的懂我」就会破裂。模型越强，人越不该管这些。", "size": 9, "color": MUTED},
        ],
        MSO_ANCHOR.MIDDLE, 0.04,
    )

    down_arrow(slide, x + Inches(2.24), Inches(3.96), Inches(0.28), Inches(0.18), LINE)

    laptop = rect(slide, x, Inches(4.18), w, Inches(0.70), SOFT, LINE, 1.0, 0.10)
    set_text(
        laptop,
        [
            {"text": "本机软件成为上限", "size": 11, "bold": True, "color": TEXT, "align": PP_ALIGN.LEFT, "after": 2},
            {"text": "笔记本按人类速度设计  ·  并行一多，人就变成调度员", "size": 9, "color": MUTED},
        ],
        MSO_ANCHOR.MIDDLE, 0.10,
    )

    facts = [
        ("01", "双入口尚未合一", "一个应用、两套工作台，历史仍分开"),
        ("02", "配置仍在用户侧", "Skills / 记忆 / 子智能体还是显式零件"),
        ("03", "程序员是首批用户", "约 2000 万，代码能力刚向全员打开"),
        ("04", "办公与代码仍分叉", "按场景切开是现在，不是终局"),
    ]
    fy, fh, fw, fg = Inches(5.00), Inches(0.98), Inches(2.30), Inches(0.18)
    for i, (num, title, desc) in enumerate(facts):
        col, row = i % 2, i // 2
        fx = x + col * (fw + fg)
        fy2 = fy + row * (fh + Inches(0.10))
        rect(slide, fx, fy2, fw, fh, WHITE, LINE, 1.0, 0.10)
        nb = oval(slide, fx + Inches(0.10), fy2 + Inches(0.14), Inches(0.28), Inches(0.28), NAVY2)
        set_text(nb, [{"text": num, "size": 8, "bold": True, "color": WHITE, "align": PP_ALIGN.CENTER}], MSO_ANCHOR.MIDDLE, 0.01)
        tt = tbox(slide, fx + Inches(0.42), fy2 + Inches(0.12), Inches(1.80), Inches(0.32))
        set_text(tt, [{"text": title, "size": 10, "bold": True, "color": TEXT}], MSO_ANCHOR.MIDDLE, 0.02)
        dd = tbox(slide, fx + Inches(0.12), fy2 + Inches(0.46), Inches(2.06), Inches(0.46))
        set_text(dd, [{"text": desc, "size": 9, "color": MUTED}], MSO_ANCHOR.TOP, 0.02)


def evolution_row(slide, x, y, w):
    """四步形态轴。w 为整行宽度。"""
    steps = [
        ("1", "独立 Codex", "IDE / 插件 / 命令行", "人管智能体", NAVY2),
        ("2", "双入口融合", "一个应用，两个工作台", "边界开始消失", BLUE),
        ("3", "自适应智能体", "同一入口，按角色适配", "壳在变，核不变", TEAL),
        ("4", "个人通用智能", "极简入口 · 语音优先", "智能体自己管自己", AMBER),
    ]
    arrow_w = Inches(0.16)
    gap = Inches(0.06)
    n = 4
    sw = (w - 3 * (arrow_w + gap * 2)) / n
    sh = Inches(1.18)
    for i, (num, title, a, b, fill) in enumerate(steps):
        sx = x + i * (sw + arrow_w + gap * 2)
        rect(slide, sx, y, sw, sh, fill, roundness=0.10)
        nb = oval(slide, sx + Inches(0.10), y + Inches(0.10), Inches(0.24), Inches(0.24), WHITE)
        set_text(nb, [{"text": num, "size": 9, "bold": True, "color": fill, "align": PP_ALIGN.CENTER}], MSO_ANCHOR.MIDDLE, 0.01)
        tt = tbox(slide, sx + Inches(0.36), y + Inches(0.08), sw - Inches(0.44), Inches(0.28))
        set_text(tt, [{"text": title, "size": 11, "bold": True, "color": WHITE}], MSO_ANCHOR.MIDDLE, 0.01)
        aa = tbox(slide, sx + Inches(0.10), y + Inches(0.40), sw - Inches(0.18), Inches(0.34))
        set_text(aa, [{"text": a, "size": 9, "color": RGBColor(0xE8, 0xF0, 0xF5)}], MSO_ANCHOR.TOP, 0.02)
        bb = tbox(slide, sx + Inches(0.10), y + Inches(0.74), sw - Inches(0.18), Inches(0.36))
        set_text(bb, [{"text": b, "size": 10, "bold": True, "color": WHITE}], MSO_ANCHOR.TOP, 0.02)
        if i < 3:
            arrow_right(slide, sx + sw + gap, y + Inches(0.50), arrow_w, Inches(0.18), RGBColor(0xB8, 0xC4, 0xD0))
    return sh


def architecture_stack(slide, x, y, w, compact=True):
    """上简 / 中同 / 下码 / 底云 架构图。"""
    # 顶层
    top_h = Inches(0.50)
    top = rect(slide, x, y, w, top_h, NAVY, roundness=0.08)
    set_text(
        top,
        [{"text": "个人通用智能  ·  极简入口        长期理解你  ·  自主完成任务  ·  不必知道在用哪个产品",
          "size": 11 if compact else 13, "bold": True, "color": WHITE, "align": PP_ALIGN.CENTER}],
        MSO_ANCHOR.MIDDLE, 0.04,
    )

    cap_y = y + top_h + Inches(0.04)
    cap = tbox(slide, x, cap_y, w, Inches(0.20))
    set_text(
        cap,
        [{"text": "同一套底层 AI，按身份 / 工具 / 权限自动适配界面  ·  不再先选「办公」或「代码」",
          "size": 9 if compact else 11, "color": MUTED, "align": PP_ALIGN.CENTER}],
        MSO_ANCHOR.MIDDLE, 0.01,
    )

    roles = [
        ("程序员", "开发环境"),
        ("设计师", "画布 / 设计"),
        ("产品", "文档 / 需求"),
        ("销售", "邮件 / 客户"),
        ("普通人", "简洁对话框"),
    ]
    rw = Inches(1.48) if compact else Inches(2.10)
    rg = Inches(0.10) if compact else Inches(0.16)
    total_r = 5 * rw + 4 * rg
    rx0 = x + (w - total_r) / 2
    ry = cap_y + Inches(0.22)
    rh = Inches(0.50) if compact else Inches(0.52)
    for i, (name, ui) in enumerate(roles):
        rx = rx0 + i * (rw + rg)
        p = rect(slide, rx, ry, rw, rh, WHITE, PILL[i], 1.35, 0.14)
        set_text(
            p,
            [
                {"text": name, "size": 10 if compact else 12, "bold": True, "color": PILL[i], "align": PP_ALIGN.CENTER, "after": 1},
                {"text": ui, "size": 8 if compact else 10, "color": MUTED, "align": PP_ALIGN.CENTER},
            ],
            MSO_ANCHOR.MIDDLE, 0.03,
        )

    # 外壳标签（右侧小条）
    tag_x = rx0 + 5 * (rw + rg) - rg + Inches(0.06)
    # 若右侧空间不够则不贴；两栏页 w=7.92 时 pills 居中后右侧约 0.3"，不够。改为 pills 下方不放。
    # 在 Harness 之上已经用文案说明。

    hy = ry + rh + Inches(0.10)
    hh = Inches(0.68) if compact else Inches(0.70)
    harness = rect(slide, x, hy, w, hh, TEAL, roundness=0.08)
    set_text(
        harness,
        [
            {"text": "统一运行底座（Harness）  ·  底层技术 / 运行时 / 设计哲学完全相同",
             "size": 11 if compact else 14, "bold": True, "color": WHITE, "align": PP_ALIGN.CENTER, "after": 3},
            {"text": "Skills  ·  记忆  ·  权限  ·  子任务     从「用户配置项」变成「系统内部件」——模型越强，用户越不用干预",
             "size": 9 if compact else 11, "color": RGBColor(0xD7, 0xF3, 0xF0), "align": PP_ALIGN.CENTER},
        ],
        MSO_ANCHOR.MIDDLE, 0.06,
    )

    ky = hy + hh + Inches(0.10)
    kh = Inches(1.00) if compact else Inches(1.04)
    kernel = rect(slide, x, ky, w, kh, AMBER, roundness=0.08)
    box(slide, x, ky, Inches(0.10), kh, GOLD)
    set_text(
        kernel,
        [
            {"text": "代码  =  AI 操作数字世界的机器语言      ★ 执行内核",
             "size": 13 if compact else 16, "bold": True, "color": WHITE, "align": PP_ALIGN.CENTER, "after": 4},
            {"text": "自然语言  →  代码 / API / 脚本 / 浏览器 / 云端任务      办公是外壳，代码才是改世界的那一层",
             "size": 10 if compact else 12, "color": RGBColor(0xFF, 0xF0, 0xD6), "align": PP_ALIGN.CENTER, "after": 2},
            {"text": "程序员只是首批受用群体  ·  最终覆盖所有知识工作者与普通用户",
             "size": 10 if compact else 12, "bold": True, "color": WHITE, "align": PP_ALIGN.CENTER},
        ],
        MSO_ANCHOR.MIDDLE, 0.08,
    )

    cy = ky + kh + Inches(0.10)
    ch = Inches(0.54) if compact else Inches(0.52)
    cloud = rect(slide, x, cy, w, ch, CLOUD, roundness=0.08)
    set_text(
        cloud,
        [{"text": "云端智能体工厂      本机只是入口  ·  真正干活的是云端并行执行（同时探索方案 / 编译 / 验证）",
          "size": 11 if compact else 13, "bold": True, "color": WHITE, "align": PP_ALIGN.CENTER}],
        MSO_ANCHOR.MIDDLE, 0.06,
    )
    return cy + ch


def build_right(slide, x, w, compact=True):
    lab = tbox(slide, x, Inches(1.28), w, Inches(0.22))
    set_text(lab, [{"text": "形态趋势  ·  从编程工具收敛为一个极简应用", "size": 10 if compact else 12, "bold": True, "color": NAVY}], MSO_ANCHOR.MIDDLE, 0.01)
    evolution_row(slide, x, Inches(1.52), w)

    lab2 = tbox(slide, x, Inches(2.80), w, Inches(0.22))
    set_text(
        lab2,
        [{"text": "为何代码智能体是内核  ·  上简、中同、下码、底云",
          "size": 10 if compact else 12, "bold": True, "color": NAVY}],
        MSO_ANCHOR.MIDDLE, 0.01,
    )
    architecture_stack(slide, x, Inches(3.10), w, compact=compact)


def slide_combined(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    header_bar(slide, "未来判断")
    col_header(slide, Inches(0.22), Inches(0.88), Inches(4.78), "当前  ·  Codex 仍是过渡形态", NAVY2)
    col_header(slide, Inches(5.18), Inches(0.88), Inches(7.92), "未来  ·  收敛为一个极简入口，代码沉到底座", AMBER)
    box(slide, Inches(5.08), Inches(0.88), Inches(0.025), Inches(6.28), LINE)
    build_left(slide)
    build_right(slide, Inches(5.18), Inches(7.92), compact=True)
    footer(slide)


def slide_future_full(prs):
    """仅未来，铺满整页——方便贴进已有「当前」左半页的母版。"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    header_bar(slide, "未来全幅")
    col_header(slide, Inches(0.28), Inches(0.88), Inches(12.78), "未来  ·  走向个人通用智能，前提是代码智能体成为执行内核", AMBER)

    x, w = Inches(0.28), Inches(12.78)
    lab = tbox(slide, x, Inches(1.30), w, Inches(0.24))
    set_text(lab, [{"text": "形态趋势  ·  从编程工具收敛为一个极简应用", "size": 12, "bold": True, "color": NAVY}], MSO_ANCHOR.MIDDLE, 0.01)
    evolution_row(slide, x, Inches(1.56), w)

    lab2 = tbox(slide, x, Inches(2.86), Inches(7.2), Inches(0.24))
    set_text(lab2, [{"text": "为何代码智能体是内核  ·  上简、中同、下码、底云", "size": 12, "bold": True, "color": NAVY}], MSO_ANCHOR.MIDDLE, 0.01)

    chips = [("上简", NAVY2), ("中同", TEAL), ("下码", AMBER), ("底云", CLOUD)]
    start = x + w - Inches(4.4)
    for i, (name, color) in enumerate(chips):
        cx = start + i * Inches(1.08)
        c = rect(slide, cx, Inches(2.84), Inches(1.00), Inches(0.28), color, roundness=0.18)
        set_text(c, [{"text": name, "size": 10, "bold": True, "color": WHITE, "align": PP_ALIGN.CENTER}], MSO_ANCHOR.MIDDLE, 0.01)

    architecture_stack(slide, x, Inches(3.20), w, compact=False)
    footer(slide)


def build():
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H
    slide_combined(prs)
    slide_future_full(prs)
    out = "/workspace/pptx/OpenAI_Codex洞察_个人通用智能与代码内核.pptx"
    prs.save(out)
    print("saved", out, "slides", len(prs.slides))
    return out


if __name__ == "__main__":
    build()
