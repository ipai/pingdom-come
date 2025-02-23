from datetime import datetime, timedelta

from sqlalchemy import select
from temporalio import activity, workflow
from temporalio.common import RetryPolicy

from ..core.database import get_session
from ..core.models import CloudflareMetrics


@activity.defn
async def fetch_cloudflare_analytics(date: str) -> dict:
    # Convert ISO string to datetime
    date = datetime.fromisoformat(date)
    """Fetch analytics data from Cloudflare for a specific date."""
    # TODO: Implement actual Cloudflare API call
    return {
        "total_requests": 1000,
        "unique_visitors": 500,
        "bandwidth_used": 1024 * 1024 * 100,  # 100MB
        "top_countries": {"US": 300, "UK": 100, "CA": 100},
        "top_pages": {"/": 400, "/about": 100},
    }


@activity.defn
async def store_analytics_data(date: str, data: dict) -> None:
    # Convert ISO string to datetime
    date = datetime.fromisoformat(date)
    """Store the analytics data in our database."""
    async with get_session() as session:
        metrics = CloudflareMetrics(
            date=date.date(),
            total_requests=data["total_requests"],
            bandwidth_used=data["bandwidth_used"],
            top_countries=data["top_countries"],
            top_pages=data["top_pages"],
        )
        session.add(metrics)
        await session.commit()


@activity.defn
async def generate_report(start_date: str, end_date: str) -> dict:
    # Convert ISO strings to datetime
    start_date = datetime.fromisoformat(start_date)
    end_date = datetime.fromisoformat(end_date)
    """Generate a report for the specified date range."""
    async with get_session() as session:
        query = select(CloudflareMetrics).where(
            CloudflareMetrics.date >= start_date.date(),
            CloudflareMetrics.date <= end_date.date(),
        )
        result = await session.execute(query)
        metrics = result.scalars().all()

    # Aggregate metrics
    total_requests = sum(m.total_requests for m in metrics)
    total_bandwidth = sum(m.bandwidth_used for m in metrics)

    # Combine top countries and pages
    countries = {}
    pages = {}
    for m in metrics:
        for country, count in m.top_countries.items():
            countries[country] = countries.get(country, 0) + count
        for page, count in m.top_pages.items():
            pages[page] = pages.get(page, 0) + count

    return {
        "period": {
            "start": start_date.isoformat(),
            "end": end_date.isoformat(),
        },
        "total_requests": total_requests,
        "total_bandwidth": total_bandwidth,
        "top_countries": dict(
            sorted(countries.items(), key=lambda x: x[1], reverse=True)[:10]
        ),
        "top_pages": dict(sorted(pages.items(), key=lambda x: x[1], reverse=True)[:10]),
    }


@workflow.defn
class AnalyticsCollectionWorkflow:
    """Workflow to collect and store Cloudflare analytics data."""

    @workflow.run
    async def run(self, start_date: str, end_date: str = None) -> dict:
        """Run the analytics collection workflow.

        Args:
            start_date: Start date for data collection (ISO format string)
            end_date: Optional end date in ISO format (defaults to start_date + 1 day)
        """
        # Convert ISO format strings back to datetime objects
        start_date = datetime.fromisoformat(start_date)
        end_date = datetime.fromisoformat(end_date) if end_date else None
        if end_date is None:
            end_date = start_date + timedelta(days=1)

        retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=1),
            maximum_interval=timedelta(minutes=10),
            maximum_attempts=3,
        )

        current_date = start_date
        while current_date < end_date:
            # Fetch analytics data
            analytics_data = await workflow.execute_activity(
                fetch_cloudflare_analytics,
                args=[current_date.isoformat()],
                start_to_close_timeout=timedelta(minutes=5),
                retry_policy=retry_policy,
            )

            # Store the data
            await workflow.execute_activity(
                store_analytics_data,
                args=[current_date.isoformat(), analytics_data],
                start_to_close_timeout=timedelta(minutes=5),
                retry_policy=retry_policy,
            )

            current_date += timedelta(days=1)

        # Generate and return the report
        return await workflow.execute_activity(
            generate_report,
            args=[start_date.isoformat(), end_date.isoformat()],
            start_to_close_timeout=timedelta(minutes=5),
            retry_policy=retry_policy,
        )
