def freq_pattern_mining():
    freq_itemsets = [] # [[400,'B'],[300,'C'],[200, 'AB'],...]
    deleted_itemsets = []
    # Turn txt to list of list
    file = open('test_input.txt', 'r')
    lines = file.readlines()
    for i in range(len(lines)): 
        lines[i] = (lines[i].strip()).split()
    min_support = int(lines[0][0])
    lines.pop(0)

    # Create output file
    outputFile = open('test_output.txt', 'w')

    # Create dictionary -- single item itemset
    support_dict = {}
    for trans in lines:
        for item in trans:
            if support_dict.get(item) == None:
                support_dict.update({item: 1})
            else: 
                support_dict.update({item: support_dict[item] + 1})

    # Save frequent itemset to freq_itemsets and remove infrequent
    # from support_dict
    for key in support_dict:
        if support_dict[key] >= min_support:
            freq_itemsets.append([support_dict[key], key])
        else: 
            deleted_itemsets.append(key)
    for deleted in deleted_itemsets:
        if support_dict.get(deleted) != None: 
            del support_dict[deleted]

    last_key_list = list(support_dict.keys())

    for setLen in range(2,200): # 2,200
        # grouping
        support_dict2 = {}
        scan_list_tmp = []
        for i in range(len(last_key_list)-1):
            for j in range(i, len(last_key_list)):
                temp = list(set(last_key_list[i]) | set(last_key_list[j]))
                if len(temp) == setLen:
                    scan_list_tmp.append(sorted(temp))

        # remove repeated items from scan_list_tmp
        scan_list = []
        [scan_list.append(x) for x in scan_list_tmp if x not in scan_list]
        # pruning
        for to_scan in scan_list:
            for deleted in deleted_itemsets:
                if all(x in to_scan for x in deleted):
                    scan_list.remove(to_scan)
                    break

        # Scanning for frequency
        # support_dict2 will have itemset: support
        for to_scan in scan_list:
            for trans in lines:
                if all(x in trans for x in to_scan):
                    if support_dict2.get(''.join(sorted(to_scan))) == None:
                        support_dict2.update({''.join(sorted(to_scan)): 1})
                    else: 
                        support_dict2.update({''.join(sorted(to_scan)): support_dict2[''.join(sorted(to_scan))] + 1})
        # Save frequent itemset to freq_itemsets and remove infrequent
        # from support_dict2
        freq_count = 0
        for key in support_dict2:
            if support_dict2[key] >= min_support:
                freq_itemsets.append([support_dict2[key], key])
                freq_count += 1
            else: 
                deleted_itemsets.append(key)
        for deleted in deleted_itemsets:
            if support_dict2.get(deleted) != None: 
                del support_dict2[deleted]
        
        last_key_list = list(support_dict2.keys())
        if freq_count < 2:
            break
    # Write frequent pattern to output file
    sorted_freq_itemsets = sorted(freq_itemsets, key=lambda x: (-x[0], x[1]))
    for item in sorted_freq_itemsets:
        outputFile.write(str(item[0]) + ": " + " ".join(item[1]) + '\n')
    outputFile.write('\n')
    
    # Closed pattern mining
    closed_itemset = sorted_freq_itemsets.copy()
    for i in range(len(sorted_freq_itemsets)):
        cand = sorted_freq_itemsets[i]
        for j in range(len(sorted_freq_itemsets)):
            if i == j:
                continue
            comp = sorted_freq_itemsets[j]
            if cand[0] == comp[0] and all(x in comp[1] for x in cand[1]):
                # print(cand)
                # print(comp)
                closed_itemset.remove(cand)
                break
    # Write closed pattern to output file
    sorted_closed = sorted(closed_itemset, key=lambda x: (-x[0], x[1]))
    for item in sorted_closed:
        outputFile.write(str(item[0]) + ": " + " ".join(item[1]) + '\n')
    outputFile.write('\n')

    # maximal pattern mining
    max_itemset = sorted_freq_itemsets.copy()
    for i in range(len(sorted_freq_itemsets)):
        cand = sorted_freq_itemsets[i]
        for j in range(len(sorted_freq_itemsets)):
            if i == j:
                continue
            comp = sorted_freq_itemsets[j]
            if all(x in comp[1] for x in cand[1]):
                # print(cand)
                # print(comp)
                max_itemset.remove(cand)
                break
    # Write closed pattern to output file
    sorted_max = sorted(max_itemset, key=lambda x: (-x[0], x[1]))
    for item in sorted_max:
        outputFile.write(str(item[0]) + ": " + " ".join(item[1]) + '\n')

    # close both files
    file.close()
    outputFile.close()

# call the function
freq_pattern_mining()