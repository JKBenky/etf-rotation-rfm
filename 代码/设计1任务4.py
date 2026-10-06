
from .config import (pd, plt, sns, ETF_MAIN, MYETF_NAME, MYETF_CODE)


def correlate(etf_data, df_main, df_myetf):
    print()
    print("*" * 66)
    print("  任务4  行业ETF月度收益率的Pearson相关分析")
    print("*" * 66 + "\n")


    my = df_myetf.copy()
    my.columns = ['myetf']
    my['ret_myetf'] = my['myetf'].pct_change() * 100


    pieces = []
    etf_keys = list(ETF_MAIN.keys())
    for i in range(len(etf_keys)):
        code = etf_keys[i]
        name = ETF_MAIN[code]
        lbl = '%s(%s)_ret' % (name, code)
        col_data = etf_data[code]['ret_%s' % code]
        pieces.append(pd.DataFrame({lbl: col_data}, index=df_main.index))


    pieces.append(pd.DataFrame(
        {'%s(%s)_ret' % (MYETF_NAME, MYETF_CODE): my['ret_myetf']},
        index=df_main.index
    ))

    all_rets = pd.concat(pieces, axis=1)
    clean = all_rets.dropna()
    nr, nc = clean.shape
    print("  有效样本: %d行 x %d列\n" % (nr, nc))


    corr = clean.corr(method='pearson')
    print("  Pearson r 矩阵:")
    print(corr.round(4).to_string())
    print()


    fig, ax = plt.subplots(figsize=(9, 7))
    h = sns.heatmap(
        corr, annot=True, fmt='.3f',
        cmap='coolwarm', center=0,
        vmin=-1, vmax=1, square=True,
        linewidths=0.6, linecolor='#eeeeee',
        cbar_kws={'label': 'r', 'shrink': 0.78},
        ax=ax
    )
    h.set_title('2020-2026 四大ETF 月度收益 Pearson r',
                fontsize=13, fontweight='bold', pad=14)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha='right', size=10)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, size=10)
    fig.tight_layout()
    fig.savefig('task4_correlation_heatmap.png', dpi=150, bbox_inches='tight')
    plt.close('all')
    print("  [OK] task4_correlation_heatmap.png 已保存\n")
    return my
