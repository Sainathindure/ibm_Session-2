import random
import math
import time

# Three cost functions are described in the project guidelines
def cost1(x, y):
    if x == y:
        return 0
    elif x < 3 and y < 3:
        return 200
    elif x < 3:
        return 200
    elif y < 3:
        return 200
    elif (x % 7) == (y % 7):
        return random.randint(5, 20)
    else:
        return abs(x - y) + 3

def cost2(x, y):
    if x == y:
        return 0
    elif (x + y) < 10:
        return abs(x - y) + 4
    elif (x + y) % 11 == 0:
        return 3
    else:
        return abs(x - y) ** 2 + 10

def cost3(x, y):
    if x == y:
        return 0
    else:
        return 0

# Function that returns a random path given a total number of cities
def random_path(no_cities, seed1):
    tour = list(range(no_cities))
    random.seed(seed1)
    random.shuffle(tour)
    return tour

# Given a list of cities, calculates the cost of the tour
def tour_cost(tours, cost_fun):
    total_cost = 0
    cost_i = 0
    n = len(tours)

    for i, city in enumerate(tours):
        if i == n - 1:
            if cost_fun == "c1":
                cost_i = cost1(tours[i], tours[0])
            elif cost_fun == "c2":
                cost_i = cost2(tours[i], tours[0])
            elif cost_fun == "c3":
                cost_i = cost3(tours[i], tours[0])
            total_cost += cost_i
        else:
            if cost_fun == "c1":
                cost_i = cost1(tours[i], tours[i + 1])
            elif cost_fun == "c2":
                cost_i = cost2(tours[i], tours[i + 1])
            elif cost_fun == "c3":
                cost_i = cost3(tours[i], tours[i + 1])
            total_cost += cost_i

    return total_cost

# Mutation operator that swaps two cities randomly to create a new path
def mutation_operator(tours):
    r1 = list(range(len(tours)))
    r2 = list(range(len(tours)))
    random.shuffle(r1)
    random.shuffle(r2)

    for i in r1:
        for j in r2:
            if i < j:
                next_state = tours[:]
                next_state[i], next_state[j] = tours[j], tours[i]
                yield next_state

# Probabilistically choosing a neighbor
def probability_acceptance(prev_score, next_score, temperature):
    if next_score < prev_score:
        return 1.0
    elif temperature == 0:
        return 0.0
    else:
        return math.exp(-abs(next_score - prev_score) / temperature)

# The cooling schedule based on Kirkpatrick model
def cooling_schedule(start_temp, cooling_constant):
    T = start_temp
    while True:
        yield T
        T = cooling_constant * T

# This function implements randomized hill climbing for TSP
def randomized_hill_climbing(no_cities, cost_func, MEB, seed1):
    best_path = random_path(no_cities, seed1)
    best_cost = tour_cost(best_path, cost_func)
    evaluations_count = 1
    dict = {}

    while evaluations_count < MEB:
        for next_city in mutation_operator(best_path):
            if evaluations_count == MEB:
                break
            str1 = ''.join(str(e) for e in next_city)

            # Skip calculating the cost of repeated paths
            if str1 in dict:
                evaluations_count += 1
                continue

            next_tCost = tour_cost(next_city, cost_func)

            # Store it in the dictionary
            dict[str1] = next_tCost
            evaluations_count += 1

            # Selecting the path with the lowest cost
            if next_tCost < best_cost:
                best_path = next_city
                best_cost = next_tCost

    return best_cost, best_path, evaluations_count

# This function implements simulated annealing for TSP
def simulated_annealing(no_cities, cost_func, MEB, seed1):
    start_temp = 70
    cooling_constant = 0.9995
    best_path = None
    best_cost = None
    current_path = random_path(int(no_cities), seed1)
    current_cost = tour_cost(current_path, cost_func)

    if best_path is None or current_cost < best_cost:
        best_cost = current_cost
        best_path = current_path

    num_evaluations = 1
    temp_schedule = cooling_schedule(start_temp, cooling_constant)

    for temperature in temp_schedule:
        flag = False

        # Examining moves around our current path
        for next_path in mutation_operator(current_path):
            if num_evaluations == MEB:
                flag = True
                break

            next_cost = tour_cost(next_path, cost_func)

            if best_path is None or next_cost < best_cost:
                best_cost = next_cost
                best_path = next_path

            num_evaluations += 1
            p = probability_acceptance(current_cost, next_cost, temperature)

            if random.random() < p:
                current_path = next_path
                current_cost = next_cost
                break

        if flag:
            break

    return best_path, best_cost, num_evaluations

keeprunning = True

while keeprunning:
    no_cities = int(input("Enter number of cities: "))
    MEB = int(input("Enter MEB: "))
    dict = {}

    cost_func = input("Enter the cost function (c1, c2, or c3): ")
    seed1 = int(input("Enter the seed: "))
    search_strat = int(input("Enter the search strategy (1 for Simple, 2 for Sophisticated): "))

    start_time = time.time()

    if search_strat == 1:
        print("This is the output of randomized hill climbing - Simple Search")
        best_path, best_cost, num_evaluations = randomized_hill_climbing(no_cities, cost_func, MEB, seed1)
    elif search_strat == 2:
        print("This is the output of simulated annealing - Sophisticated Search")
        best_path, best_cost, num_evaluations = simulated_annealing(no_cities, cost_func, MEB, seed1)
    else:
        print("Please enter a valid option either 1 or 2 !!")
        break

    print("The cost of best solution", best_cost)
    print("Path of best solution", best_path)
    print("Value of MEB count", num_evaluations)
    print("********** %s seconds *********" % (time.time() - start_time))

    # Write results to a file
    with open("2runs.txt", "a") as f:
        print("The cost of best Solution", best_cost, file=f)
        print("The path of best solution", best_path, file=f)
        print("Value of MEB count is", num_evaluations, file=f)

    stop = input("Do you want to run this program again? (yes or no): ")
    if stop == "no":
        keeprunning = False
        break
