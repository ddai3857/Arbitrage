from collections import OrderedDict
    

#TAKES IN USER INPUT FOR EXCHANGE RATE INFORMATION
def read_exchange_rates():
    num_inputs : int = int(input("How many exchange rates: "))
    
    print("")
    
    string_rates : list[str] = []
    for i in range(num_inputs):
        string_rates += [input(f"Exchange Rate " + str(i + 1) + " (curr1 curr2 rate): ").strip().lower()]
        
    return string_rates

#CREATES A LIST OF ALL CURRENCIES
def currency_list(string_rates : list[str]):
    currencies = OrderedDict()
    for sr in string_rates:
        curr1, curr2, rate = sr.split(" ")
        currencies[curr1] = 1
        currencies[curr2] = 1

    return list(currencies.keys())

#CREATES AN ADJACENCY MATRIX USING RATES
def create_exchange_matrix(curr_list : list[str], string_rates : list[str]):
    num_curr = len(curr_list)
    
    exchange_matrix : list[list[float]] = [[-1 for i in range(num_curr)] for i in range(num_curr)]
    
    for sr in string_rates:
        curr1, curr2, rate = sr.split(" ")
        idx1 = curr_list.index(curr1)
        idx2 = curr_list.index(curr2)
        exchange_matrix[idx1][idx2] = float(rate)
        exchange_matrix[idx2][idx1] = 1 / float(rate)
        
    return exchange_matrix

#PERFORMS AN EXCHANGE
def exchange(curr_list : list[str], exchange_matrix : list[list[float]], amount : float, old_curr : str, new_curr : str):
    return round(amount * exchange_matrix[curr_list.index(old_curr)][curr_list.index(new_curr)], 2)

#DEPTH FIRST SEARCH ALGORITHM TO PERFORM ALL EXCHANGE CYCLES
def dfs(outcomes : list[tuple[float, list[str]]], curr_list : list[str], exchange_matrix : list[list[float]], start_amount : float, exchange_list : list[str], to_exchange : list[str]):
    for c in to_exchange:
        new_amount = exchange(curr_list, exchange_matrix, start_amount, exchange_list[-1], c)
        if (len(exchange_list) > 1):
            outcomes += [(new_amount, exchange_list + [c])]
        new_list = to_exchange.copy()
        new_list.remove(c)
        dfs(outcomes, curr_list, exchange_matrix, new_amount, exchange_list + [c], new_list)
    
#USES THE DFS FUNCTION AND THEN CONVERTS FINAL AMOUNTS BACK TO STARTING CURRENCY AND RETURNS MAX
def arbitrage(curr_list : list[str], exchange_matrix : list[list[float]], start_amount : float, start_curr : str):
    outcomes : list[tuple[float, list[str]]] = []
    other_list = curr_list.copy()
    other_list.remove(start_curr)
    dfs(outcomes, curr_list, exchange_matrix, start_amount, [start_curr], other_list)
    
    outcomes = [(exchange(curr_list, exchange_matrix, amount, curr[-1], start_curr), curr) for (amount, curr) in outcomes]
    
    print("ALL POSSIBLE EXCHANGE CYCLES\n")
    
    for amt,cycle in outcomes:
        print(f"${amt} -> {cycle}")
    
    best_outcome = max(outcomes)
    
    print("")
    print(f"BEST OUTCOME: {best_outcome[0]} -> {best_outcome[1]}")
    
    return 0;
    
def main():
    string_rates = read_exchange_rates()

    curr_list = currency_list(string_rates)
    exchange_matrix = create_exchange_matrix(curr_list, string_rates)
    
    print("")
    
    starting : list[str] = input("Starting amount (amount curr): ").strip().lower().split()
    start_amount : float = float(starting[0])
    start_curr : str = starting[1]
    
    print("\n-----------------------------\n")
    
    arbitrage(curr_list, exchange_matrix, start_amount, start_curr)
    
    print("")  
        
if __name__=="__main__":
    main()