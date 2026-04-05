

import marimo

__generated_with = "0.13.2"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import os
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from sklearn.datasets import make_moons, make_regression
    from sklearn.model_selection import train_test_split
    return make_moons, make_regression, mo, np, os, plt, train_test_split


@app.cell
def _(mo):
    mo.md(
        r"""
        # 🧠 ML from Scratch — Interactive Course Notebook

        Welcome! In this notebook you will **implement core machine learning algorithms using only NumPy**.

        ## Learning Goals
        - Understand the math and intuition behind 8 fundamental ML models
        - Build each model from scratch (no sklearn models allowed!)
        - Compare your implementation against a reference solution
        - Explore how hyperparameters affect model behaviour interactively

        ## Rules of the Game
        - ✅ You **may** use: `numpy`, `matplotlib`
        - ✅ `scikit-learn` is allowed **only** for dataset generation
        - ❌ No `sklearn` models, no `scipy`, no `torch`

        > **"I hear and I forget. I see and I remember. I do and I understand."** — Confucius

        Let's build everything from the ground up. 🚀
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 📚 Concept: Supervised vs Unsupervised Learning

        **Supervised learning** trains a model on labelled data $(X, y)$ — we know the correct answer for each example.
        The goal is to learn a mapping $f: X \rightarrow y$.

        - *Classification*: $y$ is a discrete class label (e.g. spam / not spam)
        - *Regression*: $y$ is a continuous value (e.g. house price)

        **Unsupervised learning** works with *unlabelled* data $X$ only.
        The goal is to discover hidden structure — clusters, embeddings, density estimates.

        | | Supervised | Unsupervised |
        |---|---|---|
        | Labels | Required | Not needed |
        | Goal | Predict $y$ | Discover structure |
        | Examples | KNN, SVM, Neural Nets | K-Means, PCA, Autoencoders |
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 📚 Concept: Loss Functions & Optimisation

        A **loss function** $\mathcal{L}$ measures how wrong our model is. Training = minimising $\mathcal{L}$.

        ### Mean Squared Error (Regression)
        $$\mathcal{L}_{\text{MSE}} = \frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2$$

        ### Binary Cross-Entropy (Classification)
        $$\mathcal{L}_{\text{BCE}} = -\frac{1}{n} \sum_{i=1}^{n} \left[ y_i \log(\hat{p}_i) + (1 - y_i) \log(1 - \hat{p}_i) \right]$$

        ### Gradient Descent Update Rule
        At each step, move parameters in the direction of steepest descent:
        $$\theta \leftarrow \theta - \eta \cdot \nabla_\theta \mathcal{L}$$
        where $\eta$ is the **learning rate** — too large and we overshoot, too small and we crawl.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 📚 Concept: Bias–Variance Tradeoff

        Every model makes two kinds of errors:

        - **Bias**: error from wrong assumptions (underfitting). A linear model on non-linear data has *high bias*.
        - **Variance**: error from sensitivity to training data (overfitting). A depth-100 decision tree has *high variance*.

        The total expected error decomposes as:
        $$\text{Error} = \text{Bias}^2 + \text{Variance} + \text{Irreducible Noise}$$

        The sweet spot is a model complex enough to capture real patterns, but not so complex it memorises noise.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 📚 Concept: Decision Boundaries & Model Capacity

        A **decision boundary** is the surface in feature space where the model switches from predicting one class to another.

        - **Linear models** (Logistic Regression, Perceptron): straight-line boundaries — high bias, low variance.
        - **Non-linear models** (KNN, Decision Trees): curved boundaries — low bias, potentially high variance.

        **Model capacity** refers to the richness of functions a model can represent.
        Increasing $k$ in KNN *decreases* capacity (smoother boundary); increasing `max_depth` in a Decision Tree *increases* capacity.
        """
    )
    return


@app.cell
def _(make_moons, make_regression, train_test_split):
    # ── Dataset Generation ──────────────────────────────────────────────────────
    # Classification dataset: two interleaved half-moons (non-linearly separable)
    X_cls, y_cls = make_moons(n_samples=300, noise=0.25, random_state=42)
    X_cls_train, X_cls_test, y_cls_train, y_cls_test = train_test_split(
        X_cls, y_cls, test_size=0.2, random_state=42
    )

    # Regression dataset: 1-D with noise
    X_reg_raw, y_reg = make_regression(n_samples=200, n_features=1, noise=15, random_state=42)
    # Normalise features so gradient descent converges nicely
    X_reg = (X_reg_raw - X_reg_raw.mean()) / X_reg_raw.std()
    X_reg_train, X_reg_test, y_reg_train, y_reg_test = train_test_split(
        X_reg, y_reg, test_size=0.2, random_state=42
    )

    # Unsupervised copy (no labels used by K-Means)
    X_unsup = X_cls.copy()
    return (
        X_cls,
        X_cls_test,
        X_cls_train,
        X_reg,
        X_reg_test,
        X_reg_train,
        X_unsup,
        y_cls,
        y_cls_test,
        y_cls_train,
        y_reg,
        y_reg_test,
        y_reg_train,
    )


