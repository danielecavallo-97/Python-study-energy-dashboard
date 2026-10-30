import mapping

def Country_searcher(country: str)-> str:
    if country:
        try:
            country_lookup = mapping.lookup_area(country) 
            return country_lookup
        except ValueError as error:
            #print(f"Error occurred: {error}") #logga errore nel lookup
            country_lookup = None
    else:
        return None
    country_lookup = next((area for area in mapping.Area if country.casefold() in area.meaning.casefold()), None)
    return country_lookup if country_lookup else None


#country = input("Scrivi la nazione: ").upper()
#country_lookup = Country_searcher(country)
#print(country_lookup)
