# 🏢 Vendor Intelligence System

A comprehensive dashboard for vendor selection and comparison in wellness & biophilic consulting projects.

## 📋 Overview

The Vendor Intelligence System helps consulting teams make data-driven decisions about vendor selection by providing:

- **Smart vendor comparison** across 4 main categories (Lighting, Air Quality, Automation, Water)
- **Cost analysis & commercial terms** comparison
- **Performance scoring** based on historical data
- **Risk assessment** and delivery tracking
- **Intelligent insights** and recommendations

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python app.py
```

### 3. Access the Dashboard
- **Vendor Intelligence:** http://localhost:5000/vendor-intelligence
- **Legacy WELL Dashboard:** http://localhost:5000/

## 📊 Data Structure

### CSV Files Schema

#### vendors.csv
- `vendor_id`: Unique vendor identifier
- `vendor_name`: Company name
- `category`: Product category (Lighting/Air Quality/Automation/Water)
- `brand_tier`: Premium/Standard/Budget
- `city_support`: Cities where vendor operates
- `preferred_vendor`: TRUE/FALSE
- `after_sales_rating`: Rating (1-5)
- `reliability_rating`: Rating (1-5)

#### products.csv
- `product_id`: Unique product identifier
- `vendor_id`: Links to vendors.csv
- `product_name`: Product name
- `category`: Product category
- `subcategory`: Product subcategory
- `spec_1`, `spec_2`, `spec_3`: Technical specifications
- `warranty_years`: Warranty period
- `lead_time_days`: Delivery lead time

#### commercials.csv
- `commercial_id`: Unique commercial record ID
- `product_id`: Links to products.csv
- `list_price`: Original price
- `negotiated_price`: Final negotiated price
- `discount_percent`: Discount offered
- `credit_period_days`: Payment credit period
- `payment_style`: Payment terms (e.g., "30-70")
- `installation_cost`: Installation charges
- `maintenance_cost_annual`: Annual maintenance cost

#### project_usage.csv
- `usage_id`: Unique usage record ID
- `project_name`: Project name
- `city`: Project location
- `project_type`: Office/Retail/Residential/Hospitality/Education/Healthcare
- `certification`: WELL Gold/LEED Platinum/etc.
- `vendor_id`: Links to vendors.csv
- `product_id`: Links to products.csv
- `qty`: Quantity used
- `total_value`: Total project value
- `delivery_status`: On-time/Delayed
- `issue_flag`: TRUE/FALSE for delivery issues

#### vendor_scores.csv
- `vendor_id`: Links to vendors.csv
- `cost_score`: Cost competitiveness (1-10)
- `performance_score`: Product performance (1-10)
- `reliability_score`: Delivery reliability (1-10)
- `service_score`: After-sales service (1-10)
- `speed_score`: Delivery speed (1-10)
- `final_score`: Weighted overall score

## 📈 Calculated Metrics

### KPI Calculations
- **Avg Negotiated Price:** Mean of negotiated_price from commercials
- **Avg Lead Time:** Mean of lead_time_days from products
- **Avg Vendor Score:** Mean of final_score from vendor_scores
- **Avg Credit Period:** Mean of credit_period_days from commercials
- **Repeat Usage %:** (Preferred vendors / Total vendors) × 100

### Final Vendor Score Formula
```
Final Score = (30% × cost_score) + (25% × performance_score) + 
              (20% × reliability_score) + (15% × service_score) + 
              (10% × speed_score)
