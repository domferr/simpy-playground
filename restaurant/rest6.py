import simpy

number_of_customers = 4
number_of_tables = 2
number_of_waiters = 3

def kitchen(env, kitchen_orders, kitchen_ready_food):
    while True:
        # Wait for the next order
        cust_order, cust_name = yield kitchen_orders.get()

        print(f'Kitchen prepares {cust_name} food at time {env.now}')
        # Prepare the order's food
        yield env.timeout(4)  # Time it takes to prepare the food
        
        # Enqueue the food as ready
        yield kitchen_ready_food.put((cust_order, cust_name))
        
        print(f'{cust_name} food is ready at time {env.now}')

def waiter(env, name, kitchen_ready_food):
    while True:
        # Wait for the next food to be served
        customer_order, customer_name = yield kitchen_ready_food.get()
    
        # Serve the food to the customer
        yield env.timeout(2)

        print(f"{name} has served the food to {customer_name} at time {env.now}")
        
        # Notify the customer
        customer_order.put(name)

def customer(env, name, tables, kitchen_orders):
    with tables.request() as table_request:
        yield table_request # Wait for the resource
        print(f"{name} is seated at time {env.now}")

        choice_time = 4 # random.randint(1, 5)  # Time to choose what to eat (1-5 time units)
        yield env.timeout(choice_time)
        print(f"{name} has chosen what to eat at time {env.now}")

        # The customer places its order
        customer_order = simpy.Store(env)
        yield kitchen_orders.put((customer_order, name))

        # Wait to be served
        yield customer_order.get()

        # The customer eats
        eating_time = 10 # random.randint(2, 6)  # Time to eat (2-6 time units)
        yield env.timeout(eating_time)
        print(f"{name} has finished eating at time {env.now}")
    
def main():
    # Create a SimPy environment 
    env = simpy.Environment() 

    # Create the tables and the kitchen's queues
    tables = simpy.Resource(env, capacity=number_of_tables)
    kitchen_orders = simpy.Store(env)
    kitchen_ready_food = simpy.Store(env)

    # Create the customers processes
    for i in range(number_of_customers):
        env.process(customer(env, f'Customer {i}', tables, kitchen_orders))

    # Create the waiters processes
    for i in range(number_of_waiters):
        env.process(waiter(env, f'Waiter {i}', kitchen_ready_food))

    # Create the kithen process
    env.process(kitchen(env, kitchen_orders, kitchen_ready_food))

    # Run the simulation 
    env.run() 

if __name__ == "__main__":
    main()