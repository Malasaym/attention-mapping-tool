Offline Human Attention Mapping Tool

Overview

This project maps human attention patterns using interaction signals such as keyboard activity, mouse activity, window switching, and idle periods.

The system converts interaction data into attention states and visualizes how attention shifts over time.

The tool runs completely offline and does not collect sensitive data such as keystroke content or screen recordings.

Features

- Keyboard activity tracking (timestamps only)
- Mouse movement and clicks
- Application/window switch detection
- Idle period detection
- Attention state mapping
- Focus fragmentation detection
- Visual attention heatmap
- GitHub-style attention visualization
- Interactive dashboard

Constraints Followed

- No productivity scoring
- No keystroke content captured
- No screen capture
- Fully offline processing
- No internet or cloud services used

Project Structure

attention-mapper/
│
├── tracker.py
├── dashboard.py
├── requirements.txt
├── README.md
│
└── data/
└── attention_log.csv

Installation

Install dependencies:

pip install -r requirements.txt

Run Interaction Tracker

python tracker.py

This collects keyboard, mouse, window switch, and idle interaction signals.

Run Dashboard

streamlit run dashboard.py

The dashboard displays:

- Attention heatmap over time
- Focus fragmentation analysis
- GitHub-style attention activity visualization

Output

The system generates:

data/attention_log.csv

This file contains interaction timestamps and attention states.

Technologies Used

Python
Pandas
Matplotlib
Seaborn
Streamlit
Pynput

Purpose

This tool helps visualize how attention is distributed across time using interaction signals rather than application usage duration.
