import sys

sys.stdin = open("input.txt", "r")

T = int(input())
for test_case in range(1, T + 1):
    # ///////////////////////////////////////////////////////////////////////////////////
    str = input()
    ret = 0
    cnt = [0 for _ in range(10)]
    for i, ch in enumerate(str):
        cnt[int(ch)] = (cnt[int(ch)] + 1) & 0x1
    for i in range(10):
        ret += cnt[i - 1]
    print("#{} {}".format(test_case, ret))
    # ///////////////////////////////////////////////////////////////////////////////////
