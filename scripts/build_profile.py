#!/usr/bin/env python3
"""Generate a bilingual GitHub profile and self-contained SVG assets.

Python 3.10+, standard library only. No network access or credentials required.
"""
import argparse
import html
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
THEMES = {
    "dark": {"bg": "#0d141c", "panel": "#12232e", "text": "#f1f6fa", "muted": "#93aab9", "accent": "#6ce5dd", "line": "#2a4554", "soft": "#1b3840"},
    "light": {"bg": "#f1f6f7", "panel": "#e2edf0", "text": "#172d3b", "muted": "#516878", "accent": "#006d73", "line": "#bacfd5", "soft": "#cce6e5"},
}
PATHS = {
    "vision": '<path d="M3 16s5-9 13-9 13 9 13 9-5 9-13 9S3 16 3 16Z"/><circle cx="16" cy="16" r="4"/>',
    "model": '<path d="M7 8 25 10 17 25 7 8M7 8l-2 16 12 1M25 10l3 15-11 0"/><circle cx="7" cy="8" r="3"/><circle cx="25" cy="10" r="3"/><circle cx="17" cy="25" r="3"/>',
    "delivery": '<rect x="3" y="4" width="9" height="9" rx="2"/><rect x="20" y="19" width="9" height="9" rx="2"/><path d="M12 8h9a4 4 0 0 1 4 4v7M3 24h11m-4-4 4 4-4 4"/>',
    "evaluation": '<path d="M5 3v25h24M10 21v-6m7 6V9m7 12V5"/><path d="m9 7 3 3 6-6"/>',
    "data": '<path d="m3 10 13-7 13 7-13 7-13-7Zm0 7 13 7 13-7M3 24l13 7 13-7"/>',
    "branch": '<circle cx="8" cy="5" r="3"/><circle cx="8" cy="27" r="3"/><circle cx="24" cy="6" r="3"/><path d="M8 8v16M24 9c0 12-16 5-16 15"/>',
}


def esc(value):
    return html.escape(str(value), quote=True)


def svg_icon(kind, color):
    return f'<g fill="none" stroke="{color}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{PATHS[kind]}</g>'


def hero(locale, copy, theme, mobile=False):
    p = THEMES[theme]
    width, height = (760, 510) if mobile else (1200, 430)
    lines = []
    for x in range(24, width, 44):
        lines.append(f'<path d="M{x} 0V{height}"/>')
    for y in range(24, height, 44):
        lines.append(f'<path d="M0 {y}H{width}"/>')
    grid = f'<g stroke="{p["line"]}" stroke-width=".7" opacity=".22">{"".join(lines)}</g>'
    x, y, scale = (555, 190, .68) if mobile else (970, 210, .88)
    def cube(cx, cy, radius, depth):
        top = f"{cx},{cy-radius/2} {cx+radius},{cy} {cx},{cy+radius/2} {cx-radius},{cy}"
        left = f"{cx-radius},{cy} {cx},{cy+radius/2} {cx},{cy+radius/2+depth} {cx-radius},{cy+depth}"
        right = f"{cx},{cy+radius/2} {cx+radius},{cy} {cx+radius},{cy+depth} {cx},{cy+radius/2+depth}"
        return f'<polygon points="{left}" fill="url(#side)"/><polygon points="{right}" fill="{p["soft"]}"/><polygon points="{top}" fill="url(#top)"/><g fill="none" stroke="{p["accent"]}" stroke-opacity=".65" stroke-width="1.2"><polygon points="{top}"/><path d="M{cx-radius} {cy}v{depth}l{radius} {radius/2} {radius} {-radius/2}v{-depth}M{cx} {cy+radius/2}v{depth}"/></g>'
    cubes = cube(0, 40, 134, 22) + cube(0, -5, 104, 25) + cube(0, -67, 59, 75)
    cubes += cube(-112, -80, 24, 29) + cube(110, -20, 22, 30) + cube(82, 88, 17, 19)
    diagram = f'''<defs>
      <linearGradient id="top" x2="1" y2="1"><stop stop-color="{p['accent']}" stop-opacity=".85"/><stop offset="1" stop-color="{p['panel']}"/></linearGradient>
      <linearGradient id="side" x2="1" y2="1"><stop stop-color="{p['panel']}"/><stop offset="1" stop-color="{p['bg']}"/></linearGradient>
      <radialGradient id="halo"><stop stop-color="{p['accent']}" stop-opacity=".18"/><stop offset="1" stop-color="{p['bg']}" stop-opacity="0"/></radialGradient>
      </defs><g transform="translate({x} {y}) scale({scale})">
      <circle r="195" fill="url(#halo)"/>
      <ellipse cy="117" rx="154" ry="33" fill="{p['bg']}" opacity=".6"/>
      <ellipse rx="180" ry="76" fill="none" stroke="{p['line']}" transform="rotate(-28)"/>
      <ellipse rx="179" ry="76" fill="none" stroke="{p['accent']}" stroke-opacity=".35" stroke-dasharray="3 9" transform="rotate(28)"/>
      {cubes}
      <path d="M-112-50v26l53 27M110 10v21l-46 25" fill="none" stroke="{p['accent']}" stroke-width="2"/>
      <g transform="translate(-16 -92)">{svg_icon('model',p['text'])}</g>
      <circle cx="-166" cy="-53" r="5" fill="{p['accent']}"/>
      <circle cx="163" cy="61" r="4" fill="{p['accent']}"/>
    </g>'''
    if mobile:
        title = f'<text x="38" y="168" font-size="62" font-weight="700">{esc(copy["mobile_hero"][0])}</text><text x="38" y="240" font-size="62" font-weight="700">{esc(copy["mobile_hero"][1])}</text><text x="40" y="303" font-size="27" fill="{p["accent"]}">{esc(copy["hero"][1])}</text>'
        eyebrow_y, footer_y = 59, 450
        footer = f'<text x="40" y="{footer_y}" font-family="monospace" font-size="17" fill="{p["muted"]}">{esc(copy["hero_footer"])}</text>'
        rule = f'<path d="M40 390H720" stroke="{p["line"]}"/>'
    else:
        size = 55 if locale == "en" else 51
        title = f'<text x="52" y="178" font-size="{size}" font-weight="700">{esc(copy["hero"][0])}</text><text x="52" y="246" font-size="{size}" font-weight="700" fill="{p["accent"]}">{esc(copy["hero"][1])}</text>'
        eyebrow_y, footer_y = 69, 367
        footer = f'<text x="52" y="{footer_y}" font-family="monospace" font-size="14" letter-spacing="1.6" fill="{p["muted"]}">{esc(copy["hero_footer"])}</text><text x="1128" y="367" text-anchor="end" font-family="monospace" font-size="12" fill="{p["muted"]}">VISION / MODELS / SYSTEMS</text>'
        rule = f'<path d="M52 324H1148" stroke="{p["line"]}"/>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">Ruham Pires — {esc(copy['position'])}</title><desc id="desc">{esc(' '.join(copy['hero']))} Original isometric 3D illustration of an AI computing core and connected systems.</desc>
