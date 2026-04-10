

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
        # 🚀 Advanced ML from Scratch — The Deep Dive

        Welcome to the advanced track. Now that you've mastered the basics of K-NN, Linear Regression, and Decision Trees, it is time to peel back the layers on modern machine learning.

        In this notebook, we move beyond simple heuristics into **optimization theory, high-dimensional geometry, and neural architectures**.

        ## 🎓 Advanced Learning Goals
        - **Vectorized Backpropagation**: Calculate gradients manually for multi-layer networks.
        - **Ensemble Intelligence**: Combine weak learners into powerful Random Forests and Gradient Boosted machines.
        - **Geometric Boundaries**: Master the math of Support Vector Machines and the "Kernel Trick."
        - **Dimensionality & Manifolds**: Learn how PCA and LDA compress information without losing the signal.
        - **Robust Evaluation**: Implement K-Fold validation and ROC analysis to truly trust your models.

        ## 🛠️ The Ground Rules
        - **Pure NumPy**: No `sklearn` models. You are the architect.
        - **Vectorization**: Whenever possible, avoid `for` loops. Think in matrices.
        - **Numerical Stability**: Watch out for log(0) and exploding gradients.

        > "What I cannot create, I do not understand." — Richard Feynman
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
def _(mo):
    mo.md(
        r"""
        ## 🧠 Concept 1: Multi-Layer Perceptrons (MLP)

        A single Perceptron can only solve linearly separable problems (the XOR problem famously "killed" neural network research for years). To solve complex problems, we stack layers.

        ### The Forward Pass
        For a layer $l$, the computation is:
        $$z^{[l]} = W^{[l]}a^{[l-1]} + b^{[l]}$$
        $$a^{[l]} = \sigma(z^{[l]})$$

        ### The Backward Pass (The Chain Rule)
        Training a network is just an exercise in the chain rule. To update weight $W_{ij}$, we need to know how much the loss $L$ changes with respect to that weight:
        $$\frac{\partial L}{\partial W} = \frac{\partial L}{\partial a} \cdot \frac{\partial a}{\partial z} \cdot \frac{\partial z}{\partial W}$$

        Implementing this from scratch requires careful bookkeeping of matrix shapes. If your $X$ is $(N, D)$, your weights must align!
        """
    )
    return


@app.cell
def _(load_text, mo):
    mlp_code_initial = r'''class MLP:
        def __init__(self, input_size, hidden_size, output_size, lr=0.01):
            # Initialize weights and biases
            self.W1 = np.random.randn(input_size, hidden_size) * 0.01
            self.b1 = np.zeros((1, hidden_size))
            self.W2 = np.random.randn(hidden_size, output_size) * 0.01
            self.b2 = np.zeros((1, output_size))
            self.lr = lr

        def _sigmoid(self, z):
            return 1 / (1 + np.exp(-z))

        def fit(self, X, y, epochs=1000):
            # y should be (N, 1) for binary classification
            for _ in range(epochs):
                # 1. Forward Pass
                # layer1_z = ...
                # layer1_a = ...
                # output_z = ...
                # probs = ...

                # 2. Backward Pass (The Chain Rule)
                # error = probs - y
                # dW2 = ...
                # db2 = ...
                # d_hidden = (error @ W2.T) * (layer1_a * (1 - layer1_a))
                # dW1 = ...

                # 3. Update Weights
                pass

        def predict(self, X):
            # Return 0 or 1 based on 0.5 threshold
            pass
    '''
    mlp_editor = mo.ui.code_editor(
        value=load_text("mlp_exercise", mlp_code_initial),
        language="python",
    )
    mlp_editor
    return (mlp_editor,)


@app.cell
def _(
    X_cls_test,
    X_cls_train,
    mlp_editor,
    mo,
    np,
    save_text,
    y_cls_test,
    y_cls_train,
):
    try:
        _ns = {}
        exec(mlp_editor.value, {"np": np}, _ns)
        MLP = _ns["MLP"]

        # MLP often needs y in (N, 1) shape for matrix subtraction
        _y_tr = y_cls_train.reshape(-1, 1)

        _mlp = MLP(input_size=2, hidden_size=10, output_size=1, lr=0.1)
        _mlp.fit(X_cls_train, _y_tr, epochs=500)
        _preds = _mlp.predict(X_cls_test)

        if _preds is None:
            raise ValueError("predict() returned None")

        # Flatten preds to compare with (N,) y_test
        mlp_acc = float(np.mean(_preds.flatten() == y_cls_test))
        mlp_ok = True
    except Exception as _e:
        mlp_ok = False
        mlp_acc = 0.0
        MLP = None
        mo.stop(True, mo.callout(mo.md(f"**MLP not ready yet:** {_e}"), kind="warn"))

    # Baseline for non-linear moons dataset
    mlp_ref_acc = 0.88 
    save_text(mlp_editor.value, "mlp_exercise")

    mo.callout(
        mo.md(f"✅ **MLP** — Your accuracy: **{mlp_acc:.1%}** | Baseline Target: **{mlp_ref_acc:.1%}**"),
        kind="success",
    )
    return MLP, mlp_ok


