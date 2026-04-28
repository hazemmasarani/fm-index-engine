import tracemalloc
import random

from fm_index_engine.dc3 import build_sa_dc3
from fm_index_engine.suffix_array import build_sa_naive

# Log file to store Memory results
log_file = "log/mem_comp_log.log"

alphabet = [2, 4, 8, 16, 32, 64, 128]

num_expr_rep = 5

start_str_size = 1000

max_str_size = 100000

step_size = 1000

naive_limit = 10000  # Maximum string size for which to run the naive implementation

if __name__ == "__main__":

    for alpha in alphabet:

        for str_size in range(start_str_size, max_str_size + 1, step_size):
            print(f"Testing Alphabet Size: {alpha}, String Size: {str_size}")

            naive_mem = []
            dc3_mem = []

            for _ in range(num_expr_rep):
                # Generate random text
                text = [random.randint(1, alpha) for _ in range(str_size)]

                # Memory the naive implementation
                if str_size <= naive_limit:
                    tracemalloc.start()
                    build_sa_naive(text)
                    current, peak = tracemalloc.get_traced_memory()
                    tracemalloc.stop()
                    naive_mem.append(peak / (1024 * 1024))  # Convert to MB
                else:
                    naive_mem.append(None)  # Indicate that the naive implementation was not run

                # Memory the DC3 implementation
                tracemalloc.start()
                build_sa_dc3(text)
                current, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                dc3_mem.append(peak / (1024 * 1024))  # Convert to MB

            # Log the results
            with open(log_file, "a") as f:
                f.write(f"Alphabet Size: {alpha}, String Size: {str_size}, Naive Memory: {naive_mem}, DC3 Memory: {dc3_mem}\n")
