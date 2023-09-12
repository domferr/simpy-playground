import simpy
    
number_of_tables = 2
number_of_customers = 3;

def customer(env, name, tables, kitchen_orders):
  with tables.request() as table_request:
    yield table_request # Wait for the resource
    print(f"{name} is seated at time {env.now}")
  
    # Choose what to eat
    yield env.timeout(4)
    print(f"{name} has chosen what to eat at time {env.now}")

    # The customer places its order
    yield kitchen_orders.put(name)

    # Eat the food
    yield env.timeout(10)
    print(f"{name} has finished eating at time {env.now}")

def kitchen(env, kitchen_orders):
  while True:
    # Wait for the next order
    cust_name = yield kitchen_orders.get()

    print(f'Kitchen prepares {cust_name} food at time {env.now}')
    # Prepare the order's food
    yield env.timeout(4)  # Time it takes to prepare the food
     
    print(f'{cust_name} food is ready at time {env.now}')

def main():
  # Create a SimPy environment
  env = simpy.Environment()

  # Create the tables
  kitchen_orders = simpy.Store(env)
  tables = simpy.Resource(env, capacity=number_of_tables)

  # Create the customer processes
  for i in range(number_of_customers):
    env.process(customer(env, f'Customer {i}', tables, kitchen_orders))

  env.process(kitchen(env, kitchen_orders))

  # Run the simulation until closing time
  env.run()

if __name__ == "__main__":
  main()