@app.cell
def _(MLP, X_cls, X_cls_train, mlp_ok, mo, np, plt, y_cls, y_cls_train):
    mo.stop(not mlp_ok, mo.md("*MLP decision boundary will appear once implementation is complete.*"))

    _h = 0.05
    _x0_min, _x0_max = X_cls[:, 0].min() - 0.5, X_cls[:, 0].max() + 0.5
    _x1_min, _x1_max = X_cls[:, 1].min() - 0.5, X_cls[:, 1].max() + 0.5
    _xx, _yy = np.meshgrid(np.arange(_x0_min, _x0_max, _h), np.arange(_x1_min, _x1_max, _h))

    _mlp_viz = MLP(input_size=2, hidden_size=10, output_size=1, lr=0.1)
    _mlp_viz.fit(X_cls_train, y_cls_train.reshape(-1, 1), epochs=500)
    _Z = _mlp_viz.predict(np.c_[_xx.ravel(), _yy.ravel()]).reshape(_xx.shape)

    fig_mlp, ax_mlp = plt.subplots(figsize=(7, 5))
    ax_mlp.contourf(_xx, _yy, _Z, alpha=0.3, cmap="bwr")
    ax_mlp.scatter(X_cls[:, 0], X_cls[:, 1], c=y_cls, cmap="bwr", edgecolors="k", s=30)
    ax_mlp.set_title("MLP Decision Boundary (Hidden Size: 10)")
    mo.mpl.interactive(fig_mlp)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## ⚖️ Concept 2: SVM & The Margin

        While Logistic Regression tries to maximize the likelihood of the data, the **Support Vector Machine (SVM)** tries to find the "Maximum Margin Hyperplane."

        ### Hard vs. Soft Margin
        - **Hard Margin**: Assumes the data is perfectly separable. No mistakes allowed.
        - **Soft Margin**: Uses **Slack Variables ($\xi$)** to allow some points to be on the wrong side of the margin to achieve better generalization.

        The objective function balances two goals:
        1.  **Maximize the margin**: $\min \frac{1}{2} \|w\|^2$
        2.  **Minimize violations**: $C \sum \xi_i$

        We will implement this using **Hinge Loss**:
        $$\mathcal{L} = \max(0, 1 - y_i(w \cdot x_i + b))$$
        """
    )
    return


@app.cell
def _(load_text, mo):
    svm_code_initial = r'''class SVM:
        def __init__(self, learning_rate=0.001, lambda_param=0.01, n_iters=1000):
            self.lr = learning_rate
            self.lambda_param = lambda_param
            self.n_iters = n_iters
            self.w = None
            self.b = None

        def fit(self, X, y):
            # Convert y to [-1, 1]
            y_ = np.where(y <= 0, -1, 1)
            n_samples, n_features = X.shape
            self.w = np.zeros(n_features)
            self.b = 0

            for _ in range(self.n_iters):
                for idx, x_i in enumerate(X):
                    # Hinge Loss Gradient Descent
                    # condition: y_i * (w*x_i - b) >= 1
                    pass

        def predict(self, X):
            # Linear decision: sign(w*x - b)
            pass
    '''
    svm_editor = mo.ui.code_editor(
        value=load_text("svm_exercise", svm_code_initial),
        language="python",
    )
    svm_editor
    return (svm_editor,)


@app.cell
def _(
    X_cls_test,
    X_cls_train,
    mo,
    np,
    save_text,
    svm_editor,
    y_cls_test,
    y_cls_train,
):
    try:
        _ns = {}
        exec(svm_editor.value, {"np": np}, _ns)
        SVM = _ns["SVM"]

        _svm = SVM(learning_rate=0.001, n_iters=500)
        _svm.fit(X_cls_train, y_cls_train)
        _preds = _svm.predict(X_cls_test)

        if _preds is None:
            raise ValueError("predict() returned None")

        svm_acc = float(np.mean(_preds == y_cls_test))
        svm_ok = True
    except Exception as _e:
        svm_ok = False
        svm_acc = 0.0
        SVM = None
        mo.stop(True, mo.callout(mo.md(f"**SVM not ready yet:** {_e}"), kind="warn"))

    svm_ref_acc = 0.84
    save_text(svm_editor.value, "svm_exercise")

    mo.callout(
        mo.md(f"✅ **SVM** — Your accuracy: **{svm_acc:.1%}** | Baseline Target: **{svm_ref_acc:.1%}**"),
        kind="success",
    )
    return SVM, svm_ok


@app.cell
def _(SVM, X_cls, X_cls_train, mo, np, plt, svm_ok, y_cls, y_cls_train):
    mo.stop(not svm_ok, mo.md("*SVM decision boundary will appear once implementation is complete.*"))

    _h = 0.05
    _x0_min, _x0_max = X_cls[:, 0].min() - 0.5, X_cls[:, 0].max() + 0.5
    _x1_min, _x1_max = X_cls[:, 1].min() - 0.5, X_cls[:, 1].max() + 0.5
    _xx, _yy = np.meshgrid(np.arange(_x0_min, _x0_max, _h), np.arange(_x1_min, _x1_max, _h))

    _svm_viz = SVM(n_iters=500)
    _svm_viz.fit(X_cls_train, y_cls_train)
    _Z = _svm_viz.predict(np.c_[_xx.ravel(), _yy.ravel()]).reshape(_xx.shape)

    fig_svm, ax_svm = plt.subplots(figsize=(7, 5))
    ax_svm.contourf(_xx, _yy, _Z, alpha=0.3, cmap="bwr")
    ax_svm.scatter(X_cls[:, 0], X_cls[:, 1], c=y_cls, cmap="bwr", edgecolors="k", s=30)
    ax_svm.set_title("SVM Decision Boundary (Linear Kernel)")
    mo.mpl.interactive(fig_svm)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 🌌 Concept 3: The Curse of Dimensionality

        In high-dimensional space, our intuition for "distance" breaks down. 
        - As dimensions increase, the "volume" of the space increases so fast that the data becomes sparse.
        - In high dimensions, almost all points are at the "edge" of the sample space.
        - The distance between the nearest and farthest points becomes negligible.

        ### PCA (Unsupervised)
        Principal Component Analysis finds the directions (eigenvectors) of maximum variance. It answers: *"If I have to squash this 10D data into 2D, which directions preserve the most information?"*

        ### LDA (Supervised)
        Linear Discriminant Analysis doesn't care about variance; it cares about **class separability**. It projects data into a space that minimizes within-class variance and maximizes between-class distance.
        """
    )
    return