@app.cell
def _(X_cls, X_reg, mo, plt, y_cls, y_reg):
    fig_data, (ax_d1, ax_d2) = plt.subplots(1, 2, figsize=(12, 4))
    ax_d1.scatter(X_cls[:, 0], X_cls[:, 1], c=y_cls, cmap="bwr", edgecolors="k", linewidths=0.4, s=40)
    ax_d1.set_title("Classification Dataset (make_moons)")
    ax_d1.set_xlabel("Feature 1")
    ax_d1.set_ylabel("Feature 2")
    ax_d2.scatter(X_reg, y_reg, alpha=0.6, color="steelblue", edgecolors="k", linewidths=0.3, s=40)
    ax_d2.set_title("Regression Dataset")
    ax_d2.set_xlabel("Feature")
    ax_d2.set_ylabel("Target")
    plt.tight_layout()
    mo.mpl.interactive(fig_data)


    # ════════════════════════════════════════════════════════════════════════════════
    # MODEL 1 — K-Nearest Neighbours
    # ════════════════════════════════════════════════════════════════════════════════
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---
        ## 🟦 Model 1: K-Nearest Neighbours (KNN)

        KNN is a **lazy learner** — it stores the entire training set and defers all computation to prediction time.

        ### Algorithm
        To classify a new point $x$:
        1. Compute the **Euclidean distance** to every training point:
           $$d(x, x_i) = \sqrt{\sum_{j=1}^{p}(x_j - x_{ij})^2}$$
        2. Find the $k$ nearest neighbours.
        3. Return the **majority class** among those $k$ neighbours.

        ### Intuition
        - Small $k$ → complex, noisy boundary (low bias, high variance)
        - Large $k$ → smooth boundary (high bias, low variance)

        ### Your Task
        Implement `fit` (store the data) and `predict` (distance + majority vote) below.
        """
    )
    return


@app.cell
def _(os):
    def save_text(text, name, file_dir='local_files'):
        if not os.path.exists(file_dir):
            os.mkdir(file_dir)
        _name = f'{file_dir}/{name}.txt'
        with open(_name, 'w') as _f:
            _f.write(text)

    def load_text(name, default, file_dir='local_files'):
        if not os.path.exists(file_dir):
            os.mkdir(file_dir)
        _name = f'{file_dir}/{name}.txt'
        if not os.path.exists(_name):
            return default
        with open(_name, 'r') as _f:
            output = _f.read()
        return output
    return load_text, save_text


@app.cell
def _(load_text, mo):
    _default = '''class KNNClassifier:
    """K-Nearest Neighbours Classifier (numpy only)."""

    def __init__(self, k=3):
        self.k = k
        self.X_train = None
        self.y_train = None

    def fit(self, X, y):
        """Store training data — KNN does no real training."""
        pass

    def predict(self, X):
        """Predict class labels for each row in X."""
        predictions = []
        for x in X:
            pass
    '''
    knn_class_name = 'KNNClassifier'
    knn_editor = mo.ui.code_editor(
        value=load_text(knn_class_name, _default),
        language="python",
    )
    knn_editor
    return knn_class_name, knn_editor


@app.cell
def _(
    X_cls_test,
    X_cls_train,
    knn_class_name,
    knn_editor,
    mo,
    np,
    save_text,
    y_cls_test,
    y_cls_train,
):
    try:
        _ns = {}
        exec(knn_editor.value, {"np": np}, _ns)
        KNNClassifier = _ns["KNNClassifier"]
        _knn = KNNClassifier(k=5)
        _knn.fit(X_cls_train, y_cls_train)
        _preds = _knn.predict(X_cls_test)
        if _preds is None or len(_preds) == 0:
            raise ValueError("predict() returned None or empty array")
        knn_acc = float(np.mean(_preds == y_cls_test))
        knn_ok = True
    except Exception as _e:
        knn_ok = False
        knn_acc = 0.0
        KNNClassifier = None
        mo.stop(True, mo.callout(mo.md(f"**KNN not ready yet:** {_e}\n\nFill in the TODOs above and try again."), kind="warn"))

    def _knn_ref(X_tr, y_tr, X_te, k=5):
        preds = []
        for x in X_te:
            dists = np.sqrt(np.sum((X_tr - x) ** 2, axis=1))
            nn_idx = np.argsort(dists)[:k]
            preds.append(int(np.argmax(np.bincount(y_tr[nn_idx]))))

    _ref_preds = _knn_ref(X_cls_train, y_cls_train, X_cls_test)
    knn_ref_acc = float(np.mean(_ref_preds == y_cls_test))

    save_text(knn_editor.value, knn_class_name)

    mo.callout(
        mo.md(f"✅ **KNN** — Your accuracy: **{knn_acc:.1%}** | Reference: **{knn_ref_acc:.1%}**"),
        kind="success",
    )
    return KNNClassifier, knn_acc, knn_ok, knn_ref_acc


@app.cell
def _(
    KNNClassifier,
    X_cls,
    X_cls_train,
    knn_ok,
    mo,
    np,
    plt,
    y_cls,
    y_cls_train,
):
    mo.stop(not knn_ok, mo.md("*KNN decision boundary will appear once the implementation is complete.*"))

    _h = 0.05
    _x0_min, _x0_max = X_cls[:, 0].min() - 0.5, X_cls[:, 0].max() + 0.5
    _x1_min, _x1_max = X_cls[:, 1].min() - 0.5, X_cls[:, 1].max() + 0.5
    _xx, _yy = np.meshgrid(np.arange(_x0_min, _x0_max, _h), np.arange(_x1_min, _x1_max, _h))
    _knn_viz = KNNClassifier(k=5)
    _knn_viz.fit(X_cls_train, y_cls_train)
    _Z = _knn_viz.predict(np.c_[_xx.ravel(), _yy.ravel()]).reshape(_xx.shape)
    fig_knn, ax_knn = plt.subplots(figsize=(7, 5))
    ax_knn.contourf(_xx, _yy, _Z, alpha=0.3, cmap="bwr")
    ax_knn.scatter(X_cls[:, 0], X_cls[:, 1], c=y_cls, cmap="bwr", edgecolors="k", linewidths=0.4, s=30)
    ax_knn.set_title("KNN Decision Boundary (k=5)")
    mo.mpl.interactive(fig_knn)


    # ════════════════════════════════════════════════════════════════════════════════
    # MODEL 2 — Linear Regression
    # ════════════════════════════════════════════════════════════════════════════════
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---
        ## 🟩 Model 2: Linear Regression

        Linear Regression models the target as a linear combination of the features:
        $$\hat{y} = X\theta = \theta_0 + \theta_1 x_1 + \ldots + \theta_p x_p$$

        ### Normal Equation (closed-form)
        $$\theta^* = (X^T X)^{-1} X^T y$$

        ### Gradient Descent (iterative)
        Gradient of MSE with respect to $\theta$:
        $$\nabla_\theta \mathcal{L}_{\text{MSE}} = \frac{2}{n} X^T (X\theta - y)$$
        Update: $\theta \leftarrow \theta - \eta \cdot \nabla_\theta \mathcal{L}$

        ### Your Task
        Implement `fit_normal_equation`, `fit_gradient_descent`, and `predict`.
        """
    )
    return


@app.cell
def _(load_text, mo):
    _default = '''class LinearRegression:
    """Linear Regression via Normal Equation and Gradient Descent."""

    def __init__(self, learning_rate=0.01, epochs=1000):
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.theta = None  # weight vector (includes bias at index 0)

    def _add_bias(self, X):
        """Prepend a column of ones for the bias term."""

    def fit_normal_equation(self, X, y):
        """Solve theta = (X^T X)^{-1} X^T y."""
        Xb = self._add_bias(X)
        # TODO: compute self.theta using the normal equation
        pass

    def fit_gradient_descent(self, X, y):
        """Minimise MSE via gradient descent."""
        Xb = self._add_bias(X)
        n, d = Xb.shape
        self.theta = np.zeros(d)
        for _ in range(self.epochs):
            pass

    def predict(self, X):
        """Return predicted values."""
        Xb = self._add_bias(X)
        pass
    '''
    lr_class_name = 'LinearRegression'
    linreg_editor = mo.ui.code_editor(
        value=load_text(lr_class_name, _default),
        language="python",
    )
    linreg_editor
    return linreg_editor, lr_class_name


@app.cell
def _(
    X_reg_test,
    X_reg_train,
    linreg_editor,
    lr_class_name,
    mo,
    np,
    save_text,
    y_reg_test,
    y_reg_train,
):
    try:
        _ns = {}
        exec(linreg_editor.value, {"np": np}, _ns)
        LinearRegression = _ns["LinearRegression"]
        _lr = LinearRegression(learning_rate=0.05, epochs=2000)
        _lr.fit_gradient_descent(X_reg_train, y_reg_train)
        _preds = _lr.predict(X_reg_test)
        if _preds is None:
            raise ValueError("predict() returned None")
        linreg_mse = float(np.mean((_preds - y_reg_test) ** 2))
        linreg_ok = True
    except Exception as _e:
        linreg_ok = False
        linreg_mse = float("inf")
        LinearRegression = None
        mo.stop(True, mo.callout(mo.md(f"**Linear Regression not ready:** {_e}"), kind="warn"))

    def _linreg_ref(X_tr, y_tr, X_te):
        Xb = np.hstack([np.ones((X_tr.shape[0], 1)), X_tr])
        theta = np.linalg.pinv(Xb.T @ Xb) @ Xb.T @ y_tr
        Xb_te = np.hstack([np.ones((X_te.shape[0], 1)), X_te])
        return Xb_te @ theta

    _ref_preds = _linreg_ref(X_reg_train, y_reg_train, X_reg_test)
    linreg_ref_mse = float(np.mean((_ref_preds - y_reg_test) ** 2))

    save_text(linreg_editor.value, lr_class_name)

    mo.callout(
        mo.md(f"✅ **Linear Regression** — Your MSE: **{linreg_mse:.2f}** | Reference MSE: **{linreg_ref_mse:.2f}**"),
        kind="success",
    )
    return LinearRegression, linreg_mse, linreg_ok, linreg_ref_mse


