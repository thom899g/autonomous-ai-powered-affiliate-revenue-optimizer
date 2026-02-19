import logging
from typing import Optional
import aiohttp

class DataCollector:
    def __init__(self, api_keys: Dict[str, str]):
        self.api_keys = api_keys
        self.session = aiohttp.ClientSession()
        self.logger = logging.getLogger(__name__)
        
    async def fetch_data(self, source: str) -> Optional[pd.DataFrame]:
        """Fetches data from a specified API asynchronously."""
        if source not in self.api_keys:
            self.logger.error(f"Invalid data source: {source}")
            return None
            
        try:
            api_key = self.api_keys[source]
            async with self.session.get(f"{source}/api/v1/data?api_key={api_key}") as response:
                if response.status == 200:
                    data = await response.json()
                    return pd.DataFrame(data)
                else:
                    self.logger.error(f"Failed to fetch data from {source}. Status: {response.status}")
        except Exception as e:
            self.logger.error(f"Error fetching data from {source}: {str(e)}")
            raise
            
    async def collect_multiple_sources(self, sources: List[str]) -> pd.DataFrame:
        """Collects data from multiple sources concurrently."""
        tasks = [self.fetch_data(source) for source in sources]
        results = await asyncio.gather(*tasks)
        
        # Filter out None values and concatenate DataFrames
        filtered = [df for df in results if df is not None]
        if not filtered:
            return pd.DataFrame()
            
        combined_df = pd.concat(filtered, ignore_index=True)
        self.logger.info(f"Successfully collected data from {len(sources)} sources.")
        return combined_df
        
    async def close(self) -> None:
        """Closes the aiohttp session."""
        await self.session.close()