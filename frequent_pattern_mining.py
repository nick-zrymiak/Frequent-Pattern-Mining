from efficient_apriori import apriori
import copy

def k_itemsets_counts(itemsets):
    counts = {} 
    
    for length, itemsets_support in itemsets.items():
            counts[length] = len(itemsets_support)
            
    return counts 

def remove_empty_values(itemsets):
    for key, value in copy.deepcopy(itemsets).items():
        if not value:
            del itemsets[key]
            
    return itemsets

def remove_supports(itemsets_supports):
    itemsets_supports = itemsets_supports.values()
    itemsets = []
    
    for k_itemsets_supports in reversed(list(itemsets_supports)):
        for itemset in list(k_itemsets_supports.keys()):
            itemsets.append(itemset)
    
    return itemsets

def maximal_itemsets(frequent_itemsets):
    maximal_itemsets = frequent_itemsets
    frequent_itemsets = remove_supports(frequent_itemsets)
    
    for i, maximal_itemset in enumerate(frequent_itemsets):
        for candidate_subset in frequent_itemsets[i+1:]:
            if set(candidate_subset).issubset(maximal_itemset):
                frequent_itemsets.remove(candidate_subset)
                del maximal_itemsets[len(candidate_subset)][candidate_subset]
    
    maximal_itemset = remove_empty_values(maximal_itemsets)
    
    return maximal_itemsets

def group_by_support(itemsets):
    support_itemsets = {}
    
    for itemset_support in reversed(list(itemsets.values())):
        for itemset, support in itemset_support.items():
            if support in support_itemsets:
                support_itemsets[support].append(itemset)
            else:
                support_itemsets[support] = [itemset]
    
    return support_itemsets

def closed_itemsets(frequent_itemsets):
    closed_itemsets = frequent_itemsets
    support_itemsets = group_by_support(frequent_itemsets)  
    
    for k_support_itemsets in support_itemsets.values():
        for i, closed_itemset in enumerate(k_support_itemsets):
            for candidate_subset in k_support_itemsets[i+1:]:
                if set(candidate_subset).issubset(closed_itemset):
                    k_support_itemsets.remove(candidate_subset)
                    del closed_itemsets[len(candidate_subset)][candidate_subset]
                    
    closed_itemset = remove_empty_values(closed_itemsets)
    
    return closed_itemsets

def remove_delimiters(transaction):
    ITEM_DELIMITER = '-1'
    LINE_DELIMITER = '-2'
    transaction = list(filter((ITEM_DELIMITER).__ne__, transaction))
    transaction = list(filter((LINE_DELIMITER).__ne__, transaction))
    return transaction

def input_transactions():
    transactions_file = open('./BMS2.txt')
    transactions = []
    
    for line in transactions_file:
        transaction = line.split()
        transaction = remove_delimiters(transaction)
        transactions.append(transaction)      
    
    return transactions

if __name__ == '__main__':
    transactions = input_transactions()
    frequent_itemsets = apriori(transactions, min_support=.005, min_confidence=.7)
    
    frequent_itemsets = frequent_itemsets[0]
    closed_itemsets = closed_itemsets(copy.deepcopy(frequent_itemsets))
    maximal_itemsets = maximal_itemsets(copy.deepcopy(frequent_itemsets))
    
    frequent_itemsets_counts = k_itemsets_counts(frequent_itemsets)
    closed_itemsets_counts = k_itemsets_counts(closed_itemsets)
    maximal_itemsets_counts = k_itemsets_counts(maximal_itemsets)
    
    print('frequent itemsets:', frequent_itemsets)
    print('closed itemsets:', closed_itemsets)
    print('maximal itemsets:', maximal_itemsets, '\n')
    
    print('frequent itemsets counts:', frequent_itemsets_counts)
    print('closed itemsets counts:', closed_itemsets_counts)
    print('maximal itemsets counts:', maximal_itemsets_counts)
