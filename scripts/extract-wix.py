#!/usr/bin/env python3
"""Extract styles and page content from archived Wix HTML exports."""

import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARCHIVE = ROOT / "archive"
HOME_HTML = ARCHIVE / "Home _ Ray Mitchell.html"
EXP_HTML = ARCHIVE / "Areas of Expertise _ Ray Mitchell.html"
OUT_CSS = ROOT / "public" / "styles" / "site.css"
OUT_HOME = ROOT / "index.html"
OUT_EXPERTISE = ROOT / "areas-of-expertise" / "index.html"
FONTS_DIR = ROOT / "public" / "fonts"

FONT_URLS = [
    "https://static.parastorage.com/fonts/v2/eca8b0cd-45d8-43cf-aee7-ca462bc5497c/v1/din-next-w01-light.woff2",
    "https://static.parastorage.com/fonts/v2/8e5b5cbc-6ad9-49f7-aee7-4e5133c3ee4d/v1/futura-lt-w01-light.woff2",
    "https://static.parastorage.com/fonts/v2/d18d0657-b3bd-4cd5-acd7-eab24ec6b49e/v1/bree-w01-thin-oblique.woff2",
]

STATIC_OVERRIDES = """
/* Static site fixes */
html { scroll-behavior: smooth; }
.site-body { overflow-x: hidden; }

/* Remove empty third row that caused huge blank space on home */
[data-mesh-id="Containerh4hzqinlineContent-gridContainer"] {
  grid-template-rows: repeat(2, min-content) !important;
}
#comp-lsvshq771 { display: none !important; }

/* Hero + services text enter animations (replace Wix Thunderbolt JS) */
#comp-j6w6mgxq:not([data-motion-enter="done"]),
#comp-j6w888ep:not([data-motion-enter="done"]) {
  animation: motion-floatIn 1200ms 1000ms cubic-bezier(0.445, 0.05, 0.55, 0.95) both !important;
  --motion-translate-x: 0px;
  --motion-translate-y: 60px;
}

#comp-j6w6mgy4:not([data-motion-enter="done"]) {
  animation: motion-floatIn 1200ms 300ms cubic-bezier(0.445, 0.05, 0.55, 0.95) both !important;
  --motion-translate-x: -60px;
  --motion-translate-y: 0px;
}

#comp-mfo1u4y8:not([data-motion-enter="done"]) {
  animation: motion-floatIn 1200ms 500ms cubic-bezier(0.445, 0.05, 0.55, 0.95) both !important;
  --motion-translate-x: 0px;
  --motion-translate-y: 60px;
}

#services { scroll-margin-top: 80px; }
#home { scroll-margin-top: 80px; }

@media (max-width: 980px) {
  .comp-lsvshq76,
  .comp-lsvshq77,
  .comp-j6w6mgwv,
  .comp-j6w6mgxz,
  .comp-lsvshq6v,
  .comp-j6w7y3v6 {
    min-width: 0 !important;
  }
  [data-mesh-id="Containerh4hzqinlineContent-gridContainer"] > [id="comp-lsvshq76"],
  [data-mesh-id="Containerh4hzqinlineContent-gridContainer"] > [id="comp-lsvshq77"],
  [data-mesh-id="Containeran825inlineContent-gridContainer"] > [id="comp-lsvshq6v"] {
    margin-left: 0 !important;
  }
  .Ak0vpt { flex-direction: column !important; }
  .FDI5TK { width: 100% !important; }
  #comp-j6w6mgx8, #comp-j6w7y3v8 { width: 100% !important; }
}
"""