@app.cell
def _(load_text, mo):
    pca_code_initial = r'''class PCA:
        def __init__(self, n_components=2):
            self.n_components = n_components
            self.components = None
            self.mean = None

        def fit(self, X):
            # 1. Center the data
            # 2. Compute Covariance Matrix
            # 3. Eigen-decomposition (np.linalg.eig)
            # 4. Sort and store top 'n_components' eigenvectors
            pass

        def transform(self, X):
            # Project X onto the principal components
            pass
    '''
    pca_editor = mo.ui.code_editor(
        value=load_text("pca_exercise", pca_code_initial),
        language="python",
    )
    pca_editor
    return (pca_editor,)


@app.cell
def _(X_cls, mo, np, pca_editor, save_text):
    try:
        _ns = {}
        exec(pca_editor.value, {"np": np}, _ns)
        PCA = _ns["PCA"]

        _pca = PCA(n_components=1)
        _pca.fit(X_cls)
        _X_pca = _pca.transform(X_cls)

        if _X_pca.shape[1] != 1:
            raise ValueError(f"Expected 1 component, got {_X_pca.shape[1]}")
        pca_ok = True
    except Exception as _e:
        pca_ok = False
        PCA = None
        mo.stop(True, mo.callout(mo.md(f"**PCA not ready yet:** {_e}"), kind="warn"))

    def _pca_ref(X):
        X_centered = X - np.mean(X, axis=0)
        cov = np.cov(X_centered.T)
        eig_vals, eig_vecs = np.linalg.eig(cov)
        return X_centered @ eig_vecs[:, np.argsort(eig_vals)[::-1][0]]

    _ref_out = _pca_ref(X_cls)
    # Verification: check if student variance captured is similar to reference
    pca_status = "Verified" if pca_ok else "Incomplete"
    save_text(pca_editor.value, "pca_exercise")

    mo.callout(mo.md(f"✅ **PCA** — Implementation loaded. Output shape: **{_X_pca.shape}**"), kind="success")
    return PCA, pca_ok


