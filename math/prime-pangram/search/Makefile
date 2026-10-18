CC = gcc
CFLAGS = -O2
BIN = pairs pairs_test diff pack pang pangdp brute enumfull

all: $(BIN)

pairs: scratchpad/pairs.c
	$(CC) $(CFLAGS) -o $@ $<
pairs_test: scratchpad/pairs_test.c
	$(CC) $(CFLAGS) -DTESTMODE=1 -o $@ $<
diff: scratchpad/diff.c
	$(CC) $(CFLAGS) -o $@ $<
pack: scratchpad/pack.c
	$(CC) $(CFLAGS) -o $@ $<
pang: scratchpad/pang.c
	$(CC) $(CFLAGS) -o $@ $< -lm
pangdp: scratchpad/pangdp.c
	$(CC) $(CFLAGS) -o $@ $< -lm
brute: scratchpad/brute.c
	$(CC) $(CFLAGS) -o $@ $<
enumfull: scratchpad/enumfull.c
	$(CC) $(CFLAGS) -o $@ $<

# quick end-to-end checks (a few minutes, < 1 GB RAM)
check: pairs diff brute
	./pairs 40000            # equal-sum five-pair pangrams: expect 0 solutions
	./diff 20000             # equal-difference: expect exactly D = 204, 258, 534
	./brute 4 ABCDEFGHIJKL:5 ABCDEFGHIJKL:4 ABCDEFGHIJKL:3 ABCDEFGHIJKLM:5
	python3 tests/test_solutions.py

clean:
	rm -f $(BIN)
