# Auto-Test Results

```
[1a-gemini] 4/4 passed, correctness=5
  PASS: km miles 10 -> rc=0 out=6.21
  PASS: kg lbs 1 -> rc=0 out=2.20
  PASS: km kg 1 -> rc=1 out=Error: Invalid unit conversion from km to kg.
  PASS: km miles abc -> rc=1 out=Error: Value must be a number.
[1a-opencode] 2/4 passed, correctness=3
  PASS: km miles 10 -> rc=0 out=6.21
  PASS: kg lbs 1 -> rc=0 out=2.20
  FAIL: km kg 1 -> rc=0 out=Error: Cannot convert from km to kg. Supported pai
  FAIL: km miles abc -> rc=0 out=Error: Value must be a number.
[1b-gemini] 2/2 passed, correctness=5
  PASS: input=<csv> rc=0
  PASS: input=<empty> rc=0
[1b-opencode] 2/2 passed, correctness=5
  PASS: input=<csv> rc=0
  PASS: input=<empty> rc=0
[2a-gemini] 2/2 passed, correctness=5
  PASS: dry-run rc=0
  PASS: sync rc=0
[2a-opencode] 0/2 passed, correctness=1
  FAIL: dry-run rc=1
  FAIL: sync rc=1
[2b-gemini] 1/1 passed, correctness=5
  PASS: demo rc=0 out_len=600
[2b-opencode] 1/1 passed, correctness=5
  PASS: demo rc=0 out_len=569
```
