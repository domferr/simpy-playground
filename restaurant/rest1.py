import simpy
    
def customer(env, name):
    print(f"{name} is seated at time {env.now}")
    
    # Choose what to eat
    yield env.timeout(4)
    print(f"{name} has chosen what to eat at time {env.now}")

    # Eat the food
    yield env.timeout(10)
    print(f"{name} has finished eating at time {env.now}")

def main():
    # Create a SimPy environment
    env = simpy.Environment()
    # Create the customer process
    env.process(customer(env, "Customer"))
    # Run the simulation until closing time
    env.run()

if __name__ == "__main__":
    main()