import pandas as pd
from typing import Dict, List, Optional
from src.schemas.data_summary import DataSummary, CampaignDailyMetrics, CreativeInfo
from src.utils.logging_utils import log

class DataAgent:
    """
    Responsible for loading, cleaning, and aggregating Facebook Ads data.
    """
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.df = None

    def load_data(self):
        """Loads the CSV dataset into a Pandas DataFrame."""
        try:
            log.info(f"Loading data from {self.csv_path}")
            self.df = pd.read_csv(self.csv_path)
            self.df['date'] = pd.to_datetime(self.df['date'])
            log.info(f"Loaded {len(self.df)} rows.")
        except Exception as e:
            log.error(f"Failed to load data: {e}")
            raise

    def get_summary(self, campaign_name: Optional[str] = None) -> DataSummary:
        """
        Generates a summary of performance metrics, optionally filtered by campaign.
        """
        if self.df is None:
            self.load_data()

        df_filtered = self.df.copy()
        if campaign_name:
            df_filtered = df_filtered[df_filtered['campaign_name'] == campaign_name]

        if df_filtered.empty:
            log.warning(f"No data found for campaign: {campaign_name}")
            return DataSummary(
                total_spend=0.0, total_impressions=0, total_clicks=0,
                avg_ctr=0.0, total_purchases=0, total_revenue=0.0, avg_roas=0.0
            )

        # Calculate high-level metrics
        total_spend = df_filtered['spend'].sum()
        total_impressions = df_filtered['impressions'].sum()
        total_clicks = df_filtered['clicks'].sum()
        total_purchases = df_filtered['purchases'].sum()
        total_revenue = df_filtered['revenue'].sum()
        
        avg_ctr = (total_clicks / total_impressions) if total_impressions > 0 else 0.0
        avg_roas = (total_revenue / total_spend) if total_spend > 0 else 0.0

        # Daily Breakdown
        daily_metrics = {}
        daily_groups = df_filtered.groupby(['campaign_name', 'date']).agg({
            'spend': 'sum', 'impressions': 'sum', 'clicks': 'sum',
            'purchases': 'sum', 'revenue': 'sum'
        }).reset_index()

        for _, row in daily_groups.iterrows():
            camp = row['campaign_name']
            if camp not in daily_metrics:
                daily_metrics[camp] = []
            
            ctr = row['clicks'] / row['impressions'] if row['impressions'] > 0 else 0
            roas = row['revenue'] / row['spend'] if row['spend'] > 0 else 0
            
            daily_metrics[camp].append(CampaignDailyMetrics(
                date=row['date'].strftime('%Y-%m-%d'),
                spend=row['spend'],
                impressions=row['impressions'],
                clicks=row['clicks'],
                ctr=ctr,
                purchases=row['purchases'],
                revenue=row['revenue'],
                roas=roas
            ))

        # Top Creatives
        creative_groups = df_filtered.groupby('creative_message').agg({
            'impressions': 'sum', 'clicks': 'sum', 'revenue': 'sum'
        }).reset_index()
        
        top_creatives = []
        for _, row in creative_groups.iterrows():
            ctr = row['clicks'] / row['impressions'] if row['impressions'] > 0 else 0
            top_creatives.append(CreativeInfo(
                creative_message=row['creative_message'],
                ctr=ctr,
                revenue=row['revenue']
            ))
        
        # Sort by revenue descending
        top_creatives.sort(key=lambda x: x.revenue, reverse=True)

        # Audience Breakdown
        audience_breakdown = {}
        aud_groups = df_filtered.groupby('audience_type').agg({
            'spend': 'sum', 'revenue': 'sum', 'clicks': 'sum', 'impressions': 'sum'
        })
        for aud, row in aud_groups.iterrows():
            ctr = row['clicks'] / row['impressions'] if row['impressions'] > 0 else 0
            roas = row['revenue'] / row['spend'] if row['spend'] > 0 else 0
            audience_breakdown[aud] = {"ctr": ctr, "roas": roas}

        # Platform Breakdown
        platform_breakdown = {}
        plat_groups = df_filtered.groupby('platform').agg({
            'spend': 'sum', 'revenue': 'sum', 'clicks': 'sum', 'impressions': 'sum'
        })
        for plat, row in plat_groups.iterrows():
            ctr = row['clicks'] / row['impressions'] if row['impressions'] > 0 else 0
            roas = row['revenue'] / row['spend'] if row['spend'] > 0 else 0
            platform_breakdown[plat] = {"ctr": ctr, "roas": roas}

        return DataSummary(
            total_spend=total_spend,
            total_impressions=total_impressions,
            total_clicks=total_clicks,
            avg_ctr=avg_ctr,
            total_purchases=total_purchases,
            total_revenue=total_revenue,
            avg_roas=avg_roas,
            campaign_daily=daily_metrics,
            top_creatives=top_creatives,
            audience_breakdown=audience_breakdown,
            platform_breakdown=platform_breakdown
        )
