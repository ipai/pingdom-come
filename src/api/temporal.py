from temporalio.client import Client


async def create_temporal_client() -> Client:
    """Create and configure Temporal client."""
    return await Client.connect("temporal:7233")
