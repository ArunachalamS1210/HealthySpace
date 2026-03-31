from flask import Flask, render_template, jsonify, request
import sys
import os

# Add utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from data_processor_simple import VendorDataProcessor

app = Flask(__name__)

# Initialize data processor
processor = VendorDataProcessor()

@app.route('/')
def index():
    """Dashboard hub - navigation page"""
    return render_template('index.html')

@app.route('/well-dashboard')
def well_dashboard():
    """Original WELL dashboard with complete mock data"""
    from datetime import datetime, timedelta
    
    # Complete mock data for legacy template
    mock_data = {
        'timestamp': datetime.now(),
        'building_score': {
            'overall': {'points': 78, 'max_points': 90, 'percentage': 87},
            'air': {'points': 18, 'max_points': 20, 'percentage': 92},
            'water': {'points': 14, 'max_points': 16, 'percentage': 89},
            'lighting': {'points': 15, 'max_points': 18, 'percentage': 85},
            'movement': {'points': 16, 'max_points': 21, 'percentage': 78},
            'community': {'points': 14, 'max_points': 15, 'percentage': 91},
            'trend': 'improving'
        },
        'power_consumption': {
            'current_kwh': 245.7,
            'monthly_kwh': 7825,
            'daily_avg': 260.5,
            'efficiency_rating': 87
        },
        'air': {
            'pollutants': {
                'pm25': 8.5,
                'pm10': 22.3,
                'vocs': 0.24,
                'co2': 650,
                'formaldehyde': 0.015,
                'ozone': 0.045
            },
            'environmental': {
                'temperature': 22.5,
                'humidity': 48,
                'air_changes_per_hour': 6.2
            },
            'ventilation': {
                'fresh_air_rate': 12.5,
                'filtration_efficiency': 94,
                'hvac_override_active': False
            }
        },
        'water': {
            'quality_metrics': {
                'turbidity': 0.8,
                'dissolved_solids': 245,
                'ph_level': 7.2,
                'chlorine': 0.5,
                'lead': 0.008,
                'status': 'excellent'
            },
            'consumption': {
                'daily_usage': 2847,
                'monthly_target': 85000,
                'efficiency_rating': 92,
                'leak_alerts': 0
            },
            'filtration_status': {
                'carbon_filter': {
                    'status': 'excellent',
                    'remaining_life': 78
                },
                'sediment_filter': {
                    'status': 'good',
                    'remaining_life': 45
                },
                'uv_sterilizer': {
                    'status': 'excellent',
                    'remaining_life': 92
                }
            }
        },
        'lighting': {
            'zones': [
                {
                    'id': 'zone_1',
                    'name': 'Main Office',
                    'cct': 4000,
                    'brightness': 75,
                    'status': 'active',
                    'circadian_mode': True,
                    'glare_control': False
                }
            ],
            'system_health': {
                'failed_luminaires': 2,
                'total_luminaires': 156,
                'driver_alerts': 1,
                'acoustic_issues': 0
            },
            'daylight_metrics': {
                'exterior_illuminance': 12500,
                'daylight_autonomy': 78,
                'useful_daylight_illuminance': 85
            },
            'energy_consumption': {
                'today': 45.2,
                'week': 312.8,
                'month': 1257.4,
                'trend_percentage': 8.5
            },
            'lpd': {
                'current': 0.8,
                'target': 1.0
            }
        },
        'movement': {
            'workstation_activity': {
                'standing_desks_active': 23,
                'total_standing_desks': 45,
                'utilization_rate': 51,
                'avg_standing_time': 3.2
            },
            'circulation_metrics': {
                'stair_usage': 147,
                'elevator_usage': 89,
                'stair_preference_rate': 62,
                'step_count_average': 6800
            },
            'active_spaces': {
                'gym_occupancy': 18,
                'walking_paths_used': 7,
                'bike_parking_occupied': 14,
                'fitness_class_attendance': 12
            }
        },
        'community': {
            'wellness_surveys': {
                'satisfaction_score': 8.2,
                'stress_level': 4.1,
                'sleep_quality': 7.8,
                'productivity_rating': 8.5,
                'response_rate': 73
            },
            'policies': {
                'active_policies': 12,
                'compliance_rate': 94,
                'last_updated': datetime.now() - timedelta(days=15)
            },
            'announcements': [
                {
                    'id': 1,
                    'title': 'Wellness Wednesday: Mindfulness Session',
                    'message': 'Join us for a guided meditation session in Conference Room B',
                    'type': 'wellness',
                    'timestamp': datetime.now() - timedelta(hours=2),
                    'priority': 'medium'
                }
            ]
        }
    }
    
    return render_template('dashboard.html', data=mock_data)

