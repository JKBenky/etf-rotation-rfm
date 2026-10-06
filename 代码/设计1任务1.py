
from .config import (pd, plt, get_etf_data, ETF_MAIN, IS_ODD, CLASS_NUMBER,
                        PRINT_TARGET_CODE, PRINT_START_ROW, PRINT_END_ROW)
import time as _time


def download_and_plot():

    print()
    print("#" * 60)
    print("  TASK-1  数据下载模块  ")
    print("#" * 60)
    msg = "  取数区间 2020-01 ~ 2026-01 | 频率 M\n"
    print(msg)

    t0 = _time.time()
    collected = {}
    for ticker, label in ETF_MAIN.items():
        t1 = _time.time()
        raw = get_etf_data(ticker, label)
        if raw is not None and len(raw) > 0:
            collected[ticker] = raw
            dt = _time.time() - t1
            print("    {} 拉取成功  {:.1f}s".format(label, dt))
        _time.sleep(1)

    total_secs = _time.time() - t0
    print("\n  总计耗时 {:.1f}s".format(total_secs))


    panel = pd.concat(collected.values(), axis=1)
    col_labels = ['{}({})'.format(ETF_MAIN[k], k) for k in collected.keys()]
    panel.columns = col_labels
    n_rows, n_cols = panel.shape
    print("  合并维度: {} 行 x {} 列".format(n_rows, n_cols))


    parity_tag = "奇数" if IS_ODD else "偶数"
    print("\n  班级序号{}({}) -> 打印目标: {}({})".format(
        CLASS_NUMBER, parity_tag,
        ETF_MAIN[PRINT_TARGET_CODE], PRINT_TARGET_CODE))
    print("  行区间 [{}, {}]:".format(PRINT_START_ROW, PRINT_END_ROW))
    subset = collected[PRINT_TARGET_CODE].iloc[PRINT_START_ROW - 1:PRINT_END_ROW]
    print(subset.to_string())


    print("\n  > 绘制时序图...")
    n_etf = len(ETF_MAIN)
    fig, axes = plt.subplots(n_etf, 1, figsize=(13, 11))
    palette = ['#d62728', '#1f77b4', '#2ca02c']
    etf_list = list(ETF_MAIN.items())
    for idx in range(len(etf_list)):
        ticker, label = etf_list[idx]
        ax = axes[idx]
        series = collected[ticker][ticker]
        ax.plot(series.index, series.values,
                color=palette[idx], lw=2.2, alpha=0.9)
        title_str = '{} ({})  月度收盘价 2020-2026'.format(label, ticker)
        ax.set_title(title_str, fontsize=13, fontweight='bold')
        ax.set_xlabel('日期', fontsize=10)
        ax.set_ylabel('收盘价 (元)', fontsize=10)
        ax.grid(True, alpha=0.25, linestyle=':')
    fig.tight_layout(pad=2.2)
    fig.savefig('task1_etf_price_trends.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("  [OK] task1_etf_price_trends.png")

    print("  >> TASK-1 DONE <<\n")
    return collected, panel