@app.cell
def _(
    LinearRegression,
    X_reg,
    X_reg_train,
    linreg_ok,
    mo,
    np,
    plt,
    y_reg,
    y_reg_train,
):
    mo.stop(not linreg_ok, mo.md("*Regression fit will appear once the implementation is complete.*"))

    _lr_viz = LinearRegression(learning_rate=0.05, epochs=2000)
    _lr_viz.fit_gradient_descent(X_reg_train, y_reg_train)
    _x_line = np.linspace(X_reg.min(), X_reg.max(), 200).reshape(-1, 1)
    _y_line = _lr_viz.predict(_x_line)
    fig_linreg, ax_linreg = plt.subplots(figsize=(7, 4))
    ax_linreg.scatter(X_reg, y_reg, alpha=0.5, color="steelblue", edgecolors="k", linewidths=0.3, s=30, label="Data")
    ax_linreg.plot(_x_line, _y_line, color="crimson", lw=2, label="GD fit")
    ax_linreg.set_title("Linear Regression Fit (Gradient Descent)")
    ax_linreg.legend()
    mo.mpl.interactive(fig_linreg)


    # ════════════════════════════════════════════════════════════════════════════════
    # MODEL 3 — Logistic Regression
    # ════════════════════════════════════════════════════════════════════════════════
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---
        ## 🟧 Model 3: Logistic Regression

        Logistic Regression squashes a linear combination through the **sigmoid** function to produce class probabilities:
        $$\hat{p} = \sigma(X\theta) = \frac{1}{1 + e^{-X\theta}}$$

        We minimise **binary cross-entropy**:
        $$\mathcal{L} = -\frac{1}{n}\sum_i \left[ y_i \log \hat{p}_i + (1-y_i)\log(1-\hat{p}_i) \right]$$

        The gradient has a beautifully simple form:
        $$\nabla_\theta \mathcal{L} = \frac{1}{n} X^T (\hat{p} - y)$$

        Predict class 1 when $\hat{p} \geq 0.5$.
        """
    )
    return


@app.cell
def _(load_text, mo):
    _default = '''class LogisticRegression:
    """Binary Logistic Regression via gradient descent."""

    def __init__(self, learning_rate=0.1, epochs=1000):
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.theta = None

    def _sigmoid(self, z):
        """Numerically stable sigmoid: clip z to avoid overflow."""
        # Hint: use np.clip(z, -500, 500) inside exp for stability
        pass

    def _add_bias(self, X):

    def fit(self, X, y):
        """Train via gradient descent on binary cross-entropy."""
        Xb = self._add_bias(X)
        n, d = Xb.shape
        self.theta = np.zeros(d)
        for _ in range(self.epochs):
            pass

    def predict_proba(self, X):
        Xb = self._add_bias(X)
        pass

    def predict(self, X):
        pass
    '''
    logr_class_name = 'LogisticRegression'
    logreg_editor = mo.ui.code_editor(
        value=load_text(logr_class_name, _default),
        language="python",
    )
    logreg_editor
    return logr_class_name, logreg_editor


@app.cell
def _(
    X_cls_test,
    X_cls_train,
    logr_class_name,
    logreg_editor,
    mo,
    np,
    save_text,
    y_cls_test,
    y_cls_train,
):
    try:
        _ns = {}
        exec(logreg_editor.value, {"np": np}, _ns)
        LogisticRegression = _ns["LogisticRegression"]
        _lg = LogisticRegression(learning_rate=0.1, epochs=1000)
        _lg.fit(X_cls_train, y_cls_train)
        _preds = _lg.predict(X_cls_test)
        if _preds is None:
            raise ValueError("predict() returned None")
        logreg_acc = float(np.mean(_preds == y_cls_test))
        logreg_ok = True
    except Exception as _e:
        logreg_ok = False
        logreg_acc = 0.0
        LogisticRegression = None
        mo.stop(True, mo.callout(mo.md(f"**Logistic Regression not ready:** {_e}"), kind="warn"))

    def _sig_ref(z):
        return 1.0 / (1.0 + np.exp(-np.clip(z, -500, 500)))

    def _logreg_ref(X_tr, y_tr, X_te, lr=0.1, epochs=1000):
        Xb = np.hstack([np.ones((X_tr.shape[0], 1)), X_tr])
        theta = np.zeros(Xb.shape[1])
        n = len(y_tr)
        for _ in range(epochs):
            p = _sig_ref(Xb @ theta)
            theta -= (lr / n) * (Xb.T @ (p - y_tr))
        Xb_te = np.hstack([np.ones((X_te.shape[0], 1)), X_te])

    _ref_preds = _logreg_ref(X_cls_train, y_cls_train, X_cls_test)
    logreg_ref_acc = float(np.mean(_ref_preds == y_cls_test))

    save_text(logreg_editor.value, logr_class_name)

    mo.callout(
        mo.md(f"✅ **Logistic Regression** — Your accuracy: **{logreg_acc:.1%}** | Reference: **{logreg_ref_acc:.1%}**"),
        kind="success",
    )
    return LogisticRegression, logreg_acc, logreg_ok, logreg_ref_acc


@app.cell
def _(
    LogisticRegression,
    X_cls,
    X_cls_train,
    logreg_ok,
    mo,
    np,
    plt,
    y_cls,
    y_cls_train,
):
    mo.stop(not logreg_ok, mo.md("*Decision boundary will appear once the implementation is complete.*"))

    _h = 0.05
    _x0_min2, _x0_max2 = X_cls[:, 0].min() - 0.5, X_cls[:, 0].max() + 0.5
    _x1_min2, _x1_max2 = X_cls[:, 1].min() - 0.5, X_cls[:, 1].max() + 0.5
    _xx2, _yy2 = np.meshgrid(np.arange(_x0_min2, _x0_max2, _h), np.arange(_x1_min2, _x1_max2, _h))
    _lg_viz = LogisticRegression(learning_rate=0.1, epochs=1000)
    _lg_viz.fit(X_cls_train, y_cls_train)
    _Z2 = _lg_viz.predict(np.c_[_xx2.ravel(), _yy2.ravel()]).reshape(_xx2.shape)
    fig_logreg, ax_logreg = plt.subplots(figsize=(7, 5))
    ax_logreg.contourf(_xx2, _yy2, _Z2, alpha=0.3, cmap="bwr")
    ax_logreg.scatter(X_cls[:, 0], X_cls[:, 1], c=y_cls, cmap="bwr", edgecolors="k", linewidths=0.4, s=30)
    ax_logreg.set_title("Logistic Regression Decision Boundary")
    mo.mpl.interactive(fig_logreg)


    # ════════════════════════════════════════════════════════════════════════════════
    # MODEL 4 — Naive Bayes
    # ════════════════════════════════════════════════════════════════════════════════
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---
        ## 🟨 Model 4: Gaussian Naive Bayes

        Naive Bayes applies Bayes' theorem with the "naive" conditional independence assumption:
        $$P(y \mid x) \propto P(y) \prod_{j=1}^{p} P(x_j \mid y)$$

        For **Gaussian Naive Bayes**, each feature is assumed Gaussian given the class:
        $$P(x_j \mid y=c) = \frac{1}{\sqrt{2\pi\sigma_{cj}^2}} \exp\!\left(-\frac{(x_j - \mu_{cj})^2}{2\sigma_{cj}^2}\right)$$

        **Training**: compute $\mu_{cj}$ and $\sigma_{cj}^2$ for each class $c$ and feature $j$.

        **Prediction**: pick $\arg\max_c \left[\log P(y=c) + \sum_j \log P(x_j \mid y=c)\right]$ — use logs for numerical stability.
        """
    )
    return


