import plotly.express as px
import json
import requests
from pathlib import Path
from typing import List, Dict, Any, Optional

class WHODataManager:
    """Manager for downloading, caching in memory, and filtering WHO health data."""
    
    def __init__(self, data_dir: str = "Data", filename: str = "WHOSIS_000001.json"):
        """
        Initialize the WHO Data Manager and load data into memory.
        """
        print("Constructor execution started.")
        self.data_dir = Path(data_dir)
        self.filename = filename
        self.filepath = self.data_dir / self.filename
        self.url = "https://ghoapi.azureedge.net/api/WHOSIS_000001"
        
        # Load the data once during initialization
        self._data = self._initialize_data()
        print("Constructor execution finished.")

    def _initialize_data(self) -> Dict[str, Any]:
        """Internal helper to ensure file exists and load it into memory."""
        if not self.filepath.exists():
            print(f"File {self.filepath} not found.")
            self.download_data()
        else:
            print(f"File {self.filepath} found, loading existing data.")
        
        with open(self.filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def print_config(self) -> None:
        """Show member variables and status."""
        print(f"Data Directory: {self.data_dir}")
        print(f"File Path: {self.filepath}")
        print(f"URL: {self.url}")
        print(f"In-Memory Records: {len(self._data.get('value', [])) if self._data else 0}")

    def ensure_data_directory(self) -> None:
        """Create the data directory if it doesn't exist."""
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def download_data(self) -> None:
        """Download the JSON file from the WHO API."""
        print(f"Downloading data from {self.url}...")
        try:
            response = requests.get(self.url, timeout=30)
            response.raise_for_status()  # Best practice: check for HTTP errors
            
            self.ensure_data_directory()
            with open(self.filepath, 'wb') as f:
                f.write(response.content)
            print(f"Data successfully downloaded to {self.filepath}")
        except Exception as e:
            raise Exception(f"Failed to download data: {str(e)}")

    def filter_data(
        self,
        spatial_dim: Optional[str] = None,
        time_dimension_value: Optional[str] = None,
        dim1: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Filter the in-memory JSON data based on specified attributes.
        """
        if not self._data or 'value' not in self._data:
            raise ValueError("No data loaded or JSON missing 'value' key")
        
        filtered_entries = self._data['value']
        
        if spatial_dim:
            filtered_entries = [e for e in filtered_entries if e.get('SpatialDim') == spatial_dim]
        
        if time_dimension_value:
            filtered_entries = [e for e in filtered_entries if e.get('TimeDimensionValue') == time_dimension_value]
        
        if dim1:
            filtered_entries = [e for e in filtered_entries if e.get('Dim1') == dim1]
        
        return filtered_entries

    def get_filtered_data(
        self,
        spatial_dim: Optional[str] = None,
        time_dimension_value: Optional[str] = None,
        dim1: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Public API to get filtered data from the in-memory cache.
        """
        filtered_data = self.filter_data(
            spatial_dim=spatial_dim,
            time_dimension_value=time_dimension_value,
            dim1=dim1
        )
        
        total_count = len(self._data.get('value', []))
        print(f"Filtered {len(filtered_data)} entries from {total_count} total entries.")
        return filtered_data


def print_data_entries(data: List[Dict[str, Any]]) -> None:
    """
    Print all entries and their attributes from a list of dictionaries.
    
    Args:
        data: List of dictionary entries to print
    
    Returns:
        None
    """
    if not data:
        print("No data to display.")
        return
    
    print(f"\n{'='*80}")
    print(f"Total entries: {len(data)}")
    print(f"{'='*80}")
    
    for i, entry in enumerate(data, 1):
        print(f"\n--- Entry {i} of {len(data)} ---")
        for key, value in entry.items():
            print(f"  {key:<25}: {value}")
    
    print(f"\n{'='*80}")
    print(f"Displayed {len(data)} entries")
    print(f"{'='*80}\n")

# --- Entry 12932 ---
# Id: 9768552
# IndicatorCode: WHOSIS_000001
# SpatialDimType: COUNTRY
# SpatialDim: GUY
# ParentLocationCode: AMR
# TimeDimType: YEAR
# ParentLocation: Americas
# Dim1Type: SEX
# Dim1: SEX_BTSX
# TimeDim: 2001
# Dim2Type: None
# Dim2: None
# Dim3Type: None
# Dim3: None
# DataSourceDimType: None
# DataSourceDim: None
# Value: 64.7 [64.1-65.3]
# NumericValue: 64.66515946
# Low: 64.09505051
# High: 65.26655278
# Comments: None
# Date: 2024-08-02T09:43:39.193+02:00
# TimeDimensionValue: 2001
# TimeDimensionBegin: 2001-01-01T00:00:00+01:00
# TimeDimensionEnd: 2001-12-31T00:00:00+01:00

fewer_country_codes = ["USA", "MEX", "CAN"]

some_country_codes = ['AFG', 'AGO', 'ALB', 'ARE', 'ARG', 'ARM', 'ATG', 'AUS', 'AUT', 'AZE', 'BDI', 'BEL', 'BEN', 'BFA', 'BGD', 'BGR', 
                      'BHR', 'BHS', 'BIH', 'BLR', 'BLZ', 'BOL', 'BRA', 'BRB', 'BTN', 'BWA', 'CAF', 'CAN', 'CHE', 'CHL', 'CHN', 'CIV', 
                      'CMR', 'COD', 'COG', 'COL', 'COM', 'CPV', 'CRI', 'CUB', 'CYP', 'CZE', 'DEU', 'DJI', 'DNK', 'DOM', 'DZA', 'ECU', 
                      'EGY', 'ERI', 'ESP', 'EST', 'ETH', 'FIN', 'FJI', 'FRA', 'FSM', 'GAB', 'GBR', 'GEO', 'GHA', 'GIN', 'GMB', 'GNB', 
                      'GNQ', 'GRC', 'GRD', 'GTM', 'GUY', 'HND', 'HRV', 'HTI', 'HUN', 'IDN', 'IND', 'IRL', 'IRN', 'IRQ', 'ISL', 'ISR', 
                      'ITA', 'JAM', 'JOR', 'JPN', 'KAZ', 'KEN', 'KGZ', 'KHM', 'KIR', 'KOR', 'KWT', 'LAO', 'LBN', 'LBR', 'LBY', 'LCA', 
                      'LKA', 'LSO', 'LTU', 'LUX', 'LVA', 'MAR', 'MDA', 'MDG', 'MDV', 'MEX', 'MKD', 'MLI', 'MLT', 'MMR', 'MNE', 'MNG', 
                      'MOZ', 'MRT', 'MSU', 'MTL', 'MYS', 'NAM', 'NER', 'NGA', 'NIC', 'NLD', 'NOR', 'NZL', 'OMN', 'PAK', 'PAN', 'PER', 
                      'PHL', 'PNG', 'POL', 'PRI', 'PRK', 'PRT', 'PRY', 'PSE', 'QAT', 'ROU', 'RUS', 'RWA', 'SAU', 'SDN', 'SEN', 'SGP', 
                      'SLB', 'SLE', 'SLV', 'SOM', 'SSD', 'STP', 'SVK', 'SVN', 'SWE', 'SWZ', 'SYR', 'TCD', 'TGO', 'THA', 'TJK', 'TKM', 
                      'TLS', 'TON', 'TTO', 'TUN', 'TUR', 'TZA', 'UGA', 'UKR', 'URY', 'USA', 'UZB', 'VCT', 'VEN', 'VNM', 'VUT', 'WSM', 
                      'YEM', 'ZAF', 'ZMB', 'ZWE']

# Example usage
if __name__ == "__main__":
    # Initialize the manager
    # manager1 = WHODataManager()
    # manager1.print()
    manager = WHODataManager("Data", "WHOSIS_000001.json")
    # manager.print()
    # manager.load_data();

    data = []
    empty = []

    for i in range(len(some_country_codes)):
        specific_data = manager.get_filtered_data(
            spatial_dim = some_country_codes[i],
            time_dimension_value="2021",
            dim1="SEX_BTSX"
        )
        
        if not specific_data:
            print(f"The list is empty for {some_country_codes[i]}")
            empty.append(f"The list is empty for {some_country_codes[i]}")
        else:
            print_data_entries(specific_data);
            # Accessing the first element (index 0) and the specific key
            life_expectancy = specific_data[0]['NumericValue']
            print(f"{some_country_codes[i]} -> {life_expectancy}")
            data.append((some_country_codes[i],life_expectancy))

    print(data)
    print(empty)

    fig = px.choropleth(data, locations=0, color=1)
    fig.show()

    # # Example 1: Get all data (no filtering)
    # print("\n=== Example 1: Get all data ===")
    # all_data = manager.get_filtered_data()
    # print(f"Total entries: {len(all_data)}")

    # # Example 2: Filter by country (SpatialDim)
    # print("\n=== Example 2: Filter by country (Ghana) ===")
    # ghana_data = manager.get_filtered_data(spatial_dim="GHA")
    # if ghana_data:
    #     print(f"First Ghana entry: {ghana_data[0]}")

    # # Example 3: Filter by year
    # print("\n=== Example 3: Filter by year (2003) ===")
    # year_2003_data = manager.get_filtered_data(time_dimension_value="2003")

    # # Example 4: Filter by multiple criteria
    # print("\n=== Example 4: Filter by country, year, and sex ===")
    # specific_data = manager.get_filtered_data(
    #     spatial_dim="GHA",
    #     time_dimension_value="2003",
    #     dim1="SEX_BTSX"
    # )

    # # Example 5: Print all attributes from filtered data
    # filtered_data = manager.get_filtered_data(
    #     spatial_dim="SWE",
    #     time_dimension_value="2001"
    # )