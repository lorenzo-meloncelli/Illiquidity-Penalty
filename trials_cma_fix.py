
#%%
"""
============================================================
CHECKPOINT 1 — Asset Class Data
============================================================
Asset classes:
  MM_US          — Money Market USD
  GLOB_AGG       — Global Aggregate (hedged USD)
  GLOB_EQ_USD    — Global Equity USD
  HF_FOF         — Hedge Funds (Fund of Funds)
  GLOB_RE        — Global Real Estate (ex USD)
  GLOB_PE        — Global Private Equity (ex USD)

Illiquidity scores mapped to [0,1]:
  l_i = (score_i - min_score) / (max_score - min_score)
  min_score = 1  (MM_US)
  max_score = 4  (GLOB_PE)
============================================================
"""

import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# 1. ASSET CLASS PARAMETERS
# ============================================================

asset_names = [
    'MM_US',
    'GLOB_AGG',
    'GLOB_EQ',
    'HF_FOF',
    'GLOB_RE',
    'GLOB_PE',
]

# Expected real annual returns
mu = np.array([0.0324, 0.0459, 0.0709, 0.0518, 0.0548, 0.0980])

# Annual volatilities
sigma = np.array([0.0182, 0.0439, 0.1701, 0.0728, 0.1251, 0.2000])

# Raw illiquidity scores (1 = most liquid, 4 = most illiquid)
scores_raw = np.array([1.00, 1.45, 1.50, 2.50, 3.00, 5.00])

# Normalise to [0, 1]:  l_i = (score_i - min) / (max - min)
score_min = scores_raw.min()   # = 1.0
score_max = 5
l = (scores_raw - score_min) / (score_max - score_min)

# Correlation matrix
corr = np.array([
    [ 1.000000,  0.140529, -0.009157, -0.011059, -0.006829, -0.011961],
    [ 0.140529,  1.000000, -0.012748, -0.034921,  0.047667, -0.063755],
    [-0.009157, -0.012748,  1.000000,  0.859623,  0.509240,  0.873998],
    [-0.011059, -0.034921,  0.859623,  1.000000,  0.549894,  0.869733],
    [-0.006829,  0.047667,  0.509240,  0.549894,  1.000000,  0.642841],
    [-0.011961, -0.063755,  0.873998,  0.869733,  0.642841,  1.000000],
])

# Covariance matrix
Sigma = np.outer(sigma, sigma) * corr

n = len(mu)

# ============================================================
# 2. PRINT SUMMARY TABLE
# ============================================================

print("=" * 75)
print("  ASSET CLASS INPUTS")
print("=" * 75)
print(f"  {'Asset':<14} {'E[r]':>8} {'Sigma':>8} "
      f"{'Score':>7} {'l_i':>8}  {'Liquidity Tag'}")
print("-" * 75)

tags = [
    'Most liquid',
    'Near-liquid',
    'Semi-liquid',
    'Semi-illiquid',
    'Illiquid',
    'Most illiquid',
]

for i in range(n):
    print(f"  {asset_names[i]:<14} {mu[i]:>8.2%} {sigma[i]:>8.2%} "
          f"{scores_raw[i]:>7.2f} {l[i]:>8.2f}  {tags[i]}")
print("=" * 75)

print(f"\n  Normalisation: l_i = (score_i - {score_min:.0f}) / "
      f"({score_max:.0f} - {score_min:.0f})")
print(f"  -> MM_US  (score={score_min:.0f}) maps to l=0.00  (perfectly liquid)")
print(f"  -> GLOB_PE (score={score_max:.0f}) maps to l=1.00  (fully illiquid)")

print("\nCovariance matrix (Sigma):")
print(np.round(Sigma, 5))

# ============================================================
# 3. VISUALISATION — 3-panel figure
# ============================================================

fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle("Asset Class Overview", fontsize=14, fontweight='bold')

colors = ['#264653', '#2A9D8F', '#E9C46A', '#F4A261', '#E76F51', '#9B2226']

# ── Panel A: Risk-Return scatter ──────────────────────────
ax = axes[0]
for i in range(n):
    ax.scatter(sigma[i] * 100, mu[i] * 100,
               s=200 + l[i] * 600,
               color=colors[i], zorder=3,
               edgecolors='white', linewidths=1.2)
    ax.annotate(asset_names[i],
                xy=(sigma[i] * 100, mu[i] * 100),
                xytext=(6, 4), textcoords='offset points', fontsize=8.5)

ax.set_xlabel("Volatility (%)", fontsize=11)
ax.set_ylabel("Expected Return (%)", fontsize=11)
ax.set_title("Risk–Return Space\n(bubble size = illiquidity)", fontsize=10)
ax.grid(True, alpha=0.3)

# ── Panel B: Illiquidity indices bar chart ────────────────
ax = axes[1]
bars = ax.bar(asset_names, l, color=colors,
              edgecolor='white', linewidth=1.2)
ax.set_ylabel("Illiquidity Index  $l_i$", fontsize=11)
ax.set_title("Illiquidity Indices  $l_i$", fontsize=10)
ax.set_ylim(0, 1.15)
ax.set_xticklabels(asset_names, rotation=20, ha='right', fontsize=9)
ax.grid(True, axis='y', alpha=0.3)

for bar, val in zip(bars, l):
    ax.text(bar.get_x() + bar.get_width() / 2, val + 0.02,
            f"{val:.2f}", ha='center', va='bottom',
            fontsize=9, fontweight='bold')

ax.axhspan(0.00, 0.20, alpha=0.08, color='green',  label='Liquid zone')
ax.axhspan(0.20, 0.50, alpha=0.08, color='orange', label='Semi-illiquid')
ax.axhspan(0.50, 1.15, alpha=0.08, color='red',    label='Illiquid zone')
ax.legend(fontsize=8, loc='upper left')

# ── Panel C: Correlation heatmap ──────────────────────────
ax = axes[2]
im = ax.imshow(corr, cmap='RdYlGn_r', vmin=-1, vmax=1, aspect='auto')
plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
ax.set_xticks(range(n))
ax.set_yticks(range(n))
short_names = ['MM', 'AGG', 'EQ', 'HF', 'RE', 'PE']
ax.set_xticklabels(short_names, fontsize=9)
ax.set_yticklabels(short_names, fontsize=9)
ax.set_title("Correlation Matrix", fontsize=10)

for i in range(n):
    for j in range(n):
        ax.text(j, i, f"{corr[i, j]:.2f}",
                ha='center', va='center', fontsize=7.5,
                color='black' if abs(corr[i, j]) < 0.7 else 'white')

plt.tight_layout()
plt.savefig('Asset Class Overview CMA.png', dpi=150, bbox_inches='tight')
plt.show()


#%%
"""
============================================================
CHECKPOINT 2 — Marginal Penalty Curves
============================================================
Implements and visualises the three penalty functions:
  - Exponential:  c(L) = A * exp(b*L)
  - Power:        c(L) = alpha * L^beta
  - Quadratic:    c(L) = alpha*L + beta*L^2

For each curve, also computes:
  - T(L)  = accumulated penalty (integral of c)
  - T(L)/L = average penalty per unit of illiquidity
  - d/dL [T(L)/L] = sensitivity of adjusted returns to L
    --> this is the key stability diagnostic

============================================================
"""

# ============================================================
# PENALTY FUNCTIONS  c(L)  and  T(L)
# ============================================================

def c_exp(L, alpha=0.05, beta=1.6):
    """Exponential marginal penalty."""
    return alpha * np.exp(beta * L)

def T_exp(L, alpha=0.05, beta=1.6):
    """Accumulated penalty: integral of c_exp from 0 to L."""
    return (alpha / beta) * (np.exp(beta * L) - 1.0)

def c_power(L, alpha=0.05, beta=1.6):
    """Power marginal penalty."""
    return alpha * np.maximum(L, 1e-10) ** beta

def T_power(L, alpha=0.05, beta=1.6):
    """Accumulated penalty: integral of c_power from 0 to L."""
    return (alpha / (beta + 1.0)) * np.maximum(L, 1e-10) ** (beta + 1.0)

def c_quadratic(L, alpha=0.05, beta=1.6):
    """Quadratic marginal penalty."""
    return alpha * L + beta * L ** 2

def T_quadratic(L, alpha=0.05, beta=1.6):
    """Accumulated penalty: integral of c_quadratic from 0 to L."""
    return (alpha / 2.0) * L ** 2 + (beta / 3.0) * L ** 3

# Average penalty per unit illiquidity:  T(L) / L
def avg_penalty(T_fn, L):
    """T(L)/L — used to compute illiquidity-adjusted returns."""
    L = np.maximum(L, 1e-10)
    return T_fn(L) / L

# Sensitivity of adjusted returns to a change in L
# d/dL [ T(L)/L ]  via finite differences
def sensitivity(T_fn, L, eps=1e-6):
    """Numerical derivative of T(L)/L with respect to L."""
    L = np.maximum(L, 1e-10)
    return (avg_penalty(T_fn, L + eps) - avg_penalty(T_fn, L - eps)) / (2 * eps)

# ============================================================
# NUMERICAL SUMMARY AT KEY ILLIQUIDITY LEVELS
# ============================================================

key_levels = [0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70]

curve_specs = [
    ('Exponential', c_exp,       T_exp,       '#E63946'),
    ('Power',       c_power,     T_power,     '#457B9D'),
    ('Quadratic',   c_quadratic, T_quadratic, '#2A9D8F'),
]

print("\n" + "=" * 72)
print("  CHECKPOINT 2 — Penalty Curve Values at Key Illiquidity Levels")
print("=" * 72)

for label, c_fn, T_fn, _ in curve_specs:
    print(f"\n  {label}")
    print(f"  {'L':>6}  {'c(L)':>8}  {'T(L)':>8}  {'T(L)/L':>8}  {'d/dL[T/L]':>12}  {'Adj.ret impact (l=0.95)':>24}")
    print("  " + "-" * 68)
    for Lv in key_levels:
        c_val  = c_fn(Lv)
        T_val  = T_fn(Lv)
        avg    = avg_penalty(T_fn, Lv)
        sens   = sensitivity(T_fn, Lv)
        impact = 0.95 * avg          # adjusted return reduction for PE (l=0.95)
        print(f"  {Lv:>6.0%}  {c_val:>8.3%}  {T_val:>8.3%}  {avg:>8.3%}  {sens:>12.4f}  {impact:>24.3%}")

print("\n  NOTE: 'd/dL[T/L]' is the key stability metric.")
print("  Large values => small changes in w cause large swings in adjusted returns.")

# ============================================================
# STABILITY DIAGNOSTIC: sensitivity to cash weight
# ============================================================
# If w_cash changes by delta_w, L changes by delta_w * l_cash ~ 0
# but the adjusted return of asset i changes by:
#   delta_mu_hat_i = -l_i * d/dL[T(L)/L] * l_cash * delta_w
# With l_cash = 0 this is zero by construction for all curves.
# The real risk is with near-liquid assets (l ~ 0.05).
# We show the impact of a 1% shift in w_PublicEquity (l=0.05) at L=0.45

print("\n" + "=" * 72)
print("  STABILITY TEST: impact on mu_hat_PE of +1% Public Equity weight")
print("  (Public Equity l=0.05, Private Equity l=0.95, baseline L=0.45)")
print("=" * 72)
L_base   = 0.45
delta_w  = 0.01
l_pe_pub = 0.05    # public equity illiquidity
l_pe_prv = 0.95    # private equity illiquidity