@app.cell
def _(load_text, mo):
    _default = '''class GaussianNaiveBayes:
    """Gaussian Naive Bayes classifier."""

    def __init__(self):
        self.classes = None
        self.log_priors = {}   # log P(y=c)
        self.means = {}        # shape (n_features,) per class
        self.variances = {}    # shape (n_features,) per class

    def fit(self, X, y):
        self.classes = np.unique(y)
        n_total = len(y)
        for c in self.classes:
            X_c = X[y == c]
            pass

    def _log_likelihood(self, x, c):
        """Sum of log-Gaussian densities across features for class c."""
        mu = self.means[c]
        var = self.variances[c]
        pass

    def predict(self, X):
        preds = []
        for x in X:
            pass
    '''
    gnb_class_name = 'GaussianNaiveBayes'
    nb_editor = mo.ui.code_editor(
        value=load_text(gnb_class_name, _default),
        language="python",
    )
    nb_editor
    return gnb_class_name, nb_editor


@app.cell
def _(
    X_cls_test,
    X_cls_train,
    gnb_class_name,
    mo,
    nb_editor,
    np,
    save_text,
    y_cls_test,
    y_cls_train,
):
    try:
        _ns = {}
        exec(nb_editor.value, {"np": np}, _ns)
        GaussianNaiveBayes = _ns["GaussianNaiveBayes"]
        _gnb = GaussianNaiveBayes()
        _gnb.fit(X_cls_train, y_cls_train)
        _preds = _gnb.predict(X_cls_test)
        if _preds is None or len(_preds) == 0:
            raise ValueError("predict() returned None or empty")
        nb_acc = float(np.mean(_preds == y_cls_test))
        nb_ok = True
    except Exception as _e:
        nb_ok = False
        nb_acc = 0.0
        GaussianNaiveBayes = None
        mo.stop(True, mo.callout(mo.md(f"**Naive Bayes not ready:** {_e}"), kind="warn"))

    def _gnb_ref(X_tr, y_tr, X_te):
        classes = np.unique(y_tr)
        lp, mu, va = {}, {}, {}
        for c in classes:
            Xc = X_tr[y_tr == c]
            lp[c] = np.log(len(Xc) / len(y_tr))
            mu[c] = Xc.mean(axis=0)
            va[c] = Xc.var(axis=0) + 1e-9
        preds = []
        for x in X_te:
            best_c, best_s = None, -np.inf
            for c in classes:
                ll = np.sum(-0.5 * np.log(2 * np.pi * va[c]) - (x - mu[c]) ** 2 / (2 * va[c]))
                s = lp[c] + ll
                if s > best_s:
                    best_s, best_c = s, c
            preds.append(best_c)

    _ref_preds = _gnb_ref(X_cls_train, y_cls_train, X_cls_test)
    nb_ref_acc = float(np.mean(_ref_preds == y_cls_test))

    save_text(nb_editor.value, gnb_class_name)

    mo.callout(
        mo.md(f"✅ **Naive Bayes** — Your accuracy: **{nb_acc:.1%}** | Reference: **{nb_ref_acc:.1%}**"),
        kind="success",
    )
    return GaussianNaiveBayes, nb_acc, nb_ok, nb_ref_acc


