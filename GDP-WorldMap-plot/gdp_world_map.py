"""
Unify data via common country name in a world map.
"""

import csv
import math
import pygal

def reconcile_countries_by_name(plot_countries, gdp_countries):
    """
    Inputs:
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country names used in GDP data

    Output:
      A tuple containing a dictionary and a set.  The dictionary maps
      country codes from plot_countries to country names from
      gdp_countries The set contains the country codes from
      plot_countries that were not found in gdp_countries.
    """
    countries_dict = {}
    countries_sets = set()
    
    #Serach each code country in plot_countries
    for dummy_countries in plot_countries:
        
        #See if the country name is in the gdp_countries dictionary
        #if so, add {country code: country name} to countries_dict dictionary
        #Otherwise, add country code to the countries_sets set
        if plot_countries[dummy_countries] in gdp_countries:
            
            countries_dict[dummy_countries] = plot_countries[dummy_countries]
        
        else:
            
            countries_sets.add(dummy_countries)
    
    return countries_dict, countries_sets
    

def build_map_dict_by_name(gdpinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for

    Output:
      A tuple containing a dictionary and two sets.  The dictionary
      maps country codes from plot_countries to the log (base 10) of
      the GDP value for that country in the specified year.  The first
      set contains the country codes from plot_countries that were not
      found in the GDP data file.  The second set contains the country
      codes from plot_countries that were found in the GDP data file, but
      have no GDP data for the specified year.
    """

    gdp_countries = {}
    no_gdp_value_countries = set()
    countries_dict = {}
    
    #open file which name is in gdpinfo dictionary whose key is "gdpfile"
    with open(gdpinfo["gdpfile"], newline='') as csvfile:
        
        reader = csv.DictReader(csvfile, delimiter=gdpinfo["separator"], quotechar=gdpinfo["quote"])
        
        #Make a dictionary whose keys are country names in GDP file and values are log10(GDP)
        for row in reader:
            
            country_name = row[gdpinfo["country_name"]]
            gdp_value = row[year]
            
            #some gdp_value take '' value and brind a ValueError
            #when tring to convert yo float. If that happens: base10_value = 'None'
            try:
                gdp_value = float(gdp_value)
                base10_value = math.log10(gdp_value)
            
            except ValueError:
                base10_value = 'None'
            
            #add to gdp_countries dictionary {country_name: base10_value}
            gdp_countries.setdefault(country_name, base10_value)
           
#     data[0]: dictionary that maps country codes from
#              plot_countries to country names from gdp_countries.

#     data[1]: set that contains the country codes from
#              plot_countries that were not found in gdp_countries.
    data = reconcile_countries_by_name(plot_countries, gdp_countries)
    
    
    for dummy_code in data[0]:
        
        country = data[0][dummy_code]
        
        #See if a country in data[0] has no GDP value in gdp_countries dictionary
        #if so, add the country code to the set no_gdp_value_countries
        if gdp_countries[country] != 'None':
            countries_dict[dummy_code] = gdp_countries[country]
        
        else:
            no_gdp_value_countries.add(dummy_code)
                    
                    
    return countries_dict, data[1], no_gdp_value_countries


def render_world_map(gdpinfo, plot_countries, year, map_file):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for
      map_file       - Name of output file to create

    Output:
      Returns None.

    Action:
      Creates a world map plot of the GDP data for the given year and
      writes it to a file named by map_file.
    """
    info = build_map_dict_by_name(gdpinfo, plot_countries, year)
    
    worldmap_chart = pygal.maps.world.World()
    
    title_1 = 'GDP by country for ' + year
    title_2 = ' (log scale), unified by common country NAME'
    
    worldmap_chart.title = title_1 + title_2
    
    worldmap_chart.add('GDP for ' + year, info[0])
    worldmap_chart.add('Missing from World Bank Data', list(info[1]))
    worldmap_chart.add('No GDP data', list(info[2]))
    
    worldmap_chart.render_to_file(map_file)


def test_render_world_map():
    """
    Test the project code for several years.
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

    # Get pygal country code map
    pygal_countries = pygal.maps.world.COUNTRIES


    # 1960
    render_world_map(gdpinfo, pygal_countries, "1960", "isp_gdp_world_name_1960.svg")

    # 1980
    render_world_map(gdpinfo, pygal_countries, "1980", "isp_gdp_world_name_1980.svg")

    # 2000
    render_world_map(gdpinfo, pygal_countries, "2000", "isp_gdp_world_name_2000.svg")

    # 2010
    render_world_map(gdpinfo, pygal_countries, "2010", "isp_gdp_world_name_2010.svg")


#||=====================================================================================||
#||                                                                                     ||
#||                                     MAIN EXCECUTION                                 || 
#||                                                                                     ||
#||=====================================================================================||

test_render_world_map()
