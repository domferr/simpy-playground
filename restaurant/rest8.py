import simpy

number_of_customers = 5
number_of_waiters = 2
number_of_tables = 3
closing_time = 10

def log(env: simpy.Environment, text: str):
    print(f'[{"{: >3}".format(env.now)} ] {text}')

def kitchen(env, kitchen_orders, kitchen_ready_food):
    while True:
        customer_order, customer_name = yield kitchen_orders.get()
        log(env, f'Kitchen is preparing {customer_name} food')
        yield env.timeout(3)  # Time it takes to prepare the food
        yield kitchen_ready_food.put((customer_order, customer_name))
        log(env, f'{customer_name} food is ready')

def waiter(env, name, kitchen_ready_food):
    while True:
        customer_order, customer_name = yield kitchen_ready_food.get()
        # The waiter serves the food to the customer
        serve_time = 2 # random.randint(1, 5) # Time to serve the food to the customer
        log(env, f"{name} is bringing the food to {customer_name}")
        yield env.timeout(serve_time)
        log(env, f"{name} has served the food to {customer_name}")
        customer_order.put(name)

def customer(env, name, arriving_time, tables, kitchen_orders):
    # The customer will arrive at time <arriving_time>
    yield env.timeout(arriving_time)
    log(env, f'{name} arrives and requests a table')

    with tables.request() as table_request:
        max_waiting_time = max(0, closing_time - env.now)
        result = yield table_request | env.timeout(max_waiting_time)  # Request a table
        if table_request not in result:  # Customer leaves if no table is available within closing hours
            log(env, f'Sorry, {name}, the restaurant is closed')
            return
        
        log(env, f'{name} is seated')

        choice_time = 2 # random.randint(1, 5)  # Time to choose what to eat (1-5 time units)
        yield env.timeout(choice_time)
        log(env, f"{name} has chosen what to eat")

        # The customer places its order
        customer_order = simpy.Store(env)
        yield kitchen_orders.put((customer_order, name))

        # Wait to be served
        yield customer_order.get()

        # The customer eats
        eating_time = 5 # random.randint(2, 6)  # Time to eat (2-6 time units)
        yield env.timeout(eating_time)
        log(env, f"{name} has finished eating and leaves the restaurant")
    
def main():
    # Create a SimPy environment
    env = simpy.Environment()
    tables = simpy.Resource(env, capacity=number_of_tables)
    kitchen_orders = simpy.Store(env)
    kitchen_ready_food = simpy.Store(env)
    
    for i in range(number_of_customers):  # More customers to simulate higher demand
        env.process(customer(env, f'Customer {i}', i+4, tables, kitchen_orders))

    for i in range(number_of_waiters):
        env.process(waiter(env, f'Waiter {i}', kitchen_ready_food))

    env.process(kitchen(env, kitchen_orders, kitchen_ready_food))
    
    env.run() # Run the simulation

if __name__ == "__main__":
    main()