@app.route('/vendor-intelligence')
def vendor_intelligence():
    """New Vendor Intelligence Dashboard"""
    return render_template('vendor_intelligence.html')

@app.route('/project-management') 
def project_management():
    """Project Management Dashboard"""
    return render_template('project_management.html')

@app.route('/project/<int:project_id>')
def project_detail(project_id):
    """Project Detail Page"""
    # Mock project data - in real app this would come from database
    projects = {
        1: {
            'id': 1,
            'title': 'Corporate Wellness Center',
            'client': 'TechCorp Industries',
            'status': 'On Track',
            'stage': 'Integration',
            'progress': 78,
            'start_date': 'Jan 15, 2024',
            'due_date': 'Apr 30, 2024',
            'description': 'Comprehensive wellness center design focusing on biophilic elements and employee wellbeing.',
            'status_class': 'status-on-track',
            'border_color': '#10b981'
        },
        2: {
            'id': 2,
            'title': 'WELL Gold Certification',
            'client': 'Green Valley Residences',
            'status': 'At Risk',
            'stage': 'Assessment',
            'progress': 45,
            'start_date': 'Feb 1, 2024',
            'due_date': 'Jun 15, 2024',
            'description': 'WELL Building Standard certification process for residential complex.',
            'status_class': 'status-at-risk',
            'border_color': '#f59e0b'
        },
        3: {
            'id': 3,
            'title': 'Biophilic Office Design',
            'client': 'Innovation Hub',
            'status': 'Delayed',
            'stage': 'Planning',
            'progress': 25,
            'start_date': 'Mar 10, 2024',
            'due_date': 'Aug 30, 2024',
            'description': 'Modern office space incorporating natural elements and biophilic design principles.',
            'status_class': 'status-delayed',
            'border_color': '#ef4444'
        }
    }
    
    project = projects.get(project_id)
    if not project:
        return "Project not found", 404
        
    return render_template('project_detail.html', project=project)