```

### Derived Metrics
- **Discount %:** (list_price - negotiated_price) / list_price × 100
- **Value Score:** final_score / avg_negotiated_price × 10000 (for best value insights)
- **Cost Efficiency:** negotiated_price / performance_score
- **Risk Flag:** Based on issue_flag from project history

## 🎯 Dashboard Features

### 1. Filter Panel
- **Category:** Filter by product category
- **City:** Filter by project location
- **Project Type:** Filter by project type
- **Certification:** Filter by certification target
- **Preferred Vendor:** Show only preferred/non-preferred vendors

### 2. KPI Cards
Display key metrics at a glance:
- Average negotiated price
- Average lead time
- Average vendor score  
- Average credit period
- Repeat vendor usage percentage

### 3. Vendor Comparison Matrix
Side-by-side comparison of up to 4 vendors:
- Negotiated price
- Discount percentage
- Credit period
- Lead time
- Warranty
- Reliability rating
- After-sales rating
- Final score

### 4. Cost Breakdown Chart
Stacked bar chart showing:
- Product cost
- Installation cost
- Annual maintenance cost

### 5. Performance Radar Chart
Multi-dimensional performance comparison:
- Cost score
- Performance score
- Reliability score
- Service score
- Speed score

### 6. Historical Usage Trends
Line chart showing project usage frequency by vendor

### 7. Smart Insights
AI-powered recommendations:
- **Best Value Vendor:** Highest value score (performance vs cost)
- **Lowest Cost Option:** Most competitive pricing
- **Fastest Execution:** Shortest lead time
- **Risk Alerts:** Vendors with delivery issues

## 🔧 Technical Architecture

### Backend
- **Flask:** Web framework
- **Pandas:** Data processing and analysis
- **Python 3.8+:** Runtime environment  

### Frontend
- **HTML5/CSS3:** Structure and styling
- **Vanilla JavaScript:** Interactivity and AJAX
- **Chart.js:** Data visualizations
- **Responsive CSS Grid:** Layout system

### Data Flow
1. CSV files loaded into Pandas DataFrames
2. Data processed in `utils/data_processor.py`
3. Flask API endpoints serve processed data
4. Dashboard JavaScript fetches and displays data
5. interactive filters trigger data refresh

## 🎨 Design System

### Color Palette
- **Primary Teal:** `#008B8B`
- **Secondary Teal:** `#20B2AA`  
- **Navy:** `#1e3a5f`
- **Dark Navy:** `#0f2235`
- **Light Grey:** `#f8f9fa`
- **Medium Grey:** `#6c757d`

### Typography
- **Font Family:** Segoe UI, Tahoma, Geneva, Verdana, sans-serif
- **Headings:** 600 weight, navy color
- **Body Text:** 400 weight, medium grey
- **Labels:** 500 weight, uppercase, letter-spacing

## 🔍 API Endpoints

### Vendor Intelligence APIs
- `GET /vendor-intelligence` - Dashboard page
- `GET|POST /api/vendor-intelligence-data` - Complete dashboard data
- `POST /api/vendor-comparison` - Specific vendor comparison
- `POST /api/cost-breakdown` - Cost analysis for vendors
- `POST /api/insights` - Smart insights with filters
- `GET /api/schema-summary` - Data schema information

### Legacy WELL Building APIs (Preserved)
- `GET /` - Original WELL dashboard
- `GET /api/dashboard-data` - WELL building data
- `POST /api/update-lighting` - Lighting controls
- `POST /api/hvac-override` - HVAC controls
- `POST /api/submit-feedback` - Feedback submission

## 📱 Browser Support

- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## 🚀 Performance Optimizations

- **Client-side filtering:** Reduce server requests
- **Chart.js CDN:** Fast chart library loading
- **Responsive images:** Optimal loading across devices
- **Minimal dependencies:** Fast startup time

## 🔮 Future Enhancements

### Phase 2 Features
- [ ] Excel/CSV export functionality
- [ ] Advanced filtering (date ranges, budget sliders)
- [ ] Vendor performance forecasting
- [ ] Integration with procurement systems
- [ ] Email alerts for vendor issues
- [ ] Multi-currency support
- [ ] Vendor onboarding workflow

### Phase 3 Features
- [ ] Machine learning vendor recommendations
- [ ] Real-time pricing updates
- [ ] Contract management integration
- [ ] Mobile app version
- [ ] Multi-language support

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is proprietary software for internal use only.

---

**Built with ❤️ for smarter vendor intelligence**