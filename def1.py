def merge_list(*args, fill_value = None):
    max_length = max([len(lst) for lst in args])
    merged = []
    for i in range(max_length):
        merged.append([
        args[k][i] if i < len(args[k]) else fill_value for k in range(len(args))
    ])
    return merged
