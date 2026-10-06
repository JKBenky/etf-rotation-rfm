
from .config import (pd)


def preprocess():
    print()
    print("+" + "-" * 52 + "+")
    print("  设计二-1  原始数据清洗 & 预处理")
    print("+" + "-" * 52 + "+")

    # ========== 读入 ==========
    print("\n  第一步: 读取 excel")
    src = pd.read_excel('橙色桃子用户数据.xlsx')
    r0, c0 = src.shape
    print("      原始维度: %d 行 x %d 列" % (r0, c0))
    print("      原始列名: %s" % src.columns.tolist())

    # ========== 列名统一 ==========
    print("\n  第二步: 统一列名为英文")
    renames = {
        '用户id': 'user_id',
        '商品标题': 'product_title',
        '消费次数': 'purchase_count',
        '开销总额': 'total_spending',
        '商品标号': 'product_code',
        '店名': 'store_name',
        '最近一次购买时间': 'last_purchase_date',
    }
    data = src.rename(columns=renames)
    print("      改名后: %s" % list(data.columns))

    # ========== 缺失值 ==========
    print("\n  第三步: 检查缺失值")
    null_stats = data.isnull().sum()
    print("      %s" % null_stats.to_dict())
    total_nulls = null_stats.sum()
    if total_nulls == 0:
        print("      -> 无缺失, 跳过填充")
    else:

        for c in null_stats[null_stats > 0].index:
            if c in ('total_spending', 'purchase_count'):
                fill_v = data[c].median()
                data[c] = data[c].fillna(fill_v)
                print("      %s: 中位数填充 -> %.2f" % (c, fill_v))
            elif c == 'last_purchase_date':
                data[c] = data[c].fillna('2025-07-01')
                print("      %s: 用默认日期填充" % c)


    print("\n  第四步: 类型规范化")
    data['last_purchase_date'] = pd.to_datetime(data['last_purchase_date'])
    dmin = data['last_purchase_date'].min().date()
    dmax = data['last_purchase_date'].max().date()
    print("      last_purchase_date -> datetime64, 范围[%s ~ %s]" % (dmin, dmax))


    print("\n  第五步: IQR异常值检测 (3倍IQR)")
    need_check = ['purchase_count', 'total_spending', 'product_code']
    for col in need_check:
        q1 = data[col].quantile(0.25)
        q3 = data[col].quantile(0.75)
        iqr = q3 - q1
        lo = q1 - 3.0 * iqr
        hi = q3 + 3.0 * iqr
        outlier_mask = (data[col] < lo) | (data[col] > hi)
        n_out = outlier_mask.sum()
        pct_out = n_out / len(data) * 100
        print("      %-20s: [%8.1f, %8.1f]  异常%4d条 (%4.1f%%)" % (
            col, lo, hi, n_out, pct_out), end='')
        if n_out > 0:
            data[col] = data[col].clip(lower=lo, upper=hi)
            print(" -> Winsorize截尾")
        else:
            print()


    print("\n  第六步: 逻辑过滤")
    before = len(data)

    data = data[data['purchase_count'] > 0].copy()

    data = data[data['total_spending'] >= 0].copy()

    cutoff = pd.Timestamp('2026-05-28')
    data = data[data['last_purchase_date'] <= cutoff].copy()
    removed = before - len(data)
    n_after = len(data)
    print("      过滤前 %d -> 过滤后 %d (去除 %d 条无效)" % (before, n_after, removed))
    print("      店铺总数: %d" % data['store_name'].nunique())

    print("\n  + 数据预处理结束 +\n")
    return data
