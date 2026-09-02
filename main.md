::: titlepage
<figure data-latex-placement="h">
<img src="./logos.png" style="width:100.0%" />
</figure>

**Pricing Illiquidity in Strategic Asset Allocation:\
A Calibration Framework for Practitioners**

[Candidate]{.smallcaps}

Lorenzo Meloncelli

[Supervisor]{.smallcaps}

Prof. Emilio Barucci

[Co-supervisor]{.smallcaps}

Viviana Gisimundo

Quantitative Finance - Chair of Asset Management

Academic Year 2025/2026
:::

::: center
**Abstract**
:::

Standard mean-variance optimization, while elegant and widely adopted by
institutional investors, treats liquid and illiquid asset classes
symmetrically, ignoring the return drag and portfolio constraints that
locking up capital imposes in practice. The penalty cost approach
proposed by Hayes, Primbs and Chiquoine (2015) extends the Markowitz
framework through a marginal penalty curve that captures portfolio-level
liquidity preferences in a flexible and economically intuitive way.
However, the identification of this curve is left largely to subjective
judgement, limiting its practical applicability.

This thesis, developed in collaboration with Amundi Quant Solutions,
addresses this gap by proposing a simulation-based calibration framework
for the marginal illiquidity penalty curve. The framework quantifies the
return drag that illiquidity imposes on a portfolio, arising from forced
asset sales at a discount, secondary market haircuts, and missed
rebalancing opportunities, through a Monte Carlo simulation of a
portfolio subject to asset-specific lock-up constraints. Simulated
return losses are then mapped onto a power penalty function, whose
parameters are estimated via nonlinear least squares, yielding a
calibrated marginal cost curve grounded in portfolio-level simulation
rather than subjective assessment.

The framework is applied to three institutional investor archetypes, a
complementary pension fund, a university endowment, and a family office,
using Amundi's Capital Market Assumptions. For each archetype, the
calibrated penalty curve is used to solve the penalized mean-variance
optimization problem, producing efficient frontiers and optimal
portfolio allocations that reflect each investor's true liquidity
preferences. Results show that the penalty curve materially reshapes the
efficient frontier and portfolio composition, reducing allocations to
illiquid asset classes relative to the unconstrained case and generating
a meaningful surplus for investors who price illiquidity correctly.

# Introduction

## The illiquidity challenge in institutional asset allocation

Liquidity, in the context of asset management, refers to the ease and
speed with which an investment can be converted into cash without a
significant loss of value. A perfectly liquid asset, such as a
short-term government bond or a money market instrument, can be sold at
any time at a price close to its fair value, with minimal transaction
costs and no constraints on exit timing. An illiquid asset, by contrast,
is one where exit is constrained: either because there is no active
secondary market or because contractual lock-up periods prevent early
redemption. Private equity funds, real estate partnerships, and hedge
funds with redemption gates are canonical examples.

Illiquid asset classes have become a central component of institutional
portfolios over the past two decades. Their appeal is straightforward:
by accepting constraints on the timing and ease of exit, investors
expect to harvest an illiquidity premium over otherwise comparable
liquid investments. According to the Preqin Institutional Allocation
Study (2025), this trend has accelerated markedly in recent years.
Endowments and foundations allocated a higher share of their assets
under management to alternatives than any other institutional investor
segment in 2024, while private pensions have actively increased their
alternatives allocations between 2020 and 2024, with a particular focus
on private equity. For large institutional investors, allocations to
illiquid asset classes often represent a substantial fraction of total
portfolio value.

Yet the integration of illiquid assets into a strategic asset allocation
framework raises a set of challenges that standard portfolio theory is
ill-equipped to handle. Capital committed to illiquid investments cannot
be freely redeployed in response to changing market conditions, new
investment opportunities, or unexpected liquidity needs. Lock-up
periods, redemption gates, and the thinness of secondary markets all
constrain the portfolio manager's ability to rebalance, meet
obligations, or take advantage of tactical opportunities. These
constraints impose real costs on the portfolio, costs that are not
captured by expected return and volatility alone. The nature of these
costs is inherently non-linear: at low levels of illiquidity the
constraints are rarely binding and the costs are modest, but as
illiquidity increases the probability of facing a binding constraint
grows, the set of available responses shrinks, and the cost of each
additional unit of illiquidity rises more than proportionally.
Crucially, the degree of this convexity is not universal. It depends on
the specific investor, their liability structure, payout obligations,
and tolerance for portfolio constraints. A pension fund with near-term
benefit payments faces a steeper and more rapidly accelerating cost
curve than a family office with no contractual obligations, even at
identical levels of portfolio illiquidity.

## Existing approaches and their limitations

The academic literature has approached the problem of illiquidity in
asset allocation from several directions. One strand proposes fully
dynamic, multi-period stochastic programming models, such as those
developed in Mulvey, Pauling and Madey (2003), which incorporate
detailed cash flow models of illiquid investments and liabilities across
multiple periods. While these models can capture the specific
illiquidity characteristics of different asset classes with great
precision, they tend to generate computationally demanding optimization
problems, particularly when many asset classes and long time horizons
are involved. More fundamentally, the added numerical complexity comes
at the expense of transparency and intuition, two properties that are
essential when asset allocation decisions must be communicated to
investment committees, board members, and external constituents.

A more tractable strand of the literature attempts to modify the
mean-variance framework directly. Lo, Petrov and Wierzbicki (2003)
introduce the notion of a mean-variance-liquidity frontier, exploring
modifications to the standard optimization that incorporate a
portfolio-level liquidity term into the objective function. Kinlaw,
Kritzman and Turkington (2013) propose the use of shadow assets and
liabilities to capture liquidity effects from rebalancing, market
timing, and capital calls. While these contributions represent
meaningful advances, they share a common limitation: the marginal cost
of illiquidity is treated as constant, independent of how illiquid the
portfolio already is. This assumption is at odds with the convex nature
of illiquidity costs described above, and it prevents these frameworks
from capturing the investor-specific dimension of liquidity preferences
that is central to any rigorous approach to illiquid asset allocation.

## The Hayes, Primbs and Chiquoine (2015) framework

Hayes, Primbs and Chiquoine (2015) propose a framework that directly
addresses these limitations. Their approach modifies the standard
mean-variance objective by subtracting a portfolio-wide accumulated
illiquidity penalty, defined as the integral of a marginal penalty curve
up to the current portfolio illiquidity level. The marginal penalty
curve captures the return premium that an incremental illiquid
investment must earn over a theoretically identical liquid counterpart
in order to be a competitive portfolio addition, as a function of the
portfolio's current illiquidity level. By construction, this curve is
increasing in the portfolio illiquidity level, reflecting the convexity
of illiquidity costs.

The framework has several attractive properties. It preserves the
intuition and familiarity of mean-variance optimization, allowing for a
natural, return-based language for discussing illiquidity preferences
with investment committees and board members. It accommodates fractional
illiquidity scores across asset classes, rather than treating liquidity
as a binary characteristic. And it generates economically interpretable
quantities, including illiquidity-adjusted expected returns and an
illiquidity surplus measure that captures the net benefit of holding
illiquid assets. However, the framework leaves one critical question
unanswered: how should the marginal penalty curve be identified? The
authors acknowledge that constructing the curve requires careful
consideration of a fund's objectives, liabilities, and investment
opportunities, and that simulation models are typically required to
assess the overall costs of illiquidity. In practice, this means the
curve is often specified through subjective judgement, calibrated to a
few reference points chosen by the investment team. This subjectivity
limits the framework's replicability and its credibility as a tool for
rigorous institutional decision-making.

## This paper's contribution

This thesis addresses the calibration gap in the Hayes et al. (2015)
framework by developing a systematic, simulation-based methodology for
identifying the marginal illiquidity penalty curve. The core idea is to
estimate the curve empirically, by simulating the return drag that
illiquidity imposes on a portfolio across a range of illiquidity levels,
and then fitting a parametric penalty function to the simulated costs.

The simulation models a portfolio subject to asset-specific lock-up
constraints, a minimum liquidity buffer, and a stochastic annual payout
requirement. In each scenario, the portfolio incurs costs from three
sources: forced sales of locked assets at a secondary market discount
when the liquidity buffer falls below its minimum, haircuts on illiquid
positions that must be liquidated to meet payout obligations, and return
drag from the inability to rebalance freely to the optimal target
weights. The difference in realized return between the constrained
portfolio and a frictionless liquid benchmark, averaged across
scenarios, yields an estimate of the illiquidity cost at each portfolio
illiquidity level. These point estimates are then used to fit a power
penalty function, recovering the parameters of the marginal cost curve
through nonlinear least squares. A second contribution of this thesis is
to connect the shape of the penalty curve to the characteristics of
specific investor types, defining three institutional investor
archetypes, a complementary pension fund, a university endowment, and a
family office, and calibrating the simulation parameters for each. The
resulting curves differ meaningfully across archetypes, reflecting
genuine differences in liquidity needs and the associated costs of
holding illiquid assets.

## Institutional context: Amundi Quant Solutions

This thesis was developed in collaboration with the Quant Solutions team
at Amundi Asset Management. The team comprises four professionals and
operates within Amundi's Retirement Solutions division, working closely
with the Amundi Investment Institute, portfolio managers, and other
colleagues across the Solutions division. The team is responsible for
modelling expected returns, including the production of Capital Market
Assumptions, and for providing asset class simulations and quantitative
analyses for institutional client projects in areas such as strategic
asset allocation and asset-liability management, and is also actively
involved in producing research on retirement-related themes. The Capital
Market Assumptions used throughout this analysis, including expected
returns, volatilities, and correlations for all asset classes
considered, were provided by Amundi Quant Solutions, and the choice of
asset universe, illiquidity scores, and archetype definitions was guided
by the team's experience in designing strategic asset allocation
frameworks for institutional clients across Europe.

## Structure of the paper

The remainder of this thesis is organized as follows. Section 2 presents
the theoretical framework of Hayes et al. (2015) in detail. Section 3
describes the asset universe and Capital Market Assumptions. Section 4
discusses the functional forms considered for the penalty curve and
motivates the choice of the power specification. Section 5 introduces
the three investor archetypes and their subjective penalty curve
parametrizations. Section 6 develops the simulation-based calibration
methodology and presents the estimated penalty curves for each
archetype. Section 7 presents the results of the penalized mean-variance
optimization and their portfolio implications. Section 8 concludes and
explores potential directions for future research.

# Theoretical Framework

## Mean-Variance Optimization: setup and notation

The starting point of our framework is the classical mean-variance
optimization problem introduced by Markowitz (1952). We consider a
portfolio allocated across *$n$* risky asset classes. Let
*$\textbf{w} = (w_1, \ldots, w_n)^T$* denote the vector of portfolio
weights, *$\textbf{$\mu$} = (\mu_1, \ldots, \mu_n)^T$* the vector of
expected returns, and $\Sigma$ the *$n$×$n$* covariance matrix of
returns, with $\sigma_{ij}$ denoting the covariance between asset
classes *i* and *j* and $\sigma_{ii} = \sigma_i^2$. The standard
mean-variance optimization problem is:

$$\begin{equation}
 \max_{\mathbf{w}} \quad \mathbf{w}^T \boldsymbol{\mu} - \frac{\gamma}{2} \mathbf{w}^T \boldsymbol{\Sigma} \mathbf{w}
\end{equation}$$

