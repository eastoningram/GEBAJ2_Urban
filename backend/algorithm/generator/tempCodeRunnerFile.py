
#class to calculate amount of buildings for the give population
class generator: 
    def __init__(self, population, area): 
        self._population = population
        self._area = area
        self._building_categories = {
            'residential': 0.30,
            'commerce': 0.20,
            'industry': 0.30,
            'recreation': 0.20
        }
    
    #getter to return population
    def getPopulation(self):


        
        return self._population  # ← Returns the instance variable
    
    #getter to modify instance variable
    def getPopulation(self, value):
        self._population = value  # ← Modifies the instance variable

    #setter for population
    def setPopulation(self, value):
        """Set the population of the town."""
        if value < 0:
            raise ValueError("Population cannot be negative")
        self._population = value
    
    # adds the area 
    def setArea(self, value):
        """Set the area of the town."""
        if value <= 0:
            raise ValueError("Area must be positive")
        self._area = value
    

    def calculate_buildings(population,
                        building_categories=None,
                        avg_people_per_building=None,
                        buildings_per_sqkm=None):
    
        # Default percentages
        if building_categories is None:
            building_categories = {
                'residential': 0.30,
                'commerce': 0.20,
                'industry': 0.30,
                'recreation': 0.20
            }
            
        # Default avg people per building
        if avg_people_per_building is None:
            avg_people_per_building = {
                'residential': 4,
                'commerce': 20,
                'industry': 50,
                'recreation': 30
            }
            
        # Default buildings per square km
        if buildings_per_sqkm is None:
            buildings_per_sqkm = {
                'residential': 50,   # max residential per sq km
                'commerce': 10,      # max commercial per sq km
                'industry': 8,       # max industrial per sq km
                'recreation': 5      # max recreation per sq km
            }
        
        results = {}
        
        for category, percent in building_categories.items():
            people_in_category = population * percent
            per_building = avg_people_per_building.get(category, 10)
            
            # Buildings needed by population
            buildings_by_pop = people_in_category / per_building
            
            # Buildings limited by area capacity
            max_by_area = area * buildings_per_sqkm.get(category, 10)
            
            # Final number is the smaller of both limits
            buildings_needed = min(buildings_by_pop, max_by_area)
            
            results[category] = int(round(buildings_needed))
            
        return results
class generator: 
    def __init__(self, population, area): 
        self._population = population
        self._area = area
        self._building_categories = {
            'residential': 0.30,
            'commerce': 0.20,
            'industry': 0.30,
            'recreation': 0.20
        }
    
    def getPopulation(self):
        return self._population
    
    def setPopulation(self, value):
        self._population = value
    
    def getArea(self):
        return self._area
    
    def setArea(self, value):
        self._area = value
    
    # FIXED METHOD: Remove population and area parameters, use self._population and self._area
    def calculate_buildings(self, avg_people_per_building=None, buildings_per_sqkm=None):
        if avg_people_per_building is None:
            avg_people_per_building = {
                'residential': 4,
                'commerce': 20,
                'industry': 50,
                'recreation': 30
            }
            
        if buildings_per_sqkm is None:
            buildings_per_sqkm = {
                'residential': 50,
                'commerce': 10,
                'industry': 8,
                'recreation': 5
            }
        
        results = {}
        total_buildings = 0
        
        for category, percent in self._building_categories.items():
            # Use self._population and self._area instead of parameters
            people_in_category = self._population * percent
            per_building = avg_people_per_building.get(category, 10)
            
            buildings_by_pop = people_in_category / per_building
            max_by_area = self._area * buildings_per_sqkm.get(category, 10)
            
            buildings_needed = min(buildings_by_pop, max_by_area)
            results[category] = int(buildings_needed)
            total_buildings += results[category]
        
        results['total'] = total_buildings
        return results


def main():
    print("=== Town Building Generator ===")
    
    # Get user input
    population = int(input("Enter population: "))
    area = float(input("Enter area (sq km): "))
    
    # Create generator with user values
    town = generator(population, area)
    
    # Ask if user wants to modify values
    modify = input("Do you want to modify population or area? (y/n): ").lower()
    if modify == 'y':
        new_pop = int(input("Enter new population: "))
        new_area = float(input("Enter new area: "))
        
        # Use setters to modify
        town.setPopulation(new_pop)
        town.setArea(new_area)
    
    # Ask if user wants custom parameters
    custom = input("Use custom building parameters? (y/n): ").lower()
    
    if custom == 'y':
        print("Enter average people per building for each category:")
        residential_people = int(input("Residential: "))
        commerce_people = int(input("Commerce: "))
        industry_people = int(input("Industry: "))
        recreation_people = int(input("Recreation: "))
        
        print("Enter maximum buildings per sq km for each category:")
        residential_density = int(input("Residential: "))
        commerce_density = int(input("Commerce: "))
        industry_density = int(input("Industry: "))
        recreation_density = int(input("Recreation: "))
        
        custom_people = {
            'residential': residential_people,
            'commerce': commerce_people,
            'industry': industry_people,
            'recreation': recreation_people
        }
        
        custom_density = {
            'residential': residential_density,
            'commerce': commerce_density,
            'industry': industry_density,
            'recreation': recreation_density
        }
        
        # Get results from class method (no calculations in main)
        buildings = town.calculate_buildings(
            avg_people_per_building=custom_people,
            buildings_per_sqkm=custom_density
        )
    else:
        # Get results from class method (no calculations in main)
        buildings = town.calculate_buildings()
    
    # DISPLAY ONLY - no calculations
    print("\n" + "="*50)
    print("TOWN BUILDING REPORT")
    print("="*50)
    print(f"Population: {town.getPopulation():,}")
    print(f"Area: {town.getArea()} sq km")
    print("\nBUILDING DISTRIBUTION:")
    print("-" * 30)
    
    # Simply display what the class calculated
    for category, count in buildings.items():
        if category != 'total':
            print(f"{category.title():<12} : {count:>4} buildings")
    
    print("-" * 30)
    print(f"{'TOTAL':<12} : {buildings['total']:>4} buildings")


# Run the program
if __name__ == "__main__":
    main()