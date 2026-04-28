#include <bits/stdc++.h>

using namespace std;


vector<int> build_sa_nlogn(vector<int> &text) {
    int n = text.size();

    vector<int> sa(n), rank(n), tmp(n);

    // Initial ranking based on values
    for (int i = 0; i < n; i++) {
        sa[i] = i;
        rank[i] = text[i];
    }

    for (int k = 1; k < n; k <<= 1) {
        // Custom comparator
        auto cmp = [&](int i, int j) {
            if (rank[i] != rank[j])
                return rank[i] < rank[j];

            int ri = (i + k < n) ? rank[i + k] : -1;
            int rj = (j + k < n) ? rank[j + k] : -1;
            return ri < rj;
        };

        sort(sa.begin(), sa.end(), cmp);

        // Recompute temporary ranks
        tmp[sa[0]] = 0;
        for (int i = 1; i < n; i++) {
            tmp[sa[i]] = tmp[sa[i - 1]] + (cmp(sa[i - 1], sa[i]) ? 1 : 0);
        }

        // Copy back
        rank = tmp;

        // Optimization: stop early if all ranks are unique
        if (rank[sa[n - 1]] == n - 1)
            break;
    }

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

int main() {
    
    vector<int> str_length = {1000, 10000, 100000, 1000000, 10000000};
    vector<int> alphabet_length = {4, 8, 16, 32, 64, 128, 256};
    int runs = 2;

    ofstream("./log/latency_doubling.log", ios::trunc).close(); 

    ofstream log_file("./log/latency_doubling.log");

    log_file << "str_len,alph,run,latency_ms\n";

    for (int str_len : str_length) {
        for (int alph : alphabet_length) {

            for (int i = 0; i < runs; ++i) {
                // generate alphabet once (good)
                vector<int> alph_vec = generate_1_to_n(alph);
                
                // generate text OUTSIDE timing of SA
                vector<int> text = generate_random_string(alph_vec, str_len);

                auto start = chrono::high_resolution_clock::now();

                auto sa = build_sa_nlogn(text);

                auto end = chrono::high_resolution_clock::now();

                double latency = chrono::duration<double, milli>(end - start).count();

                // log result
                log_file << str_len << ","
                         << alph << ","
                         << i << ","
                         << latency << "\n";

                cout     << str_len << ","
                         << alph << ","
                         << i << ","
                         << latency << "\n";
            }
        }
    }

    log_file.close();

    return 0;
}