# Global EV Adoption Analysis

## Live Demo
[Click here to view the dashboard](https://global-ev-adoption-analysis-kyeibiuhbc7nsgmhqmhzwg.streamlit.app/)

## Objective
Analyze electric vehicle registration data to understand adoption trends, 
manufacturer dominance, geographic distribution, and battery range patterns.

## Dataset
- **Source:** Electric Vehicle Population Dataset (Washington State)
- **Records:** 177,473 registered electric vehicles
- **Columns:** VIN, County, City, State, Model Year, Make, Model, EV Type, 
  Electric Range, CAFV Eligibility, and more

## Tools Used
- Python 3
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Jupyter Notebook

## Project Structure
Global-EV-Adoption-Analysis/

├── data/
│   └── Electric_Vehicle_Population_Data.csv
├── notebooks/
│   └── EV_EDA.ipynb
├── images/
│   ├── ev_adoption_trend.png
│   ├── top_manufacturers.png
│   ├── top_models.png
│   ├── ev_type_distribution.png
│   ├── top_cities.png
│   ├── top_counties.png
│   ├── electric_range_distribution.png
│   └── ev_type_by_year.png
│
├── README.md
└── requirements.txt

## Key Findings
1. EV registrations increased sharply after 2017, with peak growth post-2020.
2. Tesla dominates the market with approximately 45% of all registrations.
3. Tesla Model Y and Model 3 are the most popular EV models.
4. Battery Electric Vehicles (BEVs) account for nearly 78% of all EVs.
5. Seattle and King County are the leading EV adoption regions.
6. Average electric range has improved significantly in newer model years.
7. Over one-third of vehicles qualify for CAFV incentives.

## Visualizations
 Chart | Description 

 EV Adoption Trend | Year-wise growth in EV registrations 
 Top Manufacturers | Market share by make 
 Top Models | Most registered EV models 
 EV Type Distribution | BEV vs PHEV breakdown 
 Top Cities & Counties | Geographic adoption patterns 
 Electric Range Analysis | Range distribution and outlier detection
 EV Type by Model Year | BEV vs PHEV trend over time 

## How to Run
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Open `notebooks/EV_EDA.ipynb` in Jupyter Notebook or VS Code
4. Run all cells

## Limitations
- Dataset covers Washington State only, not nationwide EV adoption.
- Base MSRP contains 98% zero values and was excluded from analysis.
- Electric range data is unavailable for a large proportion of vehicles.

## Author
Ankita Biswas