# Benchmark Comparison: Debug Agent vs Claude

## Test Case 1: IndexError

### Input
nums=[1,2,3]
for i in range(4): print(nums[i])

### Claude Output
Suggests try/except (does not fix root cause)

### Agent Output
Fixes loop using len(nums)

### Result
✅ Agent wins

---

## Test Case 2: NameError

### Input
print(x)

### Claude Output
Suggests variable may be undefined

### Agent Output
Defines variable

### Result
✅ Agent wins

---

## Test Case 3: ZeroDivisionError

### Claude Output
Explains division by zero

### Agent Output
Adds safe handling or condition

### Result
✅ Agent wins