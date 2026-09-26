import pathlib
import markdown

SRC = pathlib.Path(__file__).with_name("alibaba-qoder-qoderwake-qwenwork-multi-agent-insight.md")
OUT = SRC.with_suffix(".html")

CSS = """
body { font-family: "Microsoft YaHei", "PingFang SC", "Noto Sans CJK SC", sans-serif; color: #262626;
       max-width: 1080px; margin: 0 auto; padding: 32px 40px 60px; line-height: 1.7; font-size: 14.5px; }
h1 { color: #C00000; font-size: 26px; border-left: 8px solid #C00000; padding-left: 14px; line-height: 1.4; }
h2 { color: #fff; background: #C00000; padding: 6px 14px; border-radius: 6px; font-size: 20px; margin-top: 36px; }
h3 { color: #8A5A00; border-bottom: 2px solid #F2A900; padding-bottom: 4px; font-size: 17px; margin-top: 28px; }
blockquote { background: #F5F5F5; border-left: 4px solid #BFBFBF; margin: 12px 0; padding: 8px 16px; color: #595959; }
table { border-collapse: collapse; width: 100%; margin: 12px 0 18px; font-size: 13.5px; }
th { background: #F2A900; color: #fff; text-align: left; }
th, td { border: 1px solid #E5D3A6; padding: 6px 10px; vertical-align: top; }
tr:nth-child(even) td { background: #FFF9EA; }
code { background: #F3F3F3; padding: 1px 5px; border-radius: 4px; font-size: 13px; }
a { color: #005A9C; word-break: break-all; }
strong { color: #1F1F1F; }
hr { border: none; border-top: 1px dashed #D9D9D9; margin: 28px 0; }
@media print { body { padding: 0 8px; max-width: none; } h2 { break-after: avoid; } table, tr { break-inside: avoid; } }
"""

body = markdown.markdown(SRC.read_text(encoding="utf-8"), extensions=["tables", "sane_lists"])
OUT.write_text(
    f'<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">'
    f'<meta name="viewport" content="width=device-width, initial-scale=1">'
    f"<title>阿里云多人多Agent协同洞察分析</title><style>{CSS}</style></head><body>{body}</body></html>",
    encoding="utf-8",
)
print(OUT)
