# Data Documentation

This directory contains datasets for the Kasparro Agentic Facebook Performance Analyst.

## `synthetic_fb_ads_undergarments.csv`
A synthetic dataset containing Facebook Ads performance data for an undergarments brand.

### Columns
- `campaign_name`: Name of the ad campaign.
- `adset_name`: Name of the ad set.
- `date`: Date of the metrics (YYYY-MM-DD).
- `spend`: Amount spent in USD.
- `impressions`: Number of times ads were shown.
- `clicks`: Number of clicks on the ads.
- `ctr`: Click-through rate (clicks / impressions).
- `purchases`: Number of completed purchases.
- `revenue`: Total revenue generated.
- `roas`: Return on Ad Spend (revenue / spend).
- `creative_type`: Format of the ad (Image, Video, Carousel).
- `creative_message`: The main text/headline of the ad.
- `audience_type`: Targeting category (Broad, Retargeting, Lookalike).
- `platform`: Ad placement platform (Facebook, Instagram).
- `country`: Target country.

## Usage
To use your own data, place a CSV file here and update `config/config.yaml`:
```yaml
paths:
  data_csv: "data/your_file.csv"
```