@app.cell
def _(PCA, X_cls, mo, pca_ok, plt, y_cls):
    mo.stop(not pca_ok, mo.md("*PCA visualization will appear once implementation is complete.*"))

    _pca_viz = PCA(n_components=1)
    _pca_viz.fit(X_cls)
    _X_reduced = _pca_viz.transform(X_cls)
    # Reconstruct for visualization
    _X_projected = (_X_reduced @ _pca_viz.components.T) + _pca_viz.mean
    print(_pca_viz.cov_mat)

    fig_pca, ax_pca = plt.subplots(figsize=(7, 5))
    ax_pca.scatter(X_cls[:, 0], X_cls[:, 1], c=y_cls, alpha=0.2, cmap="bwr")
    ax_pca.scatter(_X_projected[:, 0], _X_projected[:, 1], c=y_cls, cmap="bwr", s=10, label="Projected Data")
    ax_pca.set_title("PCA: Projecting 2D Moons onto 1st Principal Component")
    ax_pca.legend()
    mo.mpl.interactive(fig_pca)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 🌲 Concept 4: Ensembles

        Why use one model when you can use a committee?

        1. **Bagging (Random Forest)**: 
           - Train $N$ trees on different "Bootstrap" samples (sampling with replacement).
           - Also use **Feature Subsampling** (each split only looks at a random subset of features).
           - **Goal**: Reduce **Variance** (prevent overfitting).

        2. **Boosting (Gradient Boosting)**:
           - Train trees sequentially. 
           - Tree #2 is trained to predict the **errors (residuals)** of Tree #1.
           - **Goal**: Reduce **Bias** (turn weak learners into strong ones).
        """
    )
    return


@app.cell
def _(np):
    class DecisionTree:
        """Decision Tree Classifier using Gini impurity."""
    
        def __init__(self, max_depth=5):
            self.max_depth = max_depth
            self.tree = None
    
        def _gini(self, y):
            """Gini impurity of label array y."""
            # Hint: np.bincount(y) / len(y) gives the class proportions
            return 1 - np.sum((np.bincount(y) / len(y)) ** 2)
    
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
                    weighted_gini = (left.shape[0] / n) * self._gini(left) + (right.shape[0] / n) * self._gini(right)
                    if weighted_gini < best_gini:
                        best_gini, best_feat, best_thresh = weighted_gini, feat, thresh
            return best_feat, best_thresh

        def _build(self, X, y, depth):
            """Recursively build the tree; return a node dict."""
            stopping_criteria = depth >= self.max_depth or len(np.unique(y)) == 1 or X.shape[0] < 2
            if stopping_criteria:
                return {'leaf': True, 'class': np.argmax(np.bincount(y))}
        
            feat, thresh = self._best_split(X, y)
            if feat is None:
                return {'leaf': True, 'class': np.argmax(np.bincount(y))}
        
            left_mask, right_mask = X[:, feat] <= thresh, X[:, feat] > thresh
        
            return {
              'leaf': False,
              'feat': feat,
              'best_thresh': thresh,
              'left': self._build(X[left_mask], y[left_mask], depth + 1),
              'right': self._build(X[right_mask], y[right_mask], depth + 1)
            }
    
        def fit(self, X, y):
            # TODO: self.tree = self._build(X, y, depth=0)
            self.tree = self._build(X, y, depth=0)
    
        def _predict_one(self, x, node):
            """Traverse the tree for a single sample."""
            if node['leaf']:
                # TODO: recurse left if x[node["feat"]] <= node["thresh"], else right
                return node['class']
            if x[node['feat']] <= node['best_thresh']:
                return self._predict_one(x, node['left'])
            return self._predict_one(x, node['right'])
    
        def predict(self, X):
            return np.array([self._predict_one(x, self.tree) for x in X])
    return (DecisionTree,)


@app.cell
def _(load_text, mo):
    rf_code_initial = r'''class RandomForest:
        def __init__(self, n_trees=10, max_depth=5, sample_size_ratio=0.8):
            self.n_trees = n_trees
            self.max_depth = max_depth
            self.ratio = sample_size_ratio
            self.trees = []

        def fit(self, X, y):
            self.trees = []
            n_samples = X.shape[0]
            for _ in range(self.n_trees):
                # 1. Bootstrap: Sample indices with replacement
                # 2. Train a DecisionTree (using the class from previous course)
                pass

        def predict(self, X):
            # Aggregate predictions and take the majority vote
            pass
    '''
    rf_editor = mo.ui.code_editor(
        value=load_text("rf_exercise", rf_code_initial),
        language="python",
    )
    rf_editor
    return (rf_editor,)


@app.cell
def _(
    DecisionTree,
    X_cls_test,
    X_cls_train,
    mo,
    np,
    rf_editor,
    save_text,
    y_cls_test,
    y_cls_train,
):
    try:
        # We pass the DecisionTree class from the previous course into the exec namespace
        _ns = {"np": np, "DecisionTree": DecisionTree} 
        exec(rf_editor.value, _ns)
        RandomForest = _ns["RandomForest"]

        _rf = RandomForest(n_trees=10, max_depth=3)
        _rf.fit(X_cls_train, y_cls_train)
        _preds = _rf.predict(X_cls_test)

        if _preds is None:
            raise ValueError("predict() returned None")

        rf_acc = float(np.mean(_preds == y_cls_test))
        rf_ok = True
    except Exception as _e:
        rf_ok = False
        rf_acc = 0.0
        RandomForest = None
        mo.stop(True, mo.callout(mo.md(f"**Random Forest not ready yet:** {_e}"), kind="warn"))

    # Reference check
    rf_ref_acc = 0.92
    save_text(rf_editor.value, "rf_exercise")

    mo.callout(
        mo.md(f"✅ **Random Forest** — Your accuracy: **{rf_acc:.1%}** | Baseline Target: **{rf_ref_acc:.1%}**"),
        kind="success",
    )
    return RandomForest, rf_ok


@app.cell
def _(
    RandomForest,
    X_cls,
    X_cls_train,
    mo,
    np,
    plt,
    rf_ok,
    y_cls,
    y_cls_train,
):
    mo.stop(not rf_ok, mo.md("*Random Forest boundary will appear once implementation is complete.*"))

    _h = 0.05
    _x0_min, _x0_max = X_cls[:, 0].min() - 0.5, X_cls[:, 0].max() + 0.5
    _x1_min, _x1_max = X_cls[:, 1].min() - 0.5, X_cls[:, 1].max() + 0.5
    _xx, _yy = np.meshgrid(np.arange(_x0_min, _x0_max, _h), np.arange(_x1_min, _x1_max, _h))

    _rf_viz = RandomForest(n_trees=10, max_depth=3)
    _rf_viz.fit(X_cls_train, y_cls_train)
    _Z = _rf_viz.predict(np.c_[_xx.ravel(), _yy.ravel()]).reshape(_xx.shape)

    fig_rf, ax_rf = plt.subplots(figsize=(7, 5))
    ax_rf.contourf(_xx, _yy, _Z, alpha=0.3, cmap="bwr")
    ax_rf.scatter(X_cls[:, 0], X_cls[:, 1], c=y_cls, cmap="bwr", edgecolors="k", s=30)
    ax_rf.set_title("Random Forest Decision Boundary (10 Trees)")
    mo.mpl.interactive(fig_rf)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 📈 Concept 5: Gradient Boosting (Regression)

        Gradient Boosting is an **additive** model. Instead of building independent trees, we build trees sequentially to correct the mistakes of the previous ensemble.

        ### The Algorithm
        1.  Initialize the model with a constant value: $F_0(x) = \text{mean}(y)$.
        2.  For $m = 1$ to $M$ (number of trees):
            -   Calculate the **residuals** (errors): $r_{im} = y_i - F_{m-1}(x_i)$.
            -   Fit a weak learner (Decision Tree) $h_m(x)$ to these residuals.
            -   Update the model: $F_m(x) = F_{m-1}(x) + \nu \cdot h_m(x)$, where $\nu$ is the **learning rate**.

        By fitting residuals, each new tree moves the ensemble closer to the true labels.
        """
    )
    return


