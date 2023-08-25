def best_line(X, Y):
    """This function plots the best-fit line for a group of datapoints broken into
    a set of independent variable values (X) and a set of dependent variable values (Y)"""
    import numpy as np
    from matplotlib import pyplot as plt
    
    X_bar = np.mean(X)
    Y_bar = np.mean(Y)
    
    X_diffs = np.asarray([i - X_bar for i in X])
    Y_diffs = np.asarray([i - Y_bar for i in Y])
    
    num = X_diffs.dot(Y_diffs)
    
    denom = np.sqrt((X_diffs ** 2).sum() * (Y_diffs ** 2).sum())
    
    r_pearson = num / denom
    
    beta_1 = r_pearson * Y_diffs.std() / X_diffs.std()
    
    beta_0 = Y_bar - beta_1 * X_bar
    
    Xs = np.linspace(np.min(X), np.max(X), 100)
    Ys = beta_1 * Xs + beta_0
    
    fig, ax = plt.subplots()
    ax.plot(X, Y, 'ro', label='datapoints')
    ax.plot(Xs, Ys, 'k', label=f'y={round(beta_1, 2)}x+{round(beta_0, 2)}')
    plt.legend()
    plt.show();