@app.cell
def _(
    GaussianNaiveBayes,
    X_cls,
    X_cls_train,
    mo,
    nb_ok,
    np,
    plt,
    y_cls,
    y_cls_train,
):
    mo.stop(not nb_ok, mo.md("*Decision boundary will appear once the implementation is complete.*"))

    _h = 0.05
    _x0_min3, _x0_max3 = X_cls[:, 0].min() - 0.5, X_cls[:, 0].max() + 0.5
    _x1_min3, _x1_max3 = X_cls[:, 1].min() - 0.5, X_cls[:, 1].max() + 0.5
    _xx3, _yy3 = np.meshgrid(np.arange(_x0_min3, _x0_max3, _h), np.arange(_x1_min3, _x1_max3, _h))
    _gnb_viz = GaussianNaiveBayes()
    _gnb_viz.fit(X_cls_train, y_cls_train)
    _Z3 = _gnb_viz.predict(np.c_[_xx3.ravel(), _yy3.ravel()]).reshape(_xx3.shape)
    fig_nb, ax_nb = plt.subplots(figsize=(7, 5))
    ax_nb.contourf(_xx3, _yy3, _Z3, alpha=0.3, cmap="bwr")
    ax_nb.scatter(X_cls[:, 0], X_cls[:, 1], c=y_cls, cmap="bwr", edgecolors="k", linewidths=0.4, s=30)
    ax_nb.set_title("Gaussian Naive Bayes Decision Boundary")
    mo.mpl.interactive(fig_nb)


    # ════════════════════════════════════════════════════════════════════════════════
    # MODEL 5 — Decision Tree
    # ════════════════════════════════════════════════════════════════════════════════
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---
        ## 🟫 Model 5: Decision Tree (Gini Impurity)

        A Decision Tree recursively partitions feature space by choosing the split that **maximally reduces impurity**.

        ### Gini Impurity
        $$G(S) = 1 - \sum_{c} p_c^2$$
        where $p_c$ is the proportion of class $c$ in set $S$. A pure node has $G=0$.

        ### Weighted Gini after a split
        $$G_{\text{split}} = \frac{|S_L|}{|S|} G(S_L) + \frac{|S_R|}{|S|} G(S_R)$$

        ### Algorithm
        1. For each feature and threshold, compute $G_{\text{split}}$.
        2. Pick the split with the lowest $G_{\text{split}}$.
        3. Recurse on left ($\leq$ threshold) and right ($>$ threshold) until `max_depth` or pure node.
        4. Leaf prediction = majority class.
        """
    )
    return


@app.cell
def _(load_text, mo):
    _default = '''class DecisionTree:
    """Decision Tree Classifier using Gini impurity."""

    def __init__(self, max_depth=5):
        self.max_depth = max_depth
        self.tree = None

    def _gini(self, y):
        """Gini impurity of label array y."""
        # Hint: np.bincount(y) / len(y) gives the class proportions
        pass

    def _best_split(self, X, y):
        """Return (feature_index, threshold) with the lowest weighted Gini."""
        best_gini = float("inf")
        best_feat, best_thresh = None, None
        n = len(y)
        for feat in range(X.shape[1]):
            for thresh in np.unique(X[:, feat]):
                left  = y[X[:, feat] <= thresh]
                right = y[X[:, feat] >  thresh]
                if len(left) == 0 or len(right) == 0:
                    continue
                # TODO: compute weighted_gini and compare to best_gini
                pass

    def _build(self, X, y, depth):
        """Recursively build the tree; return a node dict."""
        if depth >= self.max_depth or len(np.unique(y)) == 1:
        if feat is None:
        pass

    def fit(self, X, y):
        # TODO: self.tree = self._build(X, y, depth=0)
        pass

    def _predict_one(self, x, node):
        """Traverse the tree for a single sample."""
        if node["leaf"]:
        # TODO: recurse left if x[node["feat"]] <= node["thresh"], else right
        pass

    def predict(self, X):
        pass
    '''
    tree_class_name = 'DecisionTree'
    dtree_editor = mo.ui.code_editor(
        value=load_text(tree_class_name, _default),
        language="python",
    )
    dtree_editor
    return dtree_editor, tree_class_name


@app.cell
def _(
    X_cls_test,
    X_cls_train,
    dtree_editor,
    mo,
    np,
    save_text,
    tree_class_name,
    y_cls_test,
    y_cls_train,
):
    try:
        _ns = {}
        exec(dtree_editor.value, {"np": np}, _ns)
        DecisionTree = _ns["DecisionTree"]
        _dt = DecisionTree(max_depth=4)
        _dt.fit(X_cls_train, y_cls_train)
        _preds = _dt.predict(X_cls_test)
        if _preds is None or len(_preds) == 0:
            raise ValueError("predict() returned None or empty")
        dtree_acc = float(np.mean(_preds == y_cls_test))
        dtree_ok = True
    except Exception as _e:
        dtree_ok = False
        dtree_acc = 0.0
        DecisionTree = None
        mo.stop(True, mo.callout(mo.md(f"**Decision Tree not ready:** {_e}"), kind="warn"))

    class _DTRef:
        def __init__(self, max_depth=4):
            self.max_depth = max_depth
            self.tree = None
        def _gini(self, y):
            if len(y) == 0: return 0.0
            ps = np.bincount(y) / len(y)
            return 1.0 - float(np.sum(ps ** 2))
        def _best_split(self, X, y):
            best_g, best_f, best_t = float("inf"), None, None
            n = len(y)
            for f in range(X.shape[1]):
                for t in np.unique(X[:, f]):
                    l, r = y[X[:, f] <= t], y[X[:, f] > t]
                    if len(l) == 0 or len(r) == 0: continue
                    g = (len(l) * self._gini(l) + len(r) * self._gini(r)) / n
                    if g < best_g: best_g, best_f, best_t = g, f, t
            return best_f, best_t
        def _build(self, X, y, d):
            if d >= self.max_depth or len(np.unique(y)) == 1:
                return {"leaf": True, "v": int(np.argmax(np.bincount(y)))}
            f, t = self._best_split(X, y)
            if f is None: return {"leaf": True, "v": int(np.argmax(np.bincount(y)))}
            m = X[:, f] <= t
            return {"leaf": False, "f": f, "t": t,
                    "l": self._build(X[m], y[m], d + 1),
                    "r": self._build(X[~m], y[~m], d + 1)}
        def fit(self, X, y): self.tree = self._build(X, y, 0)
        def _p1(self, x, n):
            return n["v"] if n["leaf"] else self._p1(x, n["l"] if x[n["f"]] <= n["t"] else n["r"])
        def predict(self, X): return np.array([self._p1(x, self.tree) for x in X])

    _dt_ref = _DTRef(max_depth=4)
    _dt_ref.fit(X_cls_train, y_cls_train)
    _ref_preds = _dt_ref.predict(X_cls_test)
    dtree_ref_acc = float(np.mean(_ref_preds == y_cls_test))

    save_text(dtree_editor.value, tree_class_name)

    mo.callout(
        mo.md(f"✅ **Decision Tree** — Your accuracy: **{dtree_acc:.1%}** | Reference: **{dtree_ref_acc:.1%}**"),
        kind="success",
    )
    return DecisionTree, dtree_acc, dtree_ok, dtree_ref_acc


@app.cell
def _(
    DecisionTree,
    X_cls,
    X_cls_train,
    dtree_ok,
    mo,
    np,
    plt,
    y_cls,
    y_cls_train,
):
    mo.stop(not dtree_ok, mo.md("*Decision boundary will appear once the implementation is complete.*"))

    _h = 0.05
    _x0_min4, _x0_max4 = X_cls[:, 0].min() - 0.5, X_cls[:, 0].max() + 0.5
    _x1_min4, _x1_max4 = X_cls[:, 1].min() - 0.5, X_cls[:, 1].max() + 0.5
    _xx4, _yy4 = np.meshgrid(np.arange(_x0_min4, _x0_max4, _h), np.arange(_x1_min4, _x1_max4, _h))
    _dt_viz = DecisionTree(max_depth=4)
    _dt_viz.fit(X_cls_train, y_cls_train)
    _Z4 = _dt_viz.predict(np.c_[_xx4.ravel(), _yy4.ravel()]).reshape(_xx4.shape)
    fig_dt, ax_dt = plt.subplots(figsize=(7, 5))
    ax_dt.contourf(_xx4, _yy4, _Z4, alpha=0.3, cmap="bwr")
    ax_dt.scatter(X_cls[:, 0], X_cls[:, 1], c=y_cls, cmap="bwr", edgecolors="k", linewidths=0.4, s=30)
    ax_dt.set_title("Decision Tree Decision Boundary (max_depth=4)")
    mo.mpl.interactive(fig_dt)


    # ════════════════════════════════════════════════════════════════════════════════
    # MODEL 6 — K-Means Clustering
    # ════════════════════════════════════════════════════════════════════════════════
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---
        ## 🟪 Model 6: K-Means Clustering (Unsupervised)

        K-Means partitions data into $k$ clusters by alternating two steps:

        ### Assignment Step
        Assign each point to the nearest centroid:
        $$z_i = \arg\min_c \|x_i - \mu_c\|^2$$

        ### Update Step
        Recompute each centroid as the mean of its assigned points:
        $$\mu_c = \frac{1}{|C_c|} \sum_{i:\, z_i=c} x_i$$

        Repeat until assignments stop changing (convergence).

        > Note: K-Means is **unsupervised** — we never use labels. We evaluate using **inertia** (total within-cluster squared distance).
        """
    )
    return


@app.cell
def _(load_text, mo):
    _default = '''class KMeans:
    """K-Means clustering."""

    def __init__(self, k=2, max_iters=100, random_state=42):
        self.k = k
        self.max_iters = max_iters
        self.random_state = random_state
        self.centroids = None
        self.labels_ = None

    def _assign(self, X):
        """Return cluster index for each point in X."""
        # TODO:
        # Compute distance from each point to each centroid.
        pass

    def fit(self, X):
        rng = np.random.RandomState(self.random_state)
        # Initialise centroids by picking k random data points
        idx = rng.choice(len(X), self.k, replace=False)
        self.centroids = X[idx].copy()

        for _ in range(self.max_iters):
            labels = self._assign(X)
            # TODO:
            # Compute new centroids as the mean of each cluster
            # If centroids did not change, break early (np.allclose)
            pass

        self.labels_ = self._assign(X)

    def predict(self, X):

    def inertia(self, X):
        """Sum of squared distances from each point to its nearest centroid."""
        labels = self._assign(X)
        total = 0.0
        for c in range(self.k):
            pts = X[labels == c]
            # TODO: add squared distances of pts to self.centroids[c]
            pass
    '''
    kmeans_class_name = 'KMeans'
    kmeans_editor = mo.ui.code_editor(
        value=load_text(kmeans_class_name, _default),
        language="python",
    )
    kmeans_editor
    return kmeans_class_name, kmeans_editor


