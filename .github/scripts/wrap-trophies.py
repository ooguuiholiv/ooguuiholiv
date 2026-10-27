"""Rearrange the one-row trophy SVG into rows of COLUMNS panels, so GitHub does not shrink it."""
import re
import sys

COLUMNS = 5
STEP = 125  # panel size (115) + margin (10), as rendered by github-profile-trophy

path = sys.argv[1]
svg = open(path).read()
# Trophy panels are the only nested <svg> elements sized 115x115, in display order.
panel = re.compile(r'(<svg\s+)x="\d+"(\s+)y="\d+"(\s+width="115"\s+height="115")')

count = 0


def move(match):
    global count
    index = count
    count += 1
    x, y = (index % COLUMNS) * STEP, (index // COLUMNS) * STEP
    return f'{match.group(1)}x="{x}"{match.group(2)}y="{y}"{match.group(3)}'


svg = panel.sub(move, svg)
rows = -(-count // COLUMNS)
width = min(count, COLUMNS) * STEP - 10
height = rows * STEP - 10
svg = re.sub(
    r'<svg\s+width="\d+"\s+height="\d+"\s+viewBox="0 0 \d+ \d+"',
    f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}"',
    svg,
    count=1,
)
open(path, 'w').write(svg)
print(f'{count} trophies in {rows} rows: {width}x{height}')
