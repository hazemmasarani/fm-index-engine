import time
import random

from fm_index_engine.dc3 import build_sa_dc3
from fm_index_engine.doubling import build_sa_doubling
from fm_index_engine.naive import build_sa_naive

# Log file to store timing results
log_file = "log/time_comp_log.log"

alphabet = [2, 4, 8, 16, 32, 64, 128]

string_sizes = [100, 1000, 5000, 10000, 50000, 100000, 500000, 1000000]

num_expr_rep = 5

naive_limit = 10000  # Maximum string size for which to run the naive implementation

doubling_limit = 1000000  # Maximum string size for which to run the doubling implementation

if __name__ == "__main__":

    for alpha in alphabet:

        for str_size in string_sizes:
            print(f"Testing Alphabet Size: {alpha}, String Size: {str_size}")

            naive_times = []
            dc3_times = []
            doubling_time = []

            for _ in range(num_expr_rep):
                # Generate random text
                text = [random.randint(1, alpha) for _ in range(str_size)]

                # Time the naive implementation
                if str_size <= naive_limit:
                    start_time = time.time()
                    build_sa_naive(text)
                    end_time = time.time()
                    naive_times.append(end_time - start_time)
                else:
                    naive_times.append(None)  # Indicate that the naive implementation was not run

                # Time the doubling implementation
                if str_size <= doubling_limit:
                    start_time = time.time()
                    build_sa_doubling(text)
                    end_time = time.time()
                    doubling_time.append(end_time - start_time)
                else:
                    doubling_time.append(None)  # Indicate that the doubling implementation was not run

                # Time the DC3 implementation
                start_time = time.time()
                build_sa_dc3(text)
                end_time = time.time()
                dc3_times.append(end_time - start_time)

            # Log the results
            with open(log_file, "a") as f:
                f.write(f"Alphabet Size: {alpha}, String Size: {str_size}, Naive Times: {naive_times}, Doubling Times: {doubling_time}, DC3 Times: {dc3_times}\n")
