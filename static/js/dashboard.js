// Vendor Intelligence Dashboard JavaScript

let dashboardData = {};
let currentFilters = {};
let selectedVendors = [];
let charts = {};

// Initialize dashboard when page loads
document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
});

async function initializeDashboard() {
    try {
        // Load initial data
        await loadDashboardData();
        
        // Populate filter dropdowns
        populateFilters();
        
        // Load initial KPIs
        updateKPIs();
        
        // Setup default vendor comparison (top 4 vendors)
        setupDefaultVendorComparison();
        
        // Initialize charts
        initializeCharts();
        
        // Load insights
        loadInsights();
        
        console.log('✅ Dashboard initialized successfully');
    } catch (error) {
        console.error('❌ Error initializing dashboard:', error);
        showErrorMessage('Failed to load dashboard data');
    }
}

async function loadDashboardData() {
    const response = await fetch('/api/vendor-intelligence-data');
    if (!response.ok) {
        throw new Error('Failed to fetch dashboard data');
    }
    dashboardData = await response.json();
}

function populateFilters() {
    if (!dashboardData.filter_data) return;
    
    const filterData = dashboardData.filter_data;
    
    // Populate cities
    populateSelect('city-filter', filterData.cities);
    
    // Populate project types  
    populateSelect('project-type-filter', filterData.project_types);
    
    // Populate certifications
    populateSelect('certification-filter', filterData.certifications);
}

function populateSelect(elementId, options) {
    const select = document.getElementById(elementId);
    if (!select || !options) return;
    
    // Clear existing options (except first one)
    while (select.children.length > 1) {
        select.removeChild(select.lastChild);
    }
    
    // Add new options
    options.forEach(option => {
        const optionElement = document.createElement('option');
        optionElement.value = option;
        optionElement.textContent = option;
        select.appendChild(optionElement);
    });
}

function updateKPIs() {
    if (!dashboardData.kpi_data) return;
    
    const kpis = dashboardData.kpi_data;
    
    document.getElementById('avg-price').textContent = '₹' + (kpis.avg_negotiated_price || 0).toLocaleString();
    document.getElementById('avg-lead-time').textContent = kpis.avg_lead_time || 0;
    document.getElementById('avg-vendor-score').textContent = (kpis.avg_vendor_score || 0).toFixed(1);
    document.getElementById('avg-credit-period').textContent = kpis.avg_credit_period || 0;
    document.getElementById('repeat-usage').textContent = (kpis.repeat_usage_pct || 0).toFixed(1) + '%';
    document.getElementById('avg-lighting-cost').textContent = '₹' + (kpis.avg_lighting_cost_per_sqft || 0).toFixed(2);
    document.getElementById('avg-lpd').textContent = (kpis.avg_lpd || 0).toFixed(1);
}

function setupDefaultVendorComparison() {
    if (!dashboardData.comparison_data || dashboardData.comparison_data.length === 0) return;
    
    // Select first 4 vendors by default from available comparison data  
    selectedVendors = dashboardData.comparison_data.slice(0, 4).map(v => v.vendor_id);
    
    // Create vendor selection checkboxes
    createVendorSelection();
    
    // Build comparison table
    buildComparisonTable();
}

function createVendorSelection() {
    const container = document.getElementById('vendor-select');
    if (!container || !dashboardData.filter_data?.vendor_names) return;
    
    container.innerHTML = '';
    
    dashboardData.filter_data.vendor_names.forEach(vendor => {
        const checkboxDiv = document.createElement('div');
        checkboxDiv.className = 'vendor-checkbox';
        
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.id = `vendor-${vendor.vendor_id}`;
        checkbox.value = vendor.vendor_id;
        checkbox.checked = selectedVendors.includes(vendor.vendor_id);
        checkbox.addEventListener('change', handleVendorSelection);
        
        const label = document.createElement('label');
        label.htmlFor = `vendor-${vendor.vendor_id}`;
        label.textContent = vendor.vendor_name;
        
        checkboxDiv.appendChild(checkbox);
        checkboxDiv.appendChild(label);
        container.appendChild(checkboxDiv);
    });
}

function handleVendorSelection(event) {
    const vendorId = event.target.value;
    
    if (event.target.checked) {
        if (selectedVendors.length < 4) {
            selectedVendors.push(vendorId);
        } else {
            event.target.checked = false;
            alert('Maximum 4 vendors can be selected for comparison');
            return;
        }
    } else {
        selectedVendors = selectedVendors.filter(id => id !== vendorId);
    }
    
    buildComparisonTable();
    updateCharts();
}