def read_html(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def extract_styles(html: str) -> str:
    blocks = re.findall(r"<style[^>]*>(.*?)</style>", html, re.DOTALL | re.IGNORECASE)
    return "\n\n".join(blocks)


def extract_site_container(html: str) -> str:
    match = re.search(
        r'<div id="SITE_CONTAINER">(.*)</div></div>\s*<script id="wix-skip-played-animations">',
        html,
        re.DOTALL,
    )
    if not match:
        raise RuntimeError("SITE_CONTAINER not found")
    return match.group(1)


def fix_content(html: str, *, home_image: str, expertise_image: str | None = None) -> str:
    html = re.sub(
        r'\./Home _ Ray Mitchell_files/a4a096_be34a111cd124345929a6ac0e4bc9512~mv2\.jpeg',
        home_image,
        html,
    )
    html = re.sub(
        r'\./Areas of Expertise _ Ray Mitchell_files/a4a096_44cbc834465b42179c0a29d5403339c2~mv2\.jpeg',
        expertise_image or home_image,
        html,
    )
    html = re.sub(
        r'<div id="pinnedBottomRight"[^>]*>.*?</div></div>\s*<footer',
        "<footer",
        html,
        flags=re.DOTALL,
    )
    # Allow Wix motion JS to run the float-in on load
    html = html.replace('data-motion-enter="done"', "")
    return html


def fix_nav(html: str, *, active: str) -> str:
    """Set hard nav links and active page state."""
    html = re.sub(r'\saria-current="page"', "", html)

    html = re.sub(
        r'(<div class="comp-j6htcuyf[^"]*" id="comp-j6htcuyf"[^>]*>.*?href=")[^"]*(")',
        r'\1/\2',
        html,
        flags=re.DOTALL,
        count=1,
    )

    html = re.sub(
        r'(<li id="comp-j6htgi840"[^>]*>.*?<a data-testid="linkElement"[^>]*href=")[^"]*(")',
        r'\1/\2',
        html,
        flags=re.DOTALL,
        count=1,
    )
    html = re.sub(
        r'(<li id="comp-j6htgi841"[^>]*>.*?<a data-testid="linkElement"[^>]*href=")[^"]*(")',
        r'\1/#services\2',
        html,
        flags=re.DOTALL,
        count=1,
    )
    html = re.sub(
        r'(<li id="comp-j6htgi842"[^>]*>.*?<a data-testid="linkElement"[^>]*href=")[^"]*(")',
        r'\1/areas-of-expertise/\2',
        html,
        flags=re.DOTALL,
        count=1,
    )

    if active == "home":
        html = re.sub(
            r'(<li id="comp-j6htgi840"[^>]*>.*?<a data-testid="linkElement" href="/")',
            r'\1 aria-current="page"',
            html,
            flags=re.DOTALL,
            count=1,
        )
    elif active == "expertise":
        html = re.sub(
            r'(<li id="comp-j6htgi842"[^>]*>.*?<a data-testid="linkElement" href="/areas-of-expertise/")',
            r'\1 aria-current="page"',
            html,
            flags=re.DOTALL,
            count=1,
        )

    return html


def page_shell(*, title: str, description: str, canonical: str, body: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:title" content="{title}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:type" content="website">
  <link rel="stylesheet" href="/styles/site.css">
  <link rel="stylesheet" href="/styles/chat-widget.css">
</head>
<body class="site-body">
<div id="SITE_CONTAINER">
{body}
</div>
<div id="chat-widget-root"></div>
<script type="module" src="/src/main.ts"></script>
</body>
</html>
"""


def rewrite_font_urls(css: str) -> str:
    css = re.sub(r"url\('//static\.parastorage\.com([^']+)'\)", r"url('/fonts\1')", css)
    css = re.sub(r'url\("//static\.parastorage\.com([^"]+)"\)', r"url('/fonts\1')", css)
    css = re.sub(
        r"url\('/fonts/fonts/v2/eca8b0cd-45d8-43cf-aee7-ca462bc5497c/v1/din-next-w[^']+'\)",
        "url('/fonts/din-next-w01-light.woff2')",
        css,
    )
    css = re.sub(
        r"url\('/fonts/fonts/v2/8e5b5cbc-6ad9-49f7-aee7-4e5133c3ee4d/v1/futura-lt-w[^']+'\)",
        "url('/fonts/futura-lt-w01-light.woff2')",
        css,
    )
    css = re.sub(
        r"url\('/fonts/fonts/v2/d18d0657-b3bd-4cd5-acd7-eab24ec6b49e/v1/bree-w[^']+'\)",
        "url('/fonts/bree-w01-thin-oblique.woff2')",
        css,
    )
    return css


def download_fonts() -> None:
    FONTS_DIR.mkdir(parents=True, exist_ok=True)
    names = [
        "din-next-w01-light.woff2",
        "futura-lt-w01-light.woff2",
        "bree-w01-thin-oblique.woff2",
    ]
    for url, name in zip(FONT_URLS, names):
        dest = FONTS_DIR / name
        if dest.exists() and dest.stat().st_size > 1000:
            continue
        print(f"Downloading {name}...")
        urllib.request.urlretrieve(url, dest)


def main() -> None:
    home_html = read_html(HOME_HTML)
    exp_html = read_html(EXP_HTML)

    download_fonts()

    css = extract_styles(home_html) + "\n\n" + extract_styles(exp_html)
    css = re.sub(r"/\*# sourceMappingURL=[^*]+\*/", "", css)
    css = rewrite_font_urls(css) + STATIC_OVERRIDES
    OUT_CSS.parent.mkdir(parents=True, exist_ok=True)
    OUT_CSS.write_text(css, encoding="utf-8")
    print(f"Wrote {OUT_CSS} ({len(css)} bytes)")

    home_body = fix_content(
        extract_site_container(home_html),
        home_image="/assets/images/home-hero.jpeg",
    )
    home_body = fix_nav(home_body, active="home")
    home_page = page_shell(
        title="Ray Mitchell | Psychotherapist",
        description="Ray Mitchell, MSc MBACP — integrative talk therapy, organisational wellbeing, and psychotherapy in Manchester.",
        canonical="https://www.raymitchell.co.uk/",
        body=home_body,
    )
    OUT_HOME.write_text(home_page, encoding="utf-8")
    print(f"Wrote {OUT_HOME} ({len(home_page)} bytes)")

    exp_body = fix_content(
        extract_site_container(exp_html),
        home_image="/assets/images/home-hero.jpeg",
        expertise_image="/assets/images/expertise-hero.jpeg",
    )
    exp_body = fix_nav(exp_body, active="expertise")
    exp_page = page_shell(
        title="Areas of Expertise | Ray Mitchell",
        description="Ray Mitchell's areas of expertise — integrative psychotherapy, educational background, and group wellbeing sessions.",
        canonical="https://www.raymitchell.co.uk/areas-of-expertise/",
        body=exp_body,
    )
    OUT_EXPERTISE.parent.mkdir(parents=True, exist_ok=True)
    OUT_EXPERTISE.write_text(exp_page, encoding="utf-8")
    print(f"Wrote {OUT_EXPERTISE} ({len(exp_page)} bytes)")


if __name__ == "__main__":
    main()
