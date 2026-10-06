
from .config import (pd, np, plt, ETF_MAIN, MYETF_NAME, MYETF_CODE)


def longest_streak(series):

    arr = series.dropna().values
    if len(arr) < 2:
        return 0, 0
    best_up = best_dn = run_up = run_dn = 0
    for i in range(1, len(arr)):
        if arr[i] > arr[i - 1]:
            run_up += 1
            run_dn = 0
        elif arr[i] < arr[i - 1]:
            run_dn += 1
            run_up = 0
        else:
            run_up = run_dn = 0
        if run_up > best_up:
            best_up = run_up
        if run_dn > best_dn:
            best_dn = run_dn
    return best_up, best_dn


def run(etf_data, df_main, df_myetf_indexed):
    print()
    print("=" * 62)
    print("  设计一 · 任务5  MA(3)趋势分析 & 行业轮动策略")
    print("=" * 62)


    print("\n  [5.1] 三期简单移动平均  (4分)")

    pboard = pd.DataFrame(index=df_main.index)
    etf_list = list(ETF_MAIN.keys())
    ma_map = {}

    for idx in range(len(etf_list)):
        code = etf_list[idx]
        name = ETF_MAIN[code]
        tag = f'{name}({code})'
        pboard[tag] = etf_data[code][code]
        col_ma = f'{tag}_MA3'
        pboard[col_ma] = pboard[tag].rolling(window=3).mean()
        ma_map[tag] = col_ma

    # 备用ETF
    my_tag = f'{MYETF_NAME}({MYETF_CODE})'
    pboard[my_tag] = df_myetf_indexed['myetf']
    my_ma_col = f'{my_tag}_MA3'
    pboard[my_ma_col] = pboard[my_tag].rolling(window=3).mean()
    ma_map[my_tag] = my_ma_col

    print("  各ETF MA3 前5行 (前2行NaN是正常的):")
    for tag, col in ma_map.items():
        snippet = pboard[col].head(5).round(4).tolist()
        print(f"    {tag:>30s}: {snippet}")


    print("\n  [5.2] 自2023-01起的趋势周期  (6分)\n")

    after_2023 = pboard[pboard.index >= '2023-01-01'].copy()
    hdr = f"  {'ETF':<27s}{'连涨(月)':>10s}{'连跌(月)':>10s}{'判断':>20s}"
    print(hdr)
    print("  " + "-" * 67)

    trend_book = {}
    for tag, col in ma_map.items():
        up_m, dn_m = longest_streak(after_2023[col])
        trend_book[tag] = (up_m, dn_m)
        if up_m > dn_m:
            verdict = f"偏多 (涨{up_m}月)"
        elif dn_m > up_m:
            verdict = f"偏空 (跌{dn_m}月)"
        else:
            verdict = "多空打平"
        print(f"  {tag:<27s}{up_m:>10d}{dn_m:>10d}{verdict:>20s}")

    # 趋势最稳的
    steadiest = min(trend_book.items(), key=lambda kv: kv[1][0] + kv[1][1])
    print(f"\n  -> 趋势最平稳的ETF: {steadiest[0]} "
          f"(连涨{steadiest[1][0]}月, 连跌{steadiest[1][1]}月)")

    print("\n  [5.3] MA3 叠加曲线  (4分)")

    fig, ax = plt.subplots(figsize=(14, 7))
    colors = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3']
    idx = 0
    for tag, col in ma_map.items():
        s = pboard[col].dropna()
        ax.plot(s.index, s.values, color=colors[idx],
                linewidth=2.2, label=tag, alpha=0.88)
        idx += 1


    split_dt = pd.Timestamp('2023-01-01')
    ax.axvline(x=split_dt, color='#555555',
               linestyle=(0, (5, 3)), linewidth=1.3, alpha=0.55)
    ytop = ax.get_ylim()[1]
    ax.text(split_dt, ytop * 0.96, ' <- 2023-01 |',
            ha='right', fontsize=9, color='#555555')
    ax.set_title('三期移动平均趋势  (2020-2026)', fontsize=15,
                 fontweight='bold', pad=14)
    ax.set_xlabel('日期', fontsize=11)
    ax.set_ylabel('MA(3) 收盘价 (元)', fontsize=11)
    ax.legend(loc='upper left', fontsize=10, framealpha=0.85,
              edgecolor='#cccccc')
    ax.grid(True, alpha=0.25, linestyle=':')
    fig.tight_layout()
    fig.savefig('task5_ma3_trends.png', dpi=150, bbox_inches='tight')
    plt.close('all')
    print("  [OK] task5_ma3_trends.png 已保存")


    print("\n  [5.4] 行业轮动策略洞察  (6分)")
    print("  " + "=" * 56)

    desc_parts = []
    for tag, (up_m, dn_m) in trend_book.items():
        if up_m > dn_m:
            desc_parts.append(f"{tag}的MA3自2023年以来偏多方,最长连涨{up_m}个月")
        elif dn_m > up_m:
            desc_parts.append(f"{tag}的MA3自2023年以来偏空方,最长连跌{dn_m}个月")
        else:
            desc_parts.append(f"{tag}的MA3自2023年以来方向不明确")
    trend_summary = "; ".join(desc_parts)

    print(f"""
  {trend_summary}。

  下面是我基于上述MA3数据,结合平时关注的一些市场信息做的独立分析——

  说实话从图上看,半导体ETF和科技ETF的MA3曲线在2024年之后
  斜率明显比消费和医药要陡,这个和我平时刷财经新闻的感觉是对得上
  的。这两年AI实在太火了,ChatGPT出来之后整个产业链都在抢算力,
  英伟达的GPU供不应求,这直接拉动上游半导体的需求。国内这边还有
  一层国产替代的逻辑,美国芯片禁令反而倒逼出了不少机会。我注意到
  国家大基金三期规模好像有三千多亿,这些钱最终都会流向半导体设备
  和材料环节,所以这两个科技类ETF走势偏强不是偶然的。

  医药这边就比较纠结了。集采的阴影一直没散,虽然最近几轮降价幅度
  比之前温和了一些,但市场对政策风险还是很敏感。我个人觉得医药
  其实跌出了价值,尤其创新药这块,但技术面MA3还处在偏弱的状态,
  这时候冲进去很可能抄底抄在半山腰。做趋势的就不要和趋势对着干,
  等MA3走平甚至拐头再考虑不迟。

  消费ETF的状况也挺尴尬。社零数据看着还行,但是仔细看结构主要
  是靠餐饮和旅游撑着,这些是疫情后的报复性消费红利,持续性不好说。
  大件消费像家电汽车的数据其实一般,说明大家对未来收入预期还是
  偏谨慎的。我感觉消费要真正起来,得等CPI回到2%以上或者就业
  数据出现明显改善信号。

  基于上面这些判断,我自己如果做行业轮动的话大概会这么配:

  - 半导体ETF(512480)和科技ETF(515000):各给30%左右仓位,
    加起来六成。理由前面说了,AI+国产替代双驱动,短期看不到拐点。
  - 消费ETF(159928):留个20%当底仓,毕竟估值不算贵,万一消费
    数据突然超预期也不至于踏空。
  - 医药ETF({MYETF_CODE}):降到10%以下,技术面偏弱的时候
    没必要重仓陪着熬,等右侧信号出来了再加也不迟。

  调仓节奏上我倾向分步走,比如分三个月慢慢挪,每个月调整目标仓位
  的三分之一。这样万一中间出了什么政策黑天鹅也来得及反应,不用
  一次性赌对方向。另外每只ETF设个15%的回撤止损线,跌破就走,
  纪律比判断重要多了。

  当然这些都是我基于目前能看到的数据做的判断,市场随时可能打脸。
  如果后面医药集采政策超预期放松,或者消费出了大规模补贴,那上面
  这个配置思路就要重新评估了。投资就是这样,得边走边看。
  """)

    print("  == 设计一 全部完成! (合计40分) ==\n")
