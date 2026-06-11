#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build ebook artifacts for 《中论现代性解读》
Outputs:
  - zhonglun-modern.md   (merged markdown)
  - zhonglun-modern.epub (ebook)
  - zhonglun-modern.pdf  (print-ready)
"""

import os
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content" / "zh"
COVER_PATH = ROOT / "cover.png"
OUT_MD = ROOT / "zhonglun-modern.md"
OUT_EPUB = ROOT / "zhonglun-modern.epub"
OUT_PDF = ROOT / "zhonglun-modern.pdf"

# ---------------------------------------------------------------------------
# 1. Merge Markdown
# ---------------------------------------------------------------------------
def merge_markdown():
    chapters = sorted(CONTENT_DIR.glob("ch*.md"),
                      key=lambda p: int(re.search(r'\d+', p.stem).group()))
    if not chapters:
        print("No chapters found in", CONTENT_DIR)
        sys.exit(1)

    lines = []
    # Front matter
    lines.append("# 《中论现代性解读》\n")
    lines.append("> 龙树《中论》的后人类主义跨学科哲学重构\n")
    lines.append("> A Posthumanist Interdisciplinary Philosophical Reconstruction of Nāgārjuna's *Madhyamaka*\n")
    lines.append("\n---\n\n")

    for ch in chapters:
        lines.append(f"\n<!-- {ch.name} -->\n")
        lines.append(ch.read_text(encoding="utf-8"))
        lines.append("\n\n---\n\n")

    # References
    lines.append("\n## 参考文献 | References\n\n")
    lines.append("### 原始文献 | Primary Sources\n")
    lines.append("- 龙树.《中论》. 鸠摩罗什译. 北京：中华书局.\n")
    lines.append("- Nāgārjuna. *Mūlamadhyamakakārikā*. Sanskrit text edited by Louis de La Vallée Poussin. Bibliotheca Buddhica, 1903.\n\n")
    lines.append("### 现代译本与研究 | Modern Translations and Studies\n")
    lines.append("- Garfield, Jay L. *The Fundamental Wisdom of the Middle Way: Nāgārjuna's Mūlamadhyamakakārikā*. Oxford: Oxford University Press, 1995.\n")
    lines.append("- Westerhoff, Jan. *Nāgārjuna's Madhyamaka: A Philosophical Introduction*. Oxford: Oxford University Press, 2009.\n")
    lines.append("- Siderits, Mark, and Shoryu Katsura. *Nāgārjuna's Middle Way: Mūlamadhyamakakārikā*. Boston: Wisdom Publications, 2013.\n")

    OUT_MD.write_text("".join(lines), encoding="utf-8")
    print(f"[OK] Merged markdown -> {OUT_MD}")
    return "".join(lines)

# ---------------------------------------------------------------------------
# 2. Build EPUB
# ---------------------------------------------------------------------------
def build_epub(full_md: str):
    try:
        import markdown
        from ebooklib import epub
    except ImportError as e:
        print(f"[SKIP] EPUB generation: {e}")
        return

    # Convert full markdown to HTML
    md = markdown.Markdown(extensions=["extra", "toc"])
    full_html = md.convert(full_md)

    book = epub.EpubBook()
    book.set_identifier("zhonglun-modern-2026")
    book.set_title("中论现代性解读")
    book.set_language("zh")
    book.add_author("chino mana - 千野 真名")
    book.add_metadata("DC", "description",
        "龙树《中论》的后人类主义跨学科哲学重构")

    # Cover
    if COVER_PATH.exists():
        book.set_cover("cover.png", COVER_PATH.read_bytes())

    # CSS
    style = """
    body {
        font-family: "STHeiti", "PingFang SC", "Microsoft YaHei", sans-serif;
        line-height: 1.8;
        margin: 1em;
    }
    h1 { font-size: 1.8em; text-align: center; margin-top: 2em; page-break-before: always; }
    h2 { font-size: 1.4em; margin-top: 1.5em; }
    h3 { font-size: 1.2em; margin-top: 1.2em; }
    blockquote {
        border-left: 3px solid #ccc;
        margin-left: 1em;
        padding-left: 1em;
        color: #555;
        font-style: italic;
    }
    hr { border: none; border-top: 1px solid #ccc; margin: 2em 0; }
    a { color: #2a6496; text-decoration: none; }
    table { border-collapse: collapse; width: 100%; margin: 1em 0; }
    th, td { border: 1px solid #ddd; padding: 0.5em; }
    th { background: #f5f5f5; }
    """
    nav_css = epub.EpubItem(uid="style", file_name="style/style.css",
                            media_type="text/css", content=style)
    book.add_item(nav_css)

    # Split by chapters (<!-- chXX.md --> comments)
    parts = re.split(r'<!-- (ch\d+\.md) -->', full_md)
    # parts[0] = front matter, then alternating marker + content

    # Front matter chapter
    front_html = md.convert(parts[0])
    front_item = epub.EpubHtml(title="封面与前言", file_name="front.xhtml", lang="zh")
    front_item.content = f'<html><head><link rel="stylesheet" href="style/style.css"/></head><body>{front_html}</body></html>'
    front_item.add_item(nav_css)
    book.add_item(front_item)

    chapters = [front_item]
    for i in range(1, len(parts), 2):
        marker = parts[i]      # e.g. ch01.md
        content = parts[i + 1]
        ch_num = int(re.search(r'\d+', marker).group())
        # Extract title from first # line
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else f"第{ch_num}章"

        ch_html = md.convert(content)
        item = epub.EpubHtml(title=title, file_name=f"ch{ch_num:02d}.xhtml", lang="zh")
        item.content = f'<html><head><link rel="stylesheet" href="style/style.css"/></head><body>{ch_html}</body></html>'
        item.add_item(nav_css)
        book.add_item(item)
        chapters.append(item)

    book.toc = chapters
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ["nav"] + chapters

    epub.write_epub(OUT_EPUB, book, {})
    print(f"[OK] EPUB -> {OUT_EPUB}")

# ---------------------------------------------------------------------------
# 3. Build PDF
# ---------------------------------------------------------------------------
def build_pdf(full_md: str):
    try:
        import markdown
        from bs4 import BeautifulSoup, NavigableString
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, PageBreak,
            Image, Table, TableStyle, KeepTogether
        )
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
        from reportlab.lib import colors
        from reportlab.lib.units import cm
    except ImportError as e:
        print(f"[SKIP] PDF generation: {e}")
        return

    # Register Chinese fonts
    pdfmetrics.registerFont(TTFont('STHeiti', '/System/Library/Fonts/STHeiti Medium.ttc'))
    pdfmetrics.registerFont(TTFont('STHeitiBold', '/System/Library/Fonts/STHeiti Medium.ttc'))

    # Styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='BookTitle', fontName='STHeitiBold', fontSize=22, leading=30,
        alignment=TA_CENTER, spaceAfter=20, textColor=colors.HexColor('#1a1a1a')
    ))
    styles.add(ParagraphStyle(
        name='BookSubtitle', fontName='STHeiti', fontSize=12, leading=18,
        alignment=TA_CENTER, spaceAfter=30, textColor=colors.HexColor('#555555')
    ))
    styles.add(ParagraphStyle(
        name='H1', fontName='STHeitiBold', fontSize=16, leading=24,
        alignment=TA_LEFT, spaceBefore=20, spaceAfter=12,
        textColor=colors.HexColor('#1a1a1a'), borderPadding=(0, 0, 6, 0),
        borderWidth=0, borderColor=colors.HexColor('#cccccc'),
    ))
    styles.add(ParagraphStyle(
        name='H2', fontName='STHeitiBold', fontSize=13, leading=20,
        alignment=TA_LEFT, spaceBefore=16, spaceAfter=8,
        textColor=colors.HexColor('#2a2a2a')
    ))
    styles.add(ParagraphStyle(
        name='H3', fontName='STHeitiBold', fontSize=11, leading=16,
        alignment=TA_LEFT, spaceBefore=12, spaceAfter=6,
        textColor=colors.HexColor('#333333')
    ))
    styles.add(ParagraphStyle(
        name='Body', fontName='STHeiti', fontSize=10, leading=16,
        alignment=TA_JUSTIFY, spaceAfter=8, firstLineIndent=20,
        textColor=colors.HexColor('#333333')
    ))
    styles.add(ParagraphStyle(
        name='Quote', fontName='STHeiti', fontSize=10, leading=16,
        alignment=TA_LEFT, spaceAfter=8, leftIndent=20, rightIndent=10,
        textColor=colors.HexColor('#555555')
    ))
    styles.add(ParagraphStyle(
        name='ListItem', fontName='STHeiti', fontSize=10, leading=16,
        alignment=TA_LEFT, spaceAfter=4, leftIndent=30, firstLineIndent=0,
        textColor=colors.HexColor('#333333')
    ))
    styles.add(ParagraphStyle(
        name='Caption', fontName='STHeiti', fontSize=9, leading=14,
        alignment=TA_CENTER, spaceAfter=6, textColor=colors.HexColor('#777777')
    ))

    def html_to_story(html_str):
        """Convert HTML string to list of reportlab flowables."""
        soup = BeautifulSoup(html_str, "html.parser")
        story = []

        def render_inline(node):
            """Convert inline HTML node to string with reportlab-compatible tags."""
            if isinstance(node, NavigableString):
                text = str(node)
                # Escape XML special chars
                text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                return text
            tag = node.name
            if tag is None:
                return render_inline(node.string) if node.string else ""
            inner = "".join(render_inline(c) for c in node.children)
            if tag == "strong" or tag == "b":
                return f"<b>{inner}</b>"
            elif tag == "em" or tag == "i":
                return f"<i>{inner}</i>"
            elif tag == "u":
                return f"<u>{inner}</u>"
            elif tag == "a":
                href = node.get("href", "")
                return f'<a href="{href}" color="blue">{inner}</a>'
            elif tag == "code":
                return f'<font face="Courier">{inner}</font>'
            elif tag == "br":
                return "<br/>"
            elif tag == "span":
                return inner
            elif tag in ("sup", "sub"):
                return f"<{tag}>{inner}</{tag}>"
            else:
                return inner

        def process_block(node):
            """Process a block-level node and return list of flowables."""
            if isinstance(node, NavigableString):
                text = str(node).strip()
                if text:
                    return [Paragraph(text, styles['Body'])]
                return []
            tag = node.name
            if tag is None:
                return []

            # Container tags: recurse into children
            if tag in ("div", "section", "article", "header", "footer", "main"):
                result = []
                for child in node.children:
                    result.extend(process_block(child))
                return result

            # Inline wrapper at block level
            if tag in ("span", "a", "strong", "em", "b", "i", "u", "code"):
                text = render_inline(node)
                if text.strip():
                    return [Paragraph(text, styles['Body'])]
                return []

            # Headings
            if tag == "h1":
                text = render_inline(node)
                return [PageBreak(), Paragraph(text, styles['H1'])]
            if tag == "h2":
                text = render_inline(node)
                return [Paragraph(text, styles['H2'])]
            if tag == "h3":
                text = render_inline(node)
                return [Paragraph(text, styles['H3'])]
            if tag in ("h4", "h5", "h6"):
                text = render_inline(node)
                return [Paragraph(text, styles['H3'])]

            # Paragraph
            if tag == "p":
                text = render_inline(node)
                if text.strip():
                    return [Paragraph(text, styles['Body'])]
                return []

            # Blockquote
            if tag == "blockquote":
                result = []
                for child in node.children:
                    result.extend(process_block(child))
                # Wrap each paragraph in italic
                wrapped = []
                for f in result:
                    if isinstance(f, Paragraph):
                        # Re-render with italic wrapper
                        txt = f.text
                        wrapped.append(Paragraph(f"<i>{txt}</i>", styles['Quote']))
                    else:
                        wrapped.append(f)
                return wrapped

            # Horizontal rule
            if tag == "hr":
                return [Spacer(1, 12), Paragraph("—" * 30, styles['Caption']), Spacer(1, 12)]

            # Lists
            if tag == "ul":
                items = []
                for li in node.find_all("li", recursive=False):
                    li_text = render_inline(li)
                    if li_text.strip():
                        items.append(Paragraph(f"• {li_text}", styles['ListItem']))
                return items
            if tag == "ol":
                items = []
                for idx, li in enumerate(node.find_all("li", recursive=False), 1):
                    li_text = render_inline(li)
                    if li_text.strip():
                        items.append(Paragraph(f"{idx}. {li_text}", styles['ListItem']))
                return items
            if tag == "li":
                # Should be handled by parent list, but fallback
                text = render_inline(node)
                if text.strip():
                    return [Paragraph(f"• {text}", styles['ListItem'])]
                return []

            # Table
            if tag == "table":
                return build_table(node)

            # Preformatted / code block
            if tag in ("pre", "code"):
                text = node.get_text()
                return [Paragraph(f'<font face="Courier" size="9">{text}</font>', styles['Body'])]

            # Fallback
            text = render_inline(node)
            if text.strip():
                return [Paragraph(text, styles['Body'])]
            return []

        def build_table(table_node):
            rows = []
            max_cols = 0
            for tr in table_node.find_all("tr"):
                cells = []
                for td in tr.find_all(["td", "th"]):
                    text = render_inline(td)
                    style = styles['Body']
                    if td.name == "th":
                        style = ParagraphStyle(
                            name='TableHead', parent=styles['Body'],
                            fontName='STHeitiBold', textColor=colors.white,
                            alignment=TA_CENTER
                        )
                    cells.append(Paragraph(text, style))
                if cells:
                    max_cols = max(max_cols, len(cells))
                    rows.append(cells)
            if not rows:
                return []
            for row in rows:
                while len(row) < max_cols:
                    row.append(Paragraph("", styles['Body']))
            t = Table(rows, repeatRows=1)
            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f0f0f0")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#333333")),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]))
            return [Spacer(1, 8), t, Spacer(1, 8)]

        for child in soup.children:
            story.extend(process_block(child))
        return story

    # Convert markdown -> HTML
    md = markdown.Markdown(extensions=["extra", "toc"])
    full_html = md.convert(full_md)

    # Build story
    story = []

    # Cover page
    if COVER_PATH.exists():
        try:
            from PIL import Image as PILImage
            with PILImage.open(COVER_PATH) as img:
                w, h = img.size
            # Fit to page width (A4 = 595x842 pts, margins ~72pts each -> ~451pts usable)
            max_w = 14 * cm
            scale = max_w / w
            display_h = h * scale
            story.append(Spacer(1, 2 * cm))
            story.append(Image(str(COVER_PATH), width=max_w, height=display_h))
            story.append(Spacer(1, 1 * cm))
        except Exception as e:
            print(f"[WARN] Could not embed cover image: {e}")

    story.append(Paragraph("《中论现代性解读》", styles['BookTitle']))
    story.append(Paragraph("龙树《中论》的后人类主义跨学科哲学重构", styles['BookSubtitle']))
    story.append(Paragraph("A Posthumanist Interdisciplinary Philosophical Reconstruction of Nāgārjuna's <i>Mūlamadhyamakakārikā</i>", styles['BookSubtitle']))
    story.append(Spacer(1, 1 * cm))
    story.append(Paragraph("作者：chino mana - 千野 真名", styles['Caption']))
    story.append(PageBreak())

    # Main content
    story.extend(html_to_story(full_html))

    # Build PDF
    doc = SimpleDocTemplate(
        str(OUT_PDF), pagesize=A4,
        rightMargin=72, leftMargin=72,
        topMargin=72, bottomMargin=72
    )
    doc.build(story)
    print(f"[OK] PDF -> {OUT_PDF}")

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("=" * 60)
    print("Building ebook artifacts for 中论现代性解读")
    print("=" * 60)

    full_md = merge_markdown()
    build_epub(full_md)
    build_pdf(full_md)

    print("=" * 60)
    print("All done!")
    print("=" * 60)

if __name__ == "__main__":
    main()
