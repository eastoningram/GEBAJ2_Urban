#!/usr/bin/env python3

from generator.building import Building

# class to calculate amount of buildings for the given population
class TownGenerator: 
    def __init__(self, population, area, categories): 
        self.population = population
        self.area = area
        self.building_categories = categories
        self.buildings = self._generate_buildings()
    
    def _generate_buildings(self):
        # Step 1: footprint multipliers
        footprint_multipliers = [1 + self.building_categories[cat] * 5 for cat in self.building_categories]

        # Step 2: weighted sum of categories
        weighted_sum = sum(
            self.building_categories[cat] * (1 + self.building_categories[cat] * 5)
            for cat in self.building_categories
        )

        # Step 3: total buildings
        #total_buildings = self.population / (self.area / weighted_sum)
        total_buildings = (self.population * self.area) / weighted_sum

        # Step 4: distribute across categories
        buildings = []
        cat_idx = 1
        for cat in self.building_categories:
            fraction = self.building_categories[cat]
            cat_buildings = round(total_buildings * fraction)
            
            # category-specific people and area
            avg_people = (self.population * fraction) / cat_buildings
            cat_area = self.area * (fraction * (1 + fraction * 5) / weighted_sum)
            area_per_building_m2 = (cat_area / cat_buildings) * 1_000_000

            for _ in range(cat_buildings):
                b = Building(
                    -1, -1, -1, -1,
                    cat_idx,
                    area_per_building_m2,
                    avg_people
                )
                buildings.append(b)

            cat_idx += 1

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
