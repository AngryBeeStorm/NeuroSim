import matplotlib.pyplot as plt
import streamlit as st


DARK_PALETTE = {
    "figure_bg": "#111827",
    "panel_color": "#182235",
    "axis_face": "#182235",
    "text_color": "#e5edf7",
    "muted_color": "#8fa3bb",
    "grid_color": "#52647d",
    "spine_color": "#40516a",
    "target": "#55d6be",
    "stimulation": "#ffbd59",
    "response": "#ff6b9d",
}

LIGHT_PALETTE = {
    "figure_bg": "#ffffff",
    "panel_color": "#eef4f8",
    "axis_face": "#ffffff",
    "text_color": "#102b45",
    "muted_color": "#475569",
    "grid_color": "#94a3b8",
    "spine_color": "#64748b",
    "target": "#0d9488",
    "stimulation": "#b45309",
    "response": "#be185d",
}


def get_plot_palette():
    """Return a single palette shared by user-facing plots.

    Streamlit theme selection is read centrally here so every user-facing
    plot can shadow the same colors without duplicating style logic.
    """
    try:
        base = st.get_option("theme.base")
    except Exception:
        base = "dark"

    return LIGHT_PALETTE if base == "light" else DARK_PALETTE


def apply_plot_theme(fig, palette):
    fig.patch.set_facecolor(palette["figure_bg"])


def apply_axis_theme(axis, palette):
    axis.set_facecolor(palette["axis_face"])
    axis.tick_params(colors=palette["muted_color"], labelsize=9)
    axis.grid(
        axis="x",
        color=palette["grid_color"],
        alpha=0.3,
        linestyle="--",
        linewidth=0.7,
    )
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)
    axis.spines["left"].set_color(palette["spine_color"])
    axis.spines["bottom"].set_color(palette["spine_color"])
    axis.xaxis.label.set_color(palette["text_color"])
    axis.yaxis.label.set_color(palette["text_color"])


def plot_best_solution_result(target_spikes, result):
	palette = get_plot_palette()
	fig, axes = plt.subplots(
		3,
		1,
		figsize=(12, 7),
		sharex=True,
	)
	apply_plot_theme(fig, palette)

	fig.subplots_adjust(hspace=0.22, top=0.84, bottom=0.11, left=0.1, right=0.98)

	ax_target = axes[0]
	ax_stim = axes[1]
	ax_response = axes[2]

	for axis in axes:
		apply_axis_theme(axis, palette)

	ax_target.eventplot(
		target_spikes,
		lineoffsets=1,
		linelengths=0.8,
		linewidths=3.5,
		colors=palette["target"],
	)
	ax_target.set_ylabel("TARGET", fontweight="bold", color=palette["target"])
	ax_target.set_yticks([])

	ax_stim.step(
		range(len(result["stimulation"])),
		result["stimulation"],
		where="post",
		linewidth=3,
		color=palette["stimulation"],
	)
	ax_stim.fill_between(
		range(len(result["stimulation"])),
		result["stimulation"],
		step="post",
		color=palette["stimulation"],
		alpha=0.1,
	)
	ax_stim.set_ylabel("INPUT", fontweight="bold", color=palette["stimulation"])

	ax_response.eventplot(
		result["spikes"],
		lineoffsets=1,
		linelengths=0.8,
		linewidths=3.5,
		colors=palette["response"],
	)
	ax_response.set_ylabel("ACTUAL", fontweight="bold", color=palette["response"])
	ax_response.set_yticks([])
	ax_response.set_xlabel("Time (ms)")

	fig.suptitle(
		f"Best Stimulation  |  Fitness: {result['score']:.3f}  |  Generation: {result['generation']}",
		color=palette["text_color"],
		fontsize=16,
		fontweight="bold",
		x=0.1,
		ha="left",
	)

	return fig


def draw_target_timeline(spikes, stimulation_length=500):
    palette = get_plot_palette()
    fig, ax = plt.subplots(figsize=(10, 2))
    apply_plot_theme(fig, palette)
    apply_axis_theme(ax, palette)

    ax.set_xlim(0, stimulation_length)
    ax.set_ylim(0, 1)

    ax.axhline(0.5, linewidth=1, color=palette["text_color"])

    for spike in spikes:
        ax.vlines(
            spike,
            0.25,
            0.75,
            linewidth=3,
            colors=palette["target"],
        )

    ax.set_xlabel("Time (ms)", color=palette["text_color"])
    ax.set_yticks([])
    ax.set_title("Desired Neural Response", color=palette["text_color"])

    return fig

