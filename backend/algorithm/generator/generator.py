#!/usr/bin/env python3

from generator.building import Building

# class to calculate amount of buildings for the given population
class TownGenerator: 
    def __init__(self, population, area, categories): 
        self.population = population
        self.area = area
        self.building_categories = categories
        self.buildings=self.exporter()
    
    # getter to return population
    def getPopulation(self):
        return self.population

    def getBuildings(self):
        return self.buildings
    
    # setter for population
    def setPopulation(self, value):
        if value < 0:
            raise ValueError("Population cannot be negative")
        self.population = value
    
    # setter for area
    def setArea(self, value):
        if value <= 0:
            raise ValueError("Area must be positive")
        self.area = value
    
    def calculate_buildings(self):
        # Step 1: relative footprint multipliers for realistic building sizes
        # Higher number = bigger building footprint
        footprint_multipliers = {cat: 1 + self.building_categories[cat]*5 for cat in self.building_categories}
        weighted_sum = sum(self.building_categories[cat] * footprint_multipliers[cat] for cat in self.building_categories)

        # Step 2: total buildings calculated from population and area
        total_buildings = self.population / (self.area / weighted_sum)

        # Step 3: buildings per category
        category_buildings = {cat: total_buildings * self.building_categories[cat] for cat in self.building_categories}

        avg_people_per_category = {
            cat: self.population * self.building_categories[cat] / category_buildings[cat]
            for cat in self.building_categories
        }

        # Step 4: area per building per category
        area_per_building = {}
        for cat in self.building_categories:
            cat_area = self.area * (self.building_categories[cat] * footprint_multipliers[cat] / weighted_sum)
            area_per_building[cat] = cat_area / category_buildings[cat]

        # Convert all to m² once after the loop
        area_per_building_m2 = {cat: a * 1_000_000 for cat, a in area_per_building.items()}


        # Step 5: average people per building overall
        avg_people_per_building = self.population / total_buildings

        return {
            'total_buildings': round(total_buildings),
            'avg_people_per_building': avg_people_per_building,
            'category_buildings': {cat: round(num) for cat, num in category_buildings.items()},
            'area_per_building_m2': area_per_building_m2,
            'avg_people_per_category': avg_people_per_category

        }

    def exporter(self):
        results = self.calculate_buildings()
        buildings = []
        cat_idx=1
        for cat, count in results["category_buildings"].items():
            for i in range(count):
                b = Building(
                    -1, -1, -1, -1,
                    cat_idx,
                    results["area_per_building_m2"][cat],
                    results["avg_people_per_category"][cat]
                )
                buildings.append(b)
            cat_idx=cat_idx+1

        return buildings



def main():
    print("=== Town Building Generator ===")

    # Ask user for population and area
    population = int(input("Enter total population: "))
    area = float(input("Enter total area (sq km): "))

    # Ask user for category percentages
    print("Enter category percentages (as decimals, sum should be 1.0):")
    categories = {}
    for cat in ['residential', 'commerce', 'industry', 'recreation']:
        categories[cat] = float(input(f"{cat.title()}: "))

    total_pct = sum(categories.values())
    if abs(total_pct - 1.0) > 0.001:
        print("Warning: category percentages do not sum to 1.0. Results may be slightly off.")

    # Create town generator and calculate
    town = TownGenerator(population, area, categories)
    result = town.calculate_buildings()

    # Display results
    print("\n=== Town Building Report ===")
    print(f"Population: {population:,}")
    print(f"Total area: {area} sq km")
    print(f"Total buildings: {result['total_buildings']}")
    print(f"Average people per building: {result['avg_people_per_building']:.2f}\n")

    print("Buildings per category:")
    for cat, num in result['category_buildings'].items():
        print(f"  {cat.title():<12}: {num} buildings")

    print("\nArea per building per category (m2):")
    for cat, a in result['area_per_building_m2'].items():
        print(f"  {cat.title():<12}: {a:.2f} m2")



if __name__ == "__main__":
    main()