print(f"\n  {'Curve':<14}  {'sens d/dL[T/L]':>16}  {'delta mu_hat_PubEq':>20}  {'delta mu_hat_PrvEq':>20}")
print("  " + "-" * 72)
for label, _, T_fn, _ in curve_specs:
    sens   = sensitivity(T_fn, L_base)
    dmu_pub = -l_pe_pub * sens * l_pe_pub * delta_w
    dmu_prv = -l_pe_prv * sens * l_pe_pub * delta_w
    print(f"  {label:<14}  {sens:>16.4f}  {dmu_pub:>20.6%}  {dmu_prv:>20.6%}")

# ============================================================
# VISUALISATION  —  4-panel figure
# ============================================================

L_grid = np.linspace(0.001, 0.85, 400)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Penalty Curves: Shape, Accumulated Cost & Stability",
             fontsize=13, fontweight='bold')

ax1 = axes[0, 0]   # c(L)
ax2 = axes[0, 1]   # T(L)
ax3 = axes[1, 0]   # T(L)/L  — average cost
ax4 = axes[1, 1]   # d/dL[T(L)/L]  — stability diagnostic

for label, c_fn, T_fn, col in curve_specs:
    c_vals   = c_fn(L_grid)
    T_vals   = T_fn(L_grid)
    avg_vals = avg_penalty(T_fn, L_grid)
    sens_vals = sensitivity(T_fn, L_grid)

    ax1.plot(L_grid * 100, c_vals  * 100, label=label, color=col, lw=2.2)
    ax2.plot(L_grid * 100, T_vals  * 100, label=label, color=col, lw=2.2)
    ax3.plot(L_grid * 100, avg_vals * 100, label=label, color=col, lw=2.2)
    ax4.plot(L_grid * 100, sens_vals,      label=label, color=col, lw=2.2)

# Reference lines
ax1.axvline(45, color='grey', lw=1.2, ls=':', alpha=0.7, label='L=45% ref.')
ax3.axvline(45, color='grey', lw=1.2, ls=':', alpha=0.7, label='L=45% ref.')

for ax, title, ylabel in [
    (ax1, "Marginal Penalty  c(L)",               "c(L) (%)"),
    (ax2, "Accumulated Penalty  T(L)",             "T(L) (%)"),
    (ax3, "Average Cost  T(L)/L",                  "T(L)/L (%)"),
    (ax4, "Stability Diagnostic  d/dL [ T(L)/L ]", "d/dL [T/L]"),
]:
    ax.set_title(title, fontsize=10)
    ax.set_xlabel("Portfolio Illiquidity Level L (%)", fontsize=10)
    ax.set_ylabel(ylabel, fontsize=10)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 85)

# Highlight instability region on diagnostic plot
ax4.axhspan(0, 0.5,  alpha=0.07, color='green',  label='Stable zone')
ax4.axhspan(0.5, 2.0, alpha=0.07, color='orange', label='Caution zone')
ax4.axhspan(2.0, ax4.get_ylim()[1] if ax4.get_ylim()[1] > 2 else 20,
            alpha=0.07, color='red', label='Unstable zone')
ax4.set_ylim(bottom=0)
ax4.legend(fontsize=8)

plt.tight_layout()
plt.savefig('Penalty curves.png', dpi=150, bbox_inches='tight')
plt.show()

#%%
"""
============================================================
CHECKPOINT 3 — Penalized MVO with SLSQP + Multistart
============================================================
- Optimizer: scipy SLSQP with 20 random restarts per gamma
- Builds efficient frontiers for:
    Unpenalized, Exponential, Power, Quadratic penalty
- Figures:
    1. Efficient Frontiers + Illiquidity Level
    2. Net Return Frontiers (mu_P - T(L))
    3. Portfolio Composition (stacked area, 4 panels)
    4. Illiquidity Surplus
============================================================
"""

from scipy.optimize import minimize

# ============================================================
# 1.  OPTIMIZER
# ============================================================

def portfolio_variance(w, Sigma):
    return float(w @ Sigma @ w)

def portfolio_return(w, mu):
    return float(w @ mu)

def portfolio_illiquidity(w, l):
    return float(w @ l)

def mvo_penalty_objective(w, gamma, mu, Sigma, T_fn, l):
    L       = float(w @ l)
    penalty = T_fn(L) if L > 1e-10 else 0.0
    return -(float(w @ mu) - 0.5 * gamma * float(w @ Sigma @ w) - penalty)

def mvo_gradient(w, gamma, mu, Sigma, T_fn, l, eps=1e-7):
    w  = np.asarray(w, dtype=float)
    L  = float(w @ l)
    L_ = max(L, 1e-10)
    cL = (T_fn(L_ + eps) - T_fn(L_ - eps)) / (2 * eps)
    grad_f = mu - gamma * (Sigma @ w) - cL * l
    return -grad_f

def optimize_portfolio(gamma, mu, Sigma, T_fn, l, n_restarts=20, seed=0):
    n_assets = len(mu)
    rng      = np.random.default_rng(seed)
    constraints = {'type': 'eq', 'fun': lambda w: np.sum(w) - 1.0}
    bounds      = [(0.0, 1.0)] * n_assets
    best_w, best_val = None, np.inf

    for _ in range(n_restarts):
        w0  = rng.dirichlet(np.ones(n_assets))
        res = minimize(
            fun         = mvo_penalty_objective,
            x0          = w0,
            args        = (gamma, mu, Sigma, T_fn, l),
            jac         = mvo_gradient,
            method      = 'SLSQP',
            bounds      = bounds,
            constraints = constraints,
            options     = {'ftol': 1e-12, 'maxiter': 1000, 'disp': False}
        )
        if res.success and res.fun < best_val:
            best_val = res.fun
            best_w   = res.x.copy()

    if best_w is None:
        best_w = np.ones(n_assets) / n_assets
    best_w = np.maximum(best_w, 0.0)
    best_w /= best_w.sum()
    return best_w

# ============================================================
# 2.  ILLIQUIDITY SURPLUS
# ============================================================

def illiquidity_surplus(w, l, c_fn, T_fn):
    """S(w) = c(L)*L - T(L)"""
    L = float(w @ l)
    if L < 1e-10:
        return 0.0
    return float(c_fn(L) * L - T_fn(L))

# ============================================================
# 3.  BUILD EFFICIENT FRONTIERS
# ============================================================

def T_none(L):
    return 0.0

def c_none(L):
    return 0.0

gamma_grid = np.concatenate([
    np.linspace(0.05, 0.5,  10),
    np.linspace(0.5,  3.0,  20),
    np.linspace(3.0,  10.0, 16),
    np.linspace(10.0, 40.0, 10),
    np.linspace(40.0, 50.0, 50),
])

frontier_specs = [
    ('Unpenalized', c_none,      T_none,       '#333333', '--'),
    ('Exponential', c_exp,       T_exp,        '#E63946', '-' ),
    ('Power',       c_power,     T_power,      '#457B9D', '-' ),
    ('Quadratic',   c_quadratic, T_quadratic,  '#2A9D8F', '-' ),
]

print("=" * 65)
print("  CHECKPOINT 3 — SLSQP Optimizer")
print(f"  n_restarts=20  |  gamma points={len(gamma_grid)}")
print("=" * 65)

results = {}

for label, c_fn, T_fn, col, ls in frontier_specs:
    rets, vols, illiqs, surpluses, weights_list, rets_net = [], [], [], [], [], []

    for k, gamma in enumerate(gamma_grid):
        w   = optimize_portfolio(gamma, mu, Sigma, T_fn, l,
                                 n_restarts=20, seed=k)
        r   = portfolio_return(w, mu)
        v   = np.sqrt(portfolio_variance(w, Sigma))
        lq  = portfolio_illiquidity(w, l)
        s   = illiquidity_surplus(w, l, c_fn, T_fn)
        L   = float(w @ l)
        r_net = r - (T_fn(L) if L > 1e-10 else 0.0)

        rets.append(r);       vols.append(v)
        illiqs.append(lq);    surpluses.append(s)
        weights_list.append(w); rets_net.append(r_net)

    results[label] = {
        'rets':      np.array(rets),
        'rets_net':  np.array(rets_net),
        'vols':      np.array(vols),
        'illiqs':    np.array(illiqs),
        'surpluses': np.array(surpluses),
        'weights':   np.array(weights_list),
        'color':     col,
        'ls':        ls,
    }
    print(f"  {label:<14} done  |"
          f"  ret  [{min(rets):.2%}, {max(rets):.2%}]"
          f"  |  illiq [{min(illiqs):.2%}, {max(illiqs):.2%}]")

print("\n  All frontiers computed.")

# ============================================================
# 4.  PRINT PORTFOLIO SNAPSHOTS
# ============================================================

target_rets = [0.05, 0.065, 0.08]

print("\n" + "=" * 90)
print("  PORTFOLIO COMPOSITION AT SELECTED RETURN TARGETS")
print("=" * 90)

for label, info in results.items():
    print(f"\n  ── {label} ──")
    print(f"  {'Target':>8}  " +
          "  ".join(f"{a[:10]:>10}" for a in asset_names) +
          f"  {'L':>6}  {'Surplus':>8}  {'Net ret':>8}")
    print("  " + "-" * 100)
    for tgt in target_rets:
        idx  = np.argmin(np.abs(info['rets'] - tgt))
        w    = info['weights'][idx]
        lq   = info['illiqs'][idx]
        s    = info['surpluses'][idx]
        rnet = info['rets_net'][idx]
        row  = "  ".join(f"{wi:>10.1%}" for wi in w)
        print(f"  {tgt:>8.1%}  {row}  {lq:>6.1%}  {s:>8.3%}  {rnet:>8.3%}")

# ============================================================
# 5.  VISUALISATION
# ============================================================

comp_colors = ['#264653', '#2A9D8F', '#E9C46A', '#F4A261', '#E76F51', '#9B2226']

# ── FIGURE 1: Efficient Frontiers + Illiquidity Level ──────

fig1, (ax_front, ax_illiq) = plt.subplots(1, 2, figsize=(16, 6))
fig1.suptitle("Efficient Frontiers & Illiquidity Level",
              fontsize=13, fontweight='bold')

for label, info in results.items():
    ax_front.plot(info['vols'] * 100, info['rets'] * 100,
                  label=label, color=info['color'],
                  ls=info['ls'], lw=2.2)

ax_front.set_xlabel("Volatility (%)", fontsize=11)
ax_front.set_ylabel("Expected Return (%)", fontsize=11)
ax_front.set_title("Efficient Frontiers", fontsize=11)
ax_front.legend(fontsize=10)
ax_front.grid(True, alpha=0.3)

for label, info in results.items():
    ax_illiq.plot(info['rets'] * 100, info['illiqs'] * 100,
                  label=label, color=info['color'],
                  ls=info['ls'], lw=2.2)

ax_illiq.set_xlabel("Portfolio Expected Return (%)", fontsize=11)
ax_illiq.set_ylabel("Portfolio Illiquidity Level L (%)", fontsize=11)
ax_illiq.set_title("Illiquidity Level along the Frontier", fontsize=11)
ax_illiq.legend(fontsize=10)
ax_illiq.grid(True, alpha=0.3)
ax_illiq.axhline(50, color='grey', lw=1.0, ls=':', alpha=0.6)

