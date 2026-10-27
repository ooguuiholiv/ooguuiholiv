"""Build the profile README from public GitHub data (Python standard library)."""
import html
import json
import os
from pathlib import Path
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[2]
USERNAME = "ooguuiholiv"


def fetch(path):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "profile-sync"}
    if os.environ.get("GH_TOKEN"):
        headers["Authorization"] = f"Bearer {os.environ['GH_TOKEN']}"
    with urlopen(Request(f"https://api.github.com/{path}", headers=headers), timeout=30) as response:
        return json.load(response)


def escape(value):
    return html.escape(value or "", quote=True)


def card(filename, fallback, alt):
    source = f"./profile/{filename}.svg" if (ROOT / "profile" / f"{filename}.svg").exists() else fallback
    return f'<img src="{escape(source)}" alt="{escape(alt)}" />'


def main():
    user = fetch(f"users/{USERNAME}")
    repos = []
    page = 1
    while True:
        batch = fetch(f"users/{USERNAME}/repos?per_page=100&sort=updated&page={page}")
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    projects = sorted(
        (repo for repo in repos if not repo["archived"] and repo["name"].lower() != USERNAME),
        key=lambda repo: (repo["fork"], -repo["stargazers_count"], repo["name"].lower()),
    )[:6]
    lines = [
        f'<h1 align="center">Olá! 👋 Eu sou {escape(user["name"] or USERNAME)}</h1>',
        f'<p align="center">{escape(user["bio"])}</p>',
        '',
        f'<p align="center"><a href="https://github.com/{USERNAME}">',
        f'<img src="https://img.shields.io/github/followers/{USERNAME}?label=Seguidores&amp;style=flat" alt="Seguidores no GitHub" /></a>',
        f'<img src="https://komarev.com/ghpvc/?username={USERNAME}&amp;label=Visitas&amp;color=0e75b6" alt="Visitas ao perfil" /></p>',
        '', '## Sobre mim', '',
    ]
    lines.extend((ROOT / '.github/profile-about.md').read_text(encoding='utf-8').strip().splitlines())
    lines.append('')
    if user.get("location"):
        lines.append(f'📍 {escape(user["location"])}')
    lines.extend(['', f'🔗 [GitHub](https://github.com/{USERNAME})'])
    blog = user.get("blog") or ""
    if blog and not urlparse(blog).scheme:
        blog = "https://" + blog
    if urlparse(blog).scheme in ("http", "https"):
        lines.append(f'<p><a href="{escape(blog)}">Meu site / contato</a></p>')
    lines.extend(['', '## Projetos', ''])
    for repo in projects:
        query = urlencode({"username": USERNAME, "repo": repo["name"], "theme": "dark"})
        lines.append(f'<a href="{escape(repo["html_url"])}"><img src="https://github-readme-stats.vercel.app/api/pin/?{escape(query)}" alt="{escape(repo["name"])}" /></a>')
    if not projects:
        lines.append(f'[Veja meus repositórios no GitHub](https://github.com/{USERNAME}?tab=repositories).')
    lines.extend(['', '## Estatísticas do GitHub', '', '<div align="center">'])
    for filename, url, alt in [
        ('stats', f'https://github-readme-stats.vercel.app/api?username={USERNAME}&show_icons=true&include_all_commits=true&theme=dark', 'Estatísticas do GitHub'),
        ('top-langs', f'https://github-readme-stats.vercel.app/api/top-langs/?username={USERNAME}&layout=compact&langs_count=8&theme=dark', 'Linguagens mais usadas'),
        ('streak', f'https://streak-stats.demolab.com/?user={USERNAME}&theme=radical', 'Sequência de contribuições'),
        ('trophy', f'https://github-profile-trophy.vercel.app/?username={USERNAME}&theme=darkhub&column=5', 'Troféus do GitHub'),
    ]:
        lines.extend([card(filename, url, alt), '<br>'])
    lines.extend(['</div>', ''])
    if (ROOT / 'profile/snake.svg').exists():
        lines.extend(['## Contribuições', '', '<picture>', '<source media="(prefers-color-scheme: dark)" srcset="./profile/snake-dark.svg" />', '<img alt="Animação das minhas contribuições" src="./profile/snake.svg" />', '</picture>', ''])
    lines.extend(['---', '', f'Perfil sincronizado automaticamente com [@{USERNAME}](https://github.com/{USERNAME}).', ''])
    (ROOT / 'README.md').write_text('\n'.join(lines), encoding='utf-8')


if __name__ == '__main__':
    main()
