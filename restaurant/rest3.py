import simpy
    
number_of_tables = 2
number_of_customers = 4;

def customer(env, name, tables):
  with tables.request() as table_request:
    yield table_request # Wait for the resource
    print(f"{name} is seated at time {env.now}")
    
    # Choose what to eat
    yield env.timeout(4)
    print(f"{name} has chosen what to eat at time {env.now}")

    # Eat the food
    yield env.timeout(10)
    print(f"{name} has finished eating at time {env.now}")
  # Resource is automatically released

def main():
  # Create a SimPy environment
  env = simpy.Environment()

  # Create the tables
  tables = simpy.Resource(env, capacity=number_of_tables)

  # Create the customer processes
  for i in range(number_of_customers):
    env.process(customer(env, f'Customer {i}', tables))

  # Run the simulation until closing time
  env.run()

if __name__ == "__main__":
  main()