plt.tight_layout()
plt.savefig('Frontiers.png', dpi=150, bbox_inches='tight')
plt.show()

# ── FIGURE 2: Net Return Frontiers ─────────────────────────

fig2, ax_net = plt.subplots(figsize=(10, 6))
fig2.suptitle("Efficient Frontiers — Liquidity-Adjusted Net Return",
              fontsize=13, fontweight='bold')

for label, info in results.items():
    ax_net.plot(info['vols'] * 100, info['rets_net'] * 100,
                label=label, color=info['color'],
                ls=info['ls'], lw=2.2)

ax_net.set_xlabel("Volatility (%)", fontsize=11)
ax_net.set_ylabel(r"Net Return  $\hat{\mu}_P = \mu_P - T(L)$  (%)", fontsize=11)
ax_net.set_title("Net Return after Illiquidity Penalty", fontsize=11)
ax_net.legend(fontsize=10)
ax_net.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('Frontiers_net.png', dpi=150, bbox_inches='tight')
plt.show()

# ── FIGURE 3: Portfolio Composition ────────────────────────

fig3, area_axes = plt.subplots(2, 2, figsize=(16, 11))
fig3.suptitle("Portfolio Composition along the Frontier",
              fontsize=13, fontweight='bold')

area_axes_flat = [area_axes[0,0], area_axes[0,1],
                  area_axes[1,0], area_axes[1,1]]

for ax_a, (label, info) in zip(area_axes_flat, results.items()):
    sort_idx = np.argsort(info['rets'])
    x_vals   = info['rets'][sort_idx] * 100
    W_sorted = info['weights'][sort_idx]

    bottom = np.zeros(len(x_vals))
    for j in range(n):
        vals = W_sorted[:, j]
        ax_a.fill_between(x_vals, bottom, bottom + vals,
                          color=comp_colors[j], alpha=0.88,
                          label=asset_names[j])
        ax_a.plot(x_vals, bottom + vals,
                  color='white', lw=0.4, alpha=0.6)
        bottom += vals

    ax_a.set_title(label, fontsize=11, fontweight='bold',
                   color=info['color'])
    ax_a.set_xlabel("Expected Return (%)", fontsize=10)
    ax_a.set_ylabel("Portfolio Weight", fontsize=10)
    ax_a.set_ylim(0, 1.0)
    ax_a.set_xlim(x_vals.min(), x_vals.max())
    ax_a.grid(True, alpha=0.2)
    ax_a.tick_params(labelsize=9)

handles = [plt.Rectangle((0, 0), 1, 1,
                          color=comp_colors[j], alpha=0.88)
           for j in range(n)]
fig3.legend(handles, asset_names,
            loc='lower center', ncol=6,
            fontsize=10, frameon=True,
            bbox_to_anchor=(0.5, -0.02))

plt.tight_layout(rect=[0, 0.04, 1, 1])
plt.savefig('Composition.png', dpi=150, bbox_inches='tight')
plt.show()

# ── FIGURE 4: Illiquidity Surplus ───────────────────────────

fig4, ax_surplus = plt.subplots(figsize=(10, 6))
fig4.suptitle("Illiquidity Surplus  S(w) = c(L)·L − T(L)",
              fontsize=13, fontweight='bold')

for label, info in results.items():
    if label == 'Unpenalized':
        continue
    ax_surplus.plot(info['rets'] * 100, info['surpluses'] * 100,
                    label=label, color=info['color'],
                    ls=info['ls'], lw=2.4)

ax_surplus.set_xlabel("Portfolio Expected Return (%)", fontsize=11)
ax_surplus.set_ylabel("Illiquidity Surplus (%)", fontsize=11)
ax_surplus.legend(fontsize=11)
ax_surplus.grid(True, alpha=0.3)
ax_surplus.axhline(0, color='grey', lw=1.0, ls='-', alpha=0.4)
ax_surplus.set_ylim(bottom=0)

plt.tight_layout()
plt.savefig('Surplus.png', dpi=150, bbox_inches='tight')
plt.show()

# %%

# Snippet per visualizzare come varia la Power-fuction 
# per diversi valori di alpha e beta

'''
import numpy as np
import matplotlib.pyplot as plt

alpha, beta = 0.25, 1.4
L_vals = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6])
c_vals = alpha * L_vals**beta

plt.figure(figsize=(8, 5))
plt.plot(L_vals * 100, c_vals * 100, 'o-', color='#264653', lw=2, markersize=8)
for L, c in zip(L_vals, c_vals):
    plt.annotate(f"{c*100:.2f}%", xy=(L*100, c*100),
                 xytext=(4, 6), textcoords='offset points', fontsize=10)

plt.xlabel("Portfolio Illiquidity Level L (%)", fontsize=11)
plt.ylabel("Marginal Penalty c(L) (%)", fontsize=11)
plt.title(r"Power Penalty — Fondo Pensione ($\alpha=0.25$, $\beta=1.2$)", fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
'''


#%%
"""
============================================================
CHECKPOINT 4 — Power Penalty: Investor Archetypes
============================================================
Compares the Power penalty curve across three investor types:
  - Fondo Pensione Complementare  (alpha=0.25, beta=1.2)
  - Endowment Universitario       (alpha=0.12, beta=2.0)
  - Family Office                 (alpha=0.06, beta=2.8)

For each archetype:
  - Efficient frontier (gross returns)
  - Portfolio composition (stacked area chart)
============================================================
"""

# ============================================================
# 1.  ARCHETYPE PENALTY FUNCTIONS
# ============================================================

def c_pension(L):
    return 0.25 * np.maximum(L, 1e-10) ** 1.2

def T_pension(L):
    return (0.25 / 2.2) * np.maximum(L, 1e-10) ** 2.2

def c_endowment(L):
    return 0.12 * np.maximum(L, 1e-10) ** 2.0

def T_endowment(L):
    return (0.12 / 3.0) * np.maximum(L, 1e-10) ** 3.0

def c_family(L):
    return 0.06 * np.maximum(L, 1e-10) ** 2.8

def T_family(L):
    return (0.06 / 3.8) * np.maximum(L, 1e-10) ** 3.8

# ============================================================
# 2.  PRINT PENALTY VALUES AT KEY ILLIQUIDITY LEVELS
# ============================================================

key_levels = [0.10, 0.20, 0.30, 0.40, 0.50, 0.60]

archetype_specs = [
    ('Fondo Pensione', c_pension,   T_pension,   '#E63946', '-'),
    ('Endowment',      c_endowment, T_endowment, '#457B9D', '-'),
    ('Family Office',  c_family,    T_family,    '#2A9D8F', '-'),
]

print("=" * 65)
print("  CHECKPOINT 4 — Power Penalty by Investor Archetype")
print("=" * 65)

print(f"\n  {'L':>6}  " +
      "  ".join(f"{'c(L) '+label:>16}" for label, *_ in archetype_specs))
print("  " + "-" * 60)
for Lv in key_levels:
    row = f"  {Lv:>6.0%}  "
    for label, c_fn, T_fn, col, ls in archetype_specs:
        row += f"{c_fn(Lv)*100:>16.2f}%  "
    print(row)

# ============================================================
# 3.  BUILD FRONTIERS FOR EACH ARCHETYPE
# ============================================================

print("\n" + "=" * 65)
print("  Computing frontiers...")
print("=" * 65)

archetype_results = {}

for label, c_fn, T_fn, col, ls in archetype_specs:
    rets, vols, illiqs, surpluses, weights_list = [], [], [], [], []

    for k, gamma in enumerate(gamma_grid):
        w  = optimize_portfolio(gamma, mu, Sigma, T_fn, l,
                                n_restarts=20, seed=k)
        r  = portfolio_return(w, mu)
        v  = np.sqrt(portfolio_variance(w, Sigma))
        lq = portfolio_illiquidity(w, l)
        s  = illiquidity_surplus(w, l, c_fn, T_fn)

        rets.append(r);    vols.append(v)
        illiqs.append(lq); surpluses.append(s)
        weights_list.append(w)

    archetype_results[label] = {
        'rets':      np.array(rets),
        'vols':      np.array(vols),
        'illiqs':    np.array(illiqs),
        'surpluses': np.array(surpluses),
        'weights':   np.array(weights_list),
        'color':     col,
        'ls':        ls,
    }
    print(f"  {label:<22} done  |"
          f"  ret  [{min(rets):.2%}, {max(rets):.2%}]"
          f"  |  illiq [{min(illiqs):.2%}, {max(illiqs):.2%}]")

print("\n  All archetype frontiers computed.")

# ============================================================
# 4.  PRINT PORTFOLIO SNAPSHOTS
# ============================================================

target_rets = [0.05, 0.065, 0.08]

print("\n" + "=" * 90)
print("  PORTFOLIO COMPOSITION AT SELECTED RETURN TARGETS")
print("=" * 90)

for label, info in archetype_results.items():
    print(f"\n  ── {label} ──")
    print(f"  {'Target':>8}  " +
          "  ".join(f"{a[:10]:>10}" for a in asset_names) +
          f"  {'L':>6}  {'Surplus':>8}")
    print("  " + "-" * 100)
    for tgt in target_rets:
        idx = np.argmin(np.abs(info['rets'] - tgt))
        w   = info['weights'][idx]
        lq  = info['illiqs'][idx]
        s   = info['surpluses'][idx]
        row = "  ".join(f"{wi:>10.1%}" for wi in w)
        print(f"  {tgt:>8.1%}  {row}  {lq:>6.1%}  {s:>8.3%}")

# ============================================================
# 5.  VISUALISATION
# ============================================================

comp_colors = ['#264653', '#2A9D8F', '#E9C46A', '#F4A261', '#E76F51', '#9B2226']

# ── FIGURE A: Penalty curves ────────────────────────────────

L_grid_plot = np.linspace(0.001, 0.75, 300)

figA, ax_c = plt.subplots(figsize=(10, 6))
figA.suptitle("Power Penalty Curves by Investor Archetype",
              fontsize=13, fontweight='bold')

for label, c_fn, T_fn, col, ls in archetype_specs:
    ax_c.plot(L_grid_plot * 100, c_fn(L_grid_plot) * 100,
              label=label, color=col, lw=2.4)

ax_c.set_xlabel("Portfolio Illiquidity Level L (%)", fontsize=11)
ax_c.set_ylabel("Marginal Penalty c(L) (%)", fontsize=11)
ax_c.legend(fontsize=11)
ax_c.grid(True, alpha=0.3)
ax_c.set_xlim(0, 75)

plt.tight_layout()
plt.savefig('Power_penalty_curves.png', dpi=150, bbox_inches='tight')
plt.show()

# ── FIGURE B: Efficient Frontiers ───────────────────────────

figB, ax_front = plt.subplots(figsize=(10, 6))
figB.suptitle("Efficient Frontiers by Investor Archetype",
              fontsize=13, fontweight='bold')

ax_front.plot(results['Unpenalized']['vols'] * 100,
              results['Unpenalized']['rets'] * 100,
              label='Unpenalized', color='#333333',
              ls='--', lw=1.8, alpha=0.6)

for label, info in archetype_results.items():
    ax_front.plot(info['vols'] * 100, info['rets'] * 100,
                  label=label, color=info['color'],
                  ls=info['ls'], lw=2.2)

ax_front.set_xlabel("Volatility (%)", fontsize=11)
ax_front.set_ylabel("Expected Return (%)", fontsize=11)
ax_front.set_title("Efficient Frontiers", fontsize=11)
ax_front.legend(fontsize=10)
ax_front.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('Power_frontiers.png', dpi=150, bbox_inches='tight')
plt.show()

