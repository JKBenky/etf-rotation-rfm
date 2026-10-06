
from .config import (pd, ETF_MAIN)


def run(etf_dict, price_board):
    print()
    print("-" * 64)
    print("   任务3  月度收益率")
    print("-" * 64)
    print()


    ret_columns = []
    for code, name in ETF_MAIN.items():
        col_ret = f'ret_{code}'
        # 公式: (当日收盘 - 前日收盘) / |前日收盘| x 100
        etf_dict[code][col_ret] = etf_dict[code][code].pct_change() * 100.0
        wide_name = f'{name}({code})_ret'
        price_board[wide_name] = etf_dict[code][col_ret]
        ret_columns.append(wide_name)


    print("  2020-01起前12个月收益率 (%):\n")
    print(price_board[ret_columns].head(12).round(4).to_string())


    print("\n  [验证1] 首行应为NaN (首月无上月数据做参照)")
    for code, name in ETF_MAIN.items():
        first_val = etf_dict[code][f'ret_{code}'].iloc[0]
        if pd.isna(first_val):
            tag = "OK-NaN"
        else:
            tag = "FAIL"
        print(f"    {name}({code}) 首月: {first_val}  [{tag}]")


    print("\n  [验证2] 手动验算第3行收益率 (确保计算逻辑正确)")
    for code, name in ETF_MAIN.items():
        p2 = etf_dict[code][code].iloc[1]
        p3 = etf_dict[code][code].iloc[2]
        manual_ret = (p3 - p2) / abs(p2) * 100
        computed_ret = etf_dict[code][f'ret_{code}'].iloc[2]
        diff = abs(manual_ret - computed_ret)
        ok = "OK" if diff < 0.01 else "MISMATCH"
        print(f"    {name}({code}): 手动算={manual_ret:+.4f}%, "
              f"pct_change={computed_ret:+.4f}%, diff={diff:.6f} [{ok}]")


    print("\n  [额外] 2023-01之后的平均月收益率:")
    for code, name in ETF_MAIN.items():
        sub = etf_dict[code][f'ret_{code}'][etf_dict[code].index >= '2023-01-01']
        avg_ret = sub.mean()
        std_ret = sub.std()
        print(f"    {name}({code}): 均值={avg_ret:+.2f}%, 标准差={std_ret:.2f}%")


    print("\n  [摘要] 本次分析了 %d 只ETF的月度收益率" % len(ETF_MAIN))
    etf_names_str = ", ".join("%s(%s)" % (v, k) for k, v in ETF_MAIN.items())
    print("  标的: %s" % etf_names_str)
    print("  数据起止: %s ~ %s" % (
        price_board.index[0].date(), price_board.index[-1].date()))

    print("\n  --- 任务3 完成 ---\n")
    return etf_dict, price_board