@app.cell
def _(X_unsup, kmeans_class_name, kmeans_editor, mo, np, save_text):
    try:
        _ns = {}
        exec(kmeans_editor.value, {"np": np}, _ns)
        KMeans = _ns["KMeans"]
        _km = KMeans(k=2, random_state=42)
        _km.fit(X_unsup)
        _preds = _km.predict(X_unsup)
        _inertia_val = _km.inertia(X_unsup)
        if _preds is None or len(_preds) == 0:
            raise ValueError("predict() returned None or empty")
        kmeans_ok = True
        kmeans_inertia = float(_inertia_val) if _inertia_val is not None else float("inf")
    except Exception as _e:
        kmeans_ok = False
        kmeans_inertia = float("inf")
        KMeans = None
        mo.stop(True, mo.callout(mo.md(f"**K-Means not ready:** {_e}"), kind="warn"))

    def _kmeans_ref_inertia(X, k=2, seed=42):
        rng = np.random.RandomState(seed)
        centroids = X[rng.choice(len(X), k, replace=False)].copy()
        for _ in range(100):
            dists = ((X[:, None] - centroids[None]) ** 2).sum(axis=2)
            labels = dists.argmin(axis=1)
            new_c = np.array([X[labels == c].mean(axis=0) for c in range(k)])
            if np.allclose(new_c, centroids): break
            centroids = new_c
        dists = ((X[:, None] - centroids[None]) ** 2).sum(axis=2)
        labels = dists.argmin(axis=1)
        min_dists_sq = dists[np.arange(len(X)), labels]
        inertia = np.sum(min_dists_sq)
        return inertia

    kmeans_ref_inertia = _kmeans_ref_inertia(X_unsup)

    save_text(kmeans_editor.value, kmeans_class_name)

    mo.callout(
        mo.md(f"✅ **K-Means** — Your inertia: **{kmeans_inertia:.2f}** | Reference inertia: **{kmeans_ref_inertia:.2f}**"),
        kind="success",
    )
    return KMeans, kmeans_inertia, kmeans_ok, kmeans_ref_inertia


@app.cell
def _(KMeans, X_unsup, kmeans_ok, mo, plt):
    mo.stop(not kmeans_ok, mo.md("*Cluster visualisation will appear once the implementation is complete.*"))

    _km_viz = KMeans(k=2, random_state=42)
    _km_viz.fit(X_unsup)
    _labels_viz = _km_viz.predict(X_unsup)
    _centroids_viz = _km_viz.centroids
    fig_km, ax_km = plt.subplots(figsize=(7, 5))
    ax_km.scatter(X_unsup[:, 0], X_unsup[:, 1], c=_labels_viz, cmap="Spectral", edgecolors="k", linewidths=0.3, s=30)
    if _centroids_viz is not None:
        ax_km.scatter(_centroids_viz[:, 0], _centroids_viz[:, 1], c="black", marker="X", s=200, zorder=5, label="Centroids")
        ax_km.legend()
    ax_km.set_title("K-Means Clustering (k=2, unsupervised)")
    mo.mpl.interactive(fig_km)


    # ════════════════════════════════════════════════════════════════════════════════
    # MODEL 7 — Perceptron
    # ════════════════════════════════════════════════════════════════════════════════
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---
        ## ⬛ Model 7: Perceptron

        The Perceptron is the grandfather of all neural networks — a single neuron with a step activation.

        $$\hat{y}_i = \text{step}(w \cdot x_i + b) = \begin{cases} 1 & \text{if } w \cdot x_i + b \geq 0 \\ 0 & \text{otherwise} \end{cases}$$

        ### Online Update Rule
        For each **misclassified** sample $(x_i, y_i)$:
        $$w \leftarrow w + \eta \cdot (y_i - \hat{y}_i) \cdot x_i \qquad b \leftarrow b + \eta \cdot (y_i - \hat{y}_i)$$

        The Perceptron converges **if and only if** the data is linearly separable.
        For our non-linear moons it will find the best linear boundary it can.
        """
    )
    return


@app.cell
def _(load_text, mo):
    _default = '''class Perceptron:
    """Single-layer Perceptron with online (per-sample) weight updates."""

    def __init__(self, learning_rate=0.01, epochs=100):
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.weights = None
        self.bias = None

    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0.0
        for _ in range(self.epochs):
            for xi, yi in zip(X, y):
                # TODO:
                # 1. Compute prediction: 1 if (xi @ self.weights + self.bias) >= 0 else 0
                # 2. error = yi - prediction
                # 3. Update weights and biases
                pass

    def predict(self, X):
        pass
    '''
    perc_class_name = 'Perceptron'
    perceptron_editor = mo.ui.code_editor(
        value=load_text(perc_class_name, _default),
        language="python",
    )
    perceptron_editor
    return perc_class_name, perceptron_editor


@app.cell
def _(
    X_cls_test,
    X_cls_train,
    mo,
    np,
    perc_class_name,
    perceptron_editor,
    save_text,
    y_cls_test,
    y_cls_train,
):
    try:
        _ns = {}
        exec(perceptron_editor.value, {"np": np}, _ns)
        Perceptron = _ns["Perceptron"]
        _p = Perceptron(learning_rate=0.01, epochs=100)
        _p.fit(X_cls_train, y_cls_train)
        _preds = _p.predict(X_cls_test)
        if _preds is None or len(_preds) == 0:
            raise ValueError("predict() returned None or empty")
        perceptron_acc = float(np.mean(_preds == y_cls_test))
        perceptron_ok = True
    except Exception as _e:
        perceptron_ok = False
        perceptron_acc = 0.0
        Perceptron = None
        mo.stop(True, mo.callout(mo.md(f"**Perceptron not ready:** {_e}"), kind="warn"))

    def _perceptron_ref(X_tr, y_tr, X_te, lr=0.01, epochs=100):
        w = np.zeros(X_tr.shape[1])
        b = 0.0
        for _ in range(epochs):
            for xi, yi in zip(X_tr, y_tr):
                pred = 1 if xi @ w + b >= 0 else 0
                err = int(yi) - pred
                w += lr * err * xi
                b += lr * err

    _ref_preds = _perceptron_ref(X_cls_train, y_cls_train, X_cls_test)
    perceptron_ref_acc = float(np.mean(_ref_preds == y_cls_test))

    save_text(perceptron_editor.value, perc_class_name)

    mo.callout(
        mo.md(f"✅ **Perceptron** — Your accuracy: **{perceptron_acc:.1%}** | Reference: **{perceptron_ref_acc:.1%}**"),
        kind="success",
    )
    return Perceptron, perceptron_acc, perceptron_ok, perceptron_ref_acc


@app.cell
def _(
    Perceptron,
    X_cls,
    X_cls_train,
    mo,
    np,
    perceptron_ok,
    plt,
    y_cls,
    y_cls_train,
):
    mo.stop(not perceptron_ok, mo.md("*Decision boundary will appear once the implementation is complete.*"))

    _h = 0.05
    _x0_min5, _x0_max5 = X_cls[:, 0].min() - 0.5, X_cls[:, 0].max() + 0.5
    _x1_min5, _x1_max5 = X_cls[:, 1].min() - 0.5, X_cls[:, 1].max() + 0.5
    _xx5, _yy5 = np.meshgrid(np.arange(_x0_min5, _x0_max5, _h), np.arange(_x1_min5, _x1_max5, _h))
    _p_viz = Perceptron(learning_rate=0.01, epochs=100)
    _p_viz.fit(X_cls_train, y_cls_train)
    _Z5 = _p_viz.predict(np.c_[_xx5.ravel(), _yy5.ravel()]).reshape(_xx5.shape)
    fig_perc, ax_perc = plt.subplots(figsize=(7, 5))
    ax_perc.contourf(_xx5, _yy5, _Z5, alpha=0.3, cmap="bwr")
    ax_perc.scatter(X_cls[:, 0], X_cls[:, 1], c=y_cls, cmap="bwr", edgecolors="k", linewidths=0.4, s=30)
    ax_perc.set_title("Perceptron Decision Boundary (linear)")
    mo.mpl.interactive(fig_perc)


    # ════════════════════════════════════════════════════════════════════════════════
    # MODEL 8 — Ridge Regression
    # ════════════════════════════════════════════════════════════════════════════════
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---
        ## 🔷 Model 8: Ridge Regression (L2 Regularisation)

        Ridge Regression adds an L2 penalty to MSE to prevent overfitting:
        $$\mathcal{L}_{\text{Ridge}} = \frac{1}{n}\|y - X\theta\|^2 + \lambda\|\theta\|^2$$

        ### Closed-Form Solution
        $$\theta^* = (X^T X + \lambda I)^{-1} X^T y$$

        We typically **do not** regularise the bias term $\theta_0$ — set $I_{00} = 0$ after constructing $I$.

        ### Effect of $\lambda$
        - $\lambda = 0$: ordinary least squares (no regularisation)
        - Large $\lambda$: weights shrink toward zero → simpler, smoother model
        """
    )
    return


