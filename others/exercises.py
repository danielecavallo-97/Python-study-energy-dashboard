class Restaurant:
    def __init__(self, name, cuisine_type):
        self.name = name
        self.cuisine_type = cuisine_type
    def describe_restaurant(self):
        print(self.name + " serves " + self.cuisine_type + " cuisine.")

restaurant_ita = Restaurant("Dallo zozzo", "Italian")
restaurant_mex = Restaurant("El taco loco", "Mexican")
restaurant_jap = Restaurant("Sushi House", "Japanese")

print(Restaurant.describe_restaurant(restaurant_ita))
#print(Restaurant.describe_restaurant(restaurant_mex))
#print(Restaurant.describe_restaurant(restaurant_jap))
