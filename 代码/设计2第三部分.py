# 设计二 · 第三部分: 可视化数据展现与分析 (10分)
from .config import (pd, np, plt, sns)


def visualize(rfm, seg_counts, seg_means):
    print()
    print("." * 60)
    print("   设计二-3  RFM 可视化展示")
    print("." * 60)
    print()

    # 6 个子图: 2 行 x 3 列
    n_rows, n_cols = 2, 3
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(18, 11))

    # ----- 子图1: R分布 -----
    ax = axes[0, 0]
    ax.hist(rfm['recency'], bins=48, color='#3182bd',
            edgecolor='#ffffff', alpha=0.82)
    median_r = rfm['recency'].median()
    ax.axvline(median_r, color='#d62728', linestyle=(0, (6, 2)),
               linewidth=2.4, label='中位数={:.0f}d'.format(median_r))
    ax.set_title('R -- 最近购买距今天数', fontsize=13, weight='bold')
    ax.set_xlabel('天数')
    ax.set_ylabel('客户数')
    ax.legend(loc='best', fontsize=9)
    ax.grid(True, alpha=0.18, linestyle=':')

    # ----- 子图2: F分布 (log尺度) -----
    ax = axes[0, 1]
    f_logged = np.log1p(rfm['frequency'])
    ax.hist(f_logged, bins=48, color='#31a354',
            edgecolor='#e8e8e8', alpha=0.78)
    ax.axvline(f_logged.median(), color='#d62728',
               linestyle=(0, (6, 2)), linewidth=2.4,
               label='中位数={:.0f}次'.format(rfm["frequency"].median()))
    ax.set_title('F -- 购买频率 (ln尺度)', fontsize=13, weight='bold')
    ax.set_xlabel('ln(1+频次)')
    ax.set_ylabel('客户数')
    ax.legend(loc=1, fontsize=9)
    ax.grid(True, alpha=0.28, linestyle='-.')

    # ----- 子图3: M分布 (log尺度) -----
    ax = axes[0, 2]
    m_logged = np.log1p(rfm['monetary'])
    ax.hist(m_logged, bins=48, color='#e5a431',
            edgecolor='#f0f0f0', alpha=0.85)
    ax.axvline(m_logged.median(), color='#d62728',
               linestyle=(0, (6, 2)), linewidth=2.4,
               label='中位数={:.0f}元'.format(rfm["monetary"].median()))
    ax.set_title('M -- 消费金额 (ln尺度)', fontsize=13, weight='bold')
    ax.set_xlabel('ln(1+金额)')
    ax.set_ylabel('客户数')
    ax.legend(loc=2, fontsize=9)
    ax.grid(True, alpha=0.15, linestyle=(0, (3, 4)))

    # ----- 子图4: 饼图 -----
    ax = axes[1, 0]
    tier_order = ['高价值客户', '中等价值客户', '低价值客户']
    pie_vals = [seg_counts.get(t, 0) for t in tier_order]
    pie_palette = ['#d73027', '#4575b4', '#a6d96a']
    wedges, labels, pct_texts = ax.pie(
        pie_vals, labels=tier_order, colors=pie_palette,
        explode=(0.03, 0.03, 0.03), autopct='%1.1f%%',
        startangle=140, textprops={'size': 11}
    )
    for t in pct_texts:
        t.set_weight('bold')
    ax.set_title('客户价值层级占比', fontsize=13, weight='bold')

    # ----- 子图5: R-F散点 (颜色=M) -----
    ax = axes[1, 1]
    pts = ax.scatter(
        rfm['recency'], rfm['frequency'],
        c=np.log1p(rfm['monetary']), cmap='plasma',
        alpha=0.45, s=22, edgecolors='none'
    )
    ax.set_xlabel('Recency (天)')
    ax.set_ylabel('Frequency (次)')
    ax.set_title('客户 R-F 散点  [色=ln(1+M)]', fontsize=13, weight='bold')
    ax.grid(True, alpha=0.2, linestyle=':')
    cbar = fig.colorbar(pts, ax=ax, shrink=0.78)
    cbar.set_label('ln(1+M)', fontsize=9)

    # ----- 子图6: 雷达图 (已归一化到0-1) -----
    ax = axes[1, 2]
    # 归一化
    normed = seg_means.copy()
    # R反归一化: R越小越好 -> 分数越高
    rng_r = normed['recency'].max() - normed['recency'].min()
    normed['recency'] = 1.0 - (
        (normed['recency'] - normed['recency'].min()) / max(rng_r, 1e-10)
    )
    for col in ('frequency', 'monetary'):
        rng = normed[col].max() - normed[col].min()
        normed[col] = (normed[col] - normed[col].min()) / max(rng, 1e-10)

    dims = ['R\n(近度)', 'F\n(频度)', 'M\n(金额)']
    n_dim = len(dims)
    angles = np.linspace(0, 2 * np.pi, n_dim, endpoint=False).tolist()
    angles += angles[:1]  # 闭合

    radar_colors = ['#d73027', '#4575b4', '#a6d96a']
    for i, tier in enumerate(tier_order):
        if tier not in normed.index:
            continue
        vals = normed.loc[tier].tolist()
        vals += vals[:1]
        ax.fill(angles, vals, alpha=0.10, color=radar_colors[i])
        ax.plot(angles, vals, 'o-', lw=2.2, color=radar_colors[i],
                label=tier, markersize=5)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(dims, fontsize=10)
    ax.set_ylim(0, 1.08)
    ax.set_title('各层级 RFM 雷达图 (0-1归一化)', fontsize=13, weight='bold')
    ax.legend(loc='lower right', fontsize=9)
    ax.grid(True, alpha=0.25, linewidth=0.6)

    fig.tight_layout(pad=2.8)
    fig.savefig('task6_rfm_visualization.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("  [OK] task6_rfm_visualization.png 已生成")

    print("  . 可视化完成 .\n")