function buildComparisonTable() {
    if (!dashboardData.comparison_data || selectedVendors.length === 0) return;
    
    const filteredData = dashboardData.comparison_data.filter(vendor => 
        selectedVendors.includes(vendor.vendor_id)
    );
    
    // Build header
    const header = document.getElementById('comparison-header');
    header.innerHTML = '<th>Metrics</th>';
    filteredData.forEach(vendor => {
        const th = document.createElement('th');
        th.innerHTML = `<div><strong>${vendor.vendor_name}</strong><br><small>${vendor.category}</small></div>`;
        header.appendChild(th);
    });
    
    // Build body
    const tbody = document.getElementById('comparison-body');
    tbody.innerHTML = '';
    
    const metrics = [
        { key: 'avg_negotiated_price', label: 'Negotiated Price', format: 'currency' },
        { key: 'avg_discount_pct', label: 'Discount %', format: 'percentage' },
        { key: 'avg_credit_period', label: 'Credit Period', format: 'days' },
        { key: 'avg_lead_time', label: 'Lead Time', format: 'days' },
        { key: 'avg_warranty', label: 'Warranty', format: 'years' },
        { key: 'reliability_rating', label: 'Reliability', format: 'score' },
        { key: 'after_sales_rating', label: 'After Sales', format: 'score' },
        { key: 'final_score', label: 'Final Score', format: 'score' }
    ];
    
    metrics.forEach(metric => {
        const row = document.createElement('tr');
        
        // Metric label
        const labelCell = document.createElement('td');
        labelCell.textContent = metric.label;
        labelCell.style.fontWeight = '600';
        row.appendChild(labelCell);
        
        // Vendor values
        filteredData.forEach(vendor => {
            const valueCell = document.createElement('td');
            const value = vendor[metric.key];
            valueCell.innerHTML = formatValue(value, metric.format);
            
            // Add score indicator for scores
            if (metric.format === 'score') {
                valueCell.innerHTML += getScoreIndicator(value);
            }
            
            row.appendChild(valueCell);
        });
        
        tbody.appendChild(row);
    });
}

function formatValue(value, format) {
    if (value === null || value === undefined) return 'N/A';
    
    switch (format) {
        case 'currency':
            return '₹' + value.toLocaleString();
        case 'percentage':
            return value.toFixed(1) + '%';
        case 'days':
            return value + ' days';
        case 'years':
            return value + ' years';
        case 'score':
            return value.toFixed(1);
        default:
            return value;
    }
}

function getScoreIndicator(score) {
    let className = 'score-poor';
    if (score >= 8.5) className = 'score-excellent';
    else if (score >= 7.5) className = 'score-good';
    else if (score >= 6.5) className = 'score-average';
    
    return `<span class="score-indicator ${className}"></span>`;
}

function initializeCharts() {
    initializeCostChart();
    initializePerformanceChart();
    initializeHistoricalChart();
}

function initializeCostChart() {
    const ctx = document.getElementById('cost-chart');
    if (!ctx || !dashboardData.cost_data || selectedVendors.length === 0) return;
    
    // Filter cost data for selected vendors
    const costData = dashboardData.cost_data.filter(vendor => 
        selectedVendors.includes(vendor.vendor_id)
    ).slice(0, 4); // Max 4 vendors
    
    if (costData.length === 0) return; // No data to show
    
    charts.costChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: costData.map(d => d.vendor_name),
            datasets: [
                {
                    label: 'Product Cost',
                    data: costData.map(d => d.product_cost),
                    backgroundColor: 'rgba(0, 139, 139, 0.7)',
                    borderColor: 'rgba(0, 139, 139, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Installation Cost',
                    data: costData.map(d => d.installation_cost),
                    backgroundColor: 'rgba(30, 58, 95, 0.7)',
                    borderColor: 'rgba(30, 58, 95, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Annual Maintenance',
                    data: costData.map(d => d.maintenance_cost),
                    backgroundColor: 'rgba(108, 117, 125, 0.7)',
                    borderColor: 'rgba(108, 117, 125, 1)',
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return '₹' + value.toLocaleString();
                        }
                    }
                }
            },
            plugins: {
                legend: {
                    position: 'top'
                }
            }
        }
    });
}

