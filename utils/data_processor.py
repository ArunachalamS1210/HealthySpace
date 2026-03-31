import pandas as pd
import json
from datetime import datetime

class VendorDataProcessor:
    def __init__(self, data_path='data/'):
        self.data_path = data_path
        self.vendors = None
        self.products = None  
        self.commercials = None
        self.project_usage = None
        self.vendor_scores = None
        self.load_data()

    def load_data(self):
        """Load all CSV files"""
        try:
            self.vendors = pd.read_csv(f"{self.data_path}vendors.csv")
            self.products = pd.read_csv(f"{self.data_path}products.csv") 
            self.commercials = pd.read_csv(f"{self.data_path}commercials.csv")
            self.project_usage = pd.read_csv(f"{self.data_path}project_usage.csv")
            self.vendor_scores = pd.read_csv(f"{self.data_path}vendor_scores.csv")
            print("✅ All CSV files loaded successfully")
        except Exception as e:
            print(f"❌ Error loading data: {e}")

    def get_schema_summary(self):
        """Return data schema summary"""
        summary = {
            'vendors': {
                'count': len(self.vendors),
                'columns': list(self.vendors.columns),
                'categories': self.vendors['category'].unique().tolist()
            },
            'products': {
                'count': len(self.products),
                'columns': list(self.products.columns),
                'categories': self.products['category'].unique().tolist()
            },
            'commercials': {
                'count': len(self.commercials),
                'columns': list(self.commercials.columns)
            },
            'project_usage': {
                'count': len(self.project_usage),  
                'columns': list(self.project_usage.columns),
                'cities': self.project_usage['city'].unique().tolist(),
                'project_types': self.project_usage['project_type'].unique().tolist()
            },
            'vendor_scores': {
                'count': len(self.vendor_scores),
                'columns': list(self.vendor_scores.columns)
            }
        }
        return summary

    def get_kpi_data(self, filters=None):
        """Calculate KPI metrics with optional filters"""
        
        # Apply filters if provided
        filtered_commercials = self.commercials
        filtered_products = self.products
        filtered_usage = self.project_usage
        
        if filters:
            if 'category' in filters and filters['category']:
                filtered_products = filtered_products[filtered_products['category'] == filters['category']]
                # Filter commercials based on filtered products
                product_ids = filtered_products['product_id'].tolist()
                filtered_commercials = filtered_commercials[filtered_commercials['product_id'].isin(product_ids)]
            
            if 'city' in filters and filters['city']:
                filtered_usage = filtered_usage[filtered_usage['city'] == filters['city']]
        
        # Calculate KPIs
        avg_negotiated_price = filtered_commercials['negotiated_price'].mean()
        avg_lead_time = filtered_products['lead_time_days'].mean()
        avg_credit_period = filtered_commercials['credit_period_days'].mean()
        
        # Vendor scores (overall average)
        avg_vendor_score = self.vendor_scores['final_score'].mean()
        
        # Repeat vendor usage percentage
        total_projects = len(filtered_usage)
        preferred_vendors = len(self.vendors[self.vendors['preferred_vendor'] == True])
        repeat_usage_pct = (preferred_vendors / len(self.vendors)) * 100 if len(self.vendors) > 0 else 0
        
        return {
            'avg_negotiated_price': round(avg_negotiated_price, 0) if not pd.isna(avg_negotiated_price) else 0,
            'avg_lead_time': round(avg_lead_time, 1) if not pd.isna(avg_lead_time) else 0,
            'avg_vendor_score': round(avg_vendor_score, 2) if not pd.isna(avg_vendor_score) else 0,
            'avg_credit_period': round(avg_credit_period, 0) if not pd.isna(avg_credit_period) else 0,
            'repeat_usage_pct': round(repeat_usage_pct, 1)
        }

    def get_vendor_comparison_data(self, vendor_ids=None):
        """Get vendor comparison matrix data"""
        if not vendor_ids:
            vendor_ids = self.vendors['vendor_id'].head(4).tolist()  # Default to top 4
            
        comparison_data = []
        
        for vendor_id in vendor_ids:
            vendor_info = self.vendors[self.vendors['vendor_id'] == vendor_id].iloc[0]
            vendor_products = self.products[self.products['vendor_id'] == vendor_id]
            vendor_commercials = self.commercials[self.commercials['product_id'].isin(vendor_products['product_id'])]
            vendor_score = self.vendor_scores[self.vendor_scores['vendor_id'] == vendor_id]
            
            if len(vendor_commercials) > 0 and len(vendor_score) > 0:
                avg_price = vendor_commercials['negotiated_price'].mean()
                avg_discount = vendor_commercials['discount_percent'].mean() 
                avg_credit = vendor_commercials['credit_period_days'].mean()
                avg_lead_time = vendor_products['lead_time_days'].mean()
                avg_warranty = vendor_products['warranty_years'].mean()
                
                score_data = vendor_score.iloc[0]
                
                comparison_data.append({
                    'vendor_id': vendor_id,
                    'vendor_name': vendor_info['vendor_name'],
                    'category': vendor_info['category'],
                    'brand_tier': vendor_info['brand_tier'],
                    'preferred_vendor': vendor_info['preferred_vendor'],
                    'avg_negotiated_price': round(avg_price, 0) if not pd.isna(avg_price) else 0,
                    'avg_discount_pct': round(avg_discount, 1) if not pd.isna(avg_discount) else 0,
                    'avg_credit_period': round(avg_credit, 0) if not pd.isna(avg_credit) else 0,
                    'avg_lead_time': round(avg_lead_time, 1) if not pd.isna(avg_lead_time) else 0,
                    'avg_warranty': round(avg_warranty, 1) if not pd.isna(avg_warranty) else 0,
                    'reliability_rating': vendor_info['reliability_rating'],
                    'after_sales_rating': vendor_info['after_sales_rating'],
                    'final_score': score_data['final_score'],
                    'cost_score': score_data['cost_score'],
                    'performance_score': score_data['performance_score'],
                    'reliability_score': score_data['reliability_score'],
                    'service_score': score_data['service_score'],
                    'speed_score': score_data['speed_score']
                })
                
        return comparison_data

    def get_filter_data(self):
        """Get unique values for all filter options"""
        return {
            'categories': self.products['category'].unique().tolist(),
            'cities': self.project_usage['city'].unique().tolist(),
            'project_types': self.project_usage['project_type'].unique().tolist(),
            'certifications': self.project_usage['certification'].unique().tolist(),
            'brand_tiers': self.vendors['brand_tier'].unique().tolist(),
            'vendor_names': self.vendors[['vendor_id', 'vendor_name']].to_dict('records')
        }

    def get_cost_breakdown_data(self, vendor_ids=None):
        """Get cost breakdown data for selected vendors"""
        if not vendor_ids:
            vendor_ids = self.vendors['vendor_id'].head(3).tolist()
            
        cost_data = []
        for vendor_id in vendor_ids:
            vendor_info = self.vendors[self.vendors['vendor_id'] == vendor_id].iloc[0]
            vendor_products = self.products[self.products['vendor_id'] == vendor_id]
            vendor_commercials = self.commercials[self.commercials['product_id'].isin(vendor_products['product_id'])]
            
            if len(vendor_commercials) > 0:
                avg_product_cost = vendor_commercials['negotiated_price'].mean()
                avg_installation = vendor_commercials['installation_cost'].mean()
                avg_maintenance = vendor_commercials['maintenance_cost_annual'].mean()
                
                cost_data.append({
                    'vendor_name': vendor_info['vendor_name'],
                    'product_cost': round(avg_product_cost, 0) if not pd.isna(avg_product_cost) else 0,
                    'installation_cost': round(avg_installation, 0) if not pd.isna(avg_installation) else 0,
                    'maintenance_cost': round(avg_maintenance, 0) if not pd.isna(avg_maintenance) else 0
                })
                
        return cost_data

    def get_historical_trends(self):
        """Get historical trends data"""
        # Group by project completion and calculate averages
        usage_by_vendor = self.project_usage.groupby('vendor_id').agg({
            'total_value': 'mean',
            'qty': 'sum',
            'usage_id': 'count'
        }).round(0).reset_index()
        
        # Add vendor names
        usage_trends = usage_by_vendor.merge(
            self.vendors[['vendor_id', 'vendor_name']], 
            on='vendor_id'
        )
        
        return usage_trends.to_dict('records')

    def get_insights(self, filters=None):
        """Generate intelligent insights"""
        insights = []
        
        # Best value vendor (high score, competitive price)
        comparison_data = self.get_vendor_comparison_data()
        if comparison_data:
            # Calculate value score (final_score / avg_price * 10000 for normalization)
            for vendor in comparison_data:
                if vendor['avg_negotiated_price'] > 0:
                    vendor['value_score'] = vendor['final_score'] / vendor['avg_negotiated_price'] * 10000
                else:
                    vendor['value_score'] = 0
            
            best_value = max(comparison_data, key=lambda x: x['value_score'])
            insights.append({
                'type': 'best_value',
                'title': 'Best Value Vendor',
                'message': f"{best_value['vendor_name']} offers the best value with score {best_value['final_score']} at ₹{best_value['avg_negotiated_price']:,.0f}",
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
            
            # Risk assessment - vendors with issues
            risk_vendors = self.project_usage[self.project_usage['issue_flag'] == True]['vendor_id'].unique()
            if len(risk_vendors) > 0:
                risk_vendor_names = []
                for vid in risk_vendors:
                    vendor_name = self.vendors[self.vendors['vendor_id'] == vid]['vendor_name'].iloc[0]
                    risk_vendor_names.append(vendor_name)
                
                insights.append({
                    'type': 'risk_alert',
                    'title': 'Risk Alert',
                    'message': f"Consider alternatives to: {', '.join(risk_vendor_names[:3])} due to past delivery issues",
                    'vendor': 'Multiple'
                })
        
        return insights