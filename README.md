## Soil Bio-Activity and Crop Rotation Simulator

# Project Overview

This project is an interactive, research-backed agricultural simulation built in Python using Pygame and Matplotlib. It accurately models the complex, real-world dynamics between crop rotation choices, soil biological activity, climatic variables, and different fertilization systems. Users can plan multi-year farming strategies and observe the ecological and quantitative outcomes of their decisions.
Scientific Foundation

To ensure the simulation behaves realistically, the core mechanics, probabilities, and formulas are directly extracted from agronomic scientific literature rather than arbitrary assumptions.
External Resources

    Resource 1: "The effect of crop rotation on the soil biological activity" (2021) by S.A. Zamyain and R.B. Maksimova.
    Resource 2: "Influence of climatic factors and fertilization systems on grain crop yields" by Y.N. Ankudovich.

# Documented Insights and Model Mechanics

The data from these studies heavily dictated the programming logic and mathematical formulas within the simulation state engine.

    Fertilization Systems: The code implements three distinct fertilization treatments (Natural control, Organic manure, and Mineral NPK). Following the research, organic fertilizer grants a massive bonus to soil biological activity with a residual cooldown effect lasting 4 years. Conversely, mineral fertilizer provides an immediate, high-impact boost to the grain yield but lacks long-term biological sustainment.

    Climatic Modifiers: The simulation utilizes historical monthly means for temperature and precipitation (May through August). A hydrothermal coefficient is dynamically calculated each month; if the ratio falls below a specific threshold, a severe drought stress penalty is applied to the visual health and final yield of the crops.

    Crop Yield Baselines: The base yield metrics for wheat, barley, oats, and potatoes are coded as constants, serving as the starting point before weather and fertilizer multipliers modify the final harvest data.

# Visual Presentations

The simulation utilizes a dual-visualization approach to represent the data both spatially and chronologically.

    Pygame Interactive Interface: A real-time visual grid where users configure their land parcels. The simulation employs a complex color interpolation algorithm to display crop health, transitioning smoothly between dark brown for exhausted soil, yellow for drought stress, and varying saturations of green depending on the growth stage and fertilization level.

    Matplotlib Final Analysis: Upon completing the specified simulation years, an interactive line graph is generated. This plot tracks the annual agricultural yield (measured in q/ha) across all parcels, featuring hover-annotations that reveal the specific weather, crop, and fertilizer data for every data point.

# Simulation Scenarios

The flexible nature of the grid and the multi-year input allows users to test and compare highly divergent agricultural philosophies.

    Scenario A: Sustainable Organic Cycling. Users can simulate a decade of farming using strict crop rotation, periodic fallow years, and organic manure. This scenario demonstrates long-term yield stability and increased visual resilience against dry weather profiles.

    Scenario B: Intensive Mineral Cultivation. Users can simulate continuous, back-to-back planting of high-yield grain crops utilizing strictly mineral (NPK) fertilizers. This demonstrates maximum short-term quantitative output, while highlighting the total depletion of soil biological activity over time.

# Installation and Execution

    Ensure Python is installed on your system.

    Install the required dependencies using your terminal: pip install pygame matplotlib

    Run the main python script.

    Enter the desired timeframe for your simulation in years when prompted on the screen.

    Select a parcel, choose a crop and a fertilizer, and press Enter to begin the year. Press Space to advance through the summer months.
