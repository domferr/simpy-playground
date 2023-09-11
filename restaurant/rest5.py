import simpy

number_of_customers = 3
closing_time = 20

def customer(env, name, kitchen, waiters):
    choice_time = 5 # random.randint(1, 5)  # Time to choose what to eat (1-5 time units)
    yield env.timeout(choice_time)
    print(f"{name} has chosen what to eat at time {env.now}")

    # The customer places an order
    with kitchen.request() as food_request: # Generate a request event
        yield food_request  # Request access to the kitchen. Wait here
        yield env.timeout(5)  # Time it takes to prepare the food
        print(f'{name}\'s food is ready at time {env.now}')
    # Resource released automatically

    # Food is prepared, wait for a waiter to bring the food
    with waiters.request() as waiter_request: # Request access to a waiter
        yield waiter_request  # Wait for a waiter to be available
        # The waiter serves the food to the customer
        serve_time = 2 # random.randint(1, 5) # Time to serve the food to the customer
        yield env.timeout(serve_time)
        print(f"{name} has received the food at time {env.now}")

    # The customer eats
    eating_time = 3 # random.randint(2, 6)  # Time to eat (2-6 time units)
    yield env.timeout(eating_time)
    print(f"{name} has finished eating at time {env.now}")
    
def main():
    # Create a SimPy environment
    env = simpy.Environment()
    kitchen = simpy.Resource(env, capacity=1)  # 1 kitchen
    waiters = simpy.Resource(env, capacity=6)  # 6 waiters
    for i in range(number_of_customers):  # More customers to simulate higher demand
        env.process(customer(env, f'Customer {i}', kitchen, waiters))
    # Run the simulation until closing time
    env.run()

if __name__ == "__main__":
    main()