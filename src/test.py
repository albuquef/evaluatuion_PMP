import time

# Function to print even numbers for 10 seconds
def print_even_numbers_for_10_seconds():
    start_time = time.time()
    n = 2  # Starting with the first even number

    while time.time() - start_time < 0.5:
        # print(n)
        n += 2  # Move to the next even number
        # time.sleep(0.1)  # Sleep for a short duration to slow down the printing
    print(n)
# Run the function
print_even_numbers_for_10_seconds()
578800