<rect width="{width}" height="{height}" rx="16" fill="{p['bg']}"/>{grid}{diagram}<g font-family="Arial, Helvetica, sans-serif" fill="{p['text']}"><text x="{40 if mobile else 52}" y="{eyebrow_y}" font-size="{20 if mobile else 17}" letter-spacing="3" fill="{p['muted']}">RUHAM PIRES / DATA &amp; AI</text>{title}{footer}</g>{rule}
<rect x=".5" y=".5" width="{width-1}" height="{height-1}" rx="16" fill="none" stroke="{p['line']}"/></svg>\n'''


def icon_file(kind):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">{svg_icon(kind,"#198d96")}</svg>\n'


def badge(text, kind, theme):
    p = THEMES[theme]
    width = 58 + len(text) * 8
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="36" viewBox="0 0 {width} 36"><rect x=".5" y=".5" width="{width-1}" height="35" rx="8" fill="{p["panel"]}" stroke="{p["line"]}"/><g transform="translate(9 8) scale(.6)">{svg_icon(kind,p["accent"])}</g><text x="36" y="23" fill="{p["text"]}" font-family="Arial,Helvetica,sans-serif" font-size="13">{esc(text)}</text></svg>\n'


def picture(locale, alt):
    return f'''<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="assets/hero-{locale}-dark-mobile.svg">
  <source media="(max-width: 600px) and (prefers-color-scheme: light)" srcset="assets/hero-{locale}-light-mobile.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/hero-{locale}-dark.svg">
  <img src="assets/hero-{locale}-light.svg" alt="{esc(alt)}" width="1200">
