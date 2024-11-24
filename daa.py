def makePalindrome(s):
   # Function to compute the Longest Prefix Suffix (LPS) array
    def compute_lps(string):
        n = len(string)
        lps = [0] * n
        length = 0  # Length of the previous longest prefix suffix
        i = 1
        while i < n:
            if string[i] == string[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps

    # Create a new string by concatenating the original, a separator, and its reverse
    new_string = s + '#' + s[::-1]
    lps = compute_lps(new_string)

    # The minimum characters to append
    return len(s) - lps[-1]
if __name__ == "__main__":
  T = int(input().strip());
  for i in range(T):
    Str = input();
    print(makePalindrome(Str));