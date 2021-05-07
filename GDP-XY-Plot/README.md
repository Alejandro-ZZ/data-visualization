# Plot data in a XY graphic

This project creates a line plot of GDP data (stored in CSV file `isp_gdp.csv`) collected by the [World Bank](https://data.worldbank.org/indicator/NY.GDP.MKTP.CD) which is freely available for download and analysis. Data is processed and, using dictionaries, the algorithm creates plots using Pygal library.

## Note

You have to "clean" manually the csv file if you downloaded it directly from World Bank dataset. This is because it contains extra headers rows of information and some data are between double quotes.
