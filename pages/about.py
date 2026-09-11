import streamlit as st
from neurosim.izhikevich import IzhikevichNeuron
from neurosim.presets import IZHIKEVICH_PRESETS
from neurosim.plotting import get_plot_palette, apply_plot_theme, apply_axis_theme
import matplotlib.pyplot as plt
import numpy as np

def plot_voltage(voltages, spikes, preset_name):
    palette = get_plot_palette()
    time = range(len(voltages))
    fig, ax = plt.subplots(figsize=(10, 4))
    apply_plot_theme(fig, palette)
    apply_axis_theme(ax, palette)

    ax.plot(time, voltages, label="Membrane voltage", color=palette["target"])

    for spike_time in spikes:
        ax.axvline(
            spike_time,
            linestyle="--",
            alpha=0.4,
            color=palette["response"]
        )

    ax.axhline(
        30,
        linestyle=":",
        label="Spike threshold",
        color=palette["stimulation"]
    )

    ax.set_xlabel("Time (ms)", color=palette["text_color"])
    ax.set_ylabel("Membrane voltage (mV)", color=palette["text_color"])
    ax.set_title(f"Izhikevich Neuron: {preset_name}", color=palette["text_color"])
    ax.legend()

    fig.tight_layout()
    return fig




# ---------------------------------------------------------
# PAGE SETUP
# ---------------------------------------------------------

st.set_page_config(
    page_title="About NeuroSim",
    page_icon="🧠",
    layout="wide"
)

st.title("About NeuroSim")

view_mode = st.radio(
    "How much detail would you like?",
    ["Quick overview", "More detail"],
    horizontal=True
)


# =========================================================
# QUICK OVERVIEW
# =========================================================

