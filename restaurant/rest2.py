import simpy
    
number_of_tables = 3

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
  tables = simpy.Resource(env, capacity=number_of_tables)
  # Create the customer process
  env.process(customer(env, "Customer", tables))
  # Run the simulation until closing time
  env.run()

if __name__ == "__main__":
  main()