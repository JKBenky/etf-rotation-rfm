
from .config import (pd, np)


def label_segment(score):

    if score >= 11:
        return '高价值客户'
    elif score >= 7:
        return '中等价值客户'
    return '低价值客户'


def run(df):
    print()
    print("=" * 58)
    print("   设计二-2  RFM 客户分层")
    print("=" * 58)


    BASE_DT = pd.Timestamp('2026-05-28')
    print(f"\n  分析基准日: {BASE_DT.date()}")


    print("\n  [聚合] 计算 R / F / M")
    dup_check = df.groupby('user_id').size()
    multi_order_users = dup_check[dup_check > 1]
    print(f"  存在多笔记录的用户: {len(multi_order_users)} 位")

    if len(multi_order_users) > 0:

        agg_rfm = df.groupby('user_id').agg(
            last_purchase_date=('last_purchase_date', 'max'),
            frequency=('purchase_count', 'sum'),
            monetary=('total_spending', 'sum')
        ).reset_index()
    else:

        agg_rfm = df[['user_id', 'last_purchase_date',
                       'purchase_count', 'total_spending']].copy()
        agg_rfm.columns = ['user_id', 'last_purchase_date',
                           'frequency', 'monetary']


    agg_rfm['recency'] = (BASE_DT - agg_rfm['last_purchase_date']).dt.days

    print(f"\n  [描述统计]")
    print(f"    Recency : mean={agg_rfm['recency'].mean():.0f}d  "
          f"median={agg_rfm['recency'].median():.0f}d  "
          f"[{agg_rfm['recency'].min()}, {agg_rfm['recency'].max()}]")
    print(f"    Frequency: mean={agg_rfm['frequency'].mean():.1f}  "
          f"median={agg_rfm['frequency'].median():.0f}  "
          f"[{agg_rfm['frequency'].min()}, {agg_rfm['frequency'].max()}]")
    print(f"    Monetary : mean={agg_rfm['monetary'].mean():.0f}  "
          f"median={agg_rfm['monetary'].median():.0f}  "
          f"[{agg_rfm['monetary'].min()}, {agg_rfm['monetary'].max()}]")


    print(f"\n  [评分] 五分位打分 (1~5)")


    r_tmp = pd.qcut(agg_rfm['recency'], q=5, labels=[5, 4, 3, 2, 1])
    agg_rfm['R_score'] = r_tmp.astype(int)


    f_labels = [1, 2, 3, 4, 5]
    try:
        f_tmp = pd.qcut(agg_rfm['frequency'], q=5, labels=f_labels)
        agg_rfm['F_score'] = f_tmp.astype(int)
    except ValueError:

        f_ranked = agg_rfm['frequency'].rank(method='first')
        agg_rfm['F_score'] = pd.qcut(f_ranked, q=5, labels=f_labels).astype(int)


    m_labels = [1, 2, 3, 4, 5]
    try:
        m_tmp = pd.qcut(agg_rfm['monetary'], q=5, labels=m_labels)
        agg_rfm['M_score'] = m_tmp.astype(int)
    except ValueError:
        m_ranked = agg_rfm['monetary'].rank(method='first')
        agg_rfm['M_score'] = pd.qcut(m_ranked, q=5, labels=m_labels).astype(int)


    agg_rfm['RFM_total'] = (agg_rfm['R_score'] +
                            agg_rfm['F_score'] +
                            agg_rfm['M_score'])

    print(f"    R 分位分布: {agg_rfm['R_score'].value_counts().sort_index().to_dict()}")
    print(f"    F 分位分布: {agg_rfm['F_score'].value_counts().sort_index().to_dict()}")
    print(f"    M 分位分布: {agg_rfm['M_score'].value_counts().sort_index().to_dict()}")
    print(f"    RFM总分: [{agg_rfm['RFM_total'].min()}, {agg_rfm['RFM_total'].max()}]")


    print(f"\n  [分层结果]")
    agg_rfm['segment'] = agg_rfm['RFM_total'].apply(label_segment)

    dist = agg_rfm['segment'].value_counts()
    print(f"  {'层级':<14s} {'人数':>7s} {'占比':>9s}  {'柱状示意'}")
    print(f"  {'-' * 48}")
    tier_order = ['高价值客户', '中等价值客户', '低价值客户']
    total_cust = len(agg_rfm)
    for tier in tier_order:
        n = dist.get(tier, 0)
        ratio = n / total_cust * 100
        bar = '#' * int(ratio)
        print(f"  {tier:<14s} {n:>7d} {ratio:>8.2f}%  {bar}")


    tier_profile = agg_rfm.groupby('segment')[
        ['recency', 'frequency', 'monetary']
    ].mean()
    print(f"\n  各层R/F/M均值:")
    print(tier_profile.round(1).to_string())


    hi_pct = dist.get('高价值客户', 0) / total_cust * 100
    print(f"\n  [小结] 高价值客户占比 {hi_pct:.1f}%, "
          f"总客户数 {total_cust}")

    print("\n  == RFM分类完成 ==\n")
    return agg_rfm, dist, tier_profile
