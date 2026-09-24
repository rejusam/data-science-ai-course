# Linear regression cheat sheet

How to predict a number from another number, from the very beginning.

## What it is

You have past examples where you know the answer. You want to guess the answer
for a new case.

- **Supervised learning** means the computer learns from examples that come
  with the answers attached.
- **Regression** means the answer is a number, such as a price, a mark or a
  temperature.
- **Linear** means the computer draws the best straight line through the
  examples and reads its guesses off that line.

## The example

Ten students, how many hours each one studied, and the mark they got. These
numbers are made up for this sheet.

| hours | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| mark | 35 | 41 | 48 | 50 | 58 | 62 | 66 | 74 | 77 | 85 |

More hours, higher mark, rising at a roughly steady rate. That steady rise is
what a straight line can capture.

## The straight line

```
mark = start + slope × hours
```

- **start** is the mark the line gives for zero hours. Its proper name is the
  *intercept*.
- **slope** is how many extra marks each extra hour is worth. Its proper name
  is the *coefficient*.

Fitting the model means finding the start and slope that make the line pass as
close as possible to all the examples.

## The five steps

| Step | What you do | Why |
|---|---|---|
| 1. Get the data | Put it in a table | The computer needs the examples |
| 2. Split it | Keep a few rows back for a test | So you can check the model on rows it has never seen |
| 3. Fit | Let the computer find the line | This is the learning |
| 4. Predict | Use the line on the test rows | To get its guesses |
| 5. Check | Compare the guesses with the real answers | To find out how far off it is |

## The code

```python
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# 1. The data: hours studied and the mark each student got
data = pd.DataFrame({
    "hours": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "mark":  [35, 41, 48, 50, 58, 62, 66, 74, 77, 85],
})
X = data[["hours"]]   # what we know (double brackets: sklearn wants a table)
y = data["mark"]      # what we want to guess

# 2. Split: 8 rows to learn from, 2 rows kept back for the test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Fit: find the straight line that best matches the 8 learning rows
model = LinearRegression()
model.fit(X_train, y_train)

# 4. Predict: guess the marks for the 2 test rows
guesses = model.predict(X_test)

# 5. Check: how far off were the guesses, on average?
print("Start (intercept):", round(model.intercept_, 2))
print("Slope:", round(model.coef_[0], 2))
print("Test hours:", list(X_test["hours"]))
print("Real marks:", list(y_test))
print("Guesses:", [round(float(g), 1) for g in guesses])
print("Average miss (MAE):", round(mean_absolute_error(y_test, guesses), 1))

# Use it on a new student who studied 12 hours
new_student = pd.DataFrame({"hours": [12]})
print("Guess for 12 hours:", round(model.predict(new_student)[0], 1))
```

What it prints:

```
Start (intercept): 29.78
Slope: 5.45
Test hours: [9, 2]
Real marks: [77, 41]
Guesses: [78.8, 40.7]
Average miss (MAE): 1.1
Guess for 12 hours: 95.2
```

`random_state=42` makes the split pick the same rows every time, so you get
the same output as above. Any number works; 42 is only a habit.

## Reading the answer

- **Slope 5.45:** each extra hour of study is worth about 5.45 more marks.
- **Start 29.78:** the line's mark for zero hours. Nobody in the table studied
  zero hours, so treat this as the point where the line starts, not as a
  real prediction.
- **The guesses by hand:** for 9 hours, 29.78 + 5.45 × 9 = 78.8. The real mark
  was 77, so the guess was 1.8 too high. For 2 hours the guess was 40.7 against
  a real 41, so 0.3 too low.
- **Average miss (MAE) 1.1:** the average of those two misses. On rows it had
  never seen, the model was off by about 1 mark. MAE stands for *mean absolute
  error*: "mean" means average, and "absolute" means a miss counts the same
  whether it is too high or too low.

## Three traps

1. **Never test on the rows the model learned from.** It has seen those
   answers, so it will look better than it is. Always check on rows kept back.
2. **The line keeps going forever.** For 20 hours this model guesses 138.75,
   but a mark cannot go above 100. Only trust guesses inside the range of the
   examples you had.
3. **A line is not a reason.** The data shows that students who studied more
   got higher marks. It does not prove that the studying caused the marks.