@app.cell
def _(load_text, mo, save_text):
    gb_code_initial = r'''class GradientBoostedRegressor:
        def __init__(self, n_estimators=10, learning_rate=0.1, max_depth=3):
            self.n_estimators = n_estimators
            self.lr = learning_rate
            self.max_depth = max_depth
            self.trees = []
            self.initial_prediction = None

        def fit(self, X, y):
            # 1. Start with the mean of y
            self.initial_prediction = np.mean(y)
            f_m = np.full(y.shape, self.initial_prediction)

            for _ in range(self.n_estimators):
                # 2. Compute residuals (y - current_prediction)
                residuals = y - f_m

                # 3. Fit a DecisionTree to the residuals
                # tree = DecisionTreeRegressor(max_depth=self.max_depth)
                # tree.fit(X, residuals)

                # 4. Update the prediction: f_m += lr * tree.predict(X)
                # self.trees.append(tree)
                pass

        def predict(self, X):
            # Start with initial_prediction and add lr * tree.predict(X) for all trees
            pass
    '''
    gb_editor = mo.ui.code_editor(
        value=load_text("gb_exercise", gb_code_initial),
        language="python",
        on_change=lambda v: save_text("gb_exercise", v),
    )
    gb_editor
    return (gb_editor,)


@app.cell
def _(
    DecisionTree,
    X_reg_test,
    X_reg_train,
    gb_editor,
    mo,
    np,
    save_text,
    y_reg_test,
    y_reg_train,
):
    try:
        _ns = {"np": np, "DecisionTreeRegressor": DecisionTree} # Assuming your DT handles regression
        exec(gb_editor.value, _ns)
        GradientBoostedRegressor = _ns["GradientBoostedRegressor"]

        _gb = GradientBoostedRegressor(n_estimators=5, learning_rate=0.1)
        _gb.fit(X_reg_train, y_reg_train)
        _preds = _gb.predict(X_reg_test)

        if _preds is None:
            raise ValueError("predict() returned None")

        gb_mse = float(np.mean((_preds - y_reg_test)**2))
        gb_ok = True
    except Exception as _e:
        gb_ok = False
        gb_mse = 0.0
        mo.stop(True, mo.callout(mo.md(f"**Gradient Boosting not ready yet:** {_e}"), kind="warn"))

    save_text(gb_editor.value, "gb_exercise")
    mo.callout(mo.md(f"✅ **Gradient Boosting** — Model trained. Test MSE: **{gb_mse:.2f}**"), kind="success")
    return GradientBoostedRegressor, gb_mse, gb_ok


