from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import subprocess

tpl_dir = Path(__file__).parent / "templates"
env = Environment(loader=FileSystemLoader(str(tpl_dir)))


def mjml_to_html(mjml_str: str) -> str:
    # Uses Node MJML CLI (installed either in container or dev-tools)
    p = subprocess.run(["mjml", "-s"], input=mjml_str.encode(), capture_output=True, check=True)
    return p.stdout.decode()


def render_issue(sections: dict, subject: str, preface: str | None = None) -> tuple[str, str]:
    tpl = env.get_template("newsletter.mjml")
    mjml = tpl.render(
        subject=subject,
        preface=preface or "",
        sections=sections,
        brand={"name": "Brand", "color": "#000", "tagline": ""},
    )
    html = mjml_to_html(mjml)
    # plaintext
    lines = [subject, ""]
    for cat in ("policy", "tech", "experiences", "tips"):
        items = sections.get(cat, [])
        if items:
            lines.append(cat.upper())
            for it in items:
                lines.append(f"- {it['title']}: {it['blurb']}")
            lines.append("")
    plaintext = "\n".join(lines)
    return html, plaintext
