#include <bits/stdc++.h>
#include <windows.h>
#include <psapi.h>

using namespace std;


std::vector<int> build_suffix_array_naive(const std::vector<int> &s) {
    int n = s.size();

    std::vector<int> sa(n);
    for (int i = 0; i < n; i++) {
        sa[i] = i;
    }

    // Sort suffix indices
    std::sort(sa.begin(), sa.end(), [&](int a, int b) {
        int n = s.size();
        while (a < n && b < n) {
            if (s[a] != s[b])
                return s[a] < s[b];
            a++;
            b++;
        }
        return a == n; // shorter suffix comes first
    });

    return sa;
}

std::vector<int> generate_random_string(const std::vector<int>& input, int n) {
    static std::mt19937 gen(std::random_device{}());  // seeded once

    std::vector<int> result;
    result.reserve(n);

    std::uniform_int_distribution<> dist(0, input.size() - 1);

    for (int i = 0; i < n; ++i) {
        result.push_back(input[dist(gen)]);
    }

    return result;
}

std::vector<int> generate_1_to_n(int n) {
    vector<int> v(n);
    for (int i = 0; i < n; i++) {
        v[i] = i + 1;
    }
    return v;
}

size_t get_memory_usage() {
    PROCESS_MEMORY_COUNTERS info;
    GetProcessMemoryInfo(GetCurrentProcess(), &info, sizeof(info));
    return info.WorkingSetSize; // bytes
}

int main() {
    
    vector<int> str_length = {100000};
    vector<int> alphabet_length = {4, 8, 16, 32, 64, 128, 256};
    int runs = 20;

    ofstream("./log/memory_naive.log", ios::trunc).close();

    ofstream log_file("./log/memory_naive.log");

    log_file << "str_len,alph,run,memory_MB\n";

    for (int str_len : str_length) {
        for (int alph : alphabet_length) {

            
            for (int i = 0; i < runs; ++i) {
                
                
                vector<int> alph_vec = generate_1_to_n(alph);
                
                vector<int> text = generate_random_string(alph_vec, str_len);
                
                auto mem_before = get_memory_usage();

                auto sa = build_suffix_array_naive(text);

                auto mem_after = get_memory_usage();

                double used_mem = (mem_after - mem_before) / (1024 * 1024.0);

                // log result
                log_file << str_len << ","
                         << alph << ","
                         << i << ","
                         << used_mem << "\n";

                cout     << str_len << ","
                         << alph << ","
                         << i << ","
                         << used_mem << "\n";
            }
        }
    }

    log_file.close();

    return 0;
}