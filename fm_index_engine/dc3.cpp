#include <bits/stdc++.h>

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

struct Triplet {
    int a;
    int b;
    int c;
    int index;
};

std::vector<int> build_sample_indices(int n) {

    std::vector<int> idx;

    for (int i = 1; i < n - 3; i += 3) {
        idx.push_back(i);
    }

    idx.push_back(n - 3);

    for (int i = 2; i < n - 3; i += 3) {
        idx.push_back(i);
    }

    return idx;
}

std::vector<Triplet> build_triplets(const std::vector<int> &text,  const std::vector<int> &indices) {

    std::vector<Triplet> triplets;
    triplets.reserve(indices.size());

    for (int i : indices) {
        Triplet t;
        t.a = text[i];
        t.b = text[i + 1];
        t.c = text[i + 2];
        t.index = i;

        triplets.push_back(t);
    }
    
    return triplets;
}

std::vector<Triplet> counting_sort(std::vector<Triplet> &triplets, int keyIndex) {

    // Step 1: find max value for the chosen key
    int max_val = 0;

    for (const auto &t : triplets) {
        int key;
        if (keyIndex == 0) key = t.a;
        else if (keyIndex == 1) key = t.b;
        else key = t.c;

        max_val = std::max(max_val, key);
    }

    // Step 2: create buckets
    std::vector<std::vector<Triplet>> buckets(max_val + 1);

    // Step 3: distribute
    for (const auto &t : triplets) {
        int key;
        if (keyIndex == 0) key = t.a;
        else if (keyIndex == 1) key = t.b;
        else key = t.c;

        buckets[key].push_back(t);
    }
    
    // Step 4: flatten
    std::vector<Triplet> sorted_triplets;
    sorted_triplets.reserve(triplets.size());

    for (const auto &bucket : buckets) {
        for (const auto &t : bucket) {
            sorted_triplets.push_back(t);
        }
    }

    return sorted_triplets;
}

void radix_sort(std::vector<Triplet> &triplets, int exp) {
    for (int i = exp; i >= 0; i--) {
        triplets = counting_sort(triplets, i);
    }
}

std::vector<int> build_r_1_2(std::vector<int> &reduced_sa, vector<int> &indices, int n){

    std::vector<int> r_1_2(n);

    return {};
}

std::vector<int> merge_group(std::vector<int> &l_0, std::vector<int> &l_1_2, std::vector<int> &r_1_2, std::vector<int> &text) {

    int i0 = 0, i1 = 1;
    int n0 = l_0.size(), n1 = l_1_2.size();

    std::vector<int> result;
    result.reserve(n0 + n1);

    while (i0 < n0 && i1 < n1) {
        int pos0 = l_0[i0];
        int pos12 = l_1_2[i1];

        bool take0;

        if (pos12 % 3 == 1) {
            // Compare (text[pos0], rank[pos0+1]) vs (text[pos12], rank[pos12+1])
            if (text[pos0] != text[pos12]) {
                take0 = text[pos0] < text[pos12];
            } else {
                take0 = r_1_2[pos0 + 1] < r_1_2[pos12 + 1];
            }
        } else {
            // pos12 % 3 == 2
            // Compare (text[pos0], text[pos0+1], rank[pos0+2])
            // vs     (text[pos12], text[pos12+1], rank[pos12+2])
            if (text[pos0] != text[pos12]) {
                take0 = text[pos0] < text[pos12];
            } else if (text[pos0 + 1] != text[pos12 + 1]) {
                take0 = text[pos0 + 1] < text[pos12 + 1];
            } else {
                take0 = r_1_2[pos0 + 2] < r_1_2[pos12 + 2];
            }
        }

        if (take0) {
            result.push_back(pos0);
            i0++;
        } else {
            result.push_back(pos12);
            i1++;
        }
    }

    // Append remaining
    while (i0 < n0) result.push_back(l_0[i0++]);
    while (i1 < n1) result.push_back(l_1_2[i1++]);

    return result;
}

std::vector<int> build_suffix_array(const std::vector<int> &str) {

    // Base case if length of text is 3 or less built it using naive approach
    if(str.size() <= 3){
        return build_suffix_array_naive(str);
    }

    // Stack 3 zeros at the end of the text to avoid out-of-bounds when creating triplets
    std::vector<int> text = str;
    text.resize(text.size() + 3, 0);

    int n = text.size();

    std::vector<int> indices = build_sample_indices(n);
    
    std::vector<Triplet> triplets = build_triplets(text, indices);
    radix_sort(triplets, 2);

    std::vector<int> rank(n);
    int current_rank = 0;
    rank[triplets[0].index] = current_rank;
    for (int i = 1; i < triplets.size(); i++) {
        const auto &t = triplets[i];
        const auto &prev = triplets[i - 1];

        if (t.a != prev.a || t.b != prev.b || t.c != prev.c) {
            current_rank++;
        }
        rank[t.index] = current_rank;
    }

    vector<int> l_1_2(indices.size());
    if (current_rank < triplets.size()) {
        std::vector<int> reduced_text(indices.size());
        int i = 0;
        for(int idx: indices) {
            reduced_text[i] = rank[idx];
            i++;
        }
        std::vector<int> reduced_sa = build_suffix_array(reduced_text);
        
        for (i = 0; i < reduced_sa.size(); i++) {
            l_1_2[i] = indices[reduced_sa[i]];
        }

    } else {
        for (int i = 0; i < triplets.size(); i++) {
            l_1_2[i] = triplets[i].index;
        }
    }

    std::vector<int> r_1_2(n);
    for(int i = 0; i < l_1_2.size(); i++){
        r_1_2[l_1_2[i]] = i;
    }

    // Part 2
    std::vector<Triplet> buckets((n - 1) / 3);
    
    for(int i = 0; i < n - 3; i += 3){
        Triplet t;
        t.a = text[i];
        t.b = r_1_2[i + 1];
        t.index = i;

        buckets[i / 3] = t;
    }

    
    radix_sort(buckets, 1);    

    std::vector<int> l_0(buckets.size());

    for(int i = 0; i < l_0.size(); i++){
        l_0[i] = buckets[i].index;
    }
    
    std::vector<int> r_0(n - 3);
    for(int i = 0; i < l_0.size(); i++){
        r_0[l_0[i]] = i;
    }

    // Part 3 merge
    std::vector<int> merged_sa(n - 3);

    merged_sa = merge_group(l_0, l_1_2, r_1_2, text);

    return merged_sa;
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

int main() {

    // std::vector<int> text = {1,2,1,1,2,2,1};
    // std::vector<int> sa = build_suffix_array_naive(text);
    std::vector<int> text = generate_random_string({1, 2, 3, 4, 5, 6, 7, 8}, 10000000);
    
    double total = 0;
    int runs = 1;
    
    for (int i = 0; i < runs; ++i) {
        auto start = std::chrono::high_resolution_clock::now();

        auto sa = build_suffix_array(text);
        // auto sa = build_sa_nlogn(text);

        auto end = std::chrono::high_resolution_clock::now();

        total += std::chrono::duration<double, std::milli>(end - start).count();
    }

    std::cout << "Average time: " << total / runs << " ms\n";

    return 0;
}