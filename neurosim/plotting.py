import matplotlib.pyplot as plt


def plot_best_solution_result(target_spikes, result):
	fig, axes = plt.subplots(
		3,
		1,
		figsize=(12, 7),
		sharex=True,
		facecolor="#111827"
	)

	fig.subplots_adjust(hspace=0.22, top=0.84, bottom=0.11, left=0.1, right=0.98)
	panel_color = "#182235"
	text_color = "#e5edf7"
	muted_color = "#8fa3bb"
	colors = {
		"target": "#55d6be",
		"stimulation": "#ffbd59",
		"response": "#ff6b9d",
	}

	ax_target = axes[0]
	ax_stim = axes[1]
	ax_response = axes[2]

	for axis in axes:
		axis.set_facecolor(panel_color)
		axis.tick_params(colors=muted_color, labelsize=9)
		axis.grid(
			axis="x",
			color="#52647d",
			alpha=0.25,
			linestyle="--",
			linewidth=0.7,
		)
		axis.spines["top"].set_visible(False)
		axis.spines["right"].set_visible(False)
		axis.spines["left"].set_color("#40516a")
		axis.spines["bottom"].set_color("#40516a")
		axis.xaxis.label.set_color(text_color)
		axis.yaxis.label.set_color(text_color)

	ax_target.eventplot(
		target_spikes,
		lineoffsets=1,
		linelengths=0.8,
		linewidths=3.5,
		colors=colors["target"],
	)
	ax_target.set_ylabel("TARGET", fontweight="bold", color=colors["target"])
	ax_target.set_yticks([])

	ax_stim.step(
		range(len(result["stimulation"])),
		result["stimulation"],
		where="post",
		linewidth=3,
		color=colors["stimulation"],
	)
	ax_stim.fill_between(
		range(len(result["stimulation"])),
		result["stimulation"],
		step="post",
		color=colors["stimulation"],
		alpha=0.1,
	)
	ax_stim.set_ylabel("INPUT", fontweight="bold", color=colors["stimulation"])

	ax_response.eventplot(
		result["spikes"],
		lineoffsets=1,
		linelengths=0.8,
		linewidths=3.5,
		colors=colors["response"],
	)
	ax_response.set_ylabel("ACTUAL", fontweight="bold", color=colors["response"])
	ax_response.set_yticks([])
	ax_response.set_xlabel("Time (ms)")

	fig.suptitle(
		f"Best Stimulation  |  Fitness: {result['score']:.3f}  |  Generation: {result['generation']}",
		color=text_color,
		fontsize=16,
		fontweight="bold",
		x=0.1,
		ha="left",
	)

	return fig


def draw_target_timeline(spikes, stimulation_length=500):

    fig, ax = plt.subplots(figsize=(10, 2))

    ax.set_xlim(0, stimulation_length)
    ax.set_ylim(0, 1)

    ax.axhline(
        0.5,
        linewidth=1
    )

    for spike in spikes:
        ax.vlines(
            spike,
            0.25,
            0.75,
            linewidth=3
        )

    ax.set_xlabel("Time (ms)")
    ax.set_yticks([])

    ax.set_title("Desired Neural Response")

    return fig