# ── FIGURE C: Portfolio Composition ─────────────────────────

figC, area_axes = plt.subplots(1, 3, figsize=(18, 6))
figC.suptitle("Portfolio Composition by Investor Archetype",
              fontsize=13, fontweight='bold')

for ax_a, (label, info) in zip(area_axes, archetype_results.items()):
    sort_idx = np.argsort(info['rets'])
    x_vals   = info['rets'][sort_idx] * 100
    W_sorted = info['weights'][sort_idx]

    bottom = np.zeros(len(x_vals))
    for j in range(n):
        vals = W_sorted[:, j]
        ax_a.fill_between(x_vals, bottom, bottom + vals,
                          color=comp_colors[j], alpha=0.88,
                          label=asset_names[j])
        ax_a.plot(x_vals, bottom + vals,
                  color='white', lw=0.4, alpha=0.6)
        bottom += vals

    ax_a.set_title(label, fontsize=11, fontweight='bold',
                   color=info['color'])
    ax_a.set_xlabel("Expected Return (%)", fontsize=10)
    ax_a.set_ylabel("Portfolio Weight", fontsize=10)
    ax_a.set_ylim(0, 1.0)
    ax_a.set_xlim(x_vals.min(), x_vals.max())
    ax_a.grid(True, alpha=0.2)
    ax_a.tick_params(labelsize=9)

handles = [plt.Rectangle((0, 0), 1, 1,
                          color=comp_colors[j], alpha=0.88)
           for j in range(n)]
figC.legend(handles, asset_names,
            loc='lower center', ncol=6,
            fontsize=10, frameon=True,
            bbox_to_anchor=(0.5, -0.04))

plt.tight_layout(rect=[0, 0.06, 1, 1])
plt.savefig('Power_composition.png', dpi=150, bbox_inches='tight')
plt.show()



#%%
"""
============================================================
CHECKPOINT 5 (Part 1) — Setup, Target Portfolios, Tranches
============================================================
IPOTESI C: payout proporzionale da tutti gli asset
  - Liberi: no haircut
  - Locked: haircut specifico, peso ridotto (opzione A)

FIX 2a : restore_liquid_buffer vende prima illiquidi liberi
FIX 2b : restore_liquid_buffer distribuisce proventi su w_target
FIX 4  : alpha_marginal = alpha_est * (beta_est + 1)
============================================================
"""

from scipy.optimize import minimize, curve_fit
import numpy as np

# ============================================================
# 1.  PARAMETERS
# ============================================================
pi       = 0.03
mu_base  = mu.copy()   # stripping OFF — mu lordi

T_years      = 20
N_scen       = 1000
delta        = 0.1 # 10%, 5%, 3% 
gamma_fix    = 5 # 5, 3, 2
w_min_liquid = 0.4 # 40%, 30%, 20% 

haircut_by_asset = np.array([
    0.001,   # MM_US
    0.005,   # GLOB_AGG
    0.02,    # GLOB_EQ_USD
    0.08,    # HF_FOF
    0.12,    # GLOB_RE
    0.20,    # GLOB_PE
])

liquid_mask  = (l <= 0.125)
lockup_years = np.array([0, 0, 0, 2, 5, 8])

L_levels           = np.array([0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.65, 0.70])
L_levels_requested = L_levels.copy()

print("=" * 65)
print("  CHECKPOINT 5 — Parameters")
print("=" * 65)
print(f"  Ipotesi C: payout proporzionale da tutti gli asset")
print(f"  Stripping              : OFF  (mu_base = mu)")
print(f"  pi                     : {pi:.2%}")
print(f"  gamma (fixed)          : {gamma_fix}")
print(f"  Horizon                : {T_years} years")
print(f"  Scenarios              : {N_scen}")
print(f"  Annual payout delta    : {delta:.2%}")
print(f"  Min liquid weight      : {w_min_liquid:.0%}")
print(f"  Liquid mask (l<=0.125) : "
      f"{[asset_names[i] for i in range(n) if liquid_mask[i]]}")
print(f"\n  {'Asset':<14} {'mu':>6} {'l':>6} "
      f"{'lockup':>7} {'haircut':>8}")
print("  " + "-" * 48)
for i in range(n):
    print(f"  {asset_names[i]:<14} {mu[i]:>6.2%} {l[i]:>6.3f} "
          f"{lockup_years[i]:>6}yr {haircut_by_asset[i]:>8.1%}")

# ============================================================
# 2.  CONSTRAINED MVO — one portfolio per L level
# ============================================================

def build_target_portfolio(L_target, gamma, mu_b, Sig, l_vec,
                           liquid_mask, w_min_liq):
    n_assets = len(mu_b)

    def objective(w):
        return -(float(w @ mu_b) - 0.5 * gamma * float(w @ Sig @ w))

    def grad_obj(w):
        return -(mu_b - gamma * (Sig @ w))

    constraints = [
        {'type': 'eq',
         'fun': lambda w: np.sum(w) - 1.0},
        {'type': 'eq',
         'fun': lambda w: float(w @ l_vec) - L_target},
        {'type': 'ineq',
         'fun': lambda w: float(w[liquid_mask].sum()) - w_min_liq},
    ]
    bounds   = [(0.0, 1.0)] * n_assets
    rng_     = np.random.default_rng(42)
    best_w, best_val = None, np.inf

    for _ in range(40):
        w0  = rng_.dirichlet(np.ones(n_assets))
        res = minimize(objective, w0, jac=grad_obj, method='SLSQP',
                       bounds=bounds, constraints=constraints,
                       options={'ftol': 1e-12, 'maxiter': 2000,
                                'disp': False})
        if res.success and res.fun < best_val:
            best_val = res.fun
            best_w   = res.x.copy()

    if best_w is None:
        best_w = np.ones(n_assets) / n_assets
    best_w = np.maximum(best_w, 0.0)
    best_w /= best_w.sum()
    return best_w


target_portfolios = {}
L_levels_valid    = []

print("\n" + "=" * 95)
print(f"  TARGET PORTFOLIOS  (gamma={gamma_fix}, min_liq={w_min_liquid:.0%})")
print("=" * 95)
print(f"  {'L':>5}  " + "  ".join(f"{a[:8]:>8}" for a in asset_names)
      + f"  {'ret':>6}  {'vol':>6}  {'L_chk':>6}  {'liq':>5}  {'status':>8}")
print("  " + "-" * 96)

prev_vol = None

for Lv in L_levels:
    w_tgt = build_target_portfolio(Lv, gamma_fix, mu_base, Sigma, l,
                                   liquid_mask, w_min_liquid)
    ret_  = float(w_tgt @ mu_base)
    vol_  = float(np.sqrt(w_tgt @ Sigma @ w_tgt))
    lck_  = float(w_tgt @ l)
    liq_  = float(w_tgt[liquid_mask].sum())
    row   = "  ".join(f"{wi:>8.1%}" for wi in w_tgt)

    check1 = abs(lck_ - Lv) < 0.02
    check2 = liq_ >= w_min_liquid - 0.01
    check4 = vol_ < prev_vol * 1.5 if prev_vol is not None else True
    valid  = check1 and check2 and check4
    status = '✓ OK' if valid else '✗ SKIP'

    print(f"  {Lv:>5.0%}  {row}  {ret_:>6.2%}  {vol_:>6.2%}"
          f"  {lck_:>6.3f}  {liq_:>5.1%}  {status:>8}")

    if not valid:
        reasons = []
        if not check1:
            reasons.append(f"L_chk={lck_:.3f} != target={Lv:.2f}")
        if not check2:
            reasons.append(f"liq={liq_:.1%} < w_min={w_min_liquid:.0%}")
        if not check4:
            reasons.append(f"vol={vol_:.2%} > 1.5x prev={prev_vol:.2%}")
        print(f"         -> skipped: {', '.join(reasons)}")
    else:
        target_portfolios[Lv] = w_tgt
        L_levels_valid.append(Lv)
        prev_vol = vol_

L_levels = np.array(L_levels_valid)
print(f"\n  Valid L levels : {[f'{L:.0%}' for L in L_levels]}")
print(f"  Total used     : {len(L_levels)} / {len(L_levels_requested)}")

# ============================================================
# 3.  TRANCHE HELPERS
# ============================================================

def init_tranches(w_target, t_now=0):
    return [
        {'asset': i, 'weight': float(w_target[i]), 'bought_at': t_now}
        for i in range(len(w_target)) if w_target[i] > 1e-8
    ]


def locked_weights(tranches, t_now, lku):
    locked = np.zeros(len(lku))
    for tr in tranches:
        if (t_now - tr['bought_at']) < lku[tr['asset']]:
            locked[tr['asset']] += tr['weight']
    return locked


def apply_drift(tranches, r_t):
    for tr in tranches:
        tr['weight'] *= (1.0 + r_t[tr['asset']])
    total = sum(tr['weight'] for tr in tranches)
    for tr in tranches:
        tr['weight'] /= total
    return tranches


def rebalance_constrained(tranches, w_target, t_now, lku, n_assets,
                          liquid_mask, w_min_liq):
    w_locked  = locked_weights(tranches, t_now, lku)
    w_current = np.zeros(n_assets)
    for tr in tranches:
        w_current[tr['asset']] += tr['weight']

    constraints = [
        {'type': 'eq',
         'fun': lambda w: np.sum(w) - 1.0},
        {'type': 'ineq',
         'fun': lambda w: float(w[liquid_mask].sum()) - w_min_liq},
    ]
    bounds = [(float(w_locked[i]), 1.0) for i in range(n_assets)]

    res = minimize(
        fun         = lambda w: np.sum((w - w_target) ** 2),
        x0          = w_current,
        jac         = lambda w: 2.0 * (w - w_target),
        method      = 'SLSQP',
        bounds      = bounds,
        constraints = constraints,
        options     = {'ftol': 1e-12, 'maxiter': 500, 'disp': False}
    )
    w_new = np.maximum(res.x if res.success else w_current, 0.0)
    w_new /= w_new.sum()

    w_unl_old = w_current - w_locked
    w_unl_new = w_new     - w_locked
    new_tranches = []

    for tr in tranches:
        i   = tr['asset']
        age = t_now - tr['bought_at']
        if age < lku[i]:
            new_tranches.append(tr)
        else:
            old_u = w_unl_old[i]
            new_u = w_unl_new[i]
            new_w = tr['weight'] * (new_u / old_u) if old_u > 1e-10 else 0.0
            if new_w > 1e-8:
                new_tranches.append({'asset': i, 'weight': new_w,
                                     'bought_at': tr['bought_at']})

    for i in range(n_assets):
        dw = w_new[i] - w_current[i]
        if dw > 1e-8:
            new_tranches.append({'asset': i, 'weight': dw,
                                 'bought_at': t_now})
    return new_tranches

# ============================================================
# 4.  PAYOUT HANDLER — IPOTESI C
# ============================================================

