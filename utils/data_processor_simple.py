import csv
import json
from datetime import datetime

class VendorDataProcessor:
    def __init__(self, data_path='data/'):
        self.data_path = data_path
        self.vendors = []
        self.products = []  
        self.commercials = []
        self.project_usage = []
        self.vendor_scores = []
        self.load_data()

    def load_csv(self, filename):
        """Load CSV file and return list of dicts"""
        try:
            with open(f"{self.data_path}{filename}", 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                return list(reader)
        except FileNotFoundError:
            print(f"❌ Warning: {filename} not found")
            return []
        except Exception as e:
            print(f"❌ Error loading {filename}: {e}")
            return []

    def load_data(self):
        """Load all CSV files"""
        try:
            self.vendors = self.load_csv('vendors.csv')
            self.products = self.load_csv('products.csv')
            self.commercials = self.load_csv('commercials.csv')
            self.project_usage = self.load_csv('project_usage.csv')
            self.vendor_scores = self.load_csv('vendor_scores.csv')
            print("✅ All CSV files loaded successfully")
        except Exception as e:
            print(f"❌ Error loading data: {e}")

    def get_schema_summary(self):
        """Return data schema summary"""
        categories = list(set([p.get('category', '') for p in self.products if p.get('category')]))
        cities = list(set([u.get('city', '') for u in self.project_usage if u.get('city')]))
        project_types = list(set([u.get('project_type', '') for u in self.project_usage if u.get('project_type')]))
        
        summary = {
            'vendors': {
                'count': len(self.vendors),
                'columns': list(self.vendors[0].keys()) if self.vendors else [],
                'categories': categories
            },
            'products': {
                'count': len(self.products),
                'columns': list(self.products[0].keys()) if self.products else [],
                'categories': categories
            },
            'commercials': {
                'count': len(self.commercials),
                'columns': list(self.commercials[0].keys()) if self.commercials else []
            },
            'project_usage': {
                'count': len(self.project_usage),
                'columns': list(self.project_usage[0].keys()) if self.project_usage else [],
                'cities': cities,
                'project_types': project_types
            },
            'vendor_scores': {
                'count': len(self.vendor_scores),
                'columns': list(self.vendor_scores[0].keys()) if self.vendor_scores else []
            }
        }
        return summary

    def safe_float(self, value, default=0.0):
        """Safely convert value to float"""
        try:
            return float(value) if value else default
        except (ValueError, TypeError):
            return default

    def safe_int(self, value, default=0):
        """Safely convert value to int"""
        try:
            return int(value) if value else default
        except (ValueError, TypeError):
            return default

    def get_kpi_data(self, filters=None):
        """Calculate KPI metrics with optional filters"""
        
        # Apply filters if provided
        filtered_commercials = self.commercials[:]
        filtered_products = self.products[:]
        filtered_usage = self.project_usage[:]
        
        if filters:
            if 'category' in filters and filters['category']:
                filtered_products = [p for p in filtered_products if p.get('category') == filters['category']]
                # Filter commercials based on filtered products
                product_ids = [p['product_id'] for p in filtered_products]
                filtered_commercials = [c for c in filtered_commercials if c.get('product_id') in product_ids]
            
            if 'city' in filters and filters['city']:
                filtered_usage = [u for u in filtered_usage if u.get('city') == filters['city']]
        
        # Calculate KPIs
        negotiated_prices = [self.safe_float(c.get('negotiated_price', 0)) for c in filtered_commercials]
        avg_negotiated_price = sum(negotiated_prices) / len(negotiated_prices) if negotiated_prices else 0
        
        lead_times = [self.safe_float(p.get('lead_time_days', 0)) for p in filtered_products]
        avg_lead_time = sum(lead_times) / len(lead_times) if lead_times else 0
        
        credit_periods = [self.safe_float(c.get('credit_period_days', 0)) for c in filtered_commercials]
        avg_credit_period = sum(credit_periods) / len(credit_periods) if credit_periods else 0
        
        # Vendor scores (overall average)
        final_scores = [self.safe_float(s.get('final_score', 0)) for s in self.vendor_scores]
        avg_vendor_score = sum(final_scores) / len(final_scores) if final_scores else 0
        
        # Repeat vendor usage percentage
        preferred_vendors = len([v for v in self.vendors if v.get('preferred_vendor', '').upper() == 'TRUE'])
        repeat_usage_pct = (preferred_vendors / len(self.vendors)) * 100 if self.vendors else 0
        
        # Average lighting cost per sq ft (filter for lighting category)
        lighting_products = [p for p in filtered_products if p.get('category', '').lower() == 'lighting']
        lighting_product_ids = [p['product_id'] for p in lighting_products]
        lighting_commercials = [c for c in filtered_commercials if c.get('product_id') in lighting_product_ids]
        
        if lighting_commercials:
            lighting_costs = [self.safe_float(c.get('negotiated_price', 0)) for c in lighting_commercials]
            # Assuming an average installation area of 1000 sq ft for calculation
            avg_lighting_cost_per_sqft = sum(lighting_costs) / len(lighting_costs) / 1000 if lighting_costs else 0
        else:
            avg_lighting_cost_per_sqft = 0
        
        # Average LPD for lighting products
        lighting_lpd_values = []
        for p in lighting_products:
            # Try to extract LPD from product specifications or use a calculated value
            lpd = self.safe_float(p.get('lpd', 0))  # Assuming LPD field exists
            if lpd == 0:
                # Calculate estimated LPD if not provided (sample calculation)
                wattage = self.safe_float(p.get('wattage', 30))  # Default 30W
                coverage_area = self.safe_float(p.get('coverage_area', 100))  # Default 100 sq ft
                lpd = wattage / coverage_area if coverage_area > 0 else 0.8
            lighting_lpd_values.append(lpd)
        
        avg_lpd = sum(lighting_lpd_values) / len(lighting_lpd_values) if lighting_lpd_values else 0.8
        
        return {
            'avg_negotiated_price': round(avg_negotiated_price, 0),
            'avg_lead_time': round(avg_lead_time, 1),
            'avg_vendor_score': round(avg_vendor_score, 2),
            'avg_credit_period': round(avg_credit_period, 0),
            'repeat_usage_pct': round(repeat_usage_pct, 1),
            'avg_lighting_cost_per_sqft': round(avg_lighting_cost_per_sqft, 2),
            'avg_lpd': round(avg_lpd, 2)
        }

    def get_vendor_comparison_data(self, vendor_ids=None):
        """Get vendor comparison matrix data"""
        if not vendor_ids:
            # Return all vendors, not just first 4
            vendor_ids = [v['vendor_id'] for v in self.vendors]
            
        comparison_data = []
        
        for vendor_id in vendor_ids:
            vendor_info = next((v for v in self.vendors if v['vendor_id'] == vendor_id), None)
            if not vendor_info:
                continue
                
            vendor_products = [p for p in self.products if p.get('vendor_id') == vendor_id]
            if not vendor_products:
                continue
                
            product_ids = [p['product_id'] for p in vendor_products]
            vendor_commercials = [c for c in self.commercials if c.get('product_id') in product_ids]
            vendor_score = next((s for s in self.vendor_scores if s.get('vendor_id') == vendor_id), {})
            
            # More lenient condition - we need at least vendor info and score data
            if not vendor_score:
                continue
                
            # Calculate averages (handle empty commercials gracefully)
            if vendor_commercials:
                prices = [self.safe_float(c.get('negotiated_price', 0)) for c in vendor_commercials]
                avg_price = sum(prices) / len(prices) if prices else 0
                
                discounts = [self.safe_float(c.get('discount_percent', 0)) for c in vendor_commercials]
                avg_discount = sum(discounts) / len(discounts) if discounts else 0
                
                credits = [self.safe_float(c.get('credit_period_days', 0)) for c in vendor_commercials]
                avg_credit = sum(credits) / len(credits) if credits else 0
            else:
                # Use default values if no commercial data
                avg_price = 0
                avg_discount = 0
                avg_credit = 0
                
            # Product averages (handle empty products gracefully)  
            if vendor_products:
                lead_times = [self.safe_float(p.get('lead_time_days', 0)) for p in vendor_products]
                avg_lead_time = sum(lead_times) / len(lead_times) if lead_times else 0
                
                warranties = [self.safe_float(p.get('warranty_years', 0)) for p in vendor_products]
                avg_warranty = sum(warranties) / len(warranties) if warranties else 0
            else:
                avg_lead_time = 0
                avg_warranty = 0
            
            comparison_data.append({
                'vendor_id': vendor_id,
                'vendor_name': vendor_info.get('vendor_name', ''),
                'category': vendor_info.get('category', ''),
                'brand_tier': vendor_info.get('brand_tier', ''),
                'preferred_vendor': vendor_info.get('preferred_vendor', '').upper() == 'TRUE',
                'avg_negotiated_price': round(avg_price, 0),
                'avg_discount_pct': round(avg_discount, 1),
                'avg_credit_period': round(avg_credit, 0),
                'avg_lead_time': round(avg_lead_time, 1),
                'avg_warranty': round(avg_warranty, 1),
                'reliability_rating': self.safe_float(vendor_info.get('reliability_rating', 0)),
                'after_sales_rating': self.safe_float(vendor_info.get('after_sales_rating', 0)),
                'final_score': self.safe_float(vendor_score.get('final_score', 0)),
                'cost_score': self.safe_float(vendor_score.get('cost_score', 0)),
                'performance_score': self.safe_float(vendor_score.get('performance_score', 0)),
                'reliability_score': self.safe_float(vendor_score.get('reliability_score', 0)),
                'service_score': self.safe_float(vendor_score.get('service_score', 0)),
                'speed_score': self.safe_float(vendor_score.get('speed_score', 0))
            })
                
        return comparison_data

    def get_filter_data(self):
        """Get unique values for all filter options"""
        categories = list(set([p.get('category', '') for p in self.products if p.get('category')]))
        cities = list(set([u.get('city', '') for u in self.project_usage if u.get('city')]))
        project_types = list(set([u.get('project_type', '') for u in self.project_usage if u.get('project_type')]))
        certifications = list(set([u.get('certification', '') for u in self.project_usage if u.get('certification')]))
        brand_tiers = list(set([v.get('brand_tier', '') for v in self.vendors if v.get('brand_tier')]))
        
        vendor_names = [{'vendor_id': v.get('vendor_id', ''), 'vendor_name': v.get('vendor_name', '')} 
                       for v in self.vendors if v.get('vendor_id')]
        
        return {
            'categories': sorted(categories),
            'cities': sorted(cities),
            'project_types': sorted(project_types),
            'certifications': sorted(certifications),
            'brand_tiers': sorted(brand_tiers),
            'vendor_names': vendor_names
        }

    def get_cost_breakdown_data(self, vendor_ids=None):
        """Get cost breakdown data for selected vendors"""
        if not vendor_ids:
            # Return all vendors, not just first 3
            vendor_ids = [v['vendor_id'] for v in self.vendors]
            
        cost_data = []
        for vendor_id in vendor_ids:
            vendor_info = next((v for v in self.vendors if v['vendor_id'] == vendor_id), None)
            if not vendor_info:
                continue
                
            vendor_products = [p for p in self.products if p.get('vendor_id') == vendor_id]
            product_ids = [p['product_id'] for p in vendor_products]
            vendor_commercials = [c for c in self.commercials if c.get('product_id') in product_ids]
            
            if vendor_commercials:
                product_costs = [self.safe_float(c.get('negotiated_price', 0)) for c in vendor_commercials]
                installation_costs = [self.safe_float(c.get('installation_cost', 0)) for c in vendor_commercials]
                maintenance_costs = [self.safe_float(c.get('maintenance_cost_annual', 0)) for c in vendor_commercials]
                
                avg_product_cost = sum(product_costs) / len(product_costs) if product_costs else 0
                avg_installation = sum(installation_costs) / len(installation_costs) if installation_costs else 0
                avg_maintenance = sum(maintenance_costs) / len(maintenance_costs) if maintenance_costs else 0
                
                cost_data.append({
                    'vendor_id': vendor_id,
                    'vendor_name': vendor_info.get('vendor_name', ''),
                    'product_cost': round(avg_product_cost, 0),
                    'installation_cost': round(avg_installation, 0),
                    'maintenance_cost': round(avg_maintenance, 0)
                })
                
        return cost_data

    def get_historical_trends(self):
        """Get historical trends data"""
        # Group by vendor and calculate usage stats
        vendor_usage = {}
        
        for usage in self.project_usage:
            vendor_id = usage.get('vendor_id', '')
            if vendor_id not in vendor_usage:
                vendor_usage[vendor_id] = {
                    'usage_id': 0,
                    'total_value': 0,
                    'qty': 0
                }
            
            vendor_usage[vendor_id]['usage_id'] += 1
            vendor_usage[vendor_id]['total_value'] += self.safe_float(usage.get('total_value', 0))
            vendor_usage[vendor_id]['qty'] += self.safe_int(usage.get('qty', 0))
        
        # Add vendor names
        usage_trends = []
        for vendor_id, stats in vendor_usage.items():
            vendor_info = next((v for v in self.vendors if v['vendor_id'] == vendor_id), None)
            if vendor_info:
                usage_trends.append({
                    'vendor_id': vendor_id,
                    'vendor_name': vendor_info.get('vendor_name', ''),
                    'usage_id': stats['usage_id'],
                    'total_value': round(stats['total_value'] / stats['usage_id']) if stats['usage_id'] > 0 else 0,
                    'qty': stats['qty']
                })
        
        return sorted(usage_trends, key=lambda x: x['usage_id'], reverse=True)

    def get_insights(self, filters=None):
        """Generate intelligent insights"""
        insights = []
        
        # Get comparison data
        comparison_data = self.get_vendor_comparison_data()
        if not comparison_data:
            return insights
        
        # Calculate value score for each vendor
        for vendor in comparison_data:
            if vendor['avg_negotiated_price'] > 0:
                vendor['value_score'] = vendor['final_score'] / vendor['avg_negotiated_price'] * 10000
            else:
                vendor['value_score'] = 0
        
        # Best value vendor
        best_value = max(comparison_data, key=lambda x: x['value_score'])
        insights.append({
            'type': 'best_value',
            'title': 'Best Value Vendor',
            'message': f"{best_value['vendor_name']} offers the best value with score {best_value['final_score']:.1f} at ₹{best_value['avg_negotiated_price']:,.0f}",
            'vendor': best_value['vendor_name']
        })
        
        # Lowest cost option
        lowest_cost = min(comparison_data, key=lambda x: x['avg_negotiated_price'])
        insights.append({
            'type': 'lowest_cost',
            'title': 'Lowest Cost Option',
            'message': f"{lowest_cost['vendor_name']} has the most competitive pricing at ₹{lowest_cost['avg_negotiated_price']:,.0f}",
            'vendor': lowest_cost['vendor_name']
        })
        
        # Fastest execution
        fastest_execution = min(comparison_data, key=lambda x: x['avg_lead_time'])
        insights.append({
            'type': 'fastest_execution',
            'title': 'Fastest Execution',
            'message': f"{fastest_execution['vendor_name']} delivers fastest with {fastest_execution['avg_lead_time']:.1f} days lead time",
            'vendor': fastest_execution['vendor_name']
        })
        
        # Risk assessment
        risk_vendors = [u['vendor_id'] for u in self.project_usage if u.get('issue_flag', '').upper() == 'TRUE']
        if risk_vendors:
            risk_vendor_names = []
            for vid in set(risk_vendors):  # Remove duplicates
                vendor_info = next((v for v in self.vendors if v['vendor_id'] == vid), None)
                if vendor_info:
                    risk_vendor_names.append(vendor_info.get('vendor_name', ''))
            
            if risk_vendor_names:
                insights.append({
                    'type': 'risk_alert',
                    'title': 'Risk Alert',
                    'message': f"Consider alternatives to: {', '.join(risk_vendor_names[:3])} due to past delivery issues",
                    'vendor': 'Multiple'
                })
        
        return insights