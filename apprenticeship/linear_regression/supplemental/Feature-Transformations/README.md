# Feature Selection and Engineering

## Learning Goals

- Use correlations and other algorithms to inform feature selection
- Address the problem of multicollinearity in regression problems
- Create new features for use in modeling
    + Use PolynomialFeatures to build compound features

## Lecture Materials

[Jupyter Notebook: Feature Selection and Feature Engineering](feature_selection_and_feature_engineering.ipynb)

## Lesson Plan

Provide a breakdown of the lecture activities using the structure below. 

### Intro & Model Selection (5 Mins)

Motivate the importance of feature engineering and what we can do with it.

### Correlation and Multicollinearity (15 Mins)

Discuss how to use correlation to determine featues to use. But briefly discuss issues with multicollinearity; we'll address other methods to handle this in the future.

### Recursive Feature Elimination (10 Mins)

Discuss how RFE works and demonstrate the used case with Scikit-Learn's implememtnation. Briefly discuss when it should be avoided.

### Feature Engineering (20 Mins)

Go through different ways of feature engineering: thresholds, product of features (bespoke), and autogenerate polynomial features. Discuss how domain knowledge and exploration are used to make these determinations.

### Exercise (10 Mins)

Have them look at the correlation of product of features. If time, compare different models using these new features.
