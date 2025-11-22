class DecisionEngine:
    def __init__(self):
        self.speed_limit = 30  # Default speed limit in km/h
        self.safety_distance = 5  # Safety distance in meters

    def evaluate_conditions(self, pothole_detected, distance_to_obstacle):
        if pothole_detected:
            self.adjust_speed('slow_down')
        elif distance_to_obstacle < self.safety_distance:
            self.adjust_speed('avoidance')

    def adjust_speed(self, action):
        if action == 'slow_down':
            print("Slowing down to ensure safety.")
            # Implement logic to reduce speed
        elif action == 'avoidance':
            print("Taking avoidance action.")
            # Implement logic for steering or maneuvering

    def log_decision(self, action):
        # Implement logging logic here
        print(f"Action taken: {action}")

# Example usage
if __name__ == "__main__":
    engine = DecisionEngine()
    # Simulate conditions
    engine.evaluate_conditions(pothole_detected=True, distance_to_obstacle=3)