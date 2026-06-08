import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np
import io
from PIL import Image

# Month positions: May=0, Jun=1, Jul=2, Aug=3, Sep=4, Oct=5
months = ["May", "Jun", "Jul", "Aug", "Sep", "Oct"]
month_pos = {m: i for i, m in enumerate(months)}

# Waves: (label, x_start, x_end, description, color)
waves = [
    ("Wave 1", 0.0, 1.0, "Baseline\n(N ≈ 6,000)",          "#0000CD"),
    ("Wave 2", 1.0, 2.0, "No-treatment\ncheck",              "#0000CD"),
    ("Wave 3", 2.0, 2.5, "Video 1\n(no outcome)",            "#1565C0"),
    ("Wave 4", 3.0, 3.5, "Video 2\n+ Outcomes",              "#BB2222"),
    ("Wave 5", 4.0, 5.0, "Decay",                            "#2A8A2A"),
]

# Election marker
election_x = 4.5

def make_frame(n_waves_shown):
    fig, ax = plt.subplots(figsize=(12, 3.8), facecolor='white')
    fig.subplots_adjust(left=0.04, right=0.97, top=0.78, bottom=0.22)

    # Month axis
    for i, m in enumerate(months):
        ax.axvline(i, color='#DDDDDD', lw=1, zorder=0)
        ax.text(i, -0.38, m, ha='center', va='top', fontsize=11,
                color='#555555', fontweight='bold')

    # Campaign period shading
    ax.axvspan(3.0, 5.0, alpha=0.06, color='#BB2222', zorder=0)
    ax.text(4.0, 0.88, "Campaign Period", ha='center', va='center',
            fontsize=8.5, color='#BB2222', alpha=0.7, style='italic')

    # Timeline spine
    ax.axhline(0.5, color='#CCCCCC', lw=2, zorder=1)

    # Draw waves revealed so far
    for i in range(n_waves_shown):
        label, x0, x1, desc, color = waves[i]
        xc = (x0 + x1) / 2

        # Bar
        rect = FancyBboxPatch((x0 + 0.05, 0.30), (x1 - x0) - 0.10, 0.40,
                               boxstyle="round,pad=0.02",
                               facecolor=color, edgecolor='white',
                               linewidth=1.5, zorder=3)
        ax.add_patch(rect)

        # Wave label
        ax.text(xc, 0.52, label, ha='center', va='center',
                fontsize=9.5, fontweight='bold', color='white', zorder=4)

        # Description below
        ax.text(xc, 0.12, desc, ha='center', va='top',
                fontsize=8, color=color, zorder=4, linespacing=1.2,
                fontweight='bold')

        # Dot on spine
        ax.plot(xc, 0.50, 'o', color='white', markersize=6,
                markeredgecolor=color, markeredgewidth=2, zorder=5)

    # Election day marker (always visible from W4 onwards)
    if n_waves_shown >= 4:
        ax.axvline(election_x, color='#BB2222', lw=2, linestyle='--',
                   alpha=0.8, zorder=2)
        ax.text(election_x, 0.92, "Election\nDay", ha='center', va='top',
                fontsize=8, color='#BB2222', fontweight='bold')

    ax.set_xlim(-0.3, 5.3)
    ax.set_ylim(-0.5, 1.05)
    ax.axis('off')

    ax.set_title("Study Timeline — Brazil 2026",
                 fontsize=13, fontweight='bold', color='#0000CD', pad=12)

    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=130, bbox_inches='tight', facecolor='white')
    buf.seek(0)
    img = Image.open(buf).copy()
    plt.close(fig)
    return img

frames = []
durations = []
for n in range(1, 6):
    frames.append(make_frame(n))
    durations.append(1800 if n < 5 else 4000)

out = "/Users/Mello/Dropbox/publications/aware/fig_timeline.gif"
frames[0].save(out, save_all=True, append_images=frames[1:],
               duration=durations, loop=0, optimize=True)

# Strip NETSCAPE loop extension so it plays once and stops
with open(out, 'rb') as f:
    data = bytearray(f.read())
marker = b'\x21\xFF\x0BNETSCAPE2.0'
idx = data.find(marker)
if idx != -1:
    pos = idx + len(marker)
    while pos < len(data) and data[pos] != 0x00:
        pos += 1 + data[pos]
    pos += 1
    del data[idx:pos]
    with open(out, 'wb') as f:
        f.write(bytes(data))

print(f"Saved {out}")