@app.route('/api/vendor-intelligence-data', methods=['GET', 'POST'])
def api_vendor_intelligence_data():
    """API endpoint for vendor intelligence data"""
    try:
        # Get filters from POST request if available
        filters = None
        if request.method == 'POST':
            data = request.get_json()
            filters = data.get('filters', {}) if data else {}
        
        # Get all required data
        kpi_data = processor.get_kpi_data(filters)
        comparison_data = processor.get_vendor_comparison_data()
        filter_data = processor.get_filter_data()
        cost_data = processor.get_cost_breakdown_data()
        historical_data = processor.get_historical_trends()
        insights = processor.get_insights(filters)
        schema_summary = processor.get_schema_summary()
        
        return jsonify({
            'status': 'success',
            'kpi_data': kpi_data,
            'comparison_data': comparison_data,
            'filter_data': filter_data,
            'cost_data': cost_data,
            'historical_data': historical_data,
            'insights': insights,
            'schema_summary': schema_summary,
            'applied_filters': filters
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/vendor-comparison', methods=['POST'])
def api_vendor_comparison():
    """Get comparison data for specific vendors"""
    try:
        data = request.get_json()
        vendor_ids = data.get('vendor_ids', [])
        
        comparison_data = processor.get_vendor_comparison_data(vendor_ids)
        
        return jsonify({
            'status': 'success',
            'comparison_data': comparison_data
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error', 
            'message': str(e)
        }), 500

@app.route('/api/cost-breakdown', methods=['POST'])
def api_cost_breakdown():
    """Get cost breakdown for specific vendors"""
    try:
        data = request.get_json()
        vendor_ids = data.get('vendor_ids', [])
        
        cost_data = processor.get_cost_breakdown_data(vendor_ids)
        
        return jsonify({
            'status': 'success',
            'cost_data': cost_data
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/insights', methods=['POST']) 
def api_insights():
    """Get intelligent insights based on filters"""
    try:
        data = request.get_json()
        filters = data.get('filters', {}) if data else {}
        
        insights = processor.get_insights(filters)
        
        return jsonify({
            'status': 'success',
            'insights': insights
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/schema-summary')
def api_schema_summary():
    """Get data schema summary for debugging"""
    try:
        schema_summary = processor.get_schema_summary()
        
        return jsonify({
            'status': 'success',
            'schema_summary': schema_summary
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Legacy WELL Building routes (preserved for compatibility)
@app.route('/api/dashboard-data')
def api_dashboard_data():
    """Legacy WELL dashboard data"""
    from datetime import datetime, timedelta
    import random
    
    # Mock data for WELL dashboard (preserved for backward compatibility)
    legacy_data = {
        'timestamp': datetime.now(),
        'building_score': {
            'overall': {'points': 78, 'max_points': 90, 'percentage': 87},
            'air': {'points': 18, 'max_points': 20, 'percentage': 92},
            'water': {'points': 14, 'max_points': 16, 'percentage': 89},
            'lighting': {'points': 15, 'max_points': 18, 'percentage': 85},
            'movement': {'points': 16, 'max_points': 21, 'percentage': 78},
            'community': {'points': 14, 'max_points': 15, 'percentage': 91},
            'trend': 'improving'
        },
        'power_consumption': {
            'current_kwh': 245.7,
            'monthly_kwh': 7825,
            'daily_avg': 260.5,
            'efficiency_rating': 87
        },
        'air': {
            'pollutants': {
                'pm25': 8.5,
                'pm10': 22.3,
                'vocs': 0.24,
                'co2': 650,
                'formaldehyde': 0.015,
                'ozone': 0.045
            },
            'environmental': {
                'temperature': 22.5,
                'humidity': 48,
                'air_changes_per_hour': 6.2
            },
            'ventilation': {
                'fresh_air_rate': 12.5,
                'filtration_efficiency': 94,
                'hvac_override_active': False
            }
        },
        'water': {
            'quality_metrics': {
                'turbidity': 0.8,
                'dissolved_solids': 245,
                'ph_level': 7.2,
                'chlorine': 0.5,
                'lead': 0.008,
                'status': 'excellent'
            },
            'consumption': {
                'daily_usage': 2847,
                'monthly_target': 85000,
                'efficiency_rating': 92,
                'leak_alerts': 0
            }
        },
        'lighting': {
            'zones': [
                {
                    'id': 'zone_1',
                    'name': 'Main Office',
                    'cct': 4000,
                    'brightness': 75,
                    'status': 'active',
                    'circadian_mode': True,
                    'glare_control': False
                }
            ],
            'system_health': {
                'failed_luminaires': 2,
                'total_luminaires': 156,
                'driver_alerts': 1,
                'acoustic_issues': 0
            },
            'daylight_metrics': {
                'exterior_illuminance': 12500,
                'daylight_autonomy': 78,
                'useful_daylight_illuminance': 85
            },
            'energy_consumption': {
                'today': 45.2,
                'week': 312.8,
                'month': 1257.4,
                'trend_percentage': 8.5
            },
            'lpd': {
                'current': 0.8,
                'target': 1.0
            }
        },
        'movement': {
            'workstation_activity': {
                'standing_desks_active': 23,
                'total_standing_desks': 45,
                'utilization_rate': 51,
                'avg_standing_time': 3.2
            },
            'circulation_metrics': {
                'stair_usage': 147,
                'elevator_usage': 89,
                'stair_preference_rate': 62,
                'step_count_average': 6800
            }
        },
        'community': {
            'wellness_surveys': {
                'satisfaction_score': 8.2,
                'stress_level': 4.1,
                'sleep_quality': 7.8,
                'productivity_rating': 8.5,
                'response_rate': 73
            },
            'announcements': [
                {
                    'id': 1,
                    'title': 'Wellness Wednesday: Mindfulness Session',
                    'message': 'Join us for a guided meditation session in Conference Room B',
                    'type': 'wellness',
                    'timestamp': datetime.now() - timedelta(hours=2),
                    'priority': 'medium'
                }
            ]
        }
    }
    
    return jsonify(legacy_data)

@app.route('/api/update-lighting', methods=['POST'])
def update_lighting():
    """Legacy lighting control"""
    data = request.get_json()
    return jsonify({
        'status': 'success',
        'message': 'Lighting updated',
        'data': data
    })

@app.route('/api/hvac-override', methods=['POST'])
def hvac_override():
    """Legacy HVAC control"""
    data = request.get_json()
    action = data.get('action')
    return jsonify({
        'status': 'success',
        'message': f'HVAC override {action}ed',
        'active': action == 'start'
    })

@app.route('/api/submit-feedback', methods=['POST'])
def submit_feedback():
    """Legacy feedback submission"""
    data = request.get_json()
    return jsonify({
        'status': 'success',
        'message': 'Thank you for your feedback!',
        'data': data
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)