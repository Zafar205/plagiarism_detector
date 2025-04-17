
#include <string.h>

extern "C" {
    __declspec(dllexport) int check_bloom(const char* word1, const char* word2) {
        // return (strcmp(word, "hello") == 0) ? 1 : 0;
        return 1;
    }
}
