# 🎰 Galton Board (Plinko) Simulation & RTP Analysis

An interactive data simulation dashboard built with **Python & Streamlit** that models the statistical behavior, Return to Player (RTP), and bankroll decay paths of Galton Board / Plinko setups.

🔗 **Live Demo:** [plinko-simulation.streamlit.app](https://plinko-simulation.streamlit.app/)

## 📌 Features
- **Binomial Distribution Modeling:** Calculates exact theoretical probability density for each slot using $(n = 8, p = 0.5)$.
- **Theoretical RTP & House Edge Calculation:** Mathematically demonstrates a **~37.66% House Edge** on standard low-risk setups.
- **Monte Carlo Multi-Agent Simulation:** Tracks bankroll decay paths of up to 100 simultaneous players across hundreds of rounds.

## 🛠️ Tech Stack
- **Language:** Python
- **Libraries:** Streamlit, NumPy, SciPy, Matplotlib