subject to ***$w^T1 = 1$*** and ***$w\ge0$***, where $\gamma$ is the
risk aversion coefficient and **$1$** is the n-vector of ones. The term
$w^T \mu$ is the portfolio expected return and $w^T\Sigma w$ is the
portfolio variance. By varying $\gamma$ from high to low, the optimizer
traces the efficient frontier from minimum variance to maximum return
portfolios.

It is worth noting the behaviour of the objective as $\gamma \to 0$. In
this limit, the variance term vanishes and the optimizer seeks only to
maximize expected return, concentrating the portfolio in the
highest-returning asset class. In the penalized version of the problem
introduced below, this limit plays a different role: the optimizer
instead maximizes expected return net of the illiquidity penalty, and
the solution reflects a balance between return and the cost of
illiquidity rather than between return and variance. This implies a
natural lower bound on the penalized frontier that depends directly on
the aggressiveness of the penalty curve.

## Illiquidity representation

Following Hayes et al. (2015), we assign each asset class *$i$* an
illiquidity index *$l_i \in [0,1]$*, where $l_i = 0$ denotes a perfectly
liquid asset class and $l_i =1$ denotes a completely illiquid one. The
assignment of illiquidity scores is at the user's discretion and should
reflect the specific liquidity characteristics relevant to the investor.
In our implementation, scores are first assigned on a raw scale
reflecting qualitative liquidity characteristics, and then normalized to
the unit interval as:

$$\begin{equation}
 l_i = \frac{s_i - s_{\min}}{s_{\max} - s_{\min}}
\end{equation}$$

where *$s_i$* is the raw score of asset class *$i$* and *$s_{min}$*,
*$s_{max}$* are the minimum and maximum scores in the universe. We
collect the illiquidity indices in the vector
*$\textbf{l} = (l_1, \ldots, l_n)^T$*.

The overall illiquidity of the portfolio is summarized by the portfolio
illiquidity level:

$$\begin{equation}
 L(\mathbf{w}) = \mathbf{w}^T \mathbf{l} = \sum_{i=1}^{n} w_i l_i
\end{equation}$$

This quantity can be interpreted as the percentage of the portfolio that
is illiquid, and is a linear function of the portfolio weights. For
example, a portfolio with equal weights in a perfectly liquid asset and
a fully illiquid asset has $L=0.5$. Note that $L(\textbf{$w$})=0.5$ is a
portfolio-level quantity: it captures the aggregate illiquidity of the
portfolio rather than the illiquidity of any individual position, and it
changes continuously as portfolio weights change.

## The marginal penalty function and the accumulated penalty

To incorporate illiquidity costs into the optimization, Hayes et al.
(2015) introduce a marginal illiquidity penalty function $c(L)$, defined
over the portfolio illiquidity level $L \in [0,1]$. The value $c(L)$
represents the return premium that the next incremental unit of illiquid
investment must earn over a theoretically identical liquid counterpart
in order to be a competitive addition to a portfolio currently at
illiquidity level $L$. The key economic property of $c(L)$ is that it is
increasing in $L$: the marginal cost of illiquidity rises as the
portfolio becomes more illiquid, reflecting the convex nature of
liquidity costs discussed in Section 1.

The total illiquidity cost borne by a portfolio at illiquidity level $L$
is given by the accumulated penalty:

$$\begin{equation}
 T(L(\mathbf{w})) = \int_0^{L(\mathbf{w})} c(x) , dx
\end{equation}$$

This quantity represents the area under the marginal penalty curve from
zero to the current portfolio illiquidity level, and can be interpreted
as the total return drag imposed by illiquidity on the portfolio. It is
a non-linear function of the portfolio weights through $L(w)$, and it is
this non-linearity that introduces the investor-specific dimension into
the optimization problem.

![Marginal illiquidity penalty curve for three investor archetypes. The
dotted line illustrates that, at a portfolio illiquidity level of 45%,
the marginal return penalty for a university endowment is approximately
3%. Source: Hayes, Primbs and Chiquoine
(2015).](./Screenshot 2026-08-24 170322.png){#fig:penalty_curves
width="75%"}

## The penalized optimization problem

The penalized mean-variance optimization problem is obtained by
subtracting the accumulated penalty from the standard mean-variance
objective:

$$\begin{equation}
 \max_{\mathbf{w}} \quad \mathbf{w}^T \boldsymbol{\mu} - \frac{\gamma}{2} \mathbf{w}^T \boldsymbol{\Sigma} \mathbf{w} - T(L(\mathbf{w}))
\end{equation}$$

subject to ***$w^T1 = 1$*** and ***$w\ge0$***. The penalty term
$T(L(w))$ acts as a return deduction that grows with portfolio
illiquidity, discouraging excessive concentration in illiquid asset
classes without imposing hard constraints. Unlike a fixed allocation
cap, the penalty creates a continuous trade-off between the return
contribution of illiquid assets and the cost they impose on the
portfolio, with the trade-off becoming increasingly unfavourable as
illiquidity rises.

The non-linearity introduced by the penalty term has important
implications for the structure of optimal portfolios. In the standard
unpenalized problem, the only trade-off is between expected return and
variance, which is a smooth and continuous function of the weights. The
addition of the penalty term introduces a third dimension to the
trade-off, between return, variance, and illiquidity cost. This third
term can create non-linearities in the objective that produce abrupt
regime switches in the optimal portfolio composition as the risk
aversion coefficient $\gamma$ varies. In particular, as $\gamma$
decreases and the optimizer is willing to accept more risk, the penalty
may cause sudden shifts in the allocation between liquid and illiquid
asset classes, rather than the gradual transitions observed in the
unpenalized case.

## Illiquidity-adjusted expected returns

An attractive feature of the penalized formulation is that it can be
recast in terms of illiquidity-adjusted expected returns, preserving the
familiar mean-variance structure of the optimization. Combining the
expected return term and the penalty, the objective can be written as:

$$\begin{equation}
 \mathbf{w}^T \boldsymbol{\mu} - T(L(\mathbf{w})) = \mathbf{w}^T \hat{\boldsymbol{\mu}}(\mathbf{w})
\end{equation}$$

where the vector of illiquidity-adjusted expected returns is defined as:

$$\begin{equation}
 \boldsymbol{\hat{\mu}}(\mathbf{w}) = \boldsymbol{\mu} - \frac{T(L(\mathbf{w}))}{L(\mathbf{w})} \cdot l
\end{equation}$$

The quantity $T(L)/L$ is the average accumulated penalty per unit of
portfolio illiquidity, and it is applied to each asset class
proportionally to its illiquidity index $l_i$. A perfectly liquid asset
with $l_i=0$ requires no adjustment, while a fully illiquid asset with
$l_i=1$ bears the full average penalty. The penalized problem can
therefore be written equivalently as a standard mean-variance
optimization with adjusted expected returns:

$$\begin{equation}
 \max_{\mathbf{w}} \quad \mathbf{w}^T \hat{\boldsymbol{\mu}}(\mathbf{w}) - \frac{\gamma}{2} \mathbf{w}^T \boldsymbol{\Sigma} \mathbf{w}
\end{equation}$$

subject to ***$w^T1 = 1$*** and ***$w\ge0$***. This reformulation is
particularly useful for communication purposes: the effect of the
illiquidity penalty can be expressed entirely in terms of a downward
adjustment to the expected returns of illiquid asset classes, a language
that is natural and familiar to practitioners.

## The illiquidity surplus

Given an optimal portfolio $w^*$, Hayes et al. (2015) define the
illiquidity surplus as:

$$\begin{equation}
 S(\mathbf{w}^*) = c(L(\mathbf{w}^*)) \cdot L(\mathbf{w}^*) - T(L(\mathbf{w}^*))
\end{equation}$$

This quantity measures the net benefit that the portfolio derives from
holding illiquid assets. At the optimal portfolio, the marginal cost of
illiquidity is $c(L(w^*))$, which represents the premium required at the
margin to justify an additional unit of illiquid investment. For all
previous units of illiquidity up to $L(w^*)$, however, the required
premium was lower than $c(L(w^*))$, since the marginal cost curve is
increasing. The surplus captures the difference between what the
portfolio could in principle demand at the margin and what it actually
paid on average, and is geometrically equal to the area above the
penalty curve and below the horizontal line at $c(L(w^*))$, up to the
illiquidity level $L(w^*)$. A positive illiquidity surplus indicates
that the portfolio is being compensated more than adequately for the
illiquidity it holds at all but the marginal unit, and it provides a
measure of the value created by the decision to invest in illiquid asset
classes.

# Data and Asset Universe

## Asset class universe and Capital Market Assumptions

The empirical analysis is conducted on a universe of six asset classes,
chosen to span the full spectrum of liquidity characteristics relevant
to a diversified institutional portfolio. The universe includes Money
Market USD (MM_US), Global Aggregate Fixed Income hedged in USD
(GLOB_AGG), Global Equity USD (GLOB_EQ), Hedge Funds Fund of Funds
(HF_FOF), Global Real Estate (GLOB_RE), and Global Private Equity
(GLOB_PE). Together, these asset classes cover the main building blocks
of a strategic asset allocation, from the most liquid cash-equivalent
instruments to long-duration illiquid private market investments.

Expected returns, volatilities, and correlations for all asset classes
were provided by the Quant Solutions team at Amundi Asset Management as
part of their Capital Market Assumptions framework (Amundi Investment
Institute, 2026). The CMA process combines the Amundi CASM simulation
model, macroeconomic scenario analysis conducted by the Amundi
Investment Institute, and asset class specific adjustments developed by
the Quant Solutions team. All figures are based on a starting date of 31
December 2025 and reflect a ten-year forward-looking horizon. Expected
returns are expressed in local currency, nominal and gross of fees for
liquid asset classes, and net of management and administrative fees for
private and alternative assets. The 2026 edition of the CMA is framed
around the notion of structural rupture in the global investment
environment, and concludes that ten-year expected returns remain broadly
attractive across asset classes, with private equity identified as the
main growth engine and a key source of return enhancement for
institutional portfolios. The figures used in this analysis are
summarized in Table [1](#tab:asset_classes){reference-type="ref"
reference="tab:asset_classes"}, alongside the illiquidity scores
described in the following section.

## Illiquidity scoring

The illiquidity index $l_i$ for each asset class is constructed through
a two-step procedure. In the first step, each asset class is assigned a
raw illiquidity score $s_i$ on a qualitative scale that reflects its
liquidity characteristics: the ease of exit, the depth and reliability
of the secondary market, the typical length of contractual lock-up
periods, and the magnitude of transaction costs in stressed conditions.
Money market instruments receive the lowest score, reflecting
near-instantaneous liquidity at minimal cost. Global aggregate fixed
income and global equity are assigned scores close to the minimum,
reflecting deep and continuously traded markets. Hedge funds receive an
intermediate score, reflecting the presence of redemption gates and
notice periods that constrain exit timing. Global real estate and
private equity receive progressively higher scores, reflecting long
lock-up periods, limited secondary market liquidity, and significant
transaction costs.

In the second step, raw scores are normalized to the unit interval using
a linear transformation:

$$\begin{equation}
 l_i = \frac{s_i - s_{\min}}{s_{\max} - s_{\min}}
\end{equation}$$

