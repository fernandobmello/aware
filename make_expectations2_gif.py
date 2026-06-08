import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import io
from PIL import Image

waves  = [1, 2, 3, 4, 5]
labels = ["W1\nMay–Jun", "W2\nJun–Jul", "W3\nJuly", "W4\nAugust", "W5\nSep–Oct"]

# Three "other" outcomes — flat with small noise around baseline, both groups similar
outcomes = {
    "Affective Polarization\n(thermometer gap)": {
        "treat":   [0.52, 0.54, 0.51, 0.53, 0.52],
        "control": [0.52, 0.50, 0.53, 0.51, 0.52],
        "ylim":    (0.35, 0.70),
        "baseline": 0.52,
    },
    "Partisan Attitudes\n(compromise index)": {
        "treat":   [0.38, 0.40, 0.37, 0.39, 0.38],
        "control": [0.38, 0.37, 0.39, 0.38, 0.39],
        "ylim":    (0.22, 0.55),
        "baseline": 0.38,
    },
    "Trust in Institutions": {
        "treat":   [0.28, 0.27, 0.29, 0.28, 0.27],
        "control": [0.28, 0.29, 0.27, 0.29, 0.28],
        "ylim":    (0.12, 0.45),
        "baseline": 0.28,
    },
}

COLOR_TREAT   = "#BB2222"
COLOR_CONTROL = "#888888"

def make_frame(n_waves):
    fig, axes = plt.subplots(1, 3, figsize=(12, 4.2), facecolor='white')
    fig.subplots_adjust(left=0.07, right=0.97, top=0.82, bottom=0.18, wspace=0.38)

    for ax, (title, data) in zip(axes, outcomes.items()):
        wx = waves[:n_waves]
        treat   = data["treat"][:n_waves]
        control = data["control"][:n_waves]
        ylim    = data["ylim"]
        base    = data["baseline"]

        # Baseline reference line
        ax.axhline(base, color='#CCCCCC', lw=1.2, linestyle='--', zorder=0, alpha=0.8)

        # Shade treatment period
        if n_waves >= 3:
            ax.axvspan(2.5, 5.5, alpha=0.04, color="#0000CD", zorder=0)
            ax.axvline(2.5, color="#0000CD", lw=1, linestyle=':', alpha=0.4)

        ax.plot(wx, treat,   color=COLOR_TREAT,   lw=2.5, marker='o', markersize=8, zorder=3)
        ax.plot(wx, control, color=COLOR_CONTROL, lw=2.5, marker='s', markersize=8,
                zorder=3, linestyle='--')

        # Value labels on last point
        ax.annotate(f"{treat[-1]:.0%}",  xy=(wx[-1], treat[-1]),
                    xytext=(6, 4),  textcoords='offset points',
                    color=COLOR_TREAT, fontsize=9, fontweight='bold')
        ax.annotate(f"{control[-1]:.0%}", xy=(wx[-1], control[-1]),
                    xytext=(6, -13), textcoords='offset points',
                    color=COLOR_CONTROL, fontsize=9)

        ax.set_xlim(0.5, 5.5)
        ax.set_ylim(ylim)
        ax.set_xticks(waves)
        ax.set_xticklabels(labels, fontsize=8.5)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{y:.0%}"))
        ax.tick_params(axis='y', labelsize=8.5)
        ax.spines[['top','right']].set_visible(False)
        ax.grid(axis='y', alpha=0.3, lw=0.8)
        ax.set_title(title, fontsize=10.5, fontweight='bold', pad=8, color='#222222')

        # "No significant change" label
        if n_waves == 5:
            ax.text(3.0, ylim[1]*0.97, "No significant change",
                    ha='center', va='top', fontsize=7.5,
                    color='#888888', alpha=0.9, style='italic')

    # Shared legend
    handles = [
        plt.Line2D([0],[0], color=COLOR_TREAT,   lw=2.5, marker='o', label="Treatment"),
        plt.Line2D([0],[0], color=COLOR_CONTROL, lw=2.5, marker='s',
                   linestyle='--', label="Control"),
    ]
    fig.legend(handles=handles, loc='upper center', ncol=2,
               fontsize=9.5, frameon=False, bbox_to_anchor=(0.52, 0.99))

    fig.suptitle("Expected Results — Other Outcomes (Placebo Check)\n(Simulated data)",
                 fontsize=12, fontweight='bold', color='#0000CD', y=1.01)

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

out = "/Users/Mello/Dropbox/publications/aware/fig_expectations2.gif"
frames[0].save(out, save_all=True, append_images=frames[1:],
               duration=durations, loop=4, optimize=True)
print(f"Saved {out}")
