import time
import random

from fm_index_engine.dc3 import build_sa_dc3

# New log file
log_file = "log/alphabet_time_comp.log"

alphabet = [4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]
string_sizes = [1000, 10000, 100000, 1000000]

def get_repetitions(n):
    """Reduce repetitions for large inputs"""
    if n <= 10000:
        return 5
    elif n <= 100000:
        return 3
    else:
        return 1

if __name__ == "__main__":

    for alpha in alphabet:
        for str_size in string_sizes:

            num_expr_rep = 5

            print(f"Testing Alphabet Size: {alpha}, String Size: {str_size}, Reps: {num_expr_rep}")

            dc3_times = []

            for _ in range(num_expr_rep):

                # Generate random text
                text = [random.randint(1, alpha) for _ in range(str_size)]

                # Time DC3
                start_time = time.time()
                build_sa_dc3(text)
                dc3_times.append(time.time() - start_time)

            # Log results
            with open(log_file, "a") as f:
                f.write(
                    f"Alphabet Size: {alpha}, String Size: {str_size}, "
                    f"DC3 Times: {dc3_times}\n"
                )