def handle_payout(tranches, payout, t_now, lku, n_assets, hc_by_asset):
    """
    Payout proporzionale da TUTTI gli asset (Ipotesi C).

    Ogni asset contribuisce al payout in proporzione al suo peso.
      - Liberi:  vendita senza costo, peso ridotto.
      - Locked:  vendita con haircut, peso ridotto (opzione A).
                 gross = quota / (1 - haircut)
                 cost_forced += gross * haircut

    Effetto: i pesi relativi post-payout rimangono vicini
    a w_post_drift. Il payout tilt scompare.
    c_hat misura solo i costi degli haircut sui locked.

    Returns:
        tranches    : lista aggiornata
        cost_forced : costo haircut totale sui locked
    """
    w_total     = sum(tr['weight'] for tr in tranches)
    cost_forced = 0.0

    for tr in tranches:
        i   = tr['asset']
        age = t_now - tr['bought_at']

        # quota proporzionale di questa tranche al payout
        quota = (tr['weight'] / w_total) * payout

        if age >= lku[i]:
            # libero: vendo senza costo
            tr['weight'] -= quota
        else:
            # locked: vendo con haircut (opzione A)
            gross        = quota / (1.0 - hc_by_asset[i])
            cost_forced += gross * hc_by_asset[i]
            tr['weight'] -= gross

    tranches = [tr for tr in tranches if tr['weight'] > 1e-10]
    w_sum    = sum(tr['weight'] for tr in tranches)
    if w_sum > 1e-10:
        for tr in tranches:
            tr['weight'] /= w_sum

    return tranches, cost_forced

# ============================================================
# 5.  RESTORE LIQUID BUFFER — FIX 2a + 2b
# ============================================================

def restore_liquid_buffer(tranches, t_now, lku, n_assets,
                          liquid_mask, w_min_liq, hc_by_asset,
                          w_target):
    """
    Ricostituisce il buffer liquido se scende sotto w_min_liq.

    FIX 2a: vende prima illiquidi LIBERI (no haircut),
            poi illiquidi LOCKED (con haircut).
    FIX 2b: proventi distribuiti su MM/AGG/EQ
            in proporzione a w_target.

    Con payout proporzionale (Ipotesi C) i liquidi scendono
    meno rispetto al codice precedente, quindi il restore
    scatta meno frequentemente. Quando scatta misura
    un costo reale aggiuntivo.
    """
    w_current = np.zeros(n_assets)
    for tr in tranches:
        w_current[tr['asset']] += tr['weight']

    w_liq     = float(w_current[liquid_mask].sum())
    shortfall = w_min_liq - w_liq

    if shortfall <= 1e-6:
        return tranches, 0.0

    w_free_illiq   = np.zeros(n_assets)
    w_locked_illiq = np.zeros(n_assets)

    for tr in tranches:
        i   = tr['asset']
        age = t_now - tr['bought_at']
        if liquid_mask[i]:
            continue
        if age >= lku[i]:
            w_free_illiq[i]   += tr['weight']
        else:
            w_locked_illiq[i] += tr['weight']

    total_free_illiq   = w_free_illiq.sum()
    total_locked_illiq = w_locked_illiq.sum()

    if total_free_illiq + total_locked_illiq < 1e-10:
        return tranches, 0.0

    cost_haircut = 0.0
    need         = shortfall

    # STEP 1: vendo prima i liberi (no haircut)
    if total_free_illiq > 1e-10:
        sell_free = min(need, total_free_illiq)
        frac_free = sell_free / total_free_illiq
        for tr in tranches:
            i   = tr['asset']
            age = t_now - tr['bought_at']
            if not liquid_mask[i] and age >= lku[i]:
                tr['weight'] *= (1.0 - frac_free)
        need -= sell_free

    # STEP 2: poi i locked (con haircut)
    if need > 1e-10 and total_locked_illiq > 1e-10:
        for tr in tranches:
            if need <= 1e-10:
                break
            i   = tr['asset']
            age = t_now - tr['bought_at']
            if liquid_mask[i] or age >= lku[i]:
                continue
            share        = tr['weight'] / total_locked_illiq
            gross        = min(tr['weight'],
                               need * share / (1.0 - hc_by_asset[i]))
            proceeds     = gross * (1.0 - hc_by_asset[i])
            cost_haircut += gross * hc_by_asset[i]
            tr['weight'] -= gross
            need         -= proceeds

    # FIX 2b: proventi proporzionale a w_target dei liquidi
    added       = shortfall - need
    liq_tgt     = w_target[liquid_mask]
    liq_tgt_sum = liq_tgt.sum()

    if added > 1e-10 and liq_tgt_sum > 1e-10:
        for i in np.where(liquid_mask)[0]:
            inc = added * (w_target[i] / liq_tgt_sum)
            if inc > 1e-10:
                found = False
                for tr in tranches:
                    if tr['asset'] == i:
                        tr['weight'] += inc
                        found = True
                        break
                if not found:
                    tranches.append({'asset': i,
                                     'weight': inc,
                                     'bought_at': t_now})

    tranches = [tr for tr in tranches if tr['weight'] > 1e-10]
    w_sum    = sum(tr['weight'] for tr in tranches)
    if w_sum > 1e-10:
        for tr in tranches:
            tr['weight'] /= w_sum

    return tranches, cost_haircut

print("\n  Part 1 complete.")


#%%
"""
============================================================
CHECKPOINT 5 (Part 2) — Simulation, Aggregation & Fitting
============================================================
IPOTESI C: payout proporzionale da tutti gli asset.

BENCHMARK:
  Stesso fondo tutto liquido.
  r_bench = w_bd @ r_t  (post-drift).

COSTO ANNO t:
  cost_t = (r_bench - r_actual)
           + cost_hc
           + cost_forced_payout

FITTING:
  La simulazione produce c_hat(L) ≈ T(L)/L.
  Si calcola T_hat(L) = c_hat(L) * L e si fitta:
    T_hat = A * L^B
  Da cui si ricavano i parametri di c(L) = alpha * L^beta:
    beta  = B - 1
    alpha = A * B
  Questo e' matematicamente equivalente a fittare c_hat
  con correzione FIX 4, ma piu' diretto e trasparente.
============================================================
"""

import matplotlib.pyplot as plt

# ============================================================
# 4.  SINGLE SCENARIO
# ============================================================

def simulate_scenario(w_target, L_target, rng):
    """
    Simula uno scenario di T_years anni con Ipotesi C.

    IPOTESI C: payout proporzionale da tutti gli asset.
      Liberi: no haircut. Locked: haircut, peso ridotto (op. A).

    BENCHMARK: r_bench = w_bd @ r_t  (post-drift).
    r_actual calcolato PRE-rebalancing.
    Rebalancing eseguito DOPO il calcolo del costo.

    Returns:
        float: costo medio annuo su T_years anni
    """
    chol     = np.linalg.cholesky(Sigma)
    tranches = init_tranches(w_target, t_now=0)
    w_bench  = w_target.copy()
    costs    = []

    for t in range(1, T_years + 1):

        # ── A. Rendimenti realizzati ──────────────────────────────────
        r_t = mu_base + chol @ rng.standard_normal(n)

        # ── B. BENCHMARK — post-drift ─────────────────────────────────
        w_bd    = w_bench * (1.0 + r_t)
        w_bd   /= w_bd.sum()
        r_bench = float(w_bd @ r_t)
        w_bench = w_target.copy()

        # ── C1. Portafoglio reale: drift ──────────────────────────────
        tranches = apply_drift(tranches, r_t)

        # ── C2. Payout proporzionale  [IPOTESI C] ─────────────────────
        tranches, cost_forced_payout = handle_payout(
            tranches, delta, t, lockup_years, n, haircut_by_asset)

        # ── C3. Restore buffer  [FIX 2a + 2b] ────────────────────────
        tranches, cost_hc = restore_liquid_buffer(
            tranches, t, lockup_years, n,
            liquid_mask, w_min_liquid, haircut_by_asset,
            w_target)

        # ── D. COSTO — PRE-rebalancing ────────────────────────────────
        w_actual = np.zeros(n)
        for tr in tranches:
            w_actual[tr['asset']] += tr['weight']
        r_actual = float(w_actual @ r_t)

        costs.append((r_bench - r_actual) + cost_hc + cost_forced_payout)

        # ── C4. Rebalancing vincolato — DOPO il costo ─────────────────
        tranches = rebalance_constrained(
            tranches, w_target, t, lockup_years, n,
            liquid_mask, w_min_liquid)

    return float(np.mean(costs))

# ============================================================
# 5.  MAIN SIMULATION LOOP
# ============================================================

print("=" * 65)
print("  CHECKPOINT 5 (Part 2) — Running Simulations")
print("  Ipotesi C: payout proporzionale, r_bench post-drift")
print("=" * 65)

rng_master = np.random.default_rng(0)
c_hat      = {}

for Lv in L_levels:
    w_tgt      = target_portfolios[Lv]
    scen_costs = []
    for s in range(N_scen):
        rng_s = np.random.default_rng(rng_master.integers(0, 2**31))
        scen_costs.append(simulate_scenario(w_tgt, Lv, rng_s))

    c_hat[Lv] = float(np.mean(scen_costs))
    std_err    = float(np.std(scen_costs) / np.sqrt(N_scen))
    print(f"  L={Lv:.0%}  ->  c_hat={c_hat[Lv]*100:.4f}%"
          f"  (std err: {std_err*100:.4f}%,  N={N_scen})")

# ============================================================
# 6.  FITTING  T(L) = A * L^B  ->  ricava alpha e beta
# ============================================================
# La simulazione produce c_hat(L) ≈ T(L)/L.
# T_hat(L) = c_hat(L) * L  e' la stima diretta di T(L).
#
# Fittiamo: T_hat = A * L^B
#
# Per una power function T(L) = alpha/(beta+1) * L^(beta+1):
#   A    = alpha/(beta+1)
#   B    = beta+1
#   beta  = B - 1
#   alpha = A * B
# ============================================================

L_arr       = np.array(list(c_hat.keys()))
c_arr       = np.array(list(c_hat.values()))
T_hat_arr   = c_arr * L_arr
T_hat_fit   = np.maximum(T_hat_arr, 1e-10)

def T_function(L, A, B):
    return A * np.power(L, B)

popt, pcov = curve_fit(
    T_function,
    L_arr, T_hat_fit,
    p0     = [0.01, 2.5],
    bounds = ([0.0, 1.0], [np.inf, 15.0]),
    maxfev = 10000
)
A_est, B_est = popt
perr         = np.sqrt(np.diag(pcov))

beta_est       = B_est - 1.0
alpha_est      = A_est * B_est
alpha_marginal = alpha_est   # gia' il valore corretto, nessuna correzione

T_pred = T_function(L_arr, *popt)
ss_res = np.sum((T_hat_fit - T_pred) ** 2)
ss_tot = np.sum((T_hat_fit - T_hat_fit.mean()) ** 2)
r2     = 1.0 - ss_res / ss_tot if ss_tot > 0 else np.nan

print("\n" + "=" * 65)
print("  FITTING RESULTS  —  T(L) = A * L^B")
print("=" * 65)
print(f"  Fit su T_hat = c_hat * L:")
print(f"  A_est  = {A_est:.6f}  (std err: {perr[0]:.6f})")
print(f"  B_est  = {B_est:.4f}   (std err: {perr[1]:.4f})")
print(f"  R²     = {r2:.6f}")
print(f"\n  Parametri ricavati:")
print(f"  beta   = B - 1   = {B_est:.4f} - 1   = {beta_est:.4f}")
print(f"  alpha  = A * B   = {A_est:.6f} * {B_est:.4f} = {alpha_est:.6f}")
print(f"\n  c(L) = {alpha_est:.6f} * L^{beta_est:.4f}")
print(f"  T(L) = {A_est:.6f} * L^{B_est:.4f}")
print(f"\n  Verifica A = alpha/(beta+1):")
print(f"  {alpha_est:.6f} / {beta_est+1:.4f} = "
      f"{alpha_est/(beta_est+1):.6f}  "
      f"(= A_est? {np.isclose(alpha_est/(beta_est+1), A_est, atol=1e-6)})")