if view_mode == "Quick overview":

    st.markdown(
        """
        ### What is NeuroSim?

        **NeuroSim is a sandbox for exploring neural stimulation.**

        Normally, we can give a simulated neuron some input and see how it
        responds.

        NeuroSim does its best to solvew the inverse problem:

        **You choose the neural response you want, and NeuroSim searches for
        stimulation that could produce it.**
        """
    )

    st.info(
        "NeuroSim is just a tiny educational and experimental simulation tool."
    )

    st.divider()

    st.header("Why this matters")

    st.markdown(
        """
        Being able to better control neural activity could have important medical
        applications. Neural stimulation is already being explored and used to
        restore or support lost functions, from hearing and movement to vision and
        other forms of sensory feedback.

        Tools like NeuroSim explore a fundamental part of that challenge:
        **if we know the neural response we want, how can we find the stimulation
        needed to produce it?**

        Better ways of solving this problem could eventually contribute to more
        precise and personalized neurotechnology.
        """
    )

    st.divider()

    # -----------------------------------------------------
    # THE CORE IDEA
    # -----------------------------------------------------

    st.header("The main idea")

    left, right = st.columns(2)

    with left:
        st.subheader("Normal simulation")

        st.markdown(
            """
            You choose the stimulation.

            NeuroSim shows you what the neuron does.

            **Stimulation → Neuron → Spikes**
            """
        )

    with right:
        st.subheader("NeuroSim's challenge")

        st.markdown(
            """
            You choose the spikes you want.

            NeuroSim tries to discover the stimulation.

            **Target spikes → Search → Stimulation**
            """
        )

    st.divider()

    # -----------------------------------------------------
    # HOW IT WORKS
    # -----------------------------------------------------

    st.header("How it works")

    st.markdown(
        """
        NeuroSim repeats a simple cycle:

        **1.** You choose when you want the neuron to spike.  
        **2.** NeuroSim creates possible stimulation patterns.  
        **3.** Each pattern is tested on a simulated neuron.  
        **4.** The result is scored based on how closely it matches your target.  
        **5.** Better solutions are used to create new ones.  
        **6.** The process repeats until a strong match is found.
        """
    )

    st.divider()

    # -----------------------------------------------------
    # NEURON MODELS
    # -----------------------------------------------------

    st.header("Different neurons behave differently")

    st.markdown(
        """
        NeuroSim includes more than one type of simulated neuron.

        The simpler **Leaky Integrate-and-Fire** model is useful for clear,
        easy-to-understand experiments.

        The **Izhikevich model** can produce several different firing styles,
        showing that the same input does not always create the same kind of
        neural activity.
        """
    )

    st.subheader("Try the Izhikevich neuron")

    subtype = st.selectbox(
        "Izhikevich subtype",
        [
            "Regular spiking",
            "Intrinsically bursting",
            "Fast spiking",
            "Chattering"
        ]
    )

    preview_current = st.slider(
        "Input current (I)",
        min_value=0,
        max_value=50,
        value=10,
        step=1
    )

    neuron_params = IZHIKEVICH_PRESETS[subtype]

    neuron = IzhikevichNeuron(**neuron_params)

    simulation_length = 500
    current = preview_current

    if st.button(
        "Run Simulation",
        key="quick_izhikevich"
    ):
        voltages = []
        spikes = []

        for time in range(simulation_length):
            spike, display_voltage = neuron.step(current)
            voltages.append(display_voltage)

            if spike:
                spikes.append(time)

        fig = plot_voltage(
            voltages,
            spikes,
            subtype
        )

        st.pyplot(fig)

    st.caption(
        "Changing the subtype changes how the neuron responds, even when "
        "the input itself stays simple."
    )

    st.divider()

    # -----------------------------------------------------
    # ML
    # -----------------------------------------------------

    st.header("Where machine learning comes in")

    st.markdown(
        """
        NeuroSim can also learn from stimulation patterns it has already tested.

        After enough simulations, a small machine-learning model begins
        estimating which new stimulation patterns look promising.

        NeuroSim can then spend more time testing good candidates and less time
        testing poor ones.

        The final score still comes from the neuron simulation itself — the
        machine-learning model only helps decide **what to try next**.
        """
    )

    st.subheader("Example: Evolutionary vs ML-guided search")

    st.image(
        "assets/surrogate_vs_evolution.png",
        caption=(
            "Example development run comparing normal evolutionary search "
            "with ML-guided search."
        ),
        width=650,
    )

    st.caption(
        "This is one example run, not a full benchmark. In this experiment, "
        "ML guidance helped the search reach strong solutions earlier."
    )

    st.divider()

    # -----------------------------------------------------
    # LIMITATIONS
    # -----------------------------------------------------

    st.header("What NeuroSim is, and isn't")

    st.markdown(
        """
        NeuroSim uses simplified neuron models and simplified stimulation.

        It is useful for exploring ideas about optimization, neural activity,
        and stimulation, but it does **not** predict what will happen in a real
        human brain.

        A future version could include larger neural networks, more realistic
        stimulation, and models built from experimental data.
        """
    )

    st.divider()

    st.markdown(
        """
        ### The question behind NeuroSim

        **If we know the neural activity we want, can computation help us find
        the stimulation that produces it?**
        """
    )


# =========================================================
# MORE DETAIL
# =========================================================