@app.cell
def _(load_text, mo):
    _default = '''class RidgeRegression:
    """L2-regularised linear regression (closed-form solution)."""

    def __init__(self, alpha=1.0):
        """
        Parameters
        ----------
        alpha : float
            Regularisation strength (lambda). Larger = stronger regularisation.
        """
        self.alpha = alpha
        self.theta = None

    def _add_bias(self, X):

    def fit(self, X, y):
        """Solve the Ridge normal equation."""
        Xb = self._add_bias(X)
        n, d = Xb.shape
        pass

    def predict(self, X):
        Xb = self._add_bias(X)
        pass
    '''
    ridge_class_name = 'RidgeRegression'
    ridge_editor = mo.ui.code_editor(
        value=load_text(ridge_class_name, _default),
        language="python",
    )
    ridge_editor
    return ridge_class_name, ridge_editor


@app.cell
def _(
    X_reg_test,
    X_reg_train,
    mo,
    np,
    ridge_class_name,
    ridge_editor,
    save_text,
    y_reg_test,
    y_reg_train,
):
    try:
        _ns = {}
        exec(ridge_editor.value, {"np": np}, _ns)
        RidgeRegression = _ns["RidgeRegression"]
        _rr = RidgeRegression(alpha=1.0)
        _rr.fit(X_reg_train, y_reg_train)
        _preds = _rr.predict(X_reg_test)
        if _preds is None:
            raise ValueError("predict() returned None")
        ridge_mse = float(np.mean((_preds - y_reg_test) ** 2))
        ridge_ok = True
    except Exception as _e:
        ridge_ok = False
        ridge_mse = float("inf")
        RidgeRegression = None
        mo.stop(True, mo.callout(mo.md(f"**Ridge Regression not ready:** {_e}"), kind="warn"))

    def _ridge_ref(X_tr, y_tr, X_te, alpha=1.0):
        Xb = np.hstack([np.ones((X_tr.shape[0], 1)), X_tr])
        d = Xb.shape[1]
        I = np.eye(d)
        I[0, 0] = 0
        theta = np.linalg.solve(Xb.T @ Xb + alpha * I, Xb.T @ y_tr)
        Xb_te = np.hstack([np.ones((X_te.shape[0], 1)), X_te])
        return Xb_te @ theta

    _ref_preds = _ridge_ref(X_reg_train, y_reg_train, X_reg_test)
    ridge_ref_mse = float(np.mean((_ref_preds - y_reg_test) ** 2))

    save_text(ridge_editor.value, ridge_class_name)

    mo.callout(
        mo.md(f"✅ **Ridge Regression** — Your MSE: **{ridge_mse:.2f}** | Reference MSE: **{ridge_ref_mse:.2f}**"),
        kind="success",
    )
    return RidgeRegression, ridge_mse, ridge_ok, ridge_ref_mse


@app.cell
def _(
    RidgeRegression,
    X_reg,
    X_reg_train,
    mo,
    np,
    plt,
    ridge_ok,
    y_reg,
    y_reg_train,
):
    mo.stop(not ridge_ok, mo.md("*Regression fit will appear once the implementation is complete.*"))

    _rr_viz = RidgeRegression(alpha=1.0)
    _rr_viz.fit(X_reg_train, y_reg_train)
    _x_line2 = np.linspace(X_reg.min(), X_reg.max(), 200).reshape(-1, 1)
    _y_line2 = _rr_viz.predict(_x_line2)
    fig_ridge, ax_ridge = plt.subplots(figsize=(7, 4))
    ax_ridge.scatter(X_reg, y_reg, alpha=0.5, color="steelblue", edgecolors="k", linewidths=0.3, s=30, label="Data")
    ax_ridge.plot(_x_line2, _y_line2, color="darkorange", lw=2, label="Ridge fit (α=1)")
    ax_ridge.set_title("Ridge Regression Fit")
    ax_ridge.legend()
    mo.mpl.interactive(fig_ridge)


    # ════════════════════════════════════════════════════════════════════════════════
    # LEADERBOARD
    # ════════════════════════════════════════════════════════════════════════════════
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---
        ## 🏆 Model Leaderboard

        How do your implementations compare to the reference solutions?
        A ⏳ means you haven't implemented that model yet — go back and fill in the TODOs!
        """
    )
    return


@app.cell
def _(
    dtree_acc,
    dtree_ok,
    dtree_ref_acc,
    kmeans_inertia,
    kmeans_ok,
    kmeans_ref_inertia,
    knn_acc,
    knn_ok,
    knn_ref_acc,
    linreg_mse,
    linreg_ok,
    linreg_ref_mse,
    logreg_acc,
    logreg_ok,
    logreg_ref_acc,
    mo,
    nb_acc,
    nb_ok,
    nb_ref_acc,
    perceptron_acc,
    perceptron_ok,
    perceptron_ref_acc,
    ridge_mse,
    ridge_ok,
    ridge_ref_mse,
):
    def _fmt_acc(ok, yours, ref):
        if not ok:
            return "⏳ not yet", "—", "—"
        sign = "+" if yours - ref >= 0 else ""
        return f"{yours:.1%}", f"{ref:.1%}", f"{sign}{yours - ref:.1%}"

    def _fmt_mse(ok, yours, ref):
        if not ok:
            return "⏳ not yet", "—", "—"
        sign = "+" if yours - ref >= 0 else ""
        return f"{yours:.2f}", f"{ref:.2f}", f"{sign}{yours - ref:.2f}"

    _rows = []
    _y, _r, _d = _fmt_acc(knn_ok, knn_acc, knn_ref_acc)
    _rows.append({"Model": "KNN", "Type": "Classification", "Metric": "Accuracy", "Yours": _y, "Reference": _r, "Δ": _d})
    _y, _r, _d = _fmt_mse(linreg_ok, linreg_mse, linreg_ref_mse)
    _rows.append({"Model": "Linear Regression", "Type": "Regression", "Metric": "MSE ↓", "Yours": _y, "Reference": _r, "Δ": _d})
    _y, _r, _d = _fmt_acc(logreg_ok, logreg_acc, logreg_ref_acc)
    _rows.append({"Model": "Logistic Regression", "Type": "Classification", "Metric": "Accuracy", "Yours": _y, "Reference": _r, "Δ": _d})
    _y, _r, _d = _fmt_acc(nb_ok, nb_acc, nb_ref_acc)
    _rows.append({"Model": "Naive Bayes", "Type": "Classification", "Metric": "Accuracy", "Yours": _y, "Reference": _r, "Δ": _d})
    _y, _r, _d = _fmt_acc(dtree_ok, dtree_acc, dtree_ref_acc)
    _rows.append({"Model": "Decision Tree", "Type": "Classification", "Metric": "Accuracy", "Yours": _y, "Reference": _r, "Δ": _d})
    if kmeans_ok:
        _km_d = f"{kmeans_inertia - kmeans_ref_inertia:+.2f}"
        _rows.append({"Model": "K-Means", "Type": "Clustering", "Metric": "Inertia ↓", "Yours": f"{kmeans_inertia:.2f}", "Reference": f"{kmeans_ref_inertia:.2f}", "Δ": _km_d})
    else:
        _rows.append({"Model": "K-Means", "Type": "Clustering", "Metric": "Inertia ↓", "Yours": "⏳ not yet", "Reference": "—", "Δ": "—"})
    _y, _r, _d = _fmt_acc(perceptron_ok, perceptron_acc, perceptron_ref_acc)
    _rows.append({"Model": "Perceptron", "Type": "Classification", "Metric": "Accuracy", "Yours": _y, "Reference": _r, "Δ": _d})
    _y, _r, _d = _fmt_mse(ridge_ok, ridge_mse, ridge_ref_mse)
    _rows.append({"Model": "Ridge Regression", "Type": "Regression", "Metric": "MSE ↓", "Yours": _y, "Reference": _r, "Δ": _d})

    mo.ui.table(_rows)
    return


@app.cell
def _(
    dtree_ok,
    kmeans_ok,
    knn_ok,
    linreg_ok,
    logreg_ok,
    mo,
    nb_ok,
    perceptron_ok,
    ridge_ok,
):
    _all_done = all([knn_ok, linreg_ok, logreg_ok, nb_ok, dtree_ok, kmeans_ok, perceptron_ok, ridge_ok])
    mo.stop(
        not _all_done,
        mo.md("*Complete all 8 implementations to unlock the congratulations banner! 💪*"),
    )
    mo.callout(
        mo.md("🎉 **Congratulations!** You've implemented all 8 ML models from scratch using only NumPy. You're officially dangerous with arrays!"),
        kind="success",
    )


    # ════════════════════════════════════════════════════════════════════════════════
    # INTERACTIVE HYPERPARAMETER EXPLORER
    # ════════════════════════════════════════════════════════════════════════════════
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---
        ## 🎛️ Interactive Hyperparameter Explorer

        Select a model and tune its hyperparameters — the decision boundary updates in real time.
        """
    )
    return


