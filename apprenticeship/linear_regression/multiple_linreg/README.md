# Multiple Linear Regression

Two Parts (typically delivered across 2 one-hour blocks) - both use the same notebook.

# Part 1

## Learning Goals

- Use the one-hot strategy to encode categorical variables
- Conduct linear regressions in `statsmodels`

## Lecture Materials

[Jupyter Notebook: Multiple Linear Regression](multiple_linear_regression.ipynb)

## Lesson Plan

### Regression with Multiple Predictors (15 Mins)

Relate how multiple linear regression is an extenstion of simple linear regression. Can talk about how it's multi-dimensional or a bunch of dials.

### Confounding Variables (10 Mins)

Go into detail about how we can figure out we select more than one feature. Mention how multicollinearity is an issue (but we'll address this later)

### Dealing with Categorical Variables (20 Mins)

Show how we can address categorical variables for linear regression via one-hot encoding and dummying. Might be worth saying why we would do this and why it works.

### Multiple Regression in `statsmodels` (15 Mins)

Demonstrate how we can do linear regression with `statsmodels` (don't use categorical variables)

## Tips

- Aim for getting to where we start implementing linear regressions in statsmodels, so that the second lesson will be devoted to coding up linear regressions.

- Consider adding more to how categorical variables work and relating it the mathematical dsecription for multiple linear regression.


-----

# Part 2

## Learning Goals

- Use standard scaling for linear regression for better interpretation
- Conduct linear regressions in `sklearn`

## Lecture Materials

[Jupyter Notebook: Multiple Linear Regression](multiple_linear_regression.ipynb)

## Lesson Plan

### Introduction (5 Mins)

Review what we learned from last related lecture

### Perform Linear Regression: Wine Dataset (15 Mins)

Using what was learned from last lecture, perform multiple linear regression (with `statsmodels`). Could be used as a warm-up activity.

### Scaling  (20 Mins)

Discuss how scaling can help us with interpretation. This could involve relating it back to the formula for linear regression.

### Multiple Linear Regression in Scikit-Learn (20 Mins)

Perform the full steps for linear regression using `sklearn`. Emphasize how the `.fit()` and other methods work.