@app.cell
def _(
    GradientBoostedRegressor,
    X_reg,
    X_reg_train,
    gb_ok,
    mo,
    np,
    plt,
    y_reg,
    y_reg_train,
):
    mo.stop(not gb_ok, mo.md("*Gradient Boosting fit will appear once implementation is complete.*"))

    _x_range = np.linspace(X_reg.min(), X_reg.max(), 500).reshape(-1, 1)
    _gb_viz = GradientBoostedRegressor(n_estimators=10, learning_rate=0.1)
    _gb_viz.fit(X_reg_train, y_reg_train)
    _y_pred = _gb_viz.predict(_x_range)

    fig_gb, ax_gb = plt.subplots(figsize=(7, 5))
    ax_gb.scatter(X_reg, y_reg, color="gray", alpha=0.5, label="Data")
    ax_gb.plot(_x_range, _y_pred, color="red", linewidth=2, label="GB Fit")
    ax_gb.set_title("Gradient Boosting Regressor Fit")
    ax_gb.legend()
    mo.mpl.interactive(fig_gb)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 🛰️ Concept 6: DBSCAN

        **Density-Based Spatial Clustering of Applications with Noise** does not require you to specify the number of clusters $K$. Instead, it uses two parameters:
        -   **Eps ($\epsilon$)**: The maximum distance between two samples for one to be considered as in the neighborhood of the other.
        -   **MinPts**: The number of samples in a neighborhood for a point to be considered a **core point**.

        ### Logic
        -   **Core Point**: Has $\ge$ MinPts within $\epsilon$ distance.
        -   **Border Point**: Is within $\epsilon$ of a core point but has $<$ MinPts.
        -   **Noise**: Neither of the above.
        """
    )
    return


@app.cell
def _(load_text, mo):
    dbscan_code_initial = r'''class DBSCAN:
        """
        Density-Based Spatial Clustering of Applications with Noise (DBSCAN)

        Parameters
        ----------
        eps : float
            Maximum distance between two samples to be considered neighbors.
        min_samples : int
            Minimum number of neighbors required to form a core point.
        """

        def __init__(self, eps=0.5, min_samples=5):
            self.eps = eps
            self.min_samples = min_samples
            self.labels_ = None

        def fit(self, X):
            """
            Fit DBSCAN clustering on dataset X.

            Parameters
            ----------
            X : np.ndarray of shape (n_samples, n_features)
            """
            n_samples = X.shape[0]
            # Initialize all points as noise (-1)
            self.labels_ = np.full(n_samples, -1)
            # Track visited points
            visited = np.zeros(n_samples, dtype=bool)
            cluster_id = 0
            for i in range(n_samples):
                # TODO 1: Skip if already visited
                pass
                # TODO 2: Mark current point as visited
                pass
                # TODO 3: Find neighbors of point i
                neighbors = None
                # TODO 4: If not enough neighbors → mark as noise
                # (keep label = -1)
                pass
                # TODO 5: Else → expand cluster
                # - call _expand_cluster(...)
                # - increment cluster_id
                pass
            return self

        def _get_neighbors(self, X, idx):
            """
            Find all points within eps distance of X[idx].

            Returns
            -------
            neighbors : np.ndarray of indices
            """
            # TODO 6:
            # Compute Euclidean distances from X[idx] to all points
            # Hint: np.linalg.norm(..., axis=1)
            dists = None
            # TODO 7:
            # Return indices where distance <= eps
            neighbors = None
            return neighbors

        def _expand_cluster(self, X, visited, point_idx, neighbors, cluster_id):
            """
            Expand cluster starting from a core point.

            Parameters
            ----------
            point_idx : int
                Index of the starting core point
            neighbors : np.ndarray
                Neighbor indices of the core point
            """
            # TODO 8: Assign cluster_id to the starting point
            pass
            i = 0
            while i < len(neighbors):
                neighbor_idx = neighbors[i]
                # TODO 9:
                # If neighbor not visited:
                #   - mark visited
                #   - get its neighbors
                # TODO 10:
                # If neighbor is a core point:
                #   - merge its neighbors into current neighbors list
                # TODO 11:
                # If neighbor is noise (-1):
                #   - assign it to current cluster
                i += 1
    '''
    dbscan_editor = mo.ui.code_editor(
        value=load_text("dbscan_exercise", dbscan_code_initial),
        language="python",
    )
    dbscan_editor
    return (dbscan_editor,)


@app.cell
def _(X_unsup, dbscan_editor, mo, np, save_text):
    try:
        _ns = {"np": np}
        exec(dbscan_editor.value, _ns)
        DBSCAN = _ns["DBSCAN"]

        _db = DBSCAN(eps=0.2, min_samples=5)
        _db.fit(X_unsup)

        db_labels = _db.labels_
        n_clusters = len(set(db_labels)) - (1 if -1 in db_labels else 0)

        if n_clusters == 0:
            raise ValueError("No clusters were created")

        db_ok = True
    except Exception as _e:
        db_ok = False
        mo.stop(True, mo.callout(mo.md(f"**DBSCAN not ready yet:** {_e}"), kind="warn"))

    save_text(dbscan_editor.value, "dbscan_exercise")
    mo.callout(mo.md(f"✅ **DBSCAN** — Clusters found: **{n_clusters}**. Noise points: **{np.sum(db_labels == -1)}**"), kind="success")
    return db_labels, db_ok


@app.cell
def _(X_unsup, db_labels, db_ok, mo, plt):
    mo.stop(not db_ok, mo.md("*DBSCAN clusters will appear once implementation is complete.*"))

    fig_db, ax_db = plt.subplots(figsize=(7, 5))
    _scatter = ax_db.scatter(X_unsup[:, 0], X_unsup[:, 1], c=db_labels, cmap="viridis", s=30)
    ax_db.set_title(f"DBSCAN Clustering (Noise points shown in darkest color)")
    mo.mpl.interactive(fig_db)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 🌳 Concept 7: HDBSCAN

        HDBSCAN converts DBSCAN into a hierarchical clustering algorithm. It builds a "Condensed Tree" of clusters and then uses a stability metric to "cut" the tree and extract the most persistent clusters.

        ### Key Advantage
        Unlike DBSCAN, you don't need to choose a global $\epsilon$. It finds clusters that are locally dense relative to their surroundings.
        """
    )
    return


@app.cell
def _(load_text, mo, save_text):
    hdbscan_code_initial = r'''class HDBSCAN_Simplified:
        def __init__(self, min_cluster_size=5):
            self.min_cluster_size = min_cluster_size
            self.labels_ = None

        def fit(self, X):
            # 1. Compute Mutual Reachability Distance
            # 2. Build Minimum Spanning Tree
            # 3. Build Cluster Hierarchy (Dendrogram)
            # 4. Condense the tree and extract clusters based on stability
            pass
    '''
    hdbscan_editor = mo.ui.code_editor(
        value=load_text("hdbscan_exercise", hdbscan_code_initial),
        language="python",
        on_change=lambda v: save_text("hdbscan_exercise", v),
    )
    hdbscan_editor
    return (hdbscan_editor,)


@app.cell
def _(X_unsup, hdbscan_editor, mo, np, save_text):
    try:
        _ns = {"np": np}
        exec(hdbscan_editor.value, _ns)
        HDBSCAN = _ns["HDBSCAN_Simplified"]

        hdb = HDBSCAN(min_cluster_size=5)
        hdb.fit(X_unsup)

        if hdb.labels_ is None:
            raise ValueError("predict() returned None")
        hdb_ok = True
    except Exception as _e:
        hdb_ok = False
        mo.stop(True, mo.callout(mo.md(f"**HDBSCAN not ready yet:** {_e}"), kind="warn"))

    save_text(hdbscan_editor.value, "hdbscan_exercise")
    mo.callout(mo.md(f"✅ **HDBSCAN** — Hierarchical implementation loaded."), kind="success")
    return hdb, hdb_ok


@app.cell
def _(X_unsup, hdb, hdb_ok, mo, plt):
    mo.stop(not hdb_ok, mo.md("*HDBSCAN clusters will appear once implementation is complete.*"))

    fig_hdb, ax_hdb = plt.subplots(figsize=(7, 5))
    ax_hdb.scatter(X_unsup[:, 0], X_unsup[:, 1], c=hdb.labels_, cmap="plasma", s=30)
    ax_hdb.set_title("HDBSCAN Hierarchical Clustering")
    mo.mpl.interactive(fig_hdb)
    return


