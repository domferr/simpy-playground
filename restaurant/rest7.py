import simpy

number_of_customers = 8
number_of_waiters = 3
closing_time = 20

def kitchen(env, kitchen_orders, kitchen_ready_food):
    while True:
        customer_order, customer_name = yield kitchen_orders.get()
        yield env.timeout(4)  # Time it takes to prepare the food
        yield kitchen_ready_food.put((customer_order, customer_name))
        print(f'{customer_name} food is ready at time {env.now}')

def waiter(env, name, kitchen_ready_food):
    while True:
        customer_order, customer_name = yield kitchen_ready_food.get()
        # The waiter serves the food to the customer
        serve_time = 2 # random.randint(1, 5) # Time to serve the food to the customer
        yield env.timeout(serve_time)
        print(f"{name} has served the food to {customer_name} at time {env.now}")
        customer_order.put(name)

def customer(env, name, arriving_time, tables, kitchen_orders):
    # The customer will arrive at time <arriving_time>
    yield env.timeout(arriving_time)

    print(f'{name} arrives and requests a table at time {env.now}')

    with tables.request() as table_request:
        max_waiting_time = max(0, closing_time - env.now)
        result = yield table_request | env.timeout(max_waiting_time)  # Request a table
        if table_request not in result:  # Customer leaves if no table is available within closing hours
            print(f'Sorry, {name}, the restaurant is closed at time {env.now}.')
            return
        
        print(f'{name} is seated at time {env.now}')

        choice_time = 5 # random.randint(1, 5)  # Time to choose what to eat (1-5 time units)
        yield env.timeout(choice_time)
        print(f"{name} has chosen what to eat at time {env.now}")

        # The customer places its order
        customer_order = simpy.Store(env)
        yield kitchen_orders.put((customer_order, name))

        # Wait to be served
        yield customer_order.get()

        # The customer eats
        eating_time = 3 # random.randint(2, 6)  # Time to eat (2-6 time units)
        yield env.timeout(eating_time)
        print(f"{name} has finished eating at time {env.now}")
    
def main():
    # Create a SimPy environment
    env = simpy.Environment()
    tables = simpy.Resource(env, capacity=4)
    kitchen_orders = simpy.Store(env)
    kitchen_ready_food = simpy.Store(env)
    
    for i in range(number_of_customers):  # More customers to simulate higher demand
        env.process(customer(env, f'Customer {i}', i+4, tables, kitchen_orders))

    for i in range(number_of_waiters):
        env.process(waiter(env, f'Waiter {i}', kitchen_ready_food))

    env.process(kitchen(env, kitchen_orders, kitchen_ready_food))
    
    # Run the simulation
    env.run()

if __name__ == "__main__":
    main()