@app.cell
def _(mo):
    explorer_dropdown = mo.ui.dropdown(
        options=["KNN", "Logistic Regression", "Decision Tree", "Perceptron"],
        value="KNN",
        label="Select model to explore",
    )
    explorer_dropdown
    return (explorer_dropdown,)


@app.cell
def _(mo):
    # Slider bank — all sliders defined once here; we pick which to show below.
    knn_k_slider = mo.ui.slider(1, 20, value=5, label="k (neighbours)")
    lr_rate_slider = mo.ui.slider(0.001, 1.0, value=0.1, step=0.01, label="Learning rate")
    lr_epoch_slider = mo.ui.slider(100, 3000, value=500, step=100, label="Epochs")
    dt_depth_slider = mo.ui.slider(1, 10, value=4, label="max_depth")
    perc_rate_slider = mo.ui.slider(0.001, 0.5, value=0.01, step=0.005, label="Learning rate")
    perc_epoch_slider = mo.ui.slider(10, 500, value=100, step=10, label="Epochs")
    return (
        dt_depth_slider,
        knn_k_slider,
        lr_epoch_slider,
        lr_rate_slider,
        perc_epoch_slider,
        perc_rate_slider,
    )


@app.cell
def _(
    dt_depth_slider,
    explorer_dropdown,
    knn_k_slider,
    lr_epoch_slider,
    lr_rate_slider,
    mo,
    perc_epoch_slider,
    perc_rate_slider,
):
    _sel = explorer_dropdown.value
    if _sel == "KNN":
        explorer_controls = mo.vstack([mo.md("**KNN**"), knn_k_slider])
    elif _sel == "Logistic Regression":
        explorer_controls = mo.vstack([mo.md("**Logistic Regression**"), lr_rate_slider, lr_epoch_slider])
    elif _sel == "Decision Tree":
        explorer_controls = mo.vstack([mo.md("**Decision Tree**"), dt_depth_slider])
    else:
        explorer_controls = mo.vstack([mo.md("**Perceptron**"), perc_rate_slider, perc_epoch_slider])
    explorer_controls
    return


@app.cell
def _(
    DecisionTree,
    KNNClassifier,
    LogisticRegression,
    Perceptron,
    X_cls,
    X_cls_train,
    dt_depth_slider,
    dtree_ok,
    explorer_dropdown,
    knn_k_slider,
    knn_ok,
    logreg_ok,
    lr_epoch_slider,
    lr_rate_slider,
    mo,
    np,
    perc_epoch_slider,
    perc_rate_slider,
    perceptron_ok,
    plt,
    y_cls,
    y_cls_train,
):
    _sel = explorer_dropdown.value

    if _sel == "KNN":
        mo.stop(not knn_ok, mo.callout(mo.md("⏳ Implement KNN first to use the explorer."), kind="warn"))
        _model = KNNClassifier(k=int(knn_k_slider.value))
        _title = f"KNN (k={int(knn_k_slider.value)})"
    elif _sel == "Logistic Regression":
        mo.stop(not logreg_ok, mo.callout(mo.md("⏳ Implement Logistic Regression first to use the explorer."), kind="warn"))
        _model = LogisticRegression(learning_rate=float(lr_rate_slider.value), epochs=int(lr_epoch_slider.value))
        _title = f"Logistic Regression (lr={lr_rate_slider.value:.3f}, epochs={int(lr_epoch_slider.value)})"
    elif _sel == "Decision Tree":
        mo.stop(not dtree_ok, mo.callout(mo.md("⏳ Implement Decision Tree first to use the explorer."), kind="warn"))
        _model = DecisionTree(max_depth=int(dt_depth_slider.value))
        _title = f"Decision Tree (max_depth={int(dt_depth_slider.value)})"
    else:
        mo.stop(not perceptron_ok, mo.callout(mo.md("⏳ Implement Perceptron first to use the explorer."), kind="warn"))
        _model = Perceptron(learning_rate=float(perc_rate_slider.value), epochs=int(perc_epoch_slider.value))
        _title = f"Perceptron (lr={perc_rate_slider.value:.3f}, epochs={int(perc_epoch_slider.value)})"

    _model.fit(X_cls_train, y_cls_train)

    _h = 0.05
    _x0_min6, _x0_max6 = X_cls[:, 0].min() - 0.5, X_cls[:, 0].max() + 0.5
    _x1_min6, _x1_max6 = X_cls[:, 1].min() - 0.5, X_cls[:, 1].max() + 0.5
    _xx6, _yy6 = np.meshgrid(np.arange(_x0_min6, _x0_max6, _h), np.arange(_x1_min6, _x1_max6, _h))
    _Z6 = _model.predict(np.c_[_xx6.ravel(), _yy6.ravel()]).reshape(_xx6.shape)

    fig_explorer, ax_explorer = plt.subplots(figsize=(8, 5))
    ax_explorer.contourf(_xx6, _yy6, _Z6, alpha=0.35, cmap="bwr")
    ax_explorer.scatter(X_cls[:, 0], X_cls[:, 1], c=y_cls, cmap="bwr", edgecolors="k", linewidths=0.4, s=35)
    ax_explorer.set_title(_title)
    mo.mpl.interactive(fig_explorer)
    return


if __name__ == "__main__":
    app.run()