else:

    st.markdown(
        """
        ### What is NeuroSim?

        NeuroSim is an interactive computational neuroscience sandbox built
        around an **inverse stimulation problem**.

        In a normal simulation, we choose an input and observe what the neuron
        does.

        NeuroSim instead starts with a desired spike pattern and searches for
        stimulation that causes a simulated neuron to behave as closely as
        possible to that target.
        """
    )

    st.info(
        "NeuroSim is a computational and educational prototype. "
        "It is not designed for clinical use."
    )

    st.divider()



    st.header("Why this problem matters")

    st.markdown(
        """
        Neural stimulation has the potential to help when the nervous system can no
        longer receive, process, or communicate information normally. Technologies
        such as cochlear implants, visual prostheses, brain and spinal stimulation,
        and brain-computer interfaces all depend in some way on interacting with
        neural activity.

        A major challenge is determining **what stimulation will create the desired
        neural response**. Better computational methods for exploring that question
        could help researchers design more precise stimulation strategies while
        reducing the amount of trial and error required.

        NeuroSim is a simplified exploration of that larger problem, rather than a
        model of any specific medical device.
        """
    )

    st.divider()

    # -----------------------------------------------------
    # INVERSE PROBLEM
    # -----------------------------------------------------

    st.header("The problem NeuroSim explores")

    left, right = st.columns(2)

    with left:

        st.subheader("Forward simulation")

        st.markdown(
            """
            A normal neural simulation asks:

            **If I apply this input, what happens?**

            **Stimulation → Neuron → Spike response**
            """
        )

    with right:

        st.subheader("Inverse search")

        st.markdown(
            """
            NeuroSim asks:

            **If I want this response, what input should I use?**

            **Target response → Search → Stimulation**
            """
        )

    st.markdown(
        """
        Finding that stimulation can be difficult because the relationship
        between input and neural activity is not always simple. A small change
        in pulse timing or strength can change when a neuron fires.
        """
    )

    st.divider()

    # -----------------------------------------------------
    # SEARCH
    # -----------------------------------------------------

    st.header("How NeuroSim searches")

    st.markdown(
        """
        NeuroSim describes stimulation using a small set of pulses.

        Each pulse has:

        - a start time,
        - a duration,
        - and a strength.

        The search begins with many possible stimulation patterns.
        NeuroSim simulates each one and gives it a fitness score based on how
        closely its spikes match the target.
        """
    )

    st.markdown(
        """
        Better candidates are then used to create the next group of possible
        solutions.

        NeuroSim mixes parts of good solutions, makes small random changes,
        and occasionally adds completely new candidates so that the search does
        not become stuck too quickly.
        """
    )

    st.markdown(
        """
        **Target spikes → Candidate stimulation → Neuron simulation → Score → Improve → Repeat**
        """
    )

    st.divider()

    # -----------------------------------------------------
    # MODELS
    # -----------------------------------------------------

    st.header("Neuron models")

    model_left, model_right = st.columns(2)

    with model_left:

        st.subheader("Leaky Integrate-and-Fire")

        st.markdown(
            """
            The Leaky Integrate-and-Fire model is a simple neuron model.

            Its voltage rises when it receives input and slowly falls back
            toward rest. If the voltage reaches a threshold, the model records
            a spike.

            Because it is simple and fast, it is useful for demonstrating the
            stimulation search clearly.
            """
        )

    with model_right:

        st.subheader("Izhikevich")

        st.markdown(
            """
            The Izhikevich model can reproduce a wider variety of firing
            patterns without becoming extremely expensive to simulate.

            NeuroSim includes several presets that behave differently, such as
            regular firing, bursting, fast firing, and chattering.
            """
        )

    st.subheader("Explore the Izhikevich model")

    st.markdown(
        """
        Try giving the different neuron types the same kind of constant input.
        Their responses can look very different.
        """
    )

    subtype = st.selectbox(
        "Izhikevich subtype",
        [
            "Regular spiking",
            "Intrinsically bursting",
            "Fast spiking",
            "Chattering"
        ],
        key="detailed_subtype"
    )

    preview_current = st.slider(
        "Input current (I)",
        min_value=0,
        max_value=50,
        value=10,
        step=1,
        key="detailed_current"
    )

    neuron_params = IZHIKEVICH_PRESETS[subtype]

    neuron = IzhikevichNeuron(**neuron_params)

    simulation_length = 500
    current = preview_current

    if st.button(
        "Run Simulation",
        key="detailed_izhikevich"
    ):

        voltages = []
        spikes = []

        for time in range(simulation_length):

            spike, display_voltage = neuron.step(current)

            voltages.append(
                display_voltage
            )

            if spike:
                spikes.append(time)

        fig = plot_voltage(
            voltages,
            spikes,
            subtype
        )

        st.pyplot(fig)

    st.caption(
        "This is one reason the inverse problem is interesting: the best "
        "stimulation depends on the neuron being simulated."
    )

    st.divider()

    # -----------------------------------------------------
    # EVOLUTIONARY SEARCH
    # -----------------------------------------------------

    st.header("Evolutionary search")

    st.markdown(
        """
        NeuroSim's main search method is inspired by evolution.

        A population of possible stimulation patterns is tested.
        Better solutions are kept, combined, and slightly changed to create
        the next generation.

        Some new random candidates are also added so that the search keeps
        exploring new possibilities.

        Over time, the population tends to move toward stimulation patterns
        that better match the requested spike pattern.
        """
    )

    st.divider()

    # -----------------------------------------------------
    # ML GUIDANCE
    # -----------------------------------------------------

    st.header("ML-guided search")

    st.markdown(
        """
        NeuroSim can also use machine learning to help choose which stimulation
        patterns are worth testing.

        Every real simulation creates a useful example:

        **stimulation pattern → resulting fitness**

        After collecting enough examples, NeuroSim trains a Random Forest model
        to estimate the likely fitness of new candidates.
        """
    )

    st.markdown(
        """
        The search can then create a larger pool of possible offspring and ask
        the ML model to rank them.

        Only the most promising candidates are sent to the actual neuron
        simulator.

        This allows the ML model to guide the search without replacing the
        underlying simulation.
        """
    )

    st.success(
        "The ML prediction is never treated as the real result. "
        "Selected candidates still have to be tested by the neuron simulator."
    )

    # -----------------------------------------------------
    # ML GRAPH
    # -----------------------------------------------------

    st.subheader("Example result")

    st.image(
        "assets/surrogate_vs_evolution.png",
        caption=(
            "An example run comparing normal evolutionary search with "
            "ML-guided search."
        ),
        width=650,
    )

    st.markdown(
        """
        In this example, both methods eventually found a very strong solution,
        but the ML-guided search moved into the high-fitness region earlier.

        This graph represents a development experiment rather than a complete
        benchmark, so it should be treated as an example of how the two search
        methods can behave.
        """
    )

    with st.expander("See surrogate validation results"):

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Prediction error (MAE)",
                "0.042"
            )

        with col2:
            st.metric(
                "Ranking correlation",
                "0.917"
            )

        with col3:
            st.metric(
                "ML-selected mean fitness",
                "0.911"
            )

        st.markdown(
            """
            In a separate test on new offspring:

            - the model's average prediction error was about **0.042**,
            - its ranking of candidates strongly matched their real ranking,
            - and the top 20% selected by the model had an average real fitness
              of about **0.911**, compared with about **0.647** across all
              candidates.

            These results suggest that the model is useful for deciding which
            candidates are worth simulating.
            """
        )

    st.divider()

    # -----------------------------------------------------
    # NOISE
    # -----------------------------------------------------

    st.header("Noise")

    st.markdown(
        """
        NeuroSim can also add random variation to the input current.

        This is a simple way to make the simulation less perfectly predictable
        and explore how stimulation behaves when there is some variability.

        It is still only a simplified approximation of real biological noise.
        """
    )

    st.divider()

    # -----------------------------------------------------
    # LIMITATIONS
    # -----------------------------------------------------

    st.header("Limitations")

    st.markdown(
        """
        NeuroSim deliberately simplifies real neuroscience.

        At the moment:

        - it simulates individual neurons rather than full brain networks,
        - stimulation uses simplified current pulses,
        - the neuron models are mathematical approximations,
        - the noise model is basic,
        - the ML model can only learn from the simulations it has already seen,
        - and the results have not been tested against real neural tissue.

        NeuroSim is therefore best understood as a sandbox for exploring ideas,
        not as a system for designing real medical stimulation.
        """
    )

    st.divider()

    # -----------------------------------------------------
    # FUTURE
    # -----------------------------------------------------

    st.header("Where it could go next")

    st.markdown(
        """
        Future versions could explore:

        - networks of many neurons,
        - more realistic stimulation,
        - models built from experimental data,
        - stimulation that must remain effective despite noise,
        - more complex target activity,
        - and smarter ways for the ML system to choose what to test next.
        """
    )

    st.divider()

    st.header("The bigger question")

    st.markdown(
        """
        NeuroSim started from one question:

        **If we know the neural response we want, can computation help us
        discover the stimulation that produces it?**

        This prototype explores that question using neuron simulation,
        evolutionary search, and machine-learning guidance.
        """
    )