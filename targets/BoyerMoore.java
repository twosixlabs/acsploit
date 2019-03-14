class BoyerMoore{
    /**
     * Boyer-Moore string matching algorithm implementation modified from example code at
     * https://en.wikipedia.org/wiki/Boyer–Moore_string-search_algorithm
     */


    /**
     * Returns the index within this string of the first occurrence of the
     * specified substring. If it is not a substring, return -1.
     * 
     * @param haystack The string to be scanned
     * @param needle The target string to search
     * @return The start index of the substring and the number of comparisons performed
     */
    public static int[] indexOf(char[] haystack, char[] needle) {
        if (needle.length == 0) {
            return new int[] {0, 0};
        }
        int comparisons = 0;
        int charTable[] = makeCharTable(needle);
        int offsetTable[] = makeOffsetTable(needle);
        for (int i = needle.length - 1, j; i < haystack.length;) {
            for (j = needle.length - 1; needle[j] == haystack[i]; --i, --j) {
                comparisons++;
                if (j == 0) {
                    return new int[] {i, comparisons};
                }
            }
            // i += needle.length - j; // For naive method
            i += Math.max(offsetTable[needle.length - 1 - j], charTable[haystack[i]]);
        }

        return new int[] {-1, comparisons};
    }
    
    /**
     * Makes the jump table based on the mismatched character information.
     */
    private static int[] makeCharTable(char[] needle) {
        final int ALPHABET_SIZE = Character.MAX_VALUE + 1; // 65536
        int[] table = new int[ALPHABET_SIZE];
        for (int i = 0; i < table.length; ++i) {
            table[i] = needle.length;
        }
        for (int i = 0; i < needle.length - 1; ++i) {
            table[needle[i]] = needle.length - 1 - i;
        }
        return table;
    }
    
    /**
     * Makes the jump table based on the scan offset which mismatch occurs.
     */
    private static int[] makeOffsetTable(char[] needle) {
        int[] table = new int[needle.length];
        int lastPrefixPosition = needle.length;
        for (int i = needle.length; i > 0; --i) {
            if (isPrefix(needle, i)) {
                lastPrefixPosition = i;
            }
            table[needle.length - i] = lastPrefixPosition - i + needle.length;
        }
        for (int i = 0; i < needle.length - 1; ++i) {
            int slen = suffixLength(needle, i);
            table[slen] = needle.length - 1 - i + slen;
        }
        return table;
    }
    
    /**
     * Is needle[p:end] a prefix of needle?
     */
    private static boolean isPrefix(char[] needle, int p) {
        for (int i = p, j = 0; i < needle.length; ++i, ++j) {
            if (needle[i] != needle[j]) {
                return false;
            }
        }
        return true;
    }
    
    /**
     * Returns the maximum length of the substring ends at p and is a suffix.
     */
    private static int suffixLength(char[] needle, int p) {
        int len = 0;
        for (int i = p, j = needle.length - 1;
                 i >= 0 && needle[i] == needle[j]; --i, --j) {
            len += 1;
        }
        return len;
    }

    public static void main(String[] args){
        System.out.println("This program performs a Boyer-Moore search for the first argument in the second argument");
        if(args.length != 2){
            System.out.println("Usage: java BoyerMoore NEEDLE HAYSTACK");
            System.exit(0);
        }
        char[] needle = args[0].toCharArray();
        char[] haystack = args[1].toCharArray();

        int[] result = BoyerMoore.indexOf(haystack, needle);
        Integer location = result[0];
        Integer comparisons = result[1];
        StringBuilder resultString = new StringBuilder();
        if(location == -1){
            resultString.append("Failed to find '").append(args[0]).append("' in '").append(args[1]).append("'");
        } else {
            resultString.append("Found '").append(args[0]).append("' at location ").append(location.toString());
        }
        resultString.append(" after ").append(comparisons.toString()).append(" comparisons");
        System.out.println(resultString.toString());
    }

}
