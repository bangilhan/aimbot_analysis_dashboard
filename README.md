# FPS Aimbot Suspect Profiling Dashboard

A comprehensive dashboard for analyzing FPS game data to detect potential aimbot usage through advanced pattern analysis.

## Features

- **User Selection**: Choose individual players to analyze
- **Basic Info Panel**: Player ID, game session info, team details, weapon usage
- **FPS Statistics**: K/D ratio, headshot rate, reaction time, accuracy
- **Aim Sequence Analysis**: 3D visualization of mouse movement patterns
- **Suspicion Score Analysis**: AI-based scoring with percentile comparison
- **Video Playback**: Jump to suspicious game segments
- **Final Profiling**: Comprehensive judgment with evidence summary

## Technology Stack

- HTML5, CSS3, JavaScript
- Chart.js for 2D visualizations
- Plotly.js for 3D scatter plots
- Modern responsive design

## Usage

1. Open `index.html` in a web browser
2. Select a user from the user grid
3. View detailed analysis in the dashboard panels
4. Use video controls to navigate to suspicious segments

## Data Structure

The dashboard processes FPS game data including:
- Player coordinates (x, y, z)
- Time-series aim sequences
- Game session metadata
- Suspicion scoring algorithms

## Deployment

This project is deployed on Vercel and can be accessed at: [Your Vercel URL]

## License

MIT License
