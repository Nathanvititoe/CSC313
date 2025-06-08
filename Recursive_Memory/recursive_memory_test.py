import time

# display arr size in readable format
def format_arr_size(n):
    if n >= 1000000000:
        return f"{n / 1000000000:.2f} billion"
    elif n >= 1000000:
        return f"{n / 1000000:.2f} million"
    elif n >= 1000:
        return f"{n / 1000:.0f} thousand"
    else:
        return str(n)


# function to use a lot of memory
def recursive_memory_user(total_depth, curr_depth, arr):
    countdown_depth = total_depth - curr_depth + 1 

    # log recursion countdown (1/20, 2/20, etc) and size of arr
    print(f"{countdown_depth}/{total_depth} - Array size: {format_arr_size(len(arr))} elements")
    
    time.sleep(0.5)  # add delay to make monitoring easier

    # when depth reaches 0, stop recursion
    if curr_depth == 0:
        return
    
    # full copy the array and append new list of same size (double arr size)
    new_arr = arr[:] + [0] * len(arr) 

    # recursively call this function again, reduce depth by 1, pass new arr
    recursive_memory_user(total_depth, curr_depth - 1, new_arr)

if __name__ == "__main__":
    initial_array = [1] * 2000  # initial arr is 2000 elements (value 1)
    recursive_memory_user(20, 20, initial_array) # recurse 20 times
