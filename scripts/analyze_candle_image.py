from PIL import Image
from collections import Counter
import json
import os

img_path = os.path.join('data', 'model de bougies.webp')
if not os.path.exists(img_path):
    raise FileNotFoundError(img_path)

img = Image.open(img_path).convert('RGBA')
# Resize to speed up
img_small = img.resize((300, 300))

# Remove transparent pixels
pixels = [p for p in img_small.getdata() if p[3] > 20]

# Convert to RGB and count
rgb_pixels = [(p[0], p[1], p[2]) for p in pixels]

# Quantize colors using Pillow's convert
quant = img_small.convert('P', palette=Image.ADAPTIVE, colors=12)
palette = quant.getpalette()
color_counts = sorted(quant.getcolors(), reverse=True)

colors = []
for count, idx in color_counts:
    r = palette[idx*3]
    g = palette[idx*3+1]
    b = palette[idx*3+2]
    hexc = '#%02x%02x%02x' % (r, g, b)
    colors.append({'hex': hexc, 'count': count, 'percent': round(100.0 * count / len(pixels), 2)})

# helper to compute luminance
def luminance(rgb):
    r, g, b = rgb
    return 0.2126*r + 0.7152*g + 0.0722*b

# identify likely green and red (by hue approximation)
def is_green(r,g,b):
    return g > r and g > b and g > 100 and r < 150

def is_red(r,g,b):
    return r > g and r > b and r > 100 and g < 120

green_candidates = [c for c in colors if is_green(int(c['hex'][1:3],16), int(c['hex'][3:5],16), int(c['hex'][5:7],16))]
red_candidates = [c for c in colors if is_red(int(c['hex'][1:3],16), int(c['hex'][3:5],16), int(c['hex'][5:7],16))]

bg = colors[0]['hex'] if len(colors) else '#000000'

result = {
    'palette': colors,
    'green_candidates': green_candidates,
    'red_candidates': red_candidates,
    'background': bg,
    'suggested_style': {
        'body_up': green_candidates[0]['hex'] if green_candidates else '#26a69a',
        'body_down': red_candidates[0]['hex'] if red_candidates else '#ef5350',
        'wick': '#222222',
        'body_opacity': 1.0,
        'wick_width': 1.5,
        'body_line_width': 2,
        'candle_gap': 0.2
    }
}

print(json.dumps(result, indent=2, ensure_ascii=False))