print(f"\n  -> alpha={alpha_est:.4f}, beta={beta_est:.4f} usati in CP6")

# ============================================================
# 7.  VISUALISATION
# ============================================================

L_plot      = np.linspace(0.05, 0.75, 300)
comp_colors = ['#264653','#2A9D8F','#E9C46A','#F4A261','#E76F51','#9B2226']

# curve per il grafico
c_plot = alpha_est * L_plot**beta_est
T_plot = A_est * L_plot**B_est

fig, axes = plt.subplots(1, 2, figsize=(15, 6))
fig.suptitle(
    f"Simulated Illiquidity Costs & Fitted Penalty Curve\n"
    f"A={A_est:.4f}  B={B_est:.4f}  R²={r2:.4f}  "
    f"alpha={alpha_est:.4f}  beta={beta_est:.4f}  |  "
    f"delta={delta:.0%},  T={T_years}yr,  N={N_scen},  "
    f"min_liq={w_min_liquid:.0%}",
    fontsize=10, fontweight='bold'
)

# ── Panel 2: T_hat simulato + T(L) fittata ────────────────
ax = axes[0]
ax.scatter(L_arr * 100, T_hat_arr * 100, s=100, color="#E63946",
           zorder=5, label='$T_{hat}(L) = \\hat{c}(L) \\cdot L$')
ax.plot(L_plot * 100, T_plot * 100, color="#264653", lw=2.2,
        label=f'$T(L) = A \\cdot L^B$  '
              f'(A={A_est:.4f}, B={B_est:.4f}, $R^2$={r2:.3f})')
ax.set_xlabel("Portfolio Illiquidity Level L (%)", fontsize=11)
ax.set_ylabel("Accumulated Penalty T(L) (%)", fontsize=11)
ax.set_title("T(L) — Penalità Accumulata", fontsize=10)
ax.set_ylim(0, 1.0)
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

# ── Panel 3: composizione target portfolios per L ─────────
ax = axes[1]
L_labels = [f"{Lv:.0%}" for Lv in L_levels]
W_matrix = np.array([target_portfolios[Lv] for Lv in L_levels])
bottom   = np.zeros(len(L_levels))
for j in range(n):
    ax.bar(L_labels, W_matrix[:, j], bottom=bottom,
           color=comp_colors[j], alpha=0.88,
           label=asset_names[j], edgecolor='white', linewidth=0.8)
    bottom += W_matrix[:, j]
ax.set_xlabel("Portfolio Illiquidity Level L", fontsize=11)
ax.set_ylabel("Portfolio Weight", fontsize=11)
ax.set_title("Target Portfolio Composition by L", fontsize=10)
ax.set_ylim(0, 1.0)
ax.legend(fontsize=8, loc='upper right', frameon=True)
ax.grid(True, axis='y', alpha=0.3)

plt.tight_layout()
import os
os.makedirs('Simulations', exist_ok=True)
plt.savefig(
    f"Simulations/Fit_{round(alpha_est*100)}_{round(beta_est*100)}.png",
    dpi=150, bbox_inches='tight')
plt.show()

print(f"\n  Checkpoint 5 complete.")
print(f"  -> alpha = {alpha_est:.4f}  (= A*B, costo marginale)")
print(f"  -> beta  = {beta_est:.4f}  (= B-1)")
print(f"  -> A     = {A_est:.4f}   (coeff di T)")
print(f"  -> B     = {B_est:.4f}   (esp di T = beta+1)")



#%%
"""
============================================================
CHECKPOINT 5.5 — Save Simulation Log
============================================================
Salva un log completo di CP5: parametri, target portfolios,
costi simulati, A, B (fit su T), alpha e beta ricavati.
============================================================
"""

import os
from datetime import datetime

os.makedirs('Logs', exist_ok=True)

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
log_path  = f'Logs/CP5_log_{timestamp}.txt'

