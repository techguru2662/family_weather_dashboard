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
.\.venv\Scriptsctivate  # Windows
source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run the application
python weather_gui.py
```

## 📁 Project Structure

```
family_weather_dashboard/
│
├── weather_gui.py         # Main GUI application and event handlers
├── weather_api.py         # API interaction and data processing logic
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

## 🎯 Learning Outcomes

This project demonstrates:
- **API Integration** - RESTful API consumption with error handling
- **GUI Development** - Event-driven programming with CustomTkinter
- **Code Organization** - Separation of concerns (GUI vs. API logic)
- **User Experience Design** - Intuitive interface with keyboard shortcuts
- **Version Control** - Git workflow and GitHub repository management

## 🔮 Future Enhancements

- [ ] Add weather alerts and warnings display
- [ ] Implement location autocomplete
- [ ] Save favorite location pairs to local config
- [ ] Export comparison data to CSV/PDF
- [ ] Add graphical temperature trend charts
- [ ] Support international weather services (OpenWeather API)

## 📝 Notes

- **U.S. Only** - National Weather Service API is limited to U.S. locations
- **No API Key Required** - Uses free, public NWS endpoints
- **Geocoding** - ZIP codes and city names are converted to lat/lon coordinates automatically

## 👤 About

Built by David ([techguru2662](https://github.com/techguru2662)) as part of a career transition from supply chain leadership to software development and data analytics. This project demonstrates hands-on Python skills, API integration, and user-focused design. Open to feedback, collaboration, and opportunities in technical roles.

## 📄 License

MIT License - feel free to use and modify for your own projects.