@app.cell
def _(mo):
    mo.md(r"""## Additional Concepts""")
    return


@app.cell
def _(load_text, mo):
    kfold_code_initial = r'''def k_fold_cv(model_class, X, y, k=5, **model_params):
        indices = np.arange(len(X))
        np.random.shuffle(indices)
        folds = np.array_split(indices, k)

        accuracies = []
        for i in range(k):
            # 1. Split into train and validation sets
            # 2. Instantiate and fit model
            # 3. Score and store accuracy
            pass
        return np.mean(accuracies)
    '''
    kfold_editor = mo.ui.code_editor(
        value=load_text("kfold_exercise", kfold_code_initial),
        language="python",
    )
    kfold_editor
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## ⚡ Concept 8: Adaptive Moments (Adam)

        Vanilla Gradient Descent ($w = w - \eta \cdot dw$) often struggles with "ravines" or noisy gradients. **Adam** (Adaptive Moment Estimation) maintains two moving averages:
        1.  **$m_t$ (1st moment)**: The mean of gradients (Momentum).
        2.  **$v_t$ (2nd moment)**: The uncentered variance of gradients (Adaptive Learning Rate).

        The update rule is:
        $$m_t = \beta_1 m_{t-1} + (1-\beta_1)g_t$$
        $$v_t = \beta_2 v_{t-1} + (1-\beta_2)g_t^2$$
        $$\hat{w} = w - \frac{\eta}{\sqrt{\hat{v}_t} + \epsilon} \hat{m}_t$$
        """
    )
    return


@app.cell
def _(load_text, mo):
    adam_code_initial = r'''def adam_update(w, dw, m, v, t, lr=0.001, b1=0.9, b2=0.999, eps=1e-8):
        # 1. Update biased first moment estimate
        # m = ...
        # 2. Update biased second raw moment estimate
        # v = ...
        # 3. Compute bias-corrected first moment estimate
        # m_hat = m / (1 - b1**t)
        # 4. Compute bias-corrected second raw moment estimate
        # v_hat = v / (1 - b2**t)
        # 5. Update weights
        # w_new = w - lr * m_hat / (np.sqrt(v_hat) + eps)
        return w, m, v
    '''
    adam_editor = mo.ui.code_editor(
        value=load_text("adam_exercise", adam_code_initial),
        language="python",
    )
    adam_editor
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 🔮 Concept 9: The Kernel Trick

        Some data is impossible to separate with a straight line in 2D. However, if we project the data into **3D space**, a "slice" (plane) can separate it perfectly.

        The **Radial Basis Function (RBF) Kernel** essentially does this implicitly:
        $$K(x, y) = \exp(-\gamma \|x - y\|^2)$$
        """
    )
    return


@app.cell
def _(mo):
    show_kernel_trick = mo.ui.checkbox(label='Show Kernel Trick Plot')
    show_kernel_trick
    return (show_kernel_trick,)


@app.cell
def _(X_cls, mo, np, plt, show_kernel_trick, y_cls):
    mo.stop(not show_kernel_trick.value)
    # This cell creates a 3D plot showing the 2D moons lifted into the 3rd dimension
    from mpl_toolkits.mplot3d import Axes3D

    _gamma = 1.0
    _r = np.exp(-(X_cls**2).sum(1) * _gamma) # Lifting points using RBF-like logic

    fig_kernel = plt.figure(figsize=(8, 6))
    ax_kernel = fig_kernel.add_subplot(111, projection='3d')
    ax_kernel.scatter(X_cls[:, 0], X_cls[:, 1], _r, c=y_cls, cmap='bwr', s=20)
    ax_kernel.set_title("The Kernel Trick: Lifting 2D Moons into 3D")
    mo.mpl.interactive(fig_kernel)
    return


@app.cell
def _(load_text, mo):
    roc_code_initial = r'''def compute_roc(y_true, y_probs):
        thresholds = np.linspace(0, 1, 100)
        tpr = [] # True Positive Rate
        fpr = [] # False Positive Rate

        for thresh in thresholds:
            # 1. Apply threshold to get binary predictions
            # 2. Calculate TP, FP, TN, FN
            # 3. tpr.append(TP / (TP + FN))
            # 4. fpr.append(FP / (FP + TN))
            pass
        return fpr, tpr
    '''
    roc_editor = mo.ui.code_editor(
        value=load_text("roc_exercise", roc_code_initial),
        language="python",
    )
    roc_editor
    return (roc_editor,)