with open(log_path, 'w', encoding='utf-8') as f:

    # ── Header ───────────────────────────────────────────────
    f.write("=" * 65 + "\n")
    f.write("  CHECKPOINT 5 — Simulation Log\n")
    f.write(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("=" * 65 + "\n\n")

    # ── Metodologia ──────────────────────────────────────────
    f.write("METODOLOGIA\n")
    f.write("-" * 40 + "\n")
    f.write("  Ipotesi C  : payout proporzionale da tutti gli asset\n")
    f.write("               - Liberi: vendita senza haircut\n")
    f.write("               - Locked: vendita con haircut, peso ridotto (op. A)\n")
    f.write("  Benchmark  : stesso fondo tutto liquido\n")
    f.write("               r_bench = w_bd @ r_t  (pesi post-drift)\n")
    f.write("  r_actual   : calcolato PRE-rebalancing\n")
    f.write("               pesi dopo drift + payout + restore\n")
    f.write("  Rebalancing: eseguito DOPO il calcolo del costo\n\n")
    f.write("  Costo anno t:\n")
    f.write("    cost_t = (r_bench - r_actual)\n")
    f.write("             + cost_hc             (haircut restore buffer)\n")
    f.write("             + cost_forced_payout   (haircut payout locked)\n\n")
    f.write("  Fitting:\n")
    f.write("    La simulazione produce c_hat(L) ≈ T(L)/L.\n")
    f.write("    Si calcola T_hat(L) = c_hat(L) * L.\n")
    f.write("    Si fitta: T_hat = A * L^B\n")
    f.write("    Si ricavano alpha e beta:\n")
    f.write("      beta  = B - 1\n")
    f.write("      alpha = A * B   (= alpha del costo marginale c(L))\n\n")

    # ── Fixes applicati ──────────────────────────────────────
    f.write("FIXES APPLIED\n")
    f.write("-" * 40 + "\n")
    f.write("  Ipotesi C : handle_payout riscritta\n")
    f.write("              payout proporzionale, locked con haircut (op. A)\n")
    f.write("  FIX 2a   : restore_liquid_buffer vende prima illiquidi liberi\n")
    f.write("  FIX 2b   : restore proventi su w_target dei liquidi\n")
    f.write("  FIX bench: r_bench = w_bd @ r_t  (pesi post-drift)\n")
    f.write("  FIX r_act: r_actual calcolato PRE-rebalancing\n")
    f.write("  FIX fit  : fit su T_hat = c_hat*L invece di c_hat\n")
    f.write("             alpha e beta ricavati da A e B analiticamente\n\n")

    # ── Parameters ───────────────────────────────────────────
    f.write("SIMULATION PARAMETERS\n")
    f.write("-" * 40 + "\n")
    f.write(f"  T_years        : {T_years}\n")
    f.write(f"  N_scen         : {N_scen}\n")
    f.write(f"  delta          : {delta:.2%}\n")
    f.write(f"  gamma_fix      : {gamma_fix}\n")
    f.write(f"  w_min_liquid   : {w_min_liquid:.0%}\n")
    f.write(f"  pi (stripping) : {pi:.2%}  [stripping OFF — mu_base = mu]\n")
    f.write(f"  L_levels (requested) : "
            f"{[f'{L:.0%}' for L in L_levels_requested]}\n")
    f.write(f"  L_levels (valid)     : "
            f"{[f'{L:.0%}' for L in L_levels]}\n")
    skipped = [L for L in L_levels_requested if L not in L_levels]
    if skipped:
        f.write(f"  L_levels (skipped)   : "
                f"{[f'{L:.0%}' for L in skipped]}\n")
    f.write(f"  Liquid assets  : "
            f"{[asset_names[i] for i in range(n) if liquid_mask[i]]}\n\n")

    # ── Asset Parameters ─────────────────────────────────────
    f.write("ASSET PARAMETERS\n")
    f.write("-" * 40 + "\n")
    f.write(f"  {'Asset':<14} {'mu':>6} {'mu_base':>8} {'l':>7} "
            f"{'lockup':>7} {'haircut':>8}\n")
    f.write("  " + "-" * 58 + "\n")
    for i in range(n):
        f.write(f"  {asset_names[i]:<14} {mu[i]:>6.2%} {mu_base[i]:>8.2%} "
                f"{l[i]:>7.3f} {lockup_years[i]:>6}yr "
                f"{haircut_by_asset[i]:>8.1%}\n")
    f.write("\n")

    # ── Target Portfolios ────────────────────────────────────
    f.write("TARGET PORTFOLIOS (constrained MVO)\n")
    f.write("-" * 40 + "\n")
    header = (f"  {'L':>5}  "
              + "  ".join(f"{a[:8]:>8}" for a in asset_names)
              + f"  {'ret':>6}  {'vol':>6}  {'L_chk':>6}  {'liq':>5}\n")
    f.write(header)
    f.write("  " + "-" * 85 + "\n")
    for Lv in L_levels:
        w_tgt = target_portfolios[Lv]
        ret_  = float(w_tgt @ mu_base)
        vol_  = float(np.sqrt(w_tgt @ Sigma @ w_tgt))
        lck_  = float(w_tgt @ l)
        liq_  = float(w_tgt[liquid_mask].sum())
        row   = "  ".join(f"{wi:>8.1%}" for wi in w_tgt)
        f.write(f"  {Lv:>5.0%}  {row}  {ret_:>6.2%}  "
                f"{vol_:>6.2%}  {lck_:>6.3f}  {liq_:>5.1%}\n")
    f.write("\n")

    # ── Simulated Costs ──────────────────────────────────────
    f.write("SIMULATED COSTS c_hat(L) and T_hat(L)\n")
    f.write("-" * 40 + "\n")
    f.write(f"  {'L':>6}  {'c_hat':>10}  {'T_hat=c*L':>12}\n")
    f.write("  " + "-" * 32 + "\n")
    for Lv in L_levels:
        c_val = c_hat[Lv]
        T_val = c_val * Lv
        f.write(f"  {Lv:>6.0%}  {c_val*100:>10.4f}%  {T_val*100:>12.4f}%\n")
    f.write("\n")

    # ── Fitting Results ──────────────────────────────────────
    f.write("FITTING RESULTS  —  T(L) = A * L^B\n")
    f.write("-" * 40 + "\n")
    f.write(f"  Fit su T_hat = c_hat * L:\n")
    f.write(f"  A_est          : {A_est:.6f}  (std err: {perr[0]:.6f})\n")
    f.write(f"  B_est          : {B_est:.4f}   (std err: {perr[1]:.4f})\n")
    f.write(f"  R²             : {r2:.6f}\n\n")
    f.write(f"  Parametri ricavati:\n")
    f.write(f"  beta  = B - 1  : {beta_est:.4f}\n")
    f.write(f"  alpha = A * B  : {alpha_est:.6f}\n\n")
    f.write(f"  c(L) = {alpha_est:.6f} * L^{beta_est:.4f}\n")
    f.write(f"  T(L) = {A_est:.6f} * L^{B_est:.4f}\n\n")
    f.write(f"  Verifica: A = alpha/(beta+1) = "
            f"{alpha_est:.6f}/{beta_est+1:.4f} = "
            f"{alpha_est/(beta_est+1):.6f}"
            f"  (= A_est? "
            f"{abs(alpha_est/(beta_est+1) - A_est) < 1e-5})\n\n")

    # ── Footer ───────────────────────────────────────────────
    f.write("=" * 65 + "\n")
    f.write("  End of log\n")
    f.write("=" * 65 + "\n")

print(f"  Log saved to: {log_path}")


#%%
"""
============================================================
CHECKPOINT 6 — Penalized Efficient Frontier
           using alpha and beta from CP5
============================================================
Builds two efficient frontiers:
  1. Unpenalized MVO  (standard Markowitz)
  2. Penalized MVO    (Hayes et al. 2015)

Uses alpha_est and beta_est from CP5 namespace.
These are derived from fitting T(L) = A * L^B directly:
  beta  = B - 1
  alpha = A * B   (= alpha of marginal cost c(L) = alpha * L^beta)

No further correction needed — alpha is already the
marginal cost parameter by construction.

Plots:
  Figure 1:
    - Panel 1: Efficient frontiers gross return
    - Panel 2: Efficient frontiers net return  mu_P - T(L)
  Figure 2:
    - Panel 1: Portfolio composition unpenalized
    - Panel 2: Portfolio composition penalized
============================================================
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import os

# ============================================================
# 1.  PENALTY FUNCTIONS FROM CP5
# ============================================================
# Uses alpha_est and beta_est from CP5 namespace.
# alpha_est = A * B  (marginal cost parameter)
# beta_est  = B - 1
#
# If running standalone, set manually:
#   alpha_est = 0.10
#   beta_est  = 1.5

def c_sim(L):
    """Marginal cost c(L) = alpha * L^beta."""
    return alpha_est * np.power(np.maximum(L, 1e-10), beta_est)

def T_sim(L):
    """Accumulated penalty T(L) = integral_0^L c(x) dx
       = alpha/(beta+1) * L^(beta+1)
       = A * L^B   (equivalent, same A and B from fit)
    """
    return (alpha_est / (beta_est + 1.0)) * \
           np.power(np.maximum(L, 1e-10), beta_est + 1.0)

# ============================================================
# 2.  OPTIMIZER
# ============================================================

def mvo_penalized_objective(w, gamma, mu, Sigma, T_fn, l):
    L       = float(w @ l)
    penalty = T_fn(L) if L > 1e-10 else 0.0
    return -(float(w @ mu) - 0.5 * gamma * float(w @ Sigma @ w) - penalty)

def mvo_penalized_gradient(w, gamma, mu, Sigma, T_fn, l, eps=1e-7):
    L  = float(w @ l)
    L_ = max(L, 1e-10)
    cL = (T_fn(L_ + eps) - T_fn(L_ - eps)) / (2 * eps)
    grad_f = mu - gamma * (Sigma @ w) - cL * l
    return -grad_f

def optimize_portfolio(gamma, mu, Sigma, T_fn, l,
                       n_restarts=20, seed=0):
    n_assets    = len(mu)
    rng         = np.random.default_rng(seed)
    constraints = {'type': 'eq', 'fun': lambda w: np.sum(w) - 1.0}
    bounds      = [(0.0, 1.0)] * n_assets
    best_w, best_val = None, np.inf

    for _ in range(n_restarts):
        w0  = rng.dirichlet(np.ones(n_assets))
        res = minimize(
            fun         = mvo_penalized_objective,
            x0          = w0,
            args        = (gamma, mu, Sigma, T_fn, l),
            jac         = mvo_penalized_gradient,
            method      = 'SLSQP',
            bounds      = bounds,
            constraints = constraints,
            options     = {'ftol': 1e-12, 'maxiter': 1000, 'disp': False}
        )
        if res.success and res.fun < best_val:
            best_val = res.fun
            best_w   = res.x.copy()

    if best_w is None:
        best_w = np.ones(n_assets) / n_assets
    best_w = np.maximum(best_w, 0.0)
    best_w /= best_w.sum()
    return best_w

# ============================================================
# 3.  BUILD FRONTIERS
# ============================================================

def T_none(L):
    return 0.0

gamma_grid = np.concatenate([
    np.linspace(0.05, 0.5,  10),
    np.linspace(0.5,  3.0,  20),
    np.linspace(3.0,  10.0, 16),
    np.linspace(10.0, 40.0, 10),
    np.linspace(40.0, 50.0, 50),
])

frontier_specs = [
    ('Unpenalized', T_none, '#333333', '--'),
    ('Penalized',   T_sim,  '#E63946', '-' ),
]

print("=" * 65)
print("  CHECKPOINT 6 — Penalized Frontier")
print(f"  alpha = {alpha_est:.4f}  (= A*B from CP5 fit)")
print(f"  beta  = {beta_est:.4f}  (= B-1 from CP5 fit)")
print(f"  c(L)  = {alpha_est:.4f} * L^{beta_est:.4f}")
print(f"  T(L)  = {A_est:.4f} * L^{B_est:.4f}")
print("=" * 65)

results_cp6 = {}

for label, T_fn, col, ls in frontier_specs:
    rets, vols, illiqs, weights_list = [], [], [], []

    for k, gamma in enumerate(gamma_grid):
        w  = optimize_portfolio(gamma, mu, Sigma, T_fn, l,
                                n_restarts=20, seed=k)
        r  = float(w @ mu)
        v  = float(np.sqrt(w @ Sigma @ w))
        lq = float(w @ l)

        rets.append(r);    vols.append(v)
        illiqs.append(lq); weights_list.append(w)

    results_cp6[label] = {
        'rets':    np.array(rets),
        'vols':    np.array(vols),
        'illiqs':  np.array(illiqs),
        'weights': np.array(weights_list),
        'color':   col,
        'ls':      ls,
    }
    print(f"  {label:<14} done  |"
          f"  ret [{min(rets):.2%}, {max(rets):.2%}]"
          f"  |  illiq [{min(illiqs):.2%}, {max(illiqs):.2%}]")

# ============================================================
# 4.  FIGURE 1 — Frontiers (gross e net return)
# ============================================================

comp_colors = ['#264653', '#2A9D8F', '#E9C46A', '#F4A261', '#E76F51', '#9B2226']

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle(
    f"Penalized vs Unpenalized Frontier\n"
    f"$\\alpha$={alpha_est:.4f}  $\\beta$={beta_est:.4f}  "
    f"| T(L) = {A_est:.4f} $\\cdot$ $L^{{{B_est:.4f}}}$",
    fontsize=12, fontweight='bold'
)

# ── Panel 1: Gross return ──────────────────────────────────
ax = axes[0]
for label, info in results_cp6.items():
    ax.plot(info['vols'] * 100, info['rets'] * 100,
            label=label, color=info['color'],
            ls=info['ls'], lw=2.2)
ax.set_xlabel("Volatility (%)", fontsize=11)
ax.set_ylabel("Expected Return (%)", fontsize=11)
ax.set_title("Efficient Frontiers — Gross Return", fontsize=11)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)

# ── Panel 2: Net return  mu_P - T(L) ──────────────────────
ax = axes[1]
for label, info in results_cp6.items():
    net_rets = info['rets'] - np.array([T_sim(lq) for lq in info['illiqs']])
    ax.plot(info['vols'] * 100, net_rets * 100,
            label=label, color=info['color'],
            ls=info['ls'], lw=2.2)
ax.set_xlabel("Volatility (%)", fontsize=11)
ax.set_ylabel("Net Return  $\\mu_P - T(L)$  (%)", fontsize=11)
ax.set_title("Efficient Frontiers — Net Return after Illiquidity Penalty",
             fontsize=11)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)

plt.tight_layout()
os.makedirs('Simulations', exist_ok=True)
plt.savefig(
    f"Simulations/Sim_front_{round(alpha_est*100)}_{round(beta_est*100)}.png",
    dpi=150, bbox_inches='tight')
plt.show()

# ============================================================
# 5.  FIGURE 2 — Portfolio Composition stacked area
# ============================================================

fig2, area_axes = plt.subplots(1, 2, figsize=(16, 6))
fig2.suptitle(
    f"Portfolio Composition along the Frontier\n"
    f"$\\alpha$={alpha_est:.4f}  $\\beta$={beta_est:.4f}",
    fontsize=12, fontweight='bold'
)

for ax_a, (label, info) in zip(area_axes, results_cp6.items()):

    sort_idx = np.argsort(info['rets'])
    x_vals   = info['rets'][sort_idx] * 100
    W_sorted = info['weights'][sort_idx]

    bottom = np.zeros(len(x_vals))
    for j in range(n):
        vals = W_sorted[:, j]
        ax_a.fill_between(x_vals, bottom, bottom + vals,
                          color=comp_colors[j], alpha=0.88,
                          label=asset_names[j])
        ax_a.plot(x_vals, bottom + vals,
                  color='white', lw=0.4, alpha=0.6)
        bottom += vals

    ax_a.set_title(label, fontsize=11, fontweight='bold',
                   color=info['color'])
    ax_a.set_xlabel("Expected Return (%)", fontsize=10)
    ax_a.set_ylabel("Portfolio Weight", fontsize=10)
    ax_a.set_ylim(0, 1.0)
    ax_a.set_xlim(x_vals.min(), x_vals.max())
    ax_a.grid(True, alpha=0.2)
    ax_a.tick_params(labelsize=9)

handles = [plt.Rectangle((0, 0), 1, 1,
                          color=comp_colors[j], alpha=0.88)
           for j in range(n)]
fig2.legend(handles, asset_names,
            loc='lower center', ncol=6,
            fontsize=10, frameon=True,
            bbox_to_anchor=(0.5, -0.02))

plt.tight_layout(rect=[0, 0.04, 1, 1])
plt.savefig(
    f"Simulations/Sim_comp_{round(alpha_est*100)}_{round(beta_est*100)}.png",
    dpi=150, bbox_inches='tight')
plt.show()

# ============================================================
# 6.  PRINT PORTFOLIO SNAPSHOTS
# ============================================================

target_rets = [0.05, 0.065, 0.08]

print("\n" + "=" * 90)
print("  PORTFOLIO COMPOSITION AT SELECTED RETURN TARGETS")
print("=" * 90)

for label, info in results_cp6.items():
    print(f"\n  -- {label} --")
    print(f"  {'Target':>8}  " +
          "  ".join(f"{a[:10]:>10}" for a in asset_names) +
          f"  {'L':>6}  {'Net ret':>8}")
    print("  " + "-" * 85)
    for tgt in target_rets:
        idx   = np.argmin(np.abs(info['rets'] - tgt))
        w     = info['weights'][idx]
        lq    = info['illiqs'][idx]
        net_r = info['rets'][idx] - T_sim(lq)
        row   = "  ".join(f"{wi:>10.1%}" for wi in w)
        print(f"  {tgt:>8.1%}  {row}  {lq:>6.1%}  {net_r:>8.3%}")



#%%
"""
============================================================
CHECKPOINT 7 — Penalty Sensitivity Matrix
============================================================
Genera una matrice 6x6 di portfolio composition charts,
una per ogni combinazione di (alpha, beta).

Parametri:
  alpha_values : lista di 6 valori di alpha
  beta_values  : lista di 6 valori di beta
  penalty_type : "power" | "exponential" | "quadratic"

Per ogni cella (alpha_i, beta_j):
  1. Costruisce c(L) e T(L) con quei parametri
  2. Risolve la MVO penalizzata lungo la frontiera
  3. Plotta lo stacked area chart della composizione

Usa i parametri globali dal namespace:
  mu, Sigma, l, asset_names, n, gamma_grid
============================================================
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy.optimize import minimize
import os

# ============================================================
# 1.  PENALTY FUNCTIONS
# ============================================================

def build_penalty_functions(alpha, beta, penalty_type):
    """
    Costruisce c(L) e T(L) in base al tipo di penalità.

    Parameters
    ----------
    alpha        : float
    beta         : float
    penalty_type : str — "power" | "exponential" | "quadratic"

    Returns
    -------
    c_fn : callable  — costo marginale c(L)
    T_fn : callable  — penalità accumulata T(L)
    """
    if penalty_type == "power":
        def c_fn(L):
            return alpha * np.power(np.maximum(L, 1e-10), beta)
        def T_fn(L):
            return (alpha / (beta + 1.0)) * \
                   np.power(np.maximum(L, 1e-10), beta + 1.0)

    elif penalty_type == "exponential":
        def c_fn(L):
            return alpha * np.exp(beta * L)
        def T_fn(L):
            return (alpha / beta) * (np.exp(beta * L) - 1.0)

    elif penalty_type == "quadratic":
        def c_fn(L):
            return alpha * L + beta * L ** 2
        def T_fn(L):
            return (alpha / 2.0) * L ** 2 + (beta / 3.0) * L ** 3

    else:
        raise ValueError(f"penalty_type '{penalty_type}' non riconosciuto. "
                         f"Usa 'power', 'exponential' o 'quadratic'.")
    return c_fn, T_fn


# ============================================================
# 2.  OPTIMIZER (locale, non dipende dal namespace CP3/CP6)
# ============================================================

def _optimize_penalized(gamma, mu, Sigma, T_fn, l,
                        n_restarts=10, seed=0):
    """
    Risolve la MVO penalizzata per un dato gamma.
    Usa multistart SLSQP.
    """
    n_assets = len(mu)
    rng      = np.random.default_rng(seed)

    def objective(w):
        L       = float(w @ l)
        penalty = T_fn(L) if L > 1e-10 else 0.0
        return -(float(w @ mu)
                 - 0.5 * gamma * float(w @ Sigma @ w)
                 - penalty)

    def gradient(w, eps=1e-7):
        L  = float(w @ l)
        L_ = max(L, 1e-10)
        cL = (T_fn(L_ + eps) - T_fn(L_ - eps)) / (2 * eps)
        return -(mu - gamma * (Sigma @ w) - cL * l)

    constraints = {'type': 'eq', 'fun': lambda w: np.sum(w) - 1.0}
    bounds      = [(0.0, 1.0)] * n_assets
    best_w, best_val = None, np.inf

    for k in range(n_restarts):
        w0  = rng.dirichlet(np.ones(n_assets))
        res = minimize(
            fun         = objective,
            x0          = w0,
            jac         = gradient,
            method      = 'SLSQP',
            bounds      = bounds,
            constraints = constraints,
            options     = {'ftol': 1e-11, 'maxiter': 800, 'disp': False}
        )
        if res.success and res.fun < best_val:
            best_val = res.fun
            best_w   = res.x.copy()

    if best_w is None:
        best_w = np.ones(n_assets) / n_assets
    best_w = np.maximum(best_w, 0.0)
    best_w /= best_w.sum()
    return best_w


def _build_frontier(mu, Sigma, T_fn, l, gamma_grid, n_restarts=10):
    """
    Costruisce la frontiera penalizzata: lista di (ret, weights).
    """
    rets, weights = [], []
    for k, gamma in enumerate(gamma_grid):
        w = _optimize_penalized(gamma, mu, Sigma, T_fn, l,
                                n_restarts=n_restarts, seed=k)
        rets.append(float(w @ mu))
        weights.append(w)
    return np.array(rets), np.array(weights)


# ============================================================
# 3.  MAIN FUNCTION — sensitivity matrix
# ============================================================

def plot_penalty_sensitivity_matrix(
        alpha_values,
        beta_values,
        penalty_type,
        mu,
        Sigma,
        l,
        asset_names,
        gamma_grid,
        n_restarts  = 10,
        figsize_cell= (2.8, 2.2),
        save_path   = None,
        comp_colors = None,
):
    """
    Genera una matrice (n_alpha × n_beta) di stacked area charts
    della portfolio composition lungo la frontiera penalizzata.

    Righe    : valori di alpha  (crescenti dall'alto verso il basso)
    Colonne  : valori di beta   (crescenti da sinistra a destra)

    Parameters
    ----------
    alpha_values  : list[float]  — 6 valori di alpha
    beta_values   : list[float]  — 6 valori di beta
    penalty_type  : str          — "power" | "exponential" | "quadratic"
    mu            : np.ndarray
    Sigma         : np.ndarray
    l             : np.ndarray
    asset_names   : list[str]
    gamma_grid    : np.ndarray
    n_restarts    : int          — multistart per ottimizzatore
    figsize_cell  : tuple        — dimensione di ogni cella
    save_path     : str | None   — path per salvare il file
    comp_colors   : list | None  — colori per gli asset
    """

    n_alpha = len(alpha_values)
    n_beta  = len(beta_values)
    n_assets = len(mu)

    if comp_colors is None:
        comp_colors = [
            '#264653','#2A9D8F','#E9C46A',
            '#F4A261','#E76F51','#9B2226'
        ]

    figw = figsize_cell[0] * n_beta  + 1.5
    figh = figsize_cell[1] * n_alpha + 1.5

    fig, axes = plt.subplots(
        n_alpha, n_beta,
        figsize=(figw, figh),
        squeeze=False
    )

    fig.suptitle(
        f"Portfolio Composition Sensitivity — {penalty_type.capitalize()} Penalty\n"
        f"Rows: alpha  |  Cols: beta",
        fontsize=14, fontweight='bold', y=1.01
    )

    for row, alpha in enumerate(alpha_values):
        for col, beta in enumerate(beta_values):

            ax = axes[row][col]

            # costruisce penalità e frontiera
            _, T_fn = build_penalty_functions(alpha, beta, penalty_type)
            rets, W = _build_frontier(mu, Sigma, T_fn, l,
                                      gamma_grid, n_restarts)

            # ordina per rendimento crescente
            idx      = np.argsort(rets)
            x_vals   = rets[idx] * 100
            W_sorted = W[idx]

            # stacked area
            bottom = np.zeros(len(x_vals))
            for j in range(n_assets):
                vals = W_sorted[:, j]
                ax.fill_between(x_vals, bottom, bottom + vals,
                                color=comp_colors[j],
                                alpha=0.88)
                bottom += vals

            ax.set_xlim(x_vals.min(), x_vals.max())
            ax.set_ylim(0, 1)
            ax.tick_params(labelsize=8)

            # etichette solo sui bordi
            if row == n_alpha - 1:
                ax.set_xlabel("E[r] (%)", fontsize=10)
            else:
                ax.set_xticklabels([])

            if col == 0:
                ax.set_ylabel("Weight", fontsize=10)
            else:
                ax.set_yticklabels([])

            # titolo cella
            ax.set_title(
                f"α={alpha:.3f}  β={beta:.2f}",
                fontsize=10, pad=2
            )

        # etichetta riga (alpha) sul lato sinistro
        axes[row][0].annotate(
            f"α={alpha:.3f}",
            xy=(0, 0.5), xytext=(-45, 0),
            xycoords='axes fraction',
            textcoords='offset points',
            fontsize=11, va='center', ha='center',
            color='#333333', fontweight='bold',
            rotation=90
        )

    # etichette colonne (beta) in cima
    for col, beta in enumerate(beta_values):
        axes[0][col].annotate(
            f"β={beta:.2f}",
            xy=(0.5, 1.0), xytext=(0, 28),
            xycoords='axes fraction',
            textcoords='offset points',
            fontsize=11, va='center', ha='center',
            color='#333333', fontweight='bold'
        )

    # legenda asset in fondo
    handles = [
        mpatches.Patch(color=comp_colors[j], alpha=0.88,
                       label=asset_names[j])
        for j in range(n_assets)
    ]
    fig.legend(
        handles=handles,
        loc='lower center',
        ncol=n_assets,
        fontsize=12,
        frameon=True,
        bbox_to_anchor=(0.5, -0.03)
    )

    plt.tight_layout(rect=[0.04, 0.04, 1, 0.98])

    if save_path is not None:
        os.makedirs(os.path.dirname(save_path) if os.path.dirname(save_path) else '.',
                    exist_ok=True)
        plt.savefig(save_path, dpi=130, bbox_inches='tight')
        print(f"  Salvato: {save_path}")

    plt.show()
    return fig, axes


# ============================================================
# 4.  ESEMPIO DI UTILIZZO
# ============================================================

# Griglia gamma (ridotta per velocità — aumenta n_restarts per qualità)
gamma_cp7 = np.concatenate([
    np.linspace(0.1,  1.0,  8),
    np.linspace(1.0,  5.0, 12),
    np.linspace(5.0, 30.0, 10),
])

# Valori di alpha e beta da esplorare
alpha_values = [0.05, 0.10, 0.20, 0.35, 0.50, 0.70]
beta_values  = [0.8,  1.2,  1.6,  2.0,  2.5,  3.0]

# ── Power penalty ──────────────────────────────────────────
fig_power, _ = plot_penalty_sensitivity_matrix(
    alpha_values = alpha_values,
    beta_values  = beta_values,
    penalty_type = "power",
    mu           = mu,
    Sigma        = Sigma,
    l            = l,
    asset_names  = asset_names,
    gamma_grid   = gamma_cp7,
    n_restarts   = 10,
    figsize_cell = (2.8, 2.2),
    save_path    = "Sensitivity/power.png",
)

alpha_values = [0.01, 0.02, 0.04, 0.07, 0.10, 0.15]
beta_values  = [0.50, 1.00,  1.5,  2.0,  2.5,  3.0]

# ── Exponential penalty ────────────────────────────────────
# Nota: per exponential beta ha il ruolo del tasso di crescita.
# Usa valori più piccoli (0.5 – 3.0 è ragionevole).
fig_exp, _ = plot_penalty_sensitivity_matrix(
    alpha_values = alpha_values,
    beta_values  = beta_values,
    penalty_type = "exponential",
    mu           = mu,
    Sigma        = Sigma,
    l            = l,
    asset_names  = asset_names,
    gamma_grid   = gamma_cp7,
    n_restarts   = 10,
    figsize_cell = (2.8, 2.2),
    save_path    = "Sensitivity/exponential.png",
)

alpha_values = [0.02, 0.05, 0.10, 0.20, 0.35, 0.50]
beta_values  = [0.05, 0.10, 0.20, 0.40, 0.70, 1.00]

# ── Quadratic penalty ──────────────────────────────────────
# Per quadratic: c(L) = alpha*L + beta*L^2
# alpha e beta hanno interpretazioni diverse — alpha e' il
# termine lineare, beta il termine quadratico.
fig_quad, _ = plot_penalty_sensitivity_matrix(
    alpha_values = alpha_values,
    beta_values  = beta_values,
    penalty_type = "quadratic",
    mu           = mu,
    Sigma        = Sigma,
    l            = l,
    asset_names  = asset_names,
    gamma_grid   = gamma_cp7,
    n_restarts   = 10,
    figsize_cell = (2.8, 2.2),
    save_path    = "Sensitivity/quadratic.png",
)

# %%
