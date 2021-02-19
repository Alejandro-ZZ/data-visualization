"""
Read World Bank GDP data and create some basic XY plots.
"""

import csv
import pygal

def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - Name of CSV file
      keyfield  - Field to use as key for rows
      separator - Character that separates fields
      quote     - Character used to optionally quote fields

    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    info = {}
    with open(filename, newline='') as csvfile:
        
        reader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        
        for row in reader:
            info[row[keyfield]] = row
            
    return info


def build_plot_values(gdpinfo, gdpdata):
    """
    Inputs:
      gdpinfo - GDP data information dictionary
      gdpdata - A single country's GDP stored in a dictionary whose
                keys are strings indicating a year and whose values
                are strings indicating the country's corresponding GDP
                for that year.

    Output: 
      Returns a list of tuples of the form (year, GDP) for the years
      between "min_year" and "max_year", inclusive, from gdpinfo that
      exist in gdpdata.  The year will be an integer and the GDP will
      be a float.
    """
    lista = []
    
    for dummy_year in gdpdata.keys():
        
        gdp_val = gdpdata[dummy_year]
        
        if gdp_val != '':
            
            try:
                if int(dummy_year)in range(gdpinfo["min_year"], gdpinfo["max_year"]+1):
                    
                    lista.append((int(dummy_year), float(gdp_val)))
            
            except ValueError:
                return lista
    
    return lista


def build_plot_dict(gdpinfo, country_list):
    """
    Inputs:
      gdpinfo      - GDP data information dictionary
      country_list - List of strings that are country names

    Output:
      Returns a dictionary whose keys are the country names in
      country_list and whose values are lists of XY plot values 
      computed from the CSV file described by gdpinfo.

      Countries from country_list that do not appear in the
      CSV file should still be in the output dictionary, but
      with an empty XY plot value list.
    """
    read_val = read_csv_as_nested_dict(gdpinfo["gdpfile"], gdpinfo["country_name"],
                                       gdpinfo["separator"], gdpinfo["quote"])
    
    plot_dict = {}
    
    for dummy_i in range(0, len(country_list)):
        
        gdpdata = {}
        country = country_list[dummy_i]
        plot_dict.setdefault(country)
        
        try:
            values_country = read_val[country]
            
            for dummy_temp in range(gdpinfo["min_year"], gdpinfo["max_year"]+1):
                
                gdpdata[str(dummy_temp)] = values_country[str(dummy_temp)]
            
            xy_values = build_plot_values(gdpinfo, gdpdata)
            plot_dict[country] = xy_values
            xy_values = []
        
        except KeyError:
            plot_dict[country] = []
            
    return plot_dict


def render_xy_plot(gdpinfo, country_list, plot_file):
    """
    Inputs:
      gdpinfo      - GDP data information dictionary
      country_list - List of strings that are country names
      plot_file    - String that is the output plot file name

    Output:
      Returns None.

    Action:
      Creates an SVG image of an XY plot for the GDP data
      specified by gdpinfo for the countries in country_list.
      The image will be stored in a file named by plot_file.
    """
    coordinates = build_plot_dict(gdpinfo, country_list)
    
    xy_chart = pygal.XY(title=u'Plot of GDP for select countries spanning 1960 to 2015',
                        y_title='GDP in current US dollars',
                        x_title='Year')
    
    for dummy_country in coordinates:
    
        xy_chart.add(dummy_country, coordinates[dummy_country])
    
    xy_chart.render_to_file(plot_file)



def test_render_xy_plot():
    """
    Code to exercise render_xy_plot and generate plots from
    actual GDP data.
    """
    gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    }

    render_xy_plot(gdpinfo, [], "isp_gdp_xy_none.svg")
    render_xy_plot(gdpinfo, ["China"], "isp_gdp_xy_china.svg")
    render_xy_plot(gdpinfo, ["United Kingdom", "United States"],
                   "isp_gdp_xy_uk+usa.svg")

#||==============================================================================||
#||                                                                              ||
#||                                  MAIN EXECUTION                              ||
#||                                                                              ||
#||==============================================================================||

gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    }
    
test_render_xy_plot()