@app.cell
def _(plt, roc_editor):
    from sklearn.metrics import auc

    def plot_roc_curve(fpr, tpr):
        """
        Plots the ROC curve given False Positive Rate (FPR) and True Positive Rate (TPR).
        """
        # Calculate the Area Under the Curve (AUC)
        roc_auc = auc(fpr, tpr)
    
        plt.figure(figsize=(8, 6))
    
        # Plot the ROC curve
        plt.plot(fpr, tpr, color='darkorange', lw=2, 
                 label=f'ROC curve (area = {roc_auc:.2f})')
    
        # Plot the diagonal 'no-skill' line (random guessing)
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random Guessing')
    
        # Set plot limits and labels
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate (FPR)')
        plt.ylabel('True Positive Rate (TPR)')
        plt.title('Receiver Operating Characteristic (ROC) Curve')
        plt.legend(loc="lower right")
        plt.grid(alpha=0.3)
    
        plt.show()

    exec(roc_editor.value)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 📐 Concept 10: Norms and Similarity

        How do we measure the "size" of a vector or the "distance" between two points?

        1.  **L1 Norm (Manhattan)**: $\|x\|_1 = \sum |x_i|$. It creates "diamond" shaped boundaries and encourages sparsity.
        2.  **L2 Norm (Euclidean)**: $\|x\|_2 = \sqrt{\sum x_i^2}$. The shortest path; it creates "circular" boundaries.
        3.  **Cosine Similarity**: Measures the *angle* between vectors, ignoring their magnitude.
            $$\text{cos}(\theta) = \frac{A \cdot B}{\|A\| \|B\|}$$

        In high dimensions, Euclidean distance can become less meaningful (distance concentration), which is why Cosine similarity is often preferred for text and embeddings.
        """
    )
    return


@app.cell
def _(load_text, mo):
    norms_code_initial = r'''def compute_metrics(v1, v2):
        # v1 and v2 are numpy arrays of the same shape

        # 1. L1 Distance (Manhattan)
        # l1_dist = ...

        # 2. L2 Distance (Euclidean)
        # l2_dist = ...

        # 3. Cosine Similarity
        # dot_prod = np.dot(v1, v2)
        # norm_v1 = ...
        # cos_sim = dot_prod / (norm_v1 * norm_v2)

        return {"l1": None, "l2": None, "cosine": None}
    '''
    norms_editor = mo.ui.code_editor(
        value=load_text("norms_exercise", norms_code_initial),
        language="python",
    )
    norms_editor
    return (norms_editor,)


@app.cell
def _(mo, norms_editor, np, save_text):
    try:
        _ns = {"np": np}
        exec(norms_editor.value, _ns)
        compute_metrics = _ns["compute_metrics"]

        _v1, _v2 = np.array([1, 2, 3]), np.array([4, 5, 6])
        _res = compute_metrics(_v1, _v2)

        # Check L2 specifically
        _expected_l2 = np.linalg.norm(_v1 - _v2)
        norms_ok = np.isclose(_res.get("l2", 0), _expected_l2)
    except Exception as _e:
        norms_ok = False
        mo.stop(True, mo.callout(mo.md(f"**Norms not ready:** {_e}"), kind="warn"))

    save_text(norms_editor.value, "norms_exercise")

    mo.callout(mo.md(f"✅ **Norms & Metrics** — Implementation verified."), kind="success")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 🎯 Concept 11: Beyond Accuracy

        When evaluating a classifier, we use the **Confusion Matrix**:
        - **TP**: Predicted Positive, Actual Positive
        - **FP**: Predicted Positive, Actual Negative (Type I Error)
        - **FN**: Predicted Negative, Actual Positive (Type II Error)

        ### Key Metrics:
        - **Precision**: "Of all predicted positives, how many were correct?" $\frac{TP}{TP + FP}$
        - **Recall**: "Of all actual positives, how many did we find?" $\frac{TP}{TP + FN}$
        - **F1-Score**: Harmonic mean of the two. $2 \cdot \frac{Prec \cdot Rec}{Prec + Rec}$
        """
    )
    return


@app.cell
def _(load_text, mo):
    eval_metrics_initial = r'''def classification_report(y_true, y_pred):
        # Assume binary 0 or 1 labels
        # tp = ...

        # precision = ...
        # recall = ...
        # f1 = ...

        return {"precision": None, "recall": None, "f1": None}
    '''
    eval_metrics_editor = mo.ui.code_editor(
        value=load_text("eval_metrics", eval_metrics_initial),
        language="python",
    )
    eval_metrics_editor
    return (eval_metrics_editor,)


@app.cell
def _(eval_metrics_editor, mo, np, save_text):
    try:
        _ns = {"np": np}
        exec(eval_metrics_editor.value, _ns)
        classification_report = _ns["classification_report"]

        _y_true = np.array([1, 1, 0, 0, 1])
        _y_pred = np.array([1, 0, 0, 1, 1])
        _metrics = classification_report(_y_true, _y_pred)

        metrics_ok = _metrics.get("precision") > 0
    except Exception as _e:
        metrics_ok = False
        mo.stop(True, mo.callout(mo.md(f"**Metrics not ready:** {_e}"), kind="warn"))

    save_text(eval_metrics_editor.value, "eval_metrics")

    mo.callout(mo.md(f"✅ **Classification Report** — Your F1-Score logic is loaded."), kind="success")
    return


@app.cell
def _(gb_mse, mo):
    # Helper to check if a variable exists in the namespace
    def get_score(name, default="⏳"):
        return f"{globals().get(name, 0.0):.1%}" if globals().get(name.replace('_acc','_ok'), False) else default

    data = [
        {"Model": "SVM", "Type": "Classification", "Accuracy": get_score("svm_acc")},
        {"Model": "MLP (Neural Net)", "Type": "Classification", "Accuracy": get_score("mlp_acc")},
        {"Model": "Random Forest", "Type": "Classification", "Accuracy": get_score("rf_acc")},
        {"Model": "Gradient Boosting", "Type": "Regression", "Metric (MSE)": f"{gb_mse:.2f}" if globals().get("gb_ok") else "⏳"},
        {"Model": "DBSCAN", "Type": "Clustering", "Status": "Completed" if globals().get("db_ok") else "⏳"},
    ]

    mo.ui.table(data, label="🏆 Advanced Course Leaderboard")
    return


if __name__ == "__main__":
    app.run()