where $s_{min} = 1$ and $s_{max} = 5$ are the minimum and maximum scores
in the universe. This normalization ensures that MM_US maps exactly to
$l_i = 0$ and GLOB_PE maps exactly to $l_i = 1$, while intermediate
asset classes receive fractional scores that reflect the continuum of
liquidity characteristics across the universe. The use of fractional
scores, rather than a binary liquid or illiquid classification, is a key
feature of the Hayes et al. (2015) framework, as it allows the optimizer
to treat illiquidity as a continuous dimension of each asset class
rather than a hard constraint.

## Correlation structure

The correlation matrix of the six asset classes is reported in Table
[2](#tab:correlations){reference-type="ref"
reference="tab:correlations"}. Several features of this matrix are worth
noting. Money market and global aggregate fixed income are essentially
uncorrelated with all equity-like asset classes, confirming their role
as diversifying, liquid components of the portfolio. Global equity,
hedge funds, and private equity exhibit very high pairwise correlations,
in the range of 0.86 to 0.87, reflecting their common exposure to broad
equity market risk. Global real estate is moderately correlated with
both the equity cluster and with private equity.

The high correlation between GLOB_EQ, HF_FOF, and GLOB_PE has important
implications for the optimization. Since these three asset classes are
near-perfect substitutes from a correlation standpoint, the optimizer
tends to select only one of them as the representative of the equity
risk factor. Given that GLOB_PE offers the highest expected return in
the universe at 9.80%, at a volatility broadly comparable to global
equity, the unconstrained optimizer concentrates the illiquid allocation
almost entirely in private equity, eliminating hedge funds and, to a
large extent, global equity from the optimal portfolio. This
substitution effect is a key driver of the results discussed in Sections
6 and 7, and it motivates the role of the illiquidity penalty in
diversifying the allocation across the equity cluster.

::: {#tab:asset_classes}
  Asset class    Expected return   Volatility   Raw score   $l_i$
  ------------- ----------------- ------------ ----------- -------
  MM_US               3.24%          1.82%        1.00      0.00
  GLOB_AGG            4.59%          4.39%        1.45      0.11
  GLOB_EQ             7.09%          17.01%       1.50      0.13
  HF_FOF              5.18%          7.28%        2.50      0.38
  GLOB_RE             5.48%          12.51%       3.00      0.50
  GLOB_PE             9.80%          20.00%       5.00      1.00

  : Asset class universe: expected real returns, annualised
  volatilities, and illiquidity indices. Expected returns and
  volatilities are expressed as annual percentages. Source: Amundi
  Investment Institute (2026).
:::

::: {#tab:correlations}
                        MM_US                     GLOB_AGG                     GLOB_EQ                     HF_FOF                      GLOB_RE                     GLOB_PE
  ---------- --------------------------- --------------------------- --------------------------- --------------------------- --------------------------- ---------------------------
  MM_US                 1.000                       0.141             $-$`<!-- -->`{=html}0.009   $-$`<!-- -->`{=html}0.011   $-$`<!-- -->`{=html}0.007   $-$`<!-- -->`{=html}0.012
  GLOB_AGG              0.141                       1.000             $-$`<!-- -->`{=html}0.013   $-$`<!-- -->`{=html}0.035             0.048             $-$`<!-- -->`{=html}0.064
  GLOB_EQ     $-$`<!-- -->`{=html}0.009   $-$`<!-- -->`{=html}0.013             1.000                       0.860                       0.509                       0.874
  HF_FOF      $-$`<!-- -->`{=html}0.011   $-$`<!-- -->`{=html}0.035             0.860                       1.000                       0.550                       0.870
  GLOB_RE     $-$`<!-- -->`{=html}0.007             0.048                       0.509                       0.550                       1.000                       0.643
  GLOB_PE     $-$`<!-- -->`{=html}0.012   $-$`<!-- -->`{=html}0.064             0.874                       0.870                       0.643                       1.000

  : Correlation matrix of the six asset classes. Source: Amundi
  Investment Institute (2026).
:::

# Functional Forms of the Penalty Curve

## Power, Exponential and Quadratic: analytical properties

The Hayes et al. (2015) framework does not prescribe a specific
functional form for the marginal penalty curve $c(L)$, leaving the
choice to the practitioner. In this thesis we consider three candidate
specifications: the power function, the exponential function, and the
quadratic function. For each, we derive the corresponding accumulated
penalty $T(L)$ analytically. All three specifications are parametrized
with $\alpha = 0.05$ and $\beta = 1.6$ for comparison purposes.

The power specification defines the marginal penalty as:

$$\begin{equation}
 c(L) = \alpha \cdot L^{\beta}
\end{equation}$$

with accumulated penalty is:

$$\begin{equation}
 T(L) = \frac{\alpha}{\beta + 1} \cdot L^{\beta + 1}
\end{equation}$$

The exponential specification defines the marginal penalty as:

$$\begin{equation}
 c(L) = \alpha \cdot e^{\beta L}
\end{equation}$$

with accumulated penalty:

$$\begin{equation}
 T(L) = \frac{\alpha}{\beta} \left( e^{\beta L} - 1 \right)
\end{equation}$$

The quadratic specification defines the marginal penalty as:

$$\begin{equation}
 c(L) = \alpha L + \beta L^{2}
\end{equation}$$

with accumulated penalty:

$$\begin{equation}
 T(L) = \frac{\alpha}{2} L^{2} + \frac{\beta}{3} L^{3}
\end{equation}$$

Figure [2](#fig:penalty_curves){reference-type="ref"
reference="fig:penalty_curves"} illustrates the shape of the three
specifications for $\alpha = 0.05$ and $\beta = 1.6$. The top panels
show the marginal penalty $c(L)$ and the accumulated penalty $T(L)$,
while the bottom panels show the average cost $T(L)/L$ and the stability
diagnostic $\frac{\mathrm{d}}{\mathrm{d}L}\left[\frac{T(L)}{L}\right]$
discussed in Section 4.3.

<figure id="fig:penalty_curves" data-latex-placement="h">
<img src="./Penalty curves.png" />
<figcaption>Marginal penalty <span
class="math inline"><em>c</em>(<em>L</em>)</span>, accumulated penalty
<span class="math inline"><em>T</em>(<em>L</em>)</span>, average cost
<span class="math inline"><em>T</em>(<em>L</em>)/<em>L</em></span>, and
stability diagnostic <span
class="math inline">$\frac{\mathrm{d}}{\mathrm{d}L}\left[\frac{T(L)}{L}\right]$</span>
for the three functional forms, parametrized with <span
class="math inline"><em>α</em> = 0.05</span> and <span
class="math inline"><em>β</em> = 1.6</span>. The dotted vertical line
marks <span class="math inline"><em>L</em> = 45%</span> as a reference
level.</figcaption>
</figure>

## Economic intuition and desirable properties

Beyond their analytical tractability, the three functional forms differ
in important ways from an economic standpoint. A well-behaved penalty
curve should satisfy two basic properties: it should equal zero at
$L = 0$, reflecting the fact that a fully liquid portfolio bears no
illiquidity cost, and it should be strictly increasing and convex in
$L$, reflecting the non-linear nature of illiquidity costs described in
Section 1.

Both the power and the quadratic specifications satisfy $c(0) = 0$ by
construction, while the exponential does not: at $L = 0$ the exponential
penalty equals $\alpha > 0$, implying a strictly positive cost even for
a fully liquid portfolio. This is economically unappealing and can
distort the optimization by penalizing liquid portfolios that should
face no illiquidity cost. The power and quadratic specifications are
therefore preferable from a theoretical standpoint.

## Stability diagnostic

A practical concern in the penalized MVO is the numerical stability of
the optimization. The illiquidity-adjusted expected return of asset
class $i$ is:

$$\begin{equation}
 \hat{\mu_i}(\mathbf{w}) = \mu_i - \frac{T(L(\mathbf{w}))}{L(\mathbf{w})} \cdot l_{i}
\end{equation}$$

The term $T(L)/L$ is the average accumulated penalty per unit of
illiquidity, and it enters the adjusted return of every asset class
proportionally to its illiquidity index. If this term is highly
sensitive to small changes in portfolio weights, the optimization
landscape becomes steep and the optimizer may struggle to find stable
solutions. The relevant diagnostic is therefore the derivative of
$T(L)/L$ with respect to $L$:

$$\begin{equation}
 \frac{d}{dL}\left[\frac{T(L)}{L}\right] = \frac{c(L) \cdot L - T(L)}{L^{2}} = \frac{S(L)}{L^{2}}
\end{equation}$$

where $S(L) = c(L) \cdot L - T(L)$ is the illiquidity surplus introduced
in Section 2. As shown in the bottom-right panel of Figure
[2](#fig:penalty_curves){reference-type="ref"
reference="fig:penalty_curves"}, the exponential curve generates the
largest values of this diagnostic at moderate to high illiquidity
levels, confirming its numerical instability. The power and quadratic
specifications remain well-behaved across the full range of illiquidity
levels considered, with the power curve producing the lowest and most
stable values of the diagnostic throughout.

## The effect of the penalty on portfolio composition

The non-linearity introduced by the penalty term has a further
implication worth discussing explicitly. In the standard unpenalized
MVO, the trade-off is exclusively between expected return and variance,
both of which are smooth functions of the portfolio weights. The optimal
composition therefore changes continuously as the risk aversion
coefficient $\gamma$ varies, with allocations shifting gradually from
lower to higher returning asset classes as $\gamma$ decreases.

The addition of the penalty term introduces a third dimension to the
trade-off. The penalty is a non-linear function of the weights through
$L(\mathbf{w})$, and this non-linearity can produce abrupt regime
switches in the optimal portfolio composition. As $\gamma$ decreases and
the optimizer becomes willing to accept more risk, the penalty may cause
sudden discrete shifts in the allocation between liquid and illiquid
asset classes, rather than the smooth transitions observed in the
unpenalized case. These regime switches are more pronounced for penalty
curves with high curvature, and they tend to occur at illiquidity levels
where the marginal cost curve rises steeply.

Figure [3](#fig:composition){reference-type="ref"
reference="fig:composition"} illustrates this phenomenon clearly. In the
unpenalized case, the allocation to GLOB_PE grows gradually and
continuously as the target return increases, dominating the portfolio at
high return levels. Under the exponential penalty, by contrast, the
optimizer essentially eliminates private equity from the portfolio
entirely, substituting it with GLOB_EQ and GLOB_AGG, producing an abrupt
regime change at low return levels. The power penalty generates a more
gradual and economically intuitive transition, preserving a meaningful
allocation to private equity at high return targets while reducing it
significantly relative to the unpenalized case. The quadratic penalty
produces intermediate results, though with a somewhat less smooth
transition than the power specification.

The sensitivity of portfolio composition to the choice of parameters is
explored systematically in Annex A, which reports the optimal portfolio
composition along the penalized frontier for a $6 \times 6$ grid of
$(\alpha, \beta)$ values across all three functional forms. The analysis
confirms that the power specification produces the most stable and
economically intuitive transitions across the parameter space, while the
exponential penalty generates abrupt regime switches even at moderate
parameter values.

<figure id="fig:composition" data-latex-placement="h">
<span class="image placeholder"
data-original-image-src="composition.png" data-original-image-title=""
width="\textwidth"></span>
<figcaption>Portfolio composition along the efficient frontier for the
unpenalized MVO and the three penalized specifications, parametrized
with <span class="math inline"><em>α</em> = 0.05</span> and <span
class="math inline"><em>β</em> = 1.6</span>.</figcaption>
</figure>

## The power function as the reference case

On the basis of the properties discussed above, the power specification
is adopted as the reference functional form throughout the remainder of
this thesis. It satisfies $c(0) = 0$, it is strictly increasing and
convex for $\beta > 0$, it generates sable optimization landscapes, and
its two parameters $\alpha$ and $\beta$ have clear and separable
economic interpretations:

The parameter $\beta$ governs the curvature of the penalty curve and can
be interpreted as a measure of how rapidly illiquidity costs accelerate
as the portfolio becomes more illiquid. A high $\beta$ implies that
costs are low and rise slowly at moderate illiquidity levels, but
accelerate sharply as $L$ approaches high values. This profile is
characteristic of investors with long-duration liabilities and stable
cash flows, where liquidity constraints are rarely binding until the
portfolio is very heavily committed to illiquid assets. A low $\beta$,
by contrast, implies that costs begin to accumulate meaningfully even at
moderate illiquidity levels, reflecting an investor who faces binding
liquidity constraints more frequently. In this sense, $\beta$ is
primarily determined by the structural characteristics of the investor's
liability side: the duration of liabilities, the openness of the fund,
and the stability of cash flows.

The parameter $\alpha$ governs the overall level of the penalty and is
more directly linked to market conditions and transaction costs. As
$L \to 0$, the penalty $c(L) \to 0$ regardless of $\alpha$, so $\alpha$
does not represent a fixed cost at zero illiquidity. Rather, it scales
the entire curve upward or downward without altering its shape. An
investor operating in markets with high secondary market transaction
costs, wide bid-ask spreads, or long transaction times will face a
higher $\alpha$ than one with access to deep and efficient secondary
markets. In this sense, $\alpha$ can be thought of as the baseline
illiquidity cost per unit of illiquid exposure, analogous to the level
parameter of a cost function: it captures the cost that the investor
would face even for a marginal illiquid allocation, before the
non-linear effects captured by $\alpha$ begin to dominate.

The practical consequences of identifying the functional form of the
penalty with the power function are visible in Figure
[4](#fig:net_return){reference-type="ref" reference="fig:net_return"},
which shows the liquidity-adjusted net return frontier
$\hat{\mu}_P = \mu_P - T(L)$ for all three specifications. The
exponential penalty imposes by far the largest return drag across the
entire frontier, while the power penalty is the most conservative,
reflecting its slower accumulation of costs at moderate illiquidity
levels. The gap between the penalized and unpenalized frontiers widens
as volatility and illiquidity increase, confirming that the penalty has
its largest effect precisely where illiquid allocations are highest.

<figure id="fig:net_return" data-latex-placement="h">
<span class="image placeholder"
data-original-image-src="frontiers_net.png" data-original-image-title=""
width="75%"></span>
<figcaption>Liquidity-adjusted net return frontier <span
class="math inline"><em>μ̂</em><sub><em>P</em></sub> = <em>μ</em><sub><em>P</em></sub> − <em>T</em>(<em>L</em>)</span>
for the unpenalized MVO and the three penalized specifications,
parametrized with <span class="math inline"><em>α</em> = 0.05</span> and
<span class="math inline"><em>β</em> = 1.6</span>.</figcaption>
</figure>

For the power specification, the penalized MVO problem takes the form:

$$\begin{equation}
 \max_{\mathbf{w}} \quad \mathbf{w}^{T} \boldsymbol{\mu} - \frac{\gamma}{2} \mathbf{w}^{T} \boldsymbol{\Sigma} \mathbf{w} - \frac{\alpha}{\beta + 1} \cdot L(\mathbf{w})^{\beta + 1}
\end{equation}$$

subject to $\mathbf{w}^{T} \mathbf{1} = 1$ and
$\mathbf{w} \geq \mathbf{0}$, where
$L(\mathbf{w}) = \mathbf{w}^{T} \mathbf{l}$. The gradient of the
objective with respect to $\mathbf{w}$ is:

$$\begin{equation}
 \nabla_{\mathbf{w}} = \boldsymbol{\mu} - \gamma \boldsymbol{\Sigma} \mathbf{w} - \alpha \cdot L(\mathbf{w})^{\beta} \cdot \mathbf{l}
\end{equation}$$

which shows that the penalty enters the first-order conditions as a
downward adjustment to the expected return of each asset class,
proportional to its illiquidity index $l_{i}$ and to the marginal cost
$c(L) = \alpha \cdot L^{\beta}$ evaluated at the current portfolio
illiquidity level. This gradient expression is used directly in the
numerical optimization described in Section 6.

# Investor Archetypes and Penalty Curve Parametrization

## Determinants of the penalty curve shape

The marginal illiquidity penalty curve is not a universal object: its
shape depends on the specific characteristics of the investor who holds
the portfolio. Two investors with identical asset allocations but
different liability structures, payout obligations, and cash flow
dynamics will face different illiquidity costs, and should therefore be
characterized by different penalty curves. Understanding what drives the
shape of the curve is a prerequisite for any systematic calibration
methodology.

The most direct determinant is the investor's payout obligation. An
investor who must distribute a large and predictable fraction of assets
each year faces a high probability of needing to liquidate positions at
short notice, and bears a correspondingly high cost when those positions
are locked up. The level of the payout obligation governs the overall
height of the penalty curve, while its variability and correlation with
market conditions determine how steeply the curve rises as illiquidity
increases. A fund whose payout demand spikes precisely when markets are
falling, making secondary market liquidity thinnest and haircuts
largest, faces a particularly convex cost curve.

A second determinant is the maturity structure of existing liabilities
and assets. A fund with long-duration liabilities, such as a young
pension fund with decades before the bulk of benefits fall due, can
afford to lock up capital for extended periods without facing binding
liquidity constraints. A fund with short-duration liabilities, by
contrast, must maintain a higher liquid buffer and faces a steeper
penalty for illiquidity at any given portfolio level. Similarly, the
maturity profile of existing illiquid positions matters: a portfolio
with a large stock of recently committed capital, all subject to active
lock-up periods, faces higher effective illiquidity than one with a more
seasoned and diversified vintage structure.

A third determinant is whether the fund is open or closed to new
contributions. An open fund with active members, such as a pension fund
still receiving contributions or an endowment receiving regular
donations, has access to incoming cash flows that can absorb payout
obligations without requiring asset sales. This external liquidity
buffer reduces the probability of forced selling and flattens the
penalty curve. A closed fund, by contrast, must meet all obligations
from existing assets, making the liquidity buffer more fragile and the
penalty curve steeper.

Finally, the depth and reliability of secondary markets for the fund's
specific illiquid holdings matters. A fund concentrated in
well-established private equity partnerships has access to a more
developed secondary market than one holding bespoke infrastructure debt
or direct real estate. The expected haircut in a forced sale, and the
time required to complete a transaction, both feed directly into the
cost simulation and therefore into the shape of the calibrated penalty
curve.

## The three archetypes: Pension Fund, Endowment, Family Office

To make the penalty curve mapping operational, we define three
institutional investor archetypes that span the range of liquidity
profiles encountered in practice. Each archetype is characterized by a
distinct combination of payout dynamics, liability structure, and market
access, which translate into a specific set of power curve parameters.

The *pension fund* represents the most liquidity-constrained archetype.
It faces mandatory annual distributions to members, including pension
payments, early withdrawals, and redemptions, which in aggregate
represent a significant and persistent fraction of assets under
management. Payout demands tend to be correlated with adverse market
conditions, as members are more likely to request early withdrawals
during periods of financial stress. The fund is partially open, with
active members still contributing, but the contribution flow is
insufficient to offset the payout obligation at high illiquidity levels.
The combination of high payout, strong market correlation, and
regulatory minimum liquidity requirements makes this the archetype with
the steepest and most rapidly accelerating penalty curve.

The *university endowment* represents an intermediate liquidity profile.
It distributes a stable fraction of assets annually to fund university
operations, typically following a smoothing rule that partially
decouples the payout from short-term market conditions. The fund is
open, receiving regular donations that provide an additional liquidity
buffer. Its liabilities are long-duration and relatively predictable,
reducing the probability of binding liquidity constraints. The penalty
curve is less steep than that of the pension fund, reflecting both the
lower payout level and the more stable cash flow dynamics.

The *family office* represents the least liquidity-constrained
archetype. It has no contractual payout obligations and distributes
assets at the discretion of the beneficiaries. Payout demands are
idiosyncratic and weakly correlated with market conditions. The fund is
typically closed or semi-closed, with no systematic inflow of new
capital, but its absence of binding obligations means that illiquid
positions can be held to maturity without penalty in most scenarios. The
penalty curve is the flattest of the three, reflecting the low
probability of forced selling and the flexibility to time exits
optimally.

## Subjective calibration and efficient frontiers

Following the approach of Hayes et al. (2015), each archetype is
assigned a set of power curve parameters $(\alpha, \beta)$ through
subjective calibration, based on the qualitative assessment of liquidity
needs described above. The complementary pension fund is assigned
$\alpha = 0.25$ and $\beta = 1.2$, reflecting its high baseline
sensitivity to illiquidity and its relatively uniform cost accumulation
across illiquidity levels. The university endowment is assigned
$\alpha = 0.12$ and $\beta = 2.0$, reflecting a lower baseline cost and
a more convex profile that rises steeply only at high illiquidity
levels. The family office is assigned $\alpha = 0.06$ and $\beta = 2.8$,
reflecting the lowest baseline sensitivity and the most convex profile,
with meaningful costs arising only when the portfolio is very heavily
committed to illiquid assets.

These subjective parametrizations serve two purposes. First, they
provide a set of benchmark curves against which the simulation-based
calibration of Section 6 can be evaluated. Second, they illustrate how
the penalty curve framework can be used even in the absence of a full
simulation, relying instead on the investment team's qualitative
assessment of the fund's liquidity profile. Figure
[5](#fig:archetype_curves){reference-type="ref"
reference="fig:archetype_curves"} shows the three penalty curves
alongside the unpenalized case.

<figure id="fig:archetype_curves" data-latex-placement="h">
<span class="image placeholder"
data-original-image-src="power_penalty_curves.png"
data-original-image-title="" width="75%"></span>
<figcaption>Power penalty curves for the three investor archetypes under
subjective calibration. Pension Fund: <span
class="math inline"><em>α</em> = 0.25</span>, <span
class="math inline"><em>β</em> = 1.2</span>. Endowment: <span
class="math inline"><em>α</em> = 0.12</span>, <span
class="math inline"><em>β</em> = 2.0</span>. Family Office: <span
class="math inline"><em>α</em> = 0.06</span>, <span
class="math inline"><em>β</em> = 2.8</span>.</figcaption>
</figure>

## Portfolio composition across archetypes

The three penalty curves produce meaningfully different efficient
frontiers and portfolio compositions, as illustrated in Figures
[6](#fig:archetype_frontiers){reference-type="ref"
reference="fig:archetype_frontiers"} and
[7](#fig:archetype_composition){reference-type="ref"
reference="fig:archetype_composition"}. The pension fund curve, being
the steepest, imposes the largest return drag and produces the most
conservative frontier: private equity is significantly reduced relative
to the unpenalized case, with the optimizer substituting toward global
aggregate fixed income and, to a lesser extent, global equity. The
family office curve, being the flattest, produces a frontier closest to
the unpenalized case, preserving a larger allocation to private equity
across the return spectrum.

A key observation is that the penalty curve does not simply scale down
the allocation to all illiquid assets uniformly. Rather, it reshapes the
composition of the illiquid bucket, reducing allocations to
lower-returning illiquid assets such as real estate more aggressively
than to higher-returning ones such as private equity. This reflects the
fact that the penalty raises the bar for illiquid investments: only
those with sufficiently high expected returns can justify the
illiquidity cost they impose on the portfolio. Assets that sit in an
intermediate zone, illiquid enough to incur a meaningful penalty but not
high-returning enough to compensate for it, are the first to be crowded
out by the optimization.

<figure id="fig:archetype_frontiers" data-latex-placement="h">
<span class="image placeholder"
data-original-image-src="power_frontiers.png"
data-original-image-title="" width="75%"></span>
<figcaption>Efficient frontiers for the three investor archetypes under
subjective calibration, alongside the unpenalized frontier.</figcaption>
</figure>

<figure id="fig:archetype_composition" data-latex-placement="h">
<span class="image placeholder"
data-original-image-src="power_composition.png"
data-original-image-title="" width="100%"></span>
<figcaption>Portfolio composition along the efficient frontier for the
three investor archetypes under subjective calibration.</figcaption>
</figure>

# Simulation-Based Calibration of the Penalty Curve

## Simulation philosophy: real portfolio versus liquid benchmark

The core idea of the simulation-based calibration is to estimate the
illiquidity cost curve empirically, by measuring the return drag that
illiquidity imposes on a portfolio across a range of illiquidity levels,
and then fitting a parametric penalty function to the simulated costs.
The approach is grounded in the observation that the illiquidity penalty
curve should reflect what actually happens to a portfolio subject to
lock-up constraints, payout obligations, and a minimum liquidity buffer,
rather than what an investor believes should happen based on qualitative
judgement alone.

The simulation compares two portfolios. The *real portfolio* holds the
same target weights as the benchmark but is subject to asset-specific
lock-up constraints: units of an asset purchased at time $t$ cannot be
reduced until their lock-up period expires. The *liquid benchmark* holds
the same target weights but faces no lock-up constraints: it rebalances
freely every year. Both portfolios are subject to identical return
shocks, drawn from the same multivariate normal distribution calibrated
to the Amundi Capital Market Assumptions, and both pay the same
stochastic payout $\delta_t$ each year. The benchmark meets the payout
obligation by selling any asset at fair value without friction, while
the real portfolio may be forced to liquidate locked positions on the
secondary market at a discount when liquid assets are insufficient to
cover the obligation.

The illiquidity cost in each simulation year is defined as the sum of
three components: the return gap between the benchmark and the real
portfolio arising from the inability to rebalance freely, the haircut
paid on forced sales of locked positions to restore the liquidity
buffer, and the haircut paid on locked positions liquidated to meet the
payout obligation. Averaging this cost across years and scenarios yields
an estimate $\hat{c}(L)$ of the annualised illiquidity cost for a
portfolio at illiquidity level $L$. Running the simulation across a grid
of illiquidity levels produces a set of point estimates that trace the
shape of the penalty curve.

## Target portfolios

For each illiquidity level $L$ in a grid ranging from $10\%$ to $70\%$,
a target portfolio $\mathbf{w}^*(L)$ is constructed by solving a
constrained mean-variance optimization: $$\begin{equation}
 \max_{\mathbf{w}} \quad \mathbf{w}^T \boldsymbol{\mu} - \frac{\gamma}{2} \mathbf{w}^T \boldsymbol{\Sigma} \mathbf{w}
\end{equation}$$ subject to $\mathbf{w}^T \mathbf{1} = 1$,
$\mathbf{w} \geq \mathbf{0}$, $\mathbf{w}^T \mathbf{l} = L$, and
$\sum_{i \in \mathcal{L}} w_i \geq w_{\min}^{\text{liq}}$, where
$\mathcal{L}$ denotes the set of liquid asset classes and
$w_{\min}^{\text{liq}}$ is the minimum liquid fraction required to be
held at all times. Both the risk aversion coefficient $\gamma$ and the
minimum liquidity buffer $w_{\min}^{\text{liq}}$ are calibrated to each
investor archetype, reflecting the differences in risk appetite and
regulatory or self-imposed liquidity requirements across investor types.
Specifically, the pension fund is assigned $\gamma = 5$ and
$w_{\min}^{\text{liq}} = 40\%$, consistent with its conservative
investment mandate and the regulatory requirement to maintain a
significant liquid reserve to meet near-term benefit payments. The
endowment is assigned $\gamma = 3$ and $w_{\min}^{\text{liq}} = 30\%$,
reflecting an intermediate risk tolerance and a liquidity buffer
sufficient to cover the annual spending distribution without forced
selling in most scenarios. The family office is assigned $\gamma = 2$
and $w_{\min}^{\text{liq}} = 20\%$, consistent with its growth-oriented
objective and the absence of binding contractual liquidity obligations.

A target portfolio is retained only if it satisfies three validity
conditions jointly. First, the realised portfolio illiquidity level must
be within two percentage points of the target $L$. Second, the liquid
fraction must meet or exceed $w_{\min}^{\text{liq}}$. Third, the
portfolio volatility must not exceed 1.5 times the volatility of the
preceding valid portfolio in the grid, a filter designed to exclude
degenerate solutions in which the optimizer concentrates the portfolio
in a single high-volatility illiquid asset class to meet the illiquidity
constraint. Portfolios that fail any of these conditions are discarded
and the corresponding $L$ level is excluded from the simulation. The
composition of the retained target portfolios for each archetype is
shown in the right panel of Figures
[8](#fig:fit_pension){reference-type="ref" reference="fig:fit_pension"},
[9](#fig:fit_endowment){reference-type="ref"
reference="fig:fit_endowment"}, and
[10](#fig:fit_family){reference-type="ref" reference="fig:fit_family"}.

## Portfolio accounting and lock-up constraints

The real portfolio is tracked through a system of tranches. Each
purchase of an asset is recorded as a separate tranche, identified by
the asset class, the weight at the time of purchase, and the year of
purchase. A tranche is considered locked if the number of years elapsed
since purchase is strictly less than the asset class-specific lock-up
period. The lock-up periods and secondary market haircuts used in the
simulation are reported in Table [3](#tab:lockup){reference-type="ref"
reference="tab:lockup"}.

::: {#tab:lockup}
  Asset class    Lock-up (years)   Haircut
  ------------- ----------------- ---------
  MM_US                 0           0.1%
  GLOB_AGG              0           0.5%
  GLOB_EQ               0           2.0%
  HF_FOF                2           8.0%
  GLOB_RE               5           12.0%
  GLOB_PE               8           20.0%

  : Asset-specific lock-up periods and secondary market haircuts used in
  the simulation.
:::

At the start of each simulation, the portfolio is initialised at the
target weights with all tranches assigned to year zero, so that no
position is locked at inception. In each subsequent year, the simulation
proceeds through the following sequence of operations: market returns
are drawn and applied to all tranche weights proportionally; the
stochastic payout is drawn and distributed across all tranches; if the
liquid fraction falls below the minimum buffer $w_{\min}^{\text{liq}}$,
forced sales are executed to restore it; the illiquidity cost for the
year is recorded; and finally the portfolio is rebalanced toward the
target weights subject to lock-up constraints.

The rebalancing step solves a constrained quadratic program that
minimizes the squared deviation from target weights, subject to the
constraint that no locked tranche weight can be reduced and that the
liquid fraction remains above $w_{\min}^{\text{liq}}$. New purchases are
recorded as new tranches with the current year as their vintage.

## Payout, haircuts and liquidity buffer

At each time step, the portfolio must distribute a fraction $\delta_t$
of its value to satisfy the payout obligation: the payout is distributed
proportionally across all asset classes, regardless of their liquidity
status. For tranches that are freely tradeable, the weight is reduced
without any additional cost. For locked tranches, the same proportional
reduction is applied, but since the asset cannot be sold at fair value,
the actual gross amount that must be liquidated exceeds the payout quota
by a factor of $(1 - h_i)^{-1}$, where $h_i$ is the secondary market
haircut for asset class $i$ reported in Table
[3](#tab:lockup){reference-type="ref" reference="tab:lockup"}. The
difference between the gross amount liquidated and the net proceeds is
recorded as a payout haircut cost.

After the payout, the liquid fraction of the portfolio is checked
against the minimum buffer $w_{\min}^{\text{liq}}$. If the liquid
fraction falls below this threshold, the portfolio executes forced sales
to restore it. The restoration procedure follows a priority rule: freely
tradeable illiquid positions are sold first, without haircut; if these
are insufficient, locked illiquid positions are sold with the
corresponding secondary market haircut. The proceeds from forced sales
are allocated to liquid asset classes in proportion to their target
weights. The haircut paid during forced sales is recorded as a liquidity
buffer restoration cost. The minimum liquidity buffer therefore plays a
dual role in the simulation: it governs the composition of the target
portfolios through the constrained MVO, and it determines the frequency
and magnitude of forced sales during the simulation, both of which feed
directly into the estimated illiquidity cost.

## Stochastic payout process: motivation and parametrization

A central feature of the simulation is that the annual payout rate
$\delta_t$ is not fixed but follows a stochastic process. This reflects
the observation that, in practice, the payout demands of institutional
investors are neither constant nor independent of market conditions. A
pension fund facing adverse returns is more likely to receive early
withdrawal requests from members; a university endowment may be called
upon to increase its spending distribution when the institution faces
budgetary shortfalls; and a family office may alter its payout in
response to the needs of its beneficiaries. The correlation between
payout shocks and market returns is therefore a structural feature of
the investor's liquidity profile, and its omission would lead to an
underestimate of the true illiquidity cost, particularly at high
illiquidity levels where the two effects compound.

The payout process is specified as an AR(1) model correlated with the
standardised return shock of GLOB_EQ:

$$\begin{equation}
 \delta_t = \mathrm{clip}\!\left( \bar{\delta} + \rho_{\mathrm{AR}}\,(\delta_{t-1} - \bar{\delta}) + \eta_t,\; \delta_{\min},\,\delta_{\max} \right)
\end{equation}$$

where the innovation term $\eta_t$ is defined as:

$$\begin{equation}
 \eta_t = \sigma_\delta\!\left(\rho\, z_t^{\mathrm{EQ}} + \sqrt{1 - \rho^2}\,\varepsilon_t\right)
\end{equation}$$

with $z_t^{\mathrm{EQ}} \sim \mathcal{N}(0,1)$ the standardised
independent shock drawn for GLOB_EQ,
$\varepsilon_t \sim \mathcal{N}(0,1)$ an independent idiosyncratic
shock, $\sigma_\delta > 0$ the payout volatility, and $\rho \in [-1,1]$
the target correlation between the payout innovation and the equity
market shock..

The form of $\eta_t$ is chosen to satisfy two properties simultaneously.
First, since $z_t^{\mathrm{EQ}}$ and $\varepsilon_t$ are independent
standard normals, the variance of the term in parentheses is:

$$\begin{equation}
 \mathrm{Var}\!\left(\rho\, z_t^{\mathrm{EQ}} + \sqrt{1-\rho^2}\,\varepsilon_t\right) = \rho^2 + (1 - \rho^2) = 1
\end{equation}$$

so that $\eta_t \sim \mathcal{N}(0, \sigma_\delta^2)$ exactly, with
$\sigma_\delta$ being the standard deviation of the payout innovation
regardless of the value of $\rho$. Second, the correlation between
$\eta_t$ and $z_t^{\mathrm{EQ}}$ is exactly $\rho$:

$$\begin{equation}
 \mathrm{Corr}(\eta_t,\, z_t^{\mathrm{EQ}}) = \frac{\mathrm{Cov}(\sigma_\delta \rho\, z_t^{\mathrm{EQ}},\, z_t^{\mathrm{EQ}})}{\sigma_\delta \cdot 1} = \rho
\end{equation}$$

This construction is the bivariate Cholesky decomposition: it builds a
normal random variable with prescribed variance $\sigma_\delta^2$ and
prescribed correlation $\rho$ with $z_t^{\mathrm{EQ}}$, without
distorting either property as $\rho$ varies.

The parameter $\rho_{\mathrm{AR}}$ controls the persistence of payout
shocks: a high value implies that an elevated payout in one year is
likely to be followed by elevated payouts in subsequent years,
reflecting the clustered nature of pension retirements or endowment
spending pressures. The parameter $\rho$ controls the direction and
strength of the co-movement between payout and market conditions: a
negative value, as used for all three archetypes, implies that payouts
tend to increase precisely when equity markets fall, amplifying the
liquidity stress at the worst possible moment.

The parameters of the payout process are calibrated separately for each
investor archetype, drawing on the empirical literature and the
qualitative characterisation of Section 5.3. The calibration is
summarised in Table [4](#tab:payout_params){reference-type="ref"
reference="tab:payout_params"}. For the complementary pension fund,
$\bar{\delta} = 10\%$ is consistent with aggregate distribution rates
observed in Italian complementary pension funds (COVIP, 2022), which
include pension payments, anticipations, and redemptions. The
persistence parameter $\rho_{\mathrm{AR}} = 0.65$ reflects the
demographic nature of outflows, which tend to concentrate in multi-year
retirement waves with a half-life of approximately two years. The
correlation $\rho = -0.60$ captures the behavioural tendency of fund
members to request early redemptions during periods of market stress, as
documented by Dyck and Pomorski (2011) in the context of defined benefit
funds. For the university endowment, $\bar{\delta} = 5\%$ follows the
canonical value documented in the NACUBO and TIAA Study of Endowments
(2019--2023), with lower persistence ($\rho_{\mathrm{AR}} = 0.55$) and
weaker equity correlation ($\rho = -0.35$) reflecting the partial
decoupling of distributions from short-term market conditions induced by
multi-year smoothing rules. For the family office, $\bar{\delta} = 4\%$
is consistent with wealth-preservation-oriented distribution policies
(Ang, Papanikolaou and Westerfield, 2013), with low persistence
($\rho_{\mathrm{AR}} = 0.35$) and weak equity correlation
($\rho = -0.20$) reflecting the predominantly idiosyncratic nature of
beneficiary liquidity demands (Anson, 2010).

::: {#tab:payout_params}
  Archetype        $\bar{\delta}$   $\sigma_\delta$   $\rho_{\mathrm{AR}}$            $\rho$            $\delta_{\min}$   $\delta_{\max}$
  --------------- ---------------- ----------------- ---------------------- -------------------------- ----------------- -----------------
  Pension Fund          10%              2.5%                 0.65           $-$`<!-- -->`{=html}0.60         3%                18%
  Endowment              5%              1.5%                 0.55           $-$`<!-- -->`{=html}0.35         2%                9%
  Family Office          4%              2.0%                 0.35           $-$`<!-- -->`{=html}0.20         0%                10%

  : Payout process parameters by investor archetype.
:::

It should be noted that the parameters $\rho$ and $\rho_{\mathrm{AR}}$
are not estimated econometrically from the cited literature, but are
calibrated for consistency with the empirical patterns documented
therein. A direct econometric estimation would require time series of
archetype-specific payout rates regressed on equity returns, and
represents a natural extension of the present analysis.

## Estimating the simulated cost curve

For each target portfolio $\mathbf{w}^*(L)$ and each archetype, the
simulation is run over $N = 1{,}000$ independent scenarios of $T = 20$
years. In each year $t$, a vector of independent standard normal shocks
$\mathbf{z}_t \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$ is drawn. Asset
class returns are then computed as: $$\begin{equation}
 \mathbf{r}_t = \boldsymbol{\mu} + \mathbf{C} \mathbf{z}_t
\end{equation}$$ where $\mathbf{C}$ is the lower Cholesky factor of
$\boldsymbol{\Sigma}$, so that
$\mathbf{r}_t \sim \mathcal{N}(\boldsymbol{\mu}, \boldsymbol{\Sigma})$.
The standardised shock $z_t^{\mathrm{EQ}}$, the component of
$\mathbf{z}_t$ corresponding to GLOB_EQ, is then passed directly to the
payout process of equation (24), so that the co-movement between payout
innovations and equity returns is imposed by construction.

The annualised illiquidity cost for scenario $s$ at illiquidity level
$L$ is defined as the time-average of the annual costs:

$$\begin{equation}
 \hat{c}_s(L) = \frac{1}{T} \sum_{t=1}^{T} \left[ (r_t^{\text{bench}} - r_t^{\text{real}}) + \mathrm{HC}_t^{\text{buffer}} + \mathrm{HC}_t^{\text{payout}} \right]
\end{equation}$$

where $r_t^{\text{bench}}$ is the return of the liquid benchmark in year
$t$, $r_t^{\text{real}}$ is the return of the real portfolio computed on
the tranche weights prior to rebalancing,
$\mathrm{HC}_t^{\text{buffer}}$ is the haircut paid to restore the
liquidity buffer, and $\mathrm{HC}_t^{\text{payout}}$ is the haircut
paid on locked positions liquidated to meet the payout obligation. The
point estimate of the illiquidity cost at level $L$ is then the
cross-sectional average:

$$\begin{equation}
 \hat{c}(L) = \frac{1}{N} \sum_{s=1}^{N} \hat{c}_s(L)
\end{equation}$$

The benchmark return in year $t$ is computed on the post-drift weights
of a frictionless portfolio that holds the same target weights and
rebalances freely each period, ensuring that the cost measure captures
the drag attributable to lock-up constraints and forced sales, net of
the return effect of market drift alone. The real portfolio return is
computed before the rebalancing step, so that the rebalancing cost is
included in the measurement rather than neutralised by the optimization.

It is important to note the economic interpretation of $\hat{c}(L)$.
This quantity is a *total* portfolio cost: it measures the average
annual return drag that a portfolio held at illiquidity level $L$ bears
relative to its frictionless counterpart, summing across all sources of
cost. It is not a marginal cost in the sense of Hayes et al. (2015), and
it cannot be used directly as the marginal penalty curve $c(L)$ in the
penalized MVO. Rather, $\hat{c}(L)$ corresponds to the ratio $T(L)/L$ in
the framework of Section 2: the average accumulated penalty per unit of
portfolio illiquidity. This observation motivates the fitting procedure
described in the following section.

## Fitting the penalty function and parameter recovery

The simulation produces a set of point estimates
$\{(L_k,\, \hat{c}(L_k))\}$ for $k = 1, \ldots, K$. Since $\hat{c}(L)$
estimates the average accumulated penalty $T(L)/L$, the corresponding
estimates of the accumulated penalty are:

$$\begin{equation}
 \hat{T}(L_k) = \hat{c}(L_k) \cdot L_k
\end{equation}$$

We fit a power function to these accumulated penalty estimates:

$$\begin{equation}
 T(L) = A \cdot L^{B}
\end{equation}$$

by nonlinear least squares, minimising
$\sum_k (\hat{T}(L_k) - A \cdot L_k^B)^2$ over $(A, B)$ with constraints
$A > 0$ and $B > 1$. The power specification is a natural choice here
for two reasons. First, as discussed in Section 4, it satisfies all the
desirable analytical properties of a penalty function. Second, and more
importantly, the integral of a power marginal cost curve
$c(L) = \alpha \cdot L^{\beta}$ is itself a power function:

$$\begin{equation}
 T(L) = \int_0^L c(x)\, dx = \frac{\alpha}{\beta + 1} \cdot L^{\beta+1}
\end{equation}$$

which means that fitting $T(L) = A \cdot L^B$ directly to the simulated
accumulated penalties is equivalent to fitting a power marginal cost
curve. The parameters of the marginal cost curve are then recovered
analytically from the fitted coefficients:

$$\begin{equation}
 \beta = B - 1, \qquad \alpha = A \cdot B
\end{equation}$$

so that $c(L) = \alpha \cdot L^{\beta}$ and
$T(L) = \frac{\alpha}{\beta+1} \cdot L^{\beta+1}$, consistent with the
power specification of Section 4. This recovery is exact by
construction: the constraint $A = \alpha/(\beta+1)$ is satisfied
identically. The lower bound $B > 1$ ensures that the recovered marginal
cost $c(L) = \alpha \cdot L^{\beta}$ is strictly increasing in $L$,
consistent with the convexity requirement of Section 4. The quality of
the fit is assessed by the coefficient of determination $R^2$ computed
on the $\hat{T}$ values.

## Results across archetypes

The simulation is run independently for each of the three investor
archetypes, using the payout parameters of Table
[4](#tab:payout_params){reference-type="ref"
reference="tab:payout_params"}, the asset-specific lock-up and haircut
parameters of Table [3](#tab:lockup){reference-type="ref"
reference="tab:lockup"}, and the archetype-specific risk aversion and
minimum liquidity buffer reported in Table
[5](#tab:archetype_params){reference-type="ref"
reference="tab:archetype_params"}. The results are summarised in Table
[6](#tab:fit_results){reference-type="ref" reference="tab:fit_results"}
and illustrated in Figures [8](#fig:fit_pension){reference-type="ref"
reference="fig:fit_pension"},
[9](#fig:fit_endowment){reference-type="ref"
reference="fig:fit_endowment"}, and
[10](#fig:fit_family){reference-type="ref" reference="fig:fit_family"}.

::: {#tab:archetype_params}
  Archetype        $\gamma$   $w_{\min}^{\text{liq}}$
  --------------- ---------- -------------------------
  Pension Fund        5                 40%
  Endowment           3                 30%
  Family Office       2                 20%

  : Risk aversion coefficient and minimum liquidity buffer by investor
  archetype, used in both the target portfolio construction and the
  simulation.
:::

::: {#tab:fit_results}
  Archetype         $A$      $B$     $\alpha$   $\beta$   $R^2$   
  --------------- -------- -------- ---------- --------- -------- --
  Pension Fund     0.0359   3.6388    0.1305    2.6388    0.9961  
  Endowment        0.0288   5.1577    0.1484    4.1577    0.9870  
  Family Office    0.0055   2.7313    0.0150    1.7313    0.9970  

  : Fitted penalty function parameters by investor archetype. $A$ and
  $B$ are the nonlinear least squares estimates of $T(L) = A \cdot L^B$;
  $\alpha = AB$ and $\beta = B - 1$ are the recovered parameters of the
  marginal cost curve $c(L) = \alpha \cdot L^{\beta}$.
:::

The fit quality is high across all three archetypes, with $R^2$ values
ranging from 0.987 to 0.997, confirming that the power function provides
an adequate description of the simulated cost curve over the range of
illiquidity levels considered.

The results reveal a clear and economically intuitive ordering: the
pension fund bears the highest costs at any given illiquidity level, the
endowment presents the most convex profile with costs that are
negligible at low illiquidity levels but accelerate sharply above a
threshold, and the family office exhibits the mildest and most gradually
accumulating penalty. This ordering reflects directly the differences in
payout demand, market correlation, risk aversion, and minimum liquidity
buffer calibrated for each archetype, and is consistent with the
qualitative ranking established in Section 5. The most notable
divergence from the subjective parametrization of Section 5 concerns the
curvature parameter: the simulated $\beta$ values are systematically
higher than their subjective counterparts for the pension fund and
endowment, indicating that the simulation assigns a more convex cost
profile than qualitative judgement alone would suggest, particularly at
high illiquidity levels where forced selling becomes frequent and the
interaction between payout shocks and lock-up constraints amplifies the
cost nonlinearly.

<figure id="fig:fit_pension" data-latex-placement="h">
<img src="./Fit_Fondo_Pensione_13_264.png" />
<figcaption>Simulated illiquidity costs and fitted penalty curve for the
Pension Fund archetype (<span class="math inline"><em>γ</em> = 5</span>,
<span
class="math inline"><em>w</em><sub>min</sub><sup>liq</sup> = 40%</span>).
Left panel: accumulated penalty <span
class="math inline"><em>T̂</em>(<em>L</em>) = <em>ĉ</em>(<em>L</em>) ⋅ <em>L</em></span>
at each illiquidity level (dots) and fitted power function <span
class="math inline"><em>T</em>(<em>L</em>) = 0.0359 ⋅ <em>L</em><sup>3.6388</sup></span>
(<span class="math inline"><em>R</em><sup>2</sup> = 0.996</span>). Right
panel: composition of the target portfolios used in the simulation at
each illiquidity level. Simulation parameters: <span
class="math inline"><em>δ̄</em> = 10%</span>, <span
class="math inline"><em>σ</em><sub><em>δ</em></sub> = 2.5%</span>, <span
class="math inline"><em>ρ</em><sub>AR</sub> = 0.65</span>, <span
class="math inline"><em>ρ</em> = −0.60</span>, <span
class="math inline"><em>T</em> = 20</span> years, <span
class="math inline"><em>N</em> = 1, 000</span> scenarios.</figcaption>
</figure>

<figure id="fig:fit_endowment" data-latex-placement="h">
<img src="./Fit_Endowment_15_416.png" />
<figcaption>Simulated illiquidity costs and fitted penalty curve for the
Endowment archetype (<span class="math inline"><em>γ</em> = 3</span>,
<span
class="math inline"><em>w</em><sub>min</sub><sup>liq</sup> = 30%</span>).
Left panel: accumulated penalty <span
class="math inline"><em>T̂</em>(<em>L</em>)</span> (dots) and fitted
power function <span
class="math inline"><em>T</em>(<em>L</em>) = 0.0288 ⋅ <em>L</em><sup>5.1577</sup></span>
(<span class="math inline"><em>R</em><sup>2</sup> = 0.987</span>). Right
panel: composition of the target portfolios at each illiquidity level.
Simulation parameters: <span class="math inline"><em>δ̄</em> = 5%</span>,
<span class="math inline"><em>σ</em><sub><em>δ</em></sub> = 1.5%</span>,
<span class="math inline"><em>ρ</em><sub>AR</sub> = 0.55</span>, <span
class="math inline"><em>ρ</em> = −0.35</span>, <span
class="math inline"><em>T</em> = 20</span> years, <span
class="math inline"><em>N</em> = 1, 000</span> scenarios.</figcaption>
</figure>

<figure id="fig:fit_family" data-latex-placement="h">
<img src="./Fit_Family_Office_1_173.png" />
<figcaption>Simulated illiquidity costs and fitted penalty curve for the
Family Office archetype (<span
class="math inline"><em>γ</em> = 2</span>, <span
class="math inline"><em>w</em><sub>min</sub><sup>liq</sup> = 20%</span>).
Left panel: accumulated penalty <span
class="math inline"><em>T̂</em>(<em>L</em>)</span> (dots) and fitted
power function <span
class="math inline"><em>T</em>(<em>L</em>) = 0.0055 ⋅ <em>L</em><sup>2.7313</sup></span>
(<span class="math inline"><em>R</em><sup>2</sup> = 0.997</span>). Right
panel: composition of the target portfolios at each illiquidity level.
Simulation parameters: <span class="math inline"><em>δ̄</em> = 4%</span>,
<span class="math inline"><em>σ</em><sub><em>δ</em></sub> = 2.0%</span>,
<span class="math inline"><em>ρ</em><sub>AR</sub> = 0.35</span>, <span
class="math inline"><em>ρ</em> = −0.20</span>, <span
class="math inline"><em>T</em> = 20</span> years, <span
class="math inline"><em>N</em> = 1, 000</span> scenarios.</figcaption>
</figure>

# Penalized MVO: Results and Portfolio Implications

## Penalized versus unpenalized efficient frontiers

The simulation-calibrated penalty curves derived in Section 6 are used
as inputs to the penalized mean-variance optimization of Section 2.4.
For each archetype, the resulting penalized frontier is compared to the
unpenalized frontier obtained by solving the standard Markowitz problem
on the same asset universe and Capital Market Assumptions. Figures
[11](#fig:front_pension_7){reference-type="ref"
reference="fig:front_pension_7"},
[12](#fig:front_endowment_7){reference-type="ref"
reference="fig:front_endowment_7"}, and
[13](#fig:front_family_7){reference-type="ref"
reference="fig:front_family_7"} report both frontiers in two
representations: the left panel shows the efficient frontier in the
standard volatility-return space, while the right panel shows the net
return frontier $\hat{\mu}_P = \mu_P - T(L)$, obtained by subtracting
the accumulated illiquidity penalty from the gross expected return.

In \"gross\" return space, the penalized frontier lies below the
unpenalized one at high volatility levels and caps out at a lower
maximum return, reflecting the fact that the penalty discourages the
optimizer from concentrating the portfolio in private equity beyond the
point where the marginal illiquidity cost exceeds the return benefit.
The shift is not parallel: at low volatility levels the two frontiers
coincide, since both optimizers allocate predominantly to liquid asset
classes where $T(L)$ is negligible, and the divergence widens
progressively as the target return and illiquidity level increase.

The net return frontier provides the economically relevant comparison.
It measures what an investor actually expects to retain after accounting
for the return drag of illiquidity, and it is in this representation
that the penalized frontier dominates the unpenalized one across all
three archetypes. An investor who ignores illiquidity costs builds
portfolios with high gross returns but also high illiquidity levels,
incurring a large accumulated penalty $T(L)$ that erodes the net return.
The unpenalized net return frontier therefore turns hump-shaped and
eventually declines at high volatility levels, while the penalized net
return frontier remains monotonically increasing or only mildly concave.
The dominance of the penalized frontier in net return space is the
central economic result of the framework: it quantifies the value
created by pricing illiquidity correctly.

The magnitude of this dominance differs across archetypes in line with
the calibrated penalty parameters. The pension fund and endowment
exhibit the largest gap: for the pension fund the unpenalized net return
peaks around 12% volatility and then declines sharply to approximately
6.5%, while the penalized frontier delivers above 8% net return at the
same point, with a gap exceeding 150 basis points. For the endowment the
divergence is concentrated in the high-volatility region, consistent
with the highly convex penalty ($\beta = 4.1577$) that is negligible
below a threshold and then accelerates rapidly. The family office
presents frontiers that are nearly indistinguishable in both
representations, consistent with its very low $\alpha = 0.0150$: for
this archetype the unpenalized MVO provides a close approximation of the
optimal allocation in net return terms.

<figure id="fig:front_pension_7" data-latex-placement="h">
<img src="./Sim_front_Fondo_Pensione_13_264.png" />
<figcaption>Penalized versus unpenalized efficient frontier for the
Pension Fund archetype (<span
class="math inline"><em>α</em> = 0.1305</span>, <span
class="math inline"><em>β</em> = 2.6388</span>). Left panel: gross
return frontier. Right panel: net return frontier <span
class="math inline"><em>μ̂</em><sub><em>P</em></sub> = <em>μ</em><sub><em>P</em></sub> − <em>T</em>(<em>L</em>)</span>.</figcaption>
</figure>

<figure id="fig:front_endowment_7" data-latex-placement="h">
<img src="./Sim_front_Endowment_15_416.png" />
<figcaption>Penalized versus unpenalized efficient frontier for the
Endowment archetype (<span
class="math inline"><em>α</em> = 0.1484</span>, <span
class="math inline"><em>β</em> = 4.1577</span>). Left panel: gross
return frontier. Right panel: net return frontier <span
class="math inline"><em>μ̂</em><sub><em>P</em></sub> = <em>μ</em><sub><em>P</em></sub> − <em>T</em>(<em>L</em>)</span>.</figcaption>
</figure>

<figure id="fig:front_family_7" data-latex-placement="h">
<img src="./Sim_front_Family_Office_1_173.png" />
<figcaption>Penalized versus unpenalized efficient frontier for the
Family Office archetype (<span
class="math inline"><em>α</em> = 0.0150</span>, <span
class="math inline"><em>β</em> = 1.7313</span>). Left panel: gross
return frontier. Right panel: net return frontier <span
class="math inline"><em>μ̂</em><sub><em>P</em></sub> = <em>μ</em><sub><em>P</em></sub> − <em>T</em>(<em>L</em>)</span>.</figcaption>
</figure>

## Portfolio composition along the frontier

The effect of the penalty curve on portfolio composition is illustrated
in Figures [14](#fig:comp_pension_7){reference-type="ref"
reference="fig:comp_pension_7"},
[15](#fig:comp_endowment_7){reference-type="ref"
reference="fig:comp_endowment_7"}, and
[16](#fig:comp_family_7){reference-type="ref"
reference="fig:comp_family_7"}. In all three cases, the unpenalized
composition follows the same pattern: as the target return increases,
the optimizer progressively substitutes GLOB_AGG and MM_US with GLOB_PE,
which dominates the portfolio at high return levels due to its superior
expected return of 9.80% and its high correlation with the other equity
asset classes, making it the preferred representative of the equity risk
factor. The introduction of the penalty curve materially reshapes this
picture, though the degree of reshaping varies across archetypes in line
with the aggressiveness of the calibrated curve. The penalty does not
eliminate private equity from the optimal portfolio: its return
advantage over liquid alternatives is too large for that. Rather, it
raises the hurdle rate for illiquid investments, creating space for
GLOB_EQ to play a larger role as a liquid substitute for the equity risk
factor at intermediate return targets, and caps the maximum attainable
return below the unpenalized frontier at the point where the marginal
illiquidity cost of adding further private equity exceeds the return
benefit.

The simulation-calibrated compositions differ in an important way from
those produced by the subjective parametrizations of Section 5.5. The
simulated curves have systematically higher $\beta$ for the pension fund
and endowment --- $\beta = 2.64$ versus $1.2$ and $\beta = 4.16$ versus
$2.0$ respectively --- which implies a penalty that is less aggressive
at moderate illiquidity levels but accelerates more sharply at high
ones. As a result, the penalized compositions under the simulated curves
are closer to the unpenalized case at intermediate return targets and
more conservative only at the high end of the frontier, while the
subjective calibration produces a broader and more gradual reduction in
private equity allocations across the entire return spectrum. For the
family office the two calibrations are closer in spirit, though the
simulated $\alpha = 0.015$ is substantially lower than the subjective
$\alpha = 0.06$, producing compositions that are nearly
indistinguishable from the unpenalized case throughout.

These patterns are visible across the three archetypes. The pension fund
penalized composition shows the most pronounced reshaping: GLOB_EQ
emerges as a meaningful component at high return levels, absorbing part
of the equity exposure that would otherwise go to GLOB_PE, and the
maximum attainable return caps at approximately 8.5%. The endowment
displays a distinctive pattern driven by its high $\beta$: below the
threshold illiquidity level the penalized and unpenalized compositions
are nearly identical, but above it GLOB_EQ appears abruptly as a
significant component, displacing GLOB_PE in a way that reflects the
sudden acceleration of the convex penalty. The family office composition
is the closest to the unpenalized case, with GLOB_PE dominating at high
return levels in both scenarios and only a marginal increase in GLOB_AGG
at intermediate return targets, consistent with the small magnitude of
the calibrated penalty.

<figure id="fig:comp_pension_7" data-latex-placement="h">
<img src="./Sim_comp_Fondo_Pensione_13_264.png" />
<figcaption>Portfolio composition along the penalized and unpenalized
efficient frontier for the Pension Fund archetype (<span
class="math inline"><em>α</em> = 0.1305</span>, <span
class="math inline"><em>β</em> = 2.6388</span>).</figcaption>
</figure>

<figure id="fig:comp_endowment_7" data-latex-placement="h">
<img src="./Sim_comp_Endowment_15_416.png" />
<figcaption>Portfolio composition along the penalized and unpenalized
efficient frontier for the Endowment archetype (<span
class="math inline"><em>α</em> = 0.1484</span>, <span
class="math inline"><em>β</em> = 4.1577</span>).</figcaption>
</figure>

<figure id="fig:comp_family_7" data-latex-placement="h">
<img src="./Sim_comp_Family_Office_1_173.png" />
<figcaption>Portfolio composition along the penalized and unpenalized
efficient frontier for the Family Office archetype (<span
class="math inline"><em>α</em> = 0.0150</span>, <span
class="math inline"><em>β</em> = 1.7313</span>).</figcaption>
</figure>

# Conclusions

## Summary of contributions

This thesis has addressed a central gap in the practical application of
the Hayes, Primbs and Chiquoine (2015) penalty cost framework for
strategic asset allocation with illiquid asset classes: the
identification of the marginal illiquidity penalty curve. While the
framework provides an elegant and economically intuitive extension of
the Markowitz mean-variance optimization, its original formulation
leaves the specification of the penalty curve to subjective judgement,
limiting its replicability and its credibility as a tool for rigorous
institutional decision-making.

The first contribution of this thesis is a simulation-based calibration
methodology that grounds the penalty curve in portfolio-level simulation
rather than qualitative assessment. The methodology models a portfolio
subject to asset-specific lock-up constraints, a minimum liquidity
buffer, and a stochastic payout obligation, and measures the return drag
that illiquidity imposes relative to a frictionless liquid benchmark
across a grid of illiquidity levels. The simulated cost estimates are
then used to fit a power penalty function, recovering the parameters of
the marginal cost curve through nonlinear least squares. The power
specification is shown to be analytically convenient, economically
well-behaved, and numerically stable, and the fit quality is high across
all three archetypes considered, with $R^2$ values ranging from 0.987 to
0.997.

The second contribution is a systematic mapping between investor
archetypes and penalty curve parameters. Three institutional investor
types are defined, a complementary pension fund, a university endowment,
and a family office, each characterised by a distinct payout process,
liquidity buffer, and risk aversion coefficient. The simulation produces
calibrated penalty curves that differ meaningfully across archetypes in
both level and curvature, reflecting genuine differences in liquidity
needs and the associated costs of holding illiquid assets. The
calibrated curves are then used to solve the penalized MVO, producing
efficient frontiers and optimal portfolio allocations that reflect each
investor's true liquidity preferences. In net return space, the
penalized frontier dominates the unpenalized one across all archetypes,
with the dominance most pronounced for the pension fund and endowment,
where the combination of high payout demand, countercyclical
correlation, and binding liquidity constraints generates substantial
illiquidity costs at high portfolio illiquidity levels.

## Limitations and future work

Several limitations of the present framework point to natural directions
for future research.

The simulation relies on a multivariate normal distribution for asset
returns, which abstracts from fat tails, return asymmetries, and the
time-varying volatility that characterise real asset markets. Extending
the return generation process to accommodate these features, for
instance through a regime-switching or stochastic volatility model,
would produce more realistic estimates of the illiquidity cost in stress
scenarios, where forced selling is most likely and most costly.

A second limitation concerns the liability side of the portfolio. In the
present framework, investor heterogeneity is captured through the payout
process and the minimum liquidity buffer, which are calibrated
separately for each archetype. A natural extension would be to model the
asset-liability structure explicitly, distinguishing investors by their
duration gap and funding ratio. A pension fund with a large duration gap
between assets and liabilities faces a different sensitivity to interest
rate movements than one that is well-matched, and this difference feeds
directly into the probability of binding liquidity constraints and
therefore into the shape of the penalty curve. In this richer setting,
the penalty curve would become a function not only of portfolio
illiquidity but also of the investor's balance sheet position, providing
a more complete and investor-specific characterisation of illiquidity
costs.

A third direction for future work concerns the empirical identification
of the penalty curve from observed data, rather than from simulation.
Given a sufficiently rich panel of institutional portfolios with varying
degrees of illiquidity, one could estimate the illiquidity cost curve
directly from observed proxies, such as management costs, secondary
market transaction records, or realised return gaps between liquid and
illiquid portfolios held by the same investor at different points in
time. Regressing these cost proxies on portfolio illiquidity levels
across investors would yield an econometric estimate of the penalty
curve that is grounded in observed behaviour rather than simulated
scenarios, providing an independent validation of the simulation-based
approach developed in this thesis and a natural benchmark for the
calibrated curves.

::: thebibliography
99 Amundi Investment Institute (2026). *Capital Market Assumptions
2026*. Amundi Asset Management, Paris. Ang, A., and Bollen, N.P.B.
(2010). Locked Up by a Lockup: Valuing Liquidity as a Real Option.
*Financial Management*, 39(3), 1069--1096. Ang, A., Papanikolaou, D.,
and Westerfield, M.M. (2014). Portfolio Choice with Illiquid Assets.
*Management Science*, 60(11), 2737--2761. Anson, M. (2010). Measuring a
Premium for Liquidity Risk. *The Journal of Private Equity*, 13(2),
6--16. COVIP (2022). *Annual Report 2022*. Commissione di Vigilanza sui
Fondi Pensione, Rome. Derman, E. (2007). A Simple Model for the Expected
Premium for Hedge Fund Lockups. *The Journal of Investment Management*,
5(3), 5--15. Dyck, A., and Pomorski, L. (2011). Is Bigger Better? Size
and Performance in Pension Plan Management. *Rotman School of Management
Working Paper*. University of Toronto. Golts, M., and Kritzman, M.
(2010). Liquidity Options. *The Journal of Derivatives*, 18(1), 80--89.
Hayes, M., Primbs, J.A., and Chiquoine, B. (2015). A Penalty Cost
Approach to Strategic Asset Allocation with Illiquid Asset Classes. *The
Journal of Portfolio Management*, 41(2), 33--41. Hill, J. (2009). A
Perspective on Liquidity Risk and Horizon Uncertainty. *The Journal of
Portfolio Management*, 35(4), 60--68. Kinlaw, W., Kritzman, M., and
Turkington, D. (2013). Liquidity and Portfolio Choice: A Unified
Approach. *The Journal of Portfolio Management*, 39(2), 19--27. Lee, J.
(2012). *Dynamic Portfolio Management with Private Equity Funds*. PhD
Thesis, Stanford University, Palo Alto, CA. Lo, A., Petrov, C., and
Wierzbicki, M. (2003). It's 11 p.m.---Do You Know Where Your Liquidity
Is? The Mean-Variance-Liquidity Frontier. *The Journal of Investment
Management*, 1(1), 55--93. Markowitz, H. (1952). Portfolio Selection.
*Journal of Finance*, 7(1), 77--91. Mulvey, J., Pauling, W., and Madey,
R. (2003). Advantages of Multiperiod Portfolio Models. *The Journal of
Portfolio Management*, 29(2), 35--45. NACUBO--TIAA (2023). *Study of
Endowments 2022--2023*. National Association of College and University
Business Officers, Washington, DC. Preqin (2025). *Institutional
Allocation Study 2025*. Preqin Ltd., London. Takahashi, D., and
Alexander, S. (2002). Illiquid Alternative Asset Fund Modeling. *The
Journal of Portfolio Management*, 28(2), 90--100. Terhaar, K., Staub,
R., and Singer, B. (2003). Appropriate Policy Allocation for Alternative
Investments. *The Journal of Portfolio Management*, 29(3), 101--110.
:::

# Annex A - Parameters Sensitivity {#annex:sensitivity .unnumbered}

This annex reports the sensitivity of optimal portfolio composition to
the choice of penalty function parameters. For each of the three
functional forms considered in Section 4, the penalized mean-variance
optimization is solved across a $6 \times 6$ grid of $(\alpha, \beta)$
values, and the resulting portfolio composition along the efficient
frontier is displayed as a stacked area chart. Rows correspond to
increasing values of $\alpha$ and columns to increasing values of
$\beta$. The analysis is intended to provide the practitioner with an
intuitive map of how the penalty parameters translate into portfolio
allocations, independently of the calibration methodology developed in
Section 6.

<figure id="fig:sensitivity_power" data-latex-placement="h">
<img src="./Sensitivity/power.png" />
<figcaption>Portfolio composition sensitivity matrix for the power
penalty <span
class="math inline"><em>c</em>(<em>L</em>) = <em>α</em> ⋅ <em>L</em><sup><em>β</em></sup></span>.
Rows: <span
class="math inline"><em>α</em> ∈ {0.05, 0.10, 0.20, 0.35, 0.50, 0.70}</span>.
Columns: <span
class="math inline"><em>β</em> ∈ {0.80, 1.20, 1.60, 2.00, 2.50, 3.00}</span>.</figcaption>
</figure>

<figure id="fig:sensitivity_exp" data-latex-placement="h">
<img src="./Sensitivity/exponential.png" />
<figcaption>Portfolio composition sensitivity matrix for the exponential
penalty <span
class="math inline"><em>c</em>(<em>L</em>) = <em>α</em> ⋅ <em>e</em><sup><em>β</em><em>L</em></sup></span>.
Rows: <span
class="math inline"><em>α</em> ∈ {0.01, 0.02, 0.04, 0.07, 0.10, 0.15}</span>.
Columns: <span
class="math inline"><em>β</em> ∈ {0.50, 1.00, 1.50, 2.00, 2.50, 3.00}</span>.</figcaption>
</figure>

<figure id="fig:sensitivity_quad" data-latex-placement="h">
<img src="./Sensitivity/quadratic.png" />
<figcaption>Portfolio composition sensitivity matrix for the quadratic
penalty <span
class="math inline"><em>c</em>(<em>L</em>) = <em>α</em><em>L</em> + <em>β</em><em>L</em><sup>2</sup></span>.
Rows: <span
class="math inline"><em>α</em> ∈ {0.02, 0.05, 0.10, 0.20, 0.35, 0.50}</span>.
Columns: <span
class="math inline"><em>β</em> ∈ {0.05, 0.10, 0.20, 0.40, 0.70, 1.00}</span>.</figcaption>
</figure>
