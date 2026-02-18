# Family Weather Dashboard

**A Python desktop application that provides side-by-side weather comparisons for U.S. locations using the National Weather Service API.**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.0+-green.svg)

## 📋 Project Overview

Desktop GUI application built during career transition from supply chain leadership to software development. Demonstrates API integration, user interface design, and Python best practices.

**Key Use Case:** Families with members in different cities can quickly compare weather forecasts to plan travel, events, or daily check-ins.

## ✨ Features

- **Dual Location Comparison** - Enter two U.S. ZIP codes or "City, State" formats
- **7-Day Forecast View** - Detailed extended forecasts with temperature and conditions
- **Preset Buttons** - Quick access to frequently compared locations (home vs. family)
- **Location Swap** - "Flip A/B" button to reverse comparison
- **Keyboard Shortcuts** - Enter key triggers both location searches simultaneously
- **Real-Time Data** - Leverages National Weather Service API (no API key required)

## 🛠️ Technologies

- **Python 3.13**
- **CustomTkinter** - Modern GUI framework
- **Requests** - HTTP library for API calls
- **National Weather Service API** - Free, public weather data

## 🚀 Installation & Usage

```bash
# Clone the repository
git clone https://github.com/techguru2662/family_weather_dashboard.git
cd family_weather_dashboard

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run the application
python weather_gui.py