</picture>'''


def markdown(data, locale):
    c = data['locales'][locale]
    other = 'README.pt-BR.md' if locale == 'en' else 'README.md'
    language = f'English · [Português]({other})' if locale == 'en' else f'[English]({other}) · Português'
    nav = ' &nbsp; / &nbsp; '.join(f'<a href="#{a}">{esc(t)}</a>' for t, a in zip(c['navigation'], c['nav_anchors']))
    out = ['<!-- Generated by scripts/build_profile.py. Edit profile.json. -->', picture(locale, ' '.join(c['hero'])), '', f'# {data["name"]}', '', f'**{c["position"]}**', '', language, '', f'<p>{nav}</p>', '', c['intro'], '', c['intro2'], '']
    if data['selected_projects']:
        out += [f'## {c["projects_title"]}', '']
        current_group = None
        for project in data['selected_projects']:
            group = project.get('group')
            if group != current_group:
                current_group = group
                out += [f'### {data["project_groups"][group][locale]}', '']
            title = f'[{project["name"]}]({project["url"]})' if project.get('url') else project['name']
            out += [f'**{title}**', '']
            if project['summary'][locale]:
                out += [project['summary'][locale], '']
    out += [f'## {c["focus_title"]}', '']
    for a in c['areas']:
        out += [f'### <img src="assets/icons/{a["icon"]}.svg" width="22" height="22" alt=""> {a["title"]}', '', a['text'], '']
    out += [f'**{c["stack_title"]}**', '', '<p>']
    for i, label in enumerate(c['stack']):
        out += [f'<picture><source media="(prefers-color-scheme: dark)" srcset="assets/badge-{locale}-{i}-dark.svg"><img src="assets/badge-{locale}-{i}-light.svg" height="36" alt="{esc(label)}"></picture>']
    out += ['</p>', '', ' · '.join(c['stack']), '']
    out += [c['stack_context'], '', f'### {c["technology_title"]}', '', f'| {c["category_label"]} | {c["technology_label"]} |', '| --- | --- |']
    for category, technologies in c['technology_groups']:
        out += [f'| {category} | {technologies} |']
    out += ['']
    out += [f'## {c["notes_title"]}', '', c['notes_intro'], '']
    for n in c['notes']:
        out += [f'### <img src="assets/icons/{n["icon"]}.svg" width="22" height="22" alt=""> {n["title"]}', '', f'`{n["label"]}`', '', n['text'], '', f'[{n["cta"]} →]({n["path"]})', '']
    out += [f'## {c["approach_title"]}', '']
    for title, text in c['principles']:
        out += [f'- **{title}** {text}']
    out += ['', f'## {c["background_title"]}', '', c['background'], '', c['closing'], '']
    if data['contact']:
        out += [f'## {c["contact_title"]}', '', ' · '.join(f'[{x["label"]}]({x["url"]})' for x in data['contact']), '']
    out += ['---', '', f'<sub>{c["footer"]}</sub>', '']
    return '\n'.join(out)


def validate(data):
    if data.get('name') != 'Ruham Pires':
        raise ValueError('Unexpected profile identity; review name deliberately.')
    username = data.get('github_username')
    if username is not None and not re.fullmatch(r'[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?', username):
        raise ValueError('Invalid GitHub username.')
    for item in data['contact'] + data['selected_projects']:
        if not item.get('url'):
            continue
        parsed = urlparse(item['url'])
        if parsed.scheme not in ('https', 'mailto'):
            raise ValueError('Links must use https or mailto.')
        if parsed.scheme == 'https' and not parsed.netloc:
            raise ValueError('HTTPS link is missing a host.')
        if any(x in item['url'].lower() for x in ('your_username', 'example.com', 'placeholder')):
            raise ValueError('Unresolved placeholder URL.')
    if set(data['locales']) != {'en', 'pt-BR'}:
        raise ValueError('English and Brazilian Portuguese are required.')
    for c in data['locales'].values():
        assert len(c['areas']) == 3 and len(c['stack']) == len(c['stack_icons'])
        assert len(c['navigation']) == len(c['nav_anchors'])
        for note in c['notes']:
            if not (ROOT / note['path']).is_file():
                raise ValueError(f'Missing note: {note["path"]}')


def outputs(data):
    result = {}
    for locale, copy in data['locales'].items():
        filename = 'README.md' if locale == 'en' else 'README.pt-BR.md'
        result[filename] = markdown(data, locale)
        for theme in THEMES:
            result[f'assets/hero-{locale}-{theme}.svg'] = hero(locale, copy, theme)
            result[f'assets/hero-{locale}-{theme}-mobile.svg'] = hero(locale, copy, theme, True)
            for i, label in enumerate(copy['stack']):
                result[f'assets/badge-{locale}-{i}-{theme}.svg'] = badge(label, copy['stack_icons'][i], theme)
    for kind in PATHS:
        result[f'assets/icons/{kind}.svg'] = icon_file(kind)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true', help='Fail if generated files are out of date.')
    args = parser.parse_args()
    data = json.loads((ROOT / 'profile.json').read_text(encoding='utf-8'))
    validate(data)
    stale = []
    result = outputs(data)
    for name, content in result.items():
        path = ROOT / name
        if args.check:
            if not path.is_file() or path.read_text(encoding='utf-8') != content:
                stale.append(name)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding='utf-8')
    if stale:
        print('Regenerate the profile: python3 scripts/build_profile.py\n' + '\n'.join(stale), file=sys.stderr)
        return 1
    print(f'{"Verified" if args.check else "Generated"} {len(result)} profile files.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
