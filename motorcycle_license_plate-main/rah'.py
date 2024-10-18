def calculate_intervals_count(n, A, S):
    total = 0
    for i in range(n):
        club = A[i]
        intervals_count = 0
        for j in range(len(S)):
            for k in range(j, len(S)):
                if all(x in club for x in S[j:k+1]):
                    intervals_count += 1
        print(f"F({i+1}) = {intervals_count}")
        total += intervals_count
    return total

# Example usage
n = 5
A = ["ab", "b", "bc", "de", "fg"]
S = "abab"
output = calculate_intervals_count(n, A, S)
print("Total:", output)
