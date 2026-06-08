import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import io
from PIL import Image

waves  = [1, 2, 3, 4, 5]
labels = ["W1\nMay–Jun", "W2\nJun–Jul", "W3\nJuly", "W4\nAugust", "W5\nSep–Oct"]

# Concern about polarization (% who cite it as biggest concern)
concern_treat   = [0.05, 0.05, 0.10, 0.13, 0.13]
concern_control = [0.05, 0.05, 0.05, 0.05, 0.05]

COLOR_TREAT   = "#BB2222"
COLOR_CONTROL = "#888888"

def make_frame(n_waves):
    fig, ax = plt.subplots(figsize=(9, 4.5), facecolor='white')
    fig.subplots_adjust(left=0.10, right=0.72, top=0.85, bottom=0.18)

    wx = waves[:n_waves]
    ct = concern_treat[:n_waves]
    cc = concern_control[:n_waves]

    # Shade treatment period (W3+)
    if n_waves >= 3:
        ax.axvspan(2.5, 5.5, alpha=0.06, color="#0000CD", zorder=0)
        ax.axvline(2.5, color="#0000CD", lw=1, linestyle=':', alpha=0.5)
        ax.text(3.75, 0.148, "Treatment period", ha='center', va='top',
                fontsize=8, color='#0000CD', alpha=0.7, style='italic')

    ax.plot(wx, ct, color=COLOR_TREAT, lw=2.8, marker='o',
            markersize=9, zorder=3, label="Treatment")
    ax.plot(wx, cc, color=COLOR_CONTROL, lw=2.8, marker='s',
            markersize=9, zorder=3, label="Control", linestyle='--')

    # Value labels
    for i, (x, y) in enumerate(zip(wx, ct)):
        ax.annotate(f"{y:.0%}", xy=(x, y), xytext=(8, 4),
                    textcoords='offset points',
                    color=COLOR_TREAT, fontsize=10, fontweight='bold')
    for i, (x, y) in enumerate(zip(wx, cc)):
        ax.annotate(f"{y:.0%}", xy=(x, y), xytext=(8, -14),
                    textcoords='offset points',
                    color=COLOR_CONTROL, fontsize=10)

    # Difference annotation at W3+
    if n_waves >= 3:
        for i in range(2, n_waves):
            diff = concern_treat[i] - concern_control[i]
            ax.annotate(f"+{diff:.0%}", xy=(waves[i], (concern_treat[i]+concern_control[i])/2),
                        xytext=(18, 0), textcoords='offset points',
                        color='#0000CD', fontsize=9, fontweight='bold',
                        arrowprops=dict(arrowstyle='-', color='#0000CD', lw=0.8))

    ax.set_xlim(0.5, 5.5)
    ax.set_ylim(0.0, 0.20)
    ax.set_xticks(waves)
    ax.set_xticklabels(labels, fontsize=10)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{y:.0%}"))
    ax.tick_params(axis='y', labelsize=10)
    ax.spines[['top','right']].set_visible(False)
    ax.grid(axis='y', alpha=0.3, lw=0.8)
    ax.set_ylabel("Share of respondents", fontsize=10)

    # Legend
    handles = [
        plt.Line2D([0],[0], color=COLOR_TREAT,   lw=2.5, marker='o', label="Treatment"),
        plt.Line2D([0],[0], color=COLOR_CONTROL, lw=2.5, marker='s',
                   linestyle='--', label="Control"),
    ]
    ax.legend(handles=handles, fontsize=10, frameon=False, loc='upper left')

    ax.set_title("Expected Results — Concern about Polarization\n(Simulated data)",
                 fontsize=12, fontweight='bold', color='#0000CD', pad=10)

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

out = "/Users/Mello/Dropbox/publications/aware/fig_expectations.gif"
frames[0].save(out, save_all=True, append_images=frames[1:],
               duration=durations, loop=4, optimize=True)
print(f"Saved {out}")
