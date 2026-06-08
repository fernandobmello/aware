import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import io
from PIL import Image

# ── Simulated data ──────────────────────────────────────────────────────────
waves = [1, 2, 3, 4, 5]
labels = ["W1\nMay–Jun", "W2\nJun–Jul", "W3\nJul–Aug", "W4\nAug–Sep", "W5\nSep–Oct"]

# Concerns about polarization — stable for both groups (slight noise)
concern_treat   = [0.42, 0.43, 0.44, 0.43, 0.44]
concern_control = [0.42, 0.42, 0.41, 0.42, 0.42]

# Behavioral engagement — treatment rises W3 onwards, control flat
behav_treat   = [0.08, 0.08, 0.14, 0.19, 0.19]
behav_control = [0.08, 0.08, 0.08, 0.08, 0.08]

COLOR_TREAT   = "#0000CD"
COLOR_CONTROL = "#888888"
WAVE_COLORS   = ["#CCCCCC", "#CCCCCC", "#BB2222", "#BB2222", "#BB2222"]  # W3+ = treatment active

def make_frame(n_waves):
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), facecolor='white')
    fig.subplots_adjust(left=0.07, right=0.97, top=0.82, bottom=0.18, wspace=0.38)

    for ax, title, treat, control, ylim, fmt in [
        (axes[0], "Concern about Polarization",
         concern_treat, concern_control, (0.25, 0.65), lambda y: f"{y:.0%}"),
        (axes[1], "Behavioral Engagement\n(Seminar enrollment / Manual download)",
         behav_treat, behav_control, (0.0, 0.28), lambda y: f"{y:.0%}"),
    ]:
        wx = waves[:n_waves]
        ax.plot(wx, treat[:n_waves],   color=COLOR_TREAT,   lw=2.8, marker='o',
                markersize=8, zorder=3, label="Treatment")
        ax.plot(wx, control[:n_waves], color=COLOR_CONTROL, lw=2.8, marker='s',
                markersize=8, zorder=3, label="Control", linestyle='--')

        # Shade treatment period (W3+)
        if n_waves >= 3:
            ax.axvspan(2.5, 5.5, alpha=0.06, color="#0000CD", zorder=0)
            ax.axvline(2.5, color="#0000CD", lw=1, linestyle=':', alpha=0.5)

        # Value labels on last point
        if n_waves >= 1:
            ax.annotate(f"{treat[n_waves-1]:.0%}",
                        xy=(wx[-1], treat[n_waves-1]),
                        xytext=(6, 4), textcoords='offset points',
                        color=COLOR_TREAT, fontsize=9, fontweight='bold')
            ax.annotate(f"{control[n_waves-1]:.0%}",
                        xy=(wx[-1], control[n_waves-1]),
                        xytext=(6, -12), textcoords='offset points',
                        color=COLOR_CONTROL, fontsize=9)

        ax.set_xlim(0.5, 5.5)
        ax.set_ylim(ylim)
        ax.set_xticks(waves)
        ax.set_xticklabels(labels, fontsize=8.5)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{y:.0%}"))
        ax.set_title(title, fontsize=11, fontweight='bold', pad=10, color='#222222')
        ax.spines[['top','right']].set_visible(False)
        ax.tick_params(axis='y', labelsize=8.5)
        ax.grid(axis='y', alpha=0.3, lw=0.8)

        if n_waves >= 3:
            ax.text(3.0, ylim[1]*0.97, "← Treatment waves →",
                    ha='center', va='top', fontsize=7.5,
                    color='#0000CD', alpha=0.7, style='italic')

    # Shared legend
    handles = [
        mpatches.Patch(color=COLOR_TREAT,   label="Treatment group"),
        mpatches.Patch(color=COLOR_CONTROL, label="Control group"),
    ]
    fig.legend(handles=handles, loc='upper center', ncol=2,
               fontsize=9.5, frameon=False,
               bbox_to_anchor=(0.52, 0.99))

    fig.suptitle("Expected Results — Simulated Data",
                 fontsize=13, fontweight='bold', color='#0000CD', y=1.01)

    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=130, bbox_inches='tight', facecolor='white')
    buf.seek(0)
    img = Image.open(buf).copy()
    plt.close(fig)
    return img

frames = []
durations = []

# One frame per wave reveal
for n in range(1, 6):
    frames.append(make_frame(n))
    durations.append(1800 if n < 5 else 4000)

out = "/Users/Mello/Dropbox/publications/aware/fig_expectations.gif"
frames[0].save(out, save_all=True, append_images=frames[1:],
               duration=durations, loop=4, optimize=True)
print(f"Saved {out}")
