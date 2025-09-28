# class to calculate amount of buildings for the given population
import random


class TownGenerator: 
    def __init__(self, population, area, categories): 
        self.population = population
        self.area = area
        self.building_categories = categories

        self.building_sizes = {
            'residential': [0.5, 1.0, 1.5],  # small, medium, large
            'commerce': [1.0, 2.0, 3.0],
            'industry': [2.0, 4.0, 6.0],
            'recreation': [1.5, 3.0, 4.5]
        }
    

    def calculate_buildings(self):
        # Step 1: relative footprint multipliers for realistic category sizes
        footprint_multipliers = {cat: 1 + self.building_categories[cat]*5 for cat in self.building_categories}
        weighted_sum = sum(self.building_categories[cat] * footprint_multipliers[cat] for cat in self.building_categories)
        
        # Step 2: total buildings
        # Base assumptions
        base_population_per_building = 40   # average people per building
        base_area_per_building = 1.0        # 1 sq km corresponds to 1x multiplier

        # Scale buildings with both population and area
        pop_component = self.population / base_population_per_building
        area_component = max(1.0, self.area / base_area_per_building)

        total_buildings = pop_component * (area_component ** 0.5)  # square root tempers runaway growth
        
        # Step 3: buildings per category
        category_buildings = {cat: total_buildings * self.building_categories[cat] for cat in self.building_categories}

        # Step 4: assign buildings to 3 size variations per category
        buildings_per_size = {}
        area_per_building_size = {}
        people_per_building_size = {}

        for cat in self.building_categories:
            n_buildings = int(round(category_buildings[cat]))
            sizes = self.building_sizes[cat]
            # Distribute buildings proportionally: 40%, 40%, 20% by default
            proportions = [0.4, 0.4, 0.2]
            count_per_size = [max(1, int(n_buildings * p)) for p in proportions]
            # Adjust in case rounding changed total
            diff = n_buildings - sum(count_per_size)
            count_per_size[0] += diff  # add difference to first size
            count_per_size = [max(1, c) for c in count_per_size]

            
            buildings_per_size[cat] = count_per_size

            # Total category area
            category_area = self.area * (self.building_categories[cat] * footprint_multipliers[cat] / weighted_sum)
            
            # Area per building for each size
            total_multiplier = sum(sizes)
            max_building_area = 0.1 * self.area  # max 10% of total area per building
            area_per_building_size[cat] = [
                min(category_area * (s / total_multiplier) / count_per_size[i], max_building_area)
                for i, s in enumerate(sizes)
            ]   

            
            # Average people per building for each size
            total_people = self.population * self.building_categories[cat]
            people_per_building_size[cat] = [
                total_people * (s / total_multiplier) / max(1, count_per_size[i])
                for i, s in enumerate(sizes)
            ]


        # Step 5: overall average people per building
        avg_people_per_building = self.population / total_buildings

        return {
            'total_buildings': round(total_buildings),
            'avg_people_per_building': avg_people_per_building,
            'category_buildings': {cat: round(num) for cat, num in category_buildings.items()},
            'buildings_per_size': buildings_per_size,
            'area_per_building_size_m2': {cat: [a*1_000_000 for a in areas] for cat, areas in area_per_building_size.items()},
            'people_per_building_size': people_per_building_size
        }



def main():
    population = int(input("Enter total population: "))
    if population <= 0:
        raise ValueError("Population must be greater than 0.")
    
    area = float(input("Enter total area (sq km): "))
    if area <= 0:
        raise ValueError("Area must be greater than 0.")    
    
    categories = {}
    print("Enter category percentages (as decimals, sum should be 1.0):")
    for cat in ['residential', 'commerce', 'industry', 'recreation']:
        categories[cat] = float(input(f"{cat.title()}: "))

    # After reading the category inputs:
    for cat, pct in categories.items():
        if pct > 1.0:
            print(f"Note: converting {cat} from {pct} to {pct/100:.2f}")
            categories[cat] = pct / 100.0


    for cat, pct in categories.items():
        if pct < 0:
            raise ValueError(f"Category percentage for {cat} cannot be negative")

    total_pct = sum(categories.values())
    if abs(total_pct - 1.0) > 0.001:
        print("Warning: category percentages do not sum to 1.0. Normalizing automatically.")
        categories = {k: v/total_pct for k,v in categories.items()}
    
    town = TownGenerator(population, area, categories)
    result = town.calculate_buildings()

    print("\n=== Town Building Report ===")
    print(f"Population: {population:,}")
    print(f"Total area: {area} sq km")
    print(f"Total buildings: {result['total_buildings']}")
    print(f"Average people per building: {result['avg_people_per_building']:.2f}\n")
    
    for cat in ['residential', 'commerce', 'industry', 'recreation']:
        print(f"{cat.title()} buildings (total: {result['category_buildings'][cat]}):")
        for i, (count, area_m2, people) in enumerate(zip(result['buildings_per_size'][cat],
                                                          result['area_per_building_size_m2'][cat],
                                                          result['people_per_building_size'][cat])):
            print(f"  Size {i+1}: {count} buildings, {area_m2:.2f} m² each, {people:.2f} people each")
        print()



if __name__ == "__main__":
    main()
