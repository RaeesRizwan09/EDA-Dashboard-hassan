"""
charts.py — Wind Turbine Dashboard Chart Library
Aesthetic: Dark Aerospace · Industrial · Midnight navy · Electric cyan · Amber signal
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import matplotlib.colors as mcolors
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats

# ── PALETTE ──────────────────────────────────────────────────────────────────
BG0        = "#060b14"   # deepest background
BG1        = "#0b1422"   # panel background
BG2        = "#111d30"   # secondary surface
BG3        = "#162540"   # tertiary / track
CYAN       = "#00e5d0"   # primary accent
CYAN2      = "#00b8a0"   # mid cyan
CYAN3      = "#007d6e"   # dark cyan
AMBER      = "#f0a500"   # signal / highlight
AMBER2     = "#c07800"   # deep amber
STEEL      = "#3a7aad"   # steel blue
STEEL2     = "#1d4d72"   # dark steel
MUTED      = "#4a6785"   # muted text / grid
TEXT       = "#c8dff0"   # primary text
TEXT2      = "#7aa0c0"   # secondary text
TEXT3      = "#3a5570"   # tertiary / axis
GRID       = "#0f2035"   # grid lines
BORDER     = "#1a3050"   # border colour

# Manufacturer colour ramp (8 makers)
MANU_COLORS = [CYAN, STEEL, AMBER, CYAN2, STEEL2, AMBER2, CYAN3, "#5a9fd4"]

# Capacity colour ramp
CAP_RAMP = [BG3, STEEL2, STEEL, CYAN3, CYAN2, CYAN, "#80fff5"]

# State accent colours
STATE_COLORS = [CYAN, CYAN2, CYAN3, STEEL, STEEL2, AMBER, AMBER2,
                "#5a9fd4", "#2d7a6e", "#1d5a7e", "#9a6800", "#6080a0"]


# ── BASE FIGURE FACTORY ──────────────────────────────────────────────────────
def _fig(w: float = 10, h: float = 5) -> tuple:
    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_facecolor(BG1)
    ax.set_facecolor(BG2)
    ax.tick_params(colors=TEXT3, labelsize=9)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines["left"].set_color(BORDER)
    ax.spines["bottom"].set_color(BORDER)
    # Cyan top border accent
    fig.subplots_adjust(top=0.88)
    ax.axhline(y=ax.get_ylim()[1] if ax.get_ylim()[1] != 0 else 1,
               color=CYAN, linewidth=0, alpha=0)  # placeholder; redrawn per chart
    return fig, ax


def _title(ax, text: str):
    ax.set_title(
        text,
        fontsize=11,
        color=TEXT,
        fontfamily="monospace",
        loc="left",
        pad=10,
        fontweight="bold",
    )


def _grid(ax, axis: str = "y"):
    ax.grid(axis=axis, color=GRID, linewidth=0.5, alpha=0.8, linestyle="--")
    if axis == "y":
        ax.grid(axis="x", visible=False)
    else:
        ax.grid(axis="y", visible=False)


# ── 1. HORIZONTAL BAR — turbine count by state ───────────────────────────────
def bar_state_fleet(df: pd.DataFrame, top_n: int = 15) -> plt.Figure:
    if df.empty:
        return None
    counts = (df.groupby("t_state").size()
                .sort_values(ascending=True)
                .tail(top_n))

    fig, ax = _fig(10, max(4, len(counts) * 0.55))
    colors = [CYAN if c == counts.max() else STEEL for c in counts.values]
    bars = ax.barh(counts.index, counts.values, color=colors,
                   edgecolor=BG1, linewidth=0.4, height=0.7)

    for bar, val in zip(bars, counts.values):
        ax.text(
            bar.get_width() + counts.max() * 0.01,
            bar.get_y() + bar.get_height() / 2,
            f"{val:,}",
            va="center", ha="left",
            fontsize=8.5, color=TEXT2, fontfamily="monospace",
        )

    ax.set_yticklabels(counts.index, fontsize=9, color=TEXT2, fontfamily="monospace")
    ax.set_xlabel("Number of Turbines", fontsize=9, color=MUTED, labelpad=8)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    _grid(ax, "x")
    _title(ax, "Turbine Fleet Size by State")
    fig.tight_layout()
    return fig


# ── 2. HORIZONTAL BAR — installed capacity by state (MW) ─────────────────────
def bar_state_capacity(df: pd.DataFrame, top_n: int = 15) -> plt.Figure:
    if df.empty:
        return None
    cap = (df[df["t_cap"] > 0]
           .groupby("t_state")["t_cap"]
           .sum()
           .div(1000)   # kW → MW
           .sort_values(ascending=True)
           .tail(top_n))

    fig, ax = _fig(10, max(4, len(cap) * 0.55))
    colors = [AMBER if c == cap.max() else AMBER2 for c in cap.values]
    bars = ax.barh(cap.index, cap.values, color=colors,
                   edgecolor=BG1, linewidth=0.4, height=0.7)

    for bar, val in zip(bars, cap.values):
        ax.text(
            bar.get_width() + cap.max() * 0.01,
            bar.get_y() + bar.get_height() / 2,
            f"{val:,.0f} MW",
            va="center", ha="left",
            fontsize=8.5, color=TEXT2, fontfamily="monospace",
        )

    ax.set_yticklabels(cap.index, fontsize=9, color=TEXT2, fontfamily="monospace")
    ax.set_xlabel("Total Installed Capacity (MW)", fontsize=9, color=MUTED, labelpad=8)
    _grid(ax, "x")
    _title(ax, "Installed Capacity by State (MW)")
    fig.tight_layout()
    return fig


# ── 3. HISTOGRAM — turbines installed per year ────────────────────────────────
def hist_install_year(df: pd.DataFrame) -> plt.Figure:
    if df.empty or df["p_year"].dropna().empty:
        return None
    years = df["p_year"].dropna().astype(int)
    year_counts = years.value_counts().sort_index()

    fig, ax = _fig(12, 5)
    peak_year = year_counts.idxmax()
    bar_colors = [AMBER if y == peak_year else STEEL for y in year_counts.index]

    ax.bar(year_counts.index, year_counts.values, color=bar_colors,
           edgecolor=BG1, linewidth=0.3, width=0.8)

    # Annotate peak
    ax.annotate(
        f"Peak: {peak_year}\n{year_counts[peak_year]:,} turbines",
        xy=(peak_year, year_counts[peak_year]),
        xytext=(peak_year - 4, year_counts[peak_year] * 0.85),
        fontsize=8.5, color=AMBER, fontfamily="monospace",
        arrowprops=dict(arrowstyle="->", color=AMBER, lw=1.2),
    )

    ax.set_xlabel("Installation Year", fontsize=9, color=MUTED, labelpad=8)
    ax.set_ylabel("Turbines Installed", fontsize=9, color=MUTED, labelpad=8)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    _grid(ax, "y")
    _title(ax, "Annual Turbine Installations (1981–2018)")
    fig.tight_layout()
    return fig


# ── 4. LINE — cumulative turbine count over time ──────────────────────────────
def line_cumulative(df: pd.DataFrame) -> plt.Figure:
    if df.empty or df["p_year"].dropna().empty:
        return None
    years = df["p_year"].dropna().astype(int)
    year_counts = years.value_counts().sort_index()
    cumulative = year_counts.cumsum()

    fig, ax = _fig(12, 4.5)

    ax.fill_between(cumulative.index, cumulative.values,
                    color=CYAN, alpha=0.08, zorder=2)
    ax.plot(cumulative.index, cumulative.values, color=CYAN,
            linewidth=2.5, zorder=3)
    ax.scatter(cumulative.index[::3], cumulative.values[::3],
               color=CYAN, s=40, zorder=4, edgecolors=BG1, linewidth=1)

    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.set_xlabel("Year", fontsize=9, color=MUTED, labelpad=8)
    ax.set_ylabel("Cumulative Turbines", fontsize=9, color=MUTED, labelpad=8)
    _grid(ax, "y")
    _title(ax, "Cumulative US Wind Turbine Fleet Build-Up")
    fig.tight_layout()
    return fig


# ── 5. BAR — manufacturer market share ───────────────────────────────────────
def bar_manufacturer(df: pd.DataFrame, top_n: int = 10) -> plt.Figure:
    if df.empty:
        return None
    manu = (df[df["t_manu"] != "missing"]
            .groupby("t_manu").size()
            .sort_values(ascending=True)
            .tail(top_n))

    fig, ax = _fig(10, max(4, len(manu) * 0.55))
    colors = MANU_COLORS[:len(manu)][::-1]
    bars = ax.barh(manu.index, manu.values, color=colors,
                   edgecolor=BG1, linewidth=0.4, height=0.68)

    total = manu.sum()
    for bar, val in zip(bars, manu.values):
        pct = val / total * 100
        ax.text(
            bar.get_width() + manu.max() * 0.01,
            bar.get_y() + bar.get_height() / 2,
            f"{val:,}  ({pct:.1f}%)",
            va="center", ha="left",
            fontsize=8.5, color=TEXT2, fontfamily="monospace",
        )

    ax.set_yticklabels(manu.index, fontsize=9, color=TEXT2)
    ax.set_xlabel("Turbines Installed", fontsize=9, color=MUTED, labelpad=8)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    _grid(ax, "x")
    _title(ax, "Turbine Count by Manufacturer")
    fig.tight_layout()
    return fig


# ── 6. SCATTER — manufacturer count vs avg capacity ──────────────────────────
def scatter_manu_capacity(df: pd.DataFrame) -> plt.Figure:
    if df.empty:
        return None
    agg = (df[(df["t_manu"] != "missing") & (df["t_cap"] > 0)]
           .groupby("t_manu")
           .agg(count=("case_id", "count"),
                avg_cap=("t_cap", "mean"))
           .query("count >= 20")
           .reset_index())

    fig, ax = _fig(10, 6)
    sc = ax.scatter(
        agg["count"], agg["avg_cap"],
        s=agg["count"] / 40,
        c=agg["avg_cap"],
        cmap=mcolors.LinearSegmentedColormap.from_list(
            "wind", [STEEL2, CYAN3, CYAN], N=256),
        alpha=0.85,
        edgecolors=BORDER, linewidth=0.6, zorder=4,
    )

    for _, row in agg.iterrows():
        ax.annotate(
            row["t_manu"],
            (row["count"], row["avg_cap"]),
            fontsize=7.5, color=TEXT2, fontfamily="monospace",
            xytext=(6, 4), textcoords="offset points",
        )

    cbar = plt.colorbar(sc, ax=ax, shrink=0.6, pad=0.02)
    cbar.set_label("Avg Capacity (kW)", color=MUTED, fontsize=8, fontfamily="monospace")
    cbar.ax.yaxis.set_tick_params(color=MUTED, labelsize=8)
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color=TEXT2, fontfamily="monospace")
    cbar.ax.set_facecolor(BG2)

    ax.set_xlabel("Total Turbines Installed", fontsize=9, color=MUTED, labelpad=8)
    ax.set_ylabel("Average Turbine Capacity (kW)", fontsize=9, color=MUTED, labelpad=8)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    _grid(ax, "y")
    _title(ax, "Manufacturer Scale vs Turbine Capacity  (bubble ∝ count)")
    fig.tight_layout()
    return fig


# ── 7. HISTOGRAM — hub height distribution ───────────────────────────────────
def hist_hub_height(df: pd.DataFrame) -> plt.Figure:
    if df.empty:
        return None
    hh = df["t_hh"].dropna()
    hh = hh[hh > 0]
    if hh.empty:
        return None

    fig, ax = _fig(9, 4.5)
    n, bins, patches = ax.hist(hh, bins=30, color=STEEL,
                                edgecolor=BG1, linewidth=0.3)
    # Colour peak bin
    peak_bin = np.argmax(n)
    patches[peak_bin].set_facecolor(CYAN)

    # Median line
    median_hh = hh.median()
    ax.axvline(median_hh, color=AMBER, linewidth=1.5, linestyle="--", zorder=5)
    ax.text(median_hh + 0.8, ax.get_ylim()[1] * 0.88,
            f"Median: {median_hh:.0f}m",
            fontsize=8.5, color=AMBER, fontfamily="monospace")

    ax.set_xlabel("Hub Height (m)", fontsize=9, color=MUTED, labelpad=8)
    ax.set_ylabel("Turbine Count", fontsize=9, color=MUTED, labelpad=8)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    _grid(ax, "y")
    _title(ax, "Hub Height Distribution")
    fig.tight_layout()
    return fig


# ── 8. HISTOGRAM — rotor diameter distribution ────────────────────────────────
def hist_rotor_diameter(df: pd.DataFrame) -> plt.Figure:
    if df.empty:
        return None
    rd = df["t_rd"].dropna()
    rd = rd[rd > 0]
    if rd.empty:
        return None

    fig, ax = _fig(9, 4.5)
    n, bins, patches = ax.hist(rd, bins=30, color=STEEL2,
                                edgecolor=BG1, linewidth=0.3)
    peak_bin = np.argmax(n)
    patches[peak_bin].set_facecolor(CYAN2)

    median_rd = rd.median()
    ax.axvline(median_rd, color=AMBER, linewidth=1.5, linestyle="--", zorder=5)
    ax.text(median_rd + 0.8, ax.get_ylim()[1] * 0.88,
            f"Median: {median_rd:.0f}m",
            fontsize=8.5, color=AMBER, fontfamily="monospace")

    ax.set_xlabel("Rotor Diameter (m)", fontsize=9, color=MUTED, labelpad=8)
    ax.set_ylabel("Turbine Count", fontsize=9, color=MUTED, labelpad=8)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    _grid(ax, "y")
    _title(ax, "Rotor Diameter Distribution")
    fig.tight_layout()
    return fig


# ── 9. KDE — capacity density by manufacturer (top 5) ────────────────────────
def kde_capacity_by_manu(df: pd.DataFrame, top_n: int = 5) -> plt.Figure:
    if df.empty:
        return None
    top_manus = (df[df["t_manu"] != "missing"]
                 .groupby("t_manu").size()
                 .sort_values(ascending=False)
                 .head(top_n).index.tolist())

    fig, ax = _fig(10, 5)
    colors = MANU_COLORS[:top_n]

    for manu, col in zip(top_manus, colors):
        sub = df[(df["t_manu"] == manu) & (df["t_cap"] > 0) & (df["t_cap"] < 5000)]["t_cap"]
        if len(sub) < 10:
            continue
        sub.plot.kde(ax=ax, color=col, linewidth=2, label=manu)
        ax.fill_between(
            ax.lines[-1].get_xdata(),
            ax.lines[-1].get_ydata(),
            color=col, alpha=0.07,
        )

    ax.set_xlabel("Turbine Capacity (kW)", fontsize=9, color=MUTED, labelpad=8)
    ax.set_ylabel("Density", fontsize=9, color=MUTED, labelpad=8)
    ax.set_xlim(0, 5000)
    ax.legend(fontsize=9, framealpha=0.4, facecolor=BG2,
              edgecolor=BORDER, labelcolor=TEXT2)
    _grid(ax, "y")
    _title(ax, f"Capacity Distribution — Top {top_n} Manufacturers")
    fig.tight_layout()
    return fig


# ── 10. SCATTER — hub height vs turbine capacity ─────────────────────────────
def scatter_hh_capacity(df: pd.DataFrame) -> plt.Figure:
    if df.empty:
        return None
    sub = df[(df["t_hh"] > 0) & (df["t_cap"] > 0) & (df["t_cap"] < 5000)].copy()
    if sub.empty:
        return None

    # Sample for performance
    if len(sub) > 6000:
        sub = sub.sample(6000, random_state=42)

    fig, ax = _fig(10, 5.5)
    sc = ax.scatter(
        sub["t_hh"], sub["t_cap"],
        c=sub["p_year"].fillna(2000),
        cmap=mcolors.LinearSegmentedColormap.from_list(
            "era", [BG3, STEEL2, STEEL, CYAN2, CYAN], N=256),
        alpha=0.35, s=10, zorder=3, linewidths=0,
    )

    # Regression line
    slope, intercept, r, p, _ = stats.linregress(sub["t_hh"], sub["t_cap"])
    x_line = np.linspace(sub["t_hh"].min(), sub["t_hh"].max(), 100)
    ax.plot(x_line, slope * x_line + intercept,
            color=AMBER, linewidth=2, linestyle="-", zorder=4,
            label=f"Trend  r={r:.2f}")

    cbar = plt.colorbar(sc, ax=ax, shrink=0.6, pad=0.02)
    cbar.set_label("Install Year", color=MUTED, fontsize=8, fontfamily="monospace")
    cbar.ax.yaxis.set_tick_params(color=MUTED, labelsize=8)
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color=TEXT2, fontfamily="monospace")
    cbar.ax.set_facecolor(BG2)

    ax.legend(fontsize=9, framealpha=0.4, facecolor=BG2,
              edgecolor=BORDER, labelcolor=AMBER)
    ax.set_xlabel("Hub Height (m)", fontsize=9, color=MUTED, labelpad=8)
    ax.set_ylabel("Turbine Capacity (kW)", fontsize=9, color=MUTED, labelpad=8)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    _grid(ax, "y")
    _title(ax, "Hub Height vs Capacity  (colour = install year)")
    fig.tight_layout()
    return fig


# ── 11. BOX — capacity distribution by state (top N) ─────────────────────────
def box_capacity_by_state(df: pd.DataFrame, top_n: int = 12) -> plt.Figure:
    if df.empty:
        return None
    top_states = (df.groupby("t_state").size()
                  .sort_values(ascending=False)
                  .head(top_n).index.tolist())
    sub = df[(df["t_state"].isin(top_states)) & (df["t_cap"] > 0)].copy()
    if sub.empty:
        return None

    order = (sub.groupby("t_state")["t_cap"]
             .median().sort_values(ascending=False).index.tolist())
    pal = {s: STATE_COLORS[i % len(STATE_COLORS)] for i, s in enumerate(order)}

    fig, ax = _fig(11, 5.5)
    sns.boxplot(data=sub, x="t_state", y="t_cap", order=order,
                hue="t_state", palette=pal, legend=False,
                fliersize=2, linewidth=0.8, width=0.6, ax=ax,
                medianprops=dict(color=AMBER, linewidth=2))

    ax.set_xticklabels(order, fontsize=9, color=TEXT2, fontfamily="monospace")
    ax.set_xlabel("State", fontsize=9, color=MUTED, labelpad=8)
    ax.set_ylabel("Turbine Capacity (kW)", fontsize=9, color=MUTED, labelpad=8)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    _grid(ax, "y")
    _title(ax, f"Capacity Distribution — Top {top_n} States by Fleet Size")
    fig.tight_layout()
    return fig


# ── 12. STACKED BAR — manufacturer share per state (top states) ───────────────
def stacked_state_manufacturer(df: pd.DataFrame, top_n: int = 10) -> plt.Figure:
    if df.empty:
        return None
    top_states = (df.groupby("t_state").size()
                  .sort_values(ascending=False)
                  .head(top_n).index.tolist())
    top_manus = (df[df["t_manu"] != "missing"]
                 .groupby("t_manu").size()
                 .sort_values(ascending=False)
                 .head(6).index.tolist())

    sub = df[df["t_state"].isin(top_states)].copy()
    sub["t_manu_grp"] = sub["t_manu"].where(sub["t_manu"].isin(top_manus), other="Other")
    pivot = (sub.groupby(["t_state", "t_manu_grp"])
               .size().unstack(fill_value=0))
    pivot = pivot.loc[pivot.sum(axis=1).sort_values(ascending=True).index]

    manus = pivot.columns.tolist()
    color_map = dict(zip(top_manus, MANU_COLORS[:6]))
    color_map["Other"] = MUTED

    fig, ax = _fig(10, max(4.5, len(pivot) * 0.55))
    left = np.zeros(len(pivot))

    for manu in manus:
        vals = pivot[manu].values if manu in pivot.columns else np.zeros(len(pivot))
        col = color_map.get(manu, MUTED)
        bars = ax.barh(pivot.index, vals, left=left,
                       color=col, edgecolor=BG1, linewidth=0.3, height=0.65)
        for bar, val in zip(bars, vals):
            if val > pivot.values.max() * 0.05:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_y() + bar.get_height() / 2,
                    f"{int(val):,}", va="center", ha="center",
                    fontsize=7, color=BG0, fontweight="bold",
                )
        left += vals

    patches = [mpatches.Patch(color=color_map.get(m, MUTED), label=m) for m in manus]
    ax.legend(handles=patches, fontsize=8, loc="lower right",
              framealpha=0.5, facecolor=BG2, edgecolor=BORDER, labelcolor=TEXT2)
    ax.set_yticklabels(pivot.index, fontsize=9, color=TEXT2, fontfamily="monospace")
    ax.set_xlabel("Number of Turbines", fontsize=9, color=MUTED, labelpad=8)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    _grid(ax, "x")
    _title(ax, "Manufacturer Breakdown — Top States")
    fig.tight_layout()
    return fig


# ── 13. VIOLIN — hub height by install era ────────────────────────────────────
def violin_hh_by_era(df: pd.DataFrame) -> plt.Figure:
    if df.empty or df["p_year"].dropna().empty:
        return None
    sub = df[(df["t_hh"] > 0) & df["p_year"].notna()].copy()
    if sub.empty:
        return None

    sub["era"] = pd.cut(
        sub["p_year"].astype(int),
        bins=[1979, 1990, 2000, 2007, 2012, 2019],
        labels=["1980s", "1991–2000", "2001–2007", "2008–2012", "2013–2018"],
    )
    sub = sub.dropna(subset=["era"])

    order = ["1980s", "1991–2000", "2001–2007", "2008–2012", "2013–2018"]
    pal = dict(zip(order, [BG3, STEEL2, STEEL, CYAN2, CYAN]))

    fig, ax = _fig(10, 5)
    sns.violinplot(data=sub, x="era", y="t_hh", order=order,
                   hue="era", palette=pal, legend=False,
                   linewidth=0.8, inner="quartile", ax=ax,
                   inner_kws=dict(color=AMBER, linewidth=1))

    ax.set_xticklabels(order, fontsize=9, color=TEXT2)
    ax.set_xlabel("Installation Era", fontsize=9, color=MUTED, labelpad=8)
    ax.set_ylabel("Hub Height (m)", fontsize=9, color=MUTED, labelpad=8)
    _grid(ax, "y")
    _title(ax, "Hub Height Evolution by Installation Era")
    fig.tight_layout()
    return fig


# ── 14. LINE — avg capacity trend over time ───────────────────────────────────
def line_capacity_trend(df: pd.DataFrame) -> plt.Figure:
    if df.empty:
        return None
    sub = df[(df["t_cap"] > 0) & df["p_year"].notna()].copy()
    if sub.empty:
        return None

    trend = (sub.groupby("p_year")["t_cap"]
             .agg(["mean", "median", "std", "count"])
             .reset_index()
             .query("count >= 5")
             .sort_values("p_year"))

    if trend.empty:
        return None

    fig, ax = _fig(12, 5)
    ax.fill_between(trend["p_year"],
                    trend["mean"] - trend["std"],
                    trend["mean"] + trend["std"],
                    color=CYAN, alpha=0.07, label="±1 std dev")
    ax.plot(trend["p_year"], trend["median"],
            color=MUTED, linewidth=1.2, linestyle=":", label="Median")
    ax.plot(trend["p_year"], trend["mean"],
            color=CYAN, linewidth=2.5, label="Mean", zorder=4)
    ax.scatter(trend["p_year"], trend["mean"],
               color=AMBER, s=45, zorder=5, edgecolors=BG1, linewidth=1.2)

    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,} kW"))
    ax.legend(fontsize=9, framealpha=0.4, facecolor=BG2,
              edgecolor=BORDER, labelcolor=TEXT2)
    _grid(ax, "y")
    ax.set_xlabel("Installation Year", fontsize=9, color=MUTED, labelpad=8)
    ax.set_ylabel("Avg Turbine Capacity (kW)", fontsize=9, color=MUTED, labelpad=8)
    _title(ax, "Turbine Capacity Growth Over Time")
    fig.tight_layout()
    return fig


# ── 15. BUBBLE — state avg capacity × count × hub height ─────────────────────
def bubble_state(df: pd.DataFrame) -> plt.Figure:
    if df.empty:
        return None
    agg = (df[(df["t_cap"] > 0) & (df["t_hh"] > 0)]
           .groupby("t_state")
           .agg(
               count=("case_id", "count"),
               avg_cap=("t_cap", "mean"),
               avg_hh=("t_hh", "mean"),
           )
           .query("count >= 20")
           .reset_index())

    fig, ax = _fig(11, 7)
    cmap = mcolors.LinearSegmentedColormap.from_list(
        "height_ramp", [STEEL2, STEEL, CYAN2, CYAN], N=256)

    sc = ax.scatter(
        agg["count"], agg["avg_cap"],
        s=agg["avg_hh"] * 8,
        c=agg["avg_hh"],
        cmap=cmap, alpha=0.75,
        edgecolors=BORDER, linewidth=0.6, zorder=4,
    )

    for _, row in agg.iterrows():
        ax.annotate(
            row["t_state"],
            (row["count"], row["avg_cap"]),
            fontsize=7.5, color=TEXT2, fontfamily="monospace",
            xytext=(5, 4), textcoords="offset points",
        )

    cbar = plt.colorbar(sc, ax=ax, shrink=0.65, pad=0.02)
    cbar.set_label("Avg Hub Height (m)", color=MUTED, fontsize=8, fontfamily="monospace")
    cbar.ax.yaxis.set_tick_params(color=MUTED, labelsize=8)
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color=TEXT2, fontfamily="monospace")
    cbar.ax.set_facecolor(BG2)

    ax.set_xlabel("Fleet Size (turbines)", fontsize=9, color=MUTED, labelpad=8)
    ax.set_ylabel("Average Capacity (kW)", fontsize=9, color=MUTED, labelpad=8)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    _grid(ax, "y")
    _title(ax, "State: Fleet Size × Avg Capacity × Hub Height  (bubble = hub height)")
    fig.tight_layout()
    return fig
