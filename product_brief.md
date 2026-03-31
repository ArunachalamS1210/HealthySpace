# Vendor Intelligence Dashboard MVP

## Goal
Build a dashboard for selecting vendors and products across Lighting, Air Quality, Automation, and Water systems for wellness-oriented projects.

## Users
- Founder / business team
- Project estimator
- Procurement lead
- Design/specification lead

## Core decisions supported
1. Which vendor is best for this project?
2. What will it cost?
3. Which option has lower execution risk?
4. Which vendor gives better commercial terms?

## Filters
- Project type
- City
- Category
- Certification goal
- Budget range
- Preferred vendor
- Brand tier

## KPI cards
- Average negotiated price
- Average lead time
- Average vendor score
- Repeat vendor usage
- Average credit period

## Main visuals
- Vendor comparison table
- Cost breakdown chart
- Vendor score radar/bar
- Historical price trend
- Project usage frequency

## Scoring logic
Final score =
30% cost +
25% performance +
20% reliability +
15% service +
10% speed

## Data Structure
- vendors.csv: Core vendor information
- products.csv: Product specifications and details
- commercials.csv: Pricing and commercial terms
- project_usage.csv: Historical project performance
- vendor_scores.csv: Calculated vendor performance scores