function initializePerformanceChart() {
    const ctx = document.getElementById('performance-chart');
    if (!ctx || !dashboardData.comparison_data || selectedVendors.length === 0) return;
    
    // Filter performance data for selected vendors
    const performanceData = dashboardData.comparison_data.filter(vendor => 
        selectedVendors.includes(vendor.vendor_id)
    );
    
    if (performanceData.length === 0) return; // No data to show
    
    charts.performanceChart = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['Cost Score', 'Performance', 'Reliability', 'Service', 'Speed'],
            datasets: performanceData.map((vendor, index) => ({
                label: vendor.vendor_name,
                data: [
                    vendor.cost_score,
                    vendor.performance_score,
                    vendor.reliability_score,
                    vendor.service_score,
                    vendor.speed_score
                ],
                backgroundColor: `rgba(${index * 60}, 139, 139, 0.2)`,
                borderColor: `rgba(${index * 60}, 139, 139, 1)`,
                borderWidth: 2,
                pointBackgroundColor: `rgba(${index * 60}, 139, 139, 1)`
            }))
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    beginAtZero: true,
                    max: 10,
                    ticks: {
                        stepSize: 2
                    }
                }
            },
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

function initializeHistoricalChart() {
    const ctx = document.getElementById('historical-chart');
    if (!ctx || !dashboardData.historical_data || selectedVendors.length === 0) return;
    
    // Filter historical data for selected vendors
    const historicalData = dashboardData.historical_data.filter(vendor => 
        selectedVendors.includes(vendor.vendor_id)
    ).slice(0, 6); // Max 6 vendors for readability
    
    if (historicalData.length === 0) return; // No data to show
    
    charts.historicalChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: historicalData.map(d => d.vendor_name),
            datasets: [
                {
                    label: 'Project Count',
                    data: historicalData.map(d => d.usage_id),
                    backgroundColor: 'rgba(0, 139, 139, 0.1)',
                    borderColor: 'rgba(0, 139, 139, 1)',
                    borderWidth: 2,
                    fill: true
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

function loadInsights() {
    const container = document.getElementById('insights-list');
    if (!container || !dashboardData.insights) return;
    
    container.innerHTML = '';
    
    dashboardData.insights.forEach(insight => {
        const insightDiv = document.createElement('div');
        insightDiv.className = 'insight-item';
        
        insightDiv.innerHTML = `
            <div class="insight-title">${insight.title}</div>
            <div class="insight-message">${insight.message}</div>
        `;
        
        container.appendChild(insightDiv);
    });
}

async function applyFilters() {
    // Collect filter values
    currentFilters = {
        category: document.getElementById('category-filter').value,
        city: document.getElementById('city-filter').value,
        project_type: document.getElementById('project-type-filter').value,
        certification: document.getElementById('certification-filter').value,
        preferred_vendor: document.getElementById('preferred-vendor-filter').value
    };
    
    // Remove empty filters
    Object.keys(currentFilters).forEach(key => {
        if (!currentFilters[key]) delete currentFilters[key];
    });
    
    try {
        // Reload data with filters
        const response = await fetch('/api/vendor-intelligence-data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ filters: currentFilters })
        });
        
        if (!response.ok) throw new Error('Failed to apply filters');
        
        dashboardData = await response.json();
        
        // Update all components
        updateKPIs();
        createVendorSelection();
        buildComparisonTable();
        updateCharts();
        loadInsights();
        
        console.log('✅ Filters applied successfully');
    } catch (error) {
        console.error('❌ Error applying filters:', error);
        showErrorMessage('Failed to apply filters');
    }
}

function updateCharts() {
    // Destroy existing charts
    Object.values(charts).forEach(chart => {
        if (chart) chart.destroy();
    });
    
    // Reinitialize charts
    initializeCharts();
}

function showErrorMessage(message) {
    // Create a simple error notification
    const errorDiv = document.createElement('div');
    errorDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #dc3545;
        color: white;
        padding: 15px;
        border-radius: 5px;
        z-index: 1000;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    `;
    errorDiv.textContent = message;
    
    document.body.appendChild(errorDiv);
    
    // Remove after 5 seconds
    setTimeout(() => {
        if (errorDiv.parentNode) {
            errorDiv.parentNode.removeChild(errorDiv);
        }
    }, 5000);
}

// Utility functions for future expansion
function exportData() {
    // Future: Export current view data to CSV/Excel
    console.log('Export functionality - Coming soon');
}

function refreshData() {
    // Refresh data without filters
    currentFilters = {};
    initializeDashboard();
}