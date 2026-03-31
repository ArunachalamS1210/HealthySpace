# WELL v2 Building Management Dashboard

A comprehensive Building Management Dashboard UI built with Python Flask, designed to monitor and control various wellness and facility metrics based on the WELL v2 standard.

## Features

### 🏢 Core WELL v2 Compliance Modules

#### 1. **Circadian Lighting Controls**
- Interactive CCT (Correlated Color Temperature) sliders (2700K-6500K)
- Zone-based brightness controls with dimming capabilities
- Circadian rhythm support toggles
- Automated glare control systems
- DMX decoder integration endpoints
- System health monitoring (luminaire status, driver alerts, acoustic issues)
- Daylight metrics (exterior illuminance, daylight autonomy)

#### 2. **Water Quality Management**
- Real-time water quality metrics (turbidity, dissolved solids, pH, chlorine, lead)
- WELL v2 standard compliance indicators
- Daily and monthly consumption tracking
- Leak detection alerts
- Filtration system status monitoring
- Water efficiency ratings

#### 3. **Enhanced Air Quality**
- Comprehensive pollutant monitoring (PM2.5, PM10, VOCs, CO₂, formaldehyde, ozone)
- Environmental conditions tracking (temperature, humidity)
- Ventilation system controls with fresh air rate monitoring
- HVAC override controls for air flush operations
- WELL Air Concept compliance indicators

#### 4. **Movement & Physical Activity**
- Active workstation utilization tracking
- Standing desk controls and monitoring
- Building circulation metrics (stair vs. elevator usage)
- Physical activity space occupancy
- Fitness class attendance tracking
- Movement initiative management

#### 5. **Mind & Community Wellness**
- Wellness survey results dashboard
- Community announcements feed
- Interactive feedback submission system
- WELL policy compliance tracking
- Mental health and productivity indicators

### 🎨 Modern UI/UX Design
- Clean, responsive design inspired by medical logistics platforms
- Tailwind CSS-based styling with custom gradients
- Interactive cards with hover effects
- Real-time data visualization
- Mobile-responsive layout
- Intuitive sidebar navigation

### 🔧 Technical Features
- Flask backend with RESTful API endpoints
- Mock sensor data generation for all WELL v2 categories
- Real-time data updates every 30 seconds
- Interactive controls with backend integration
- Emergency protocol activation
- Notification system for user feedback
- Toast notifications for system alerts

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Quick Start

1. **Clone or download the project** to your local machine

2. **Navigate to the project directory:**
   ```bash
   cd "BBP Prototype UI"
   ```

3. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   ```

4. **Activate the virtual environment:**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

5. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

6. **Run the Flask application:**
   ```bash
   python app.py
   ```

7. **Open your web browser and navigate to:**
   ```
   http://localhost:5000
   ```

## API Endpoints

### Dashboard Data
- `GET /` - Main dashboard page
- `GET /api/dashboard-data` - Get all sensor data in JSON format

### Control Endpoints
- `POST /api/update-lighting` - Update lighting zone controls
- `POST /api/hvac-override` - Control HVAC air flush system
- `POST /api/submit-feedback` - Submit community wellness feedback

## WELL v2 Standards Alignment

This dashboard implements monitoring and controls for all five core WELL v2 concepts:

### Air (92% Score)
- Pollutant monitoring with WELL thresholds
- Ventilation effectiveness tracking
- Indoor air quality alerts

### Water (89% Score)
- Multi-parameter water quality testing
- WELL Water Concept compliance
- Filtration system monitoring

### Light (85% Score)
- Circadian rhythm support
- Glare control automation
- Daylight integration metrics

### Movement (78% Score)
- Active workstation promotion
- Circulation encouragement
- Physical activity tracking

### Mind (91% Score)
- Stress and wellness monitoring
- Community engagement platform
- Mental health support features

## Data Structure

The dashboard uses comprehensive mock data that simulates real building sensors:

```python
{
    'lighting': {
        'zones': [...],           # CCT, brightness, status per zone
        'system_health': {...},   # Luminaire and driver status
        'daylight_metrics': {...} # External light conditions
    },
    'water': {
        'quality_metrics': {...}, # All WELL water parameters
        'consumption': {...},     # Usage and efficiency tracking
        'filtration_status': {...} # Filter life and status
    },
    'air': {
        'pollutants': {...},      # PM2.5, VOCs, CO2, etc.
        'environmental': {...},   # Temperature, humidity
        'ventilation': {...}      # HVAC system status
    },
    'movement': {
        'workstation_activity': {...}, # Standing desk usage
        'circulation_metrics': {...},  # Stair/elevator usage
        'active_spaces': {...}         # Gym, bike parking, etc.
    },
    'community': {
        'wellness_surveys': {...},     # Satisfaction, stress levels
        'announcements': [...],        # Community feed
        'policies': {...}              # WELL policy compliance
    },
    'building_score': {
        'overall': 87              # Combined WELL score
    }
}
```

## Customization

### Adding New Sensors
1. Update the `get_dashboard_data()` function in `app.py`
2. Add corresponding UI elements in `templates/dashboard.html`
3. Create API endpoints for sensor controls

### Styling Changes
- Modify Tailwind classes in the HTML template
- Update custom CSS in the `<style>` section
- Adjust color scheme in the Tailwind config

### Integration with Real Systems
- Replace mock data with actual sensor APIs
- Implement real DMX/lighting system controls
- Add database persistence for historical data

## Browser Compatibility
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Contributing

This dashboard is designed as a prototype for WELL v2 building management. Key areas for enhancement:
- Real hardware integration
- Historical data storage
- Advanced analytics and reporting
- User authentication and permissions
- Mobile app companion

## License

This project is created for educational and demonstration purposes as part of building management system development.

---

**Built with ❤️ for WELL v2 certified buildings and occupant wellness**