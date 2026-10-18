"""Sample-size calculations reported in Table 4 of the synopsis."""
import math
from scipy.stats import norm, ncf, f as fdist


def ci_proportion(z=1.96, p=0.5, e=0.05):
    """n = Z^2 p(1-p) / e^2 (Equation 1)."""
    return math.ceil(z**2 * p * (1 - p) / e**2)


def mcnemar_noninferiority(p_disc=0.10, delta=0.05, alpha=0.05, power=0.80):
    """Paired non-inferiority, true difference 0, one-sided alpha (Equation 2)."""
    za, zb = norm.ppf(1 - alpha), norm.ppf(power)
    return math.ceil((za + zb) ** 2 * p_disc / delta**2)


def anova_f(f, df1, k, alpha=0.05, power=0.80):
    """Smallest total N giving the requested power for an F test with numerator df1 and k cells."""
    for n in range(k + 2, 100000):
        df2 = n - k
        crit = fdist.ppf(1 - alpha, df1, df2)
        if 1 - ncf.cdf(crit, df1, df2, f * f * n) >= power:
            return n
    raise ValueError("no solution")


def table():
    return {
        "RQ1 (CI, e=0.05)": ci_proportion(),
        "RQ2 (paired NI, delta=0.05)": mcnemar_noninferiority(),
        "RQ3 (2-way interaction, f=0.25, df=6, 12 cells)": anova_f(0.25, 6, 12),
        "RQ4 (regression, f2=0.35)": anova_f(math.sqrt(0.35), 1, 2),
    }


if __name__ == "__main__":
    for k, v in table().items():
        print(f"{k}: {v}")
