
from .config import (pd, get_etf_data, MYETF_CODE, MYETF_NAME, CLASS_NUMBER, IS_GROUP1)


def run():
    print()
    print("~ " * 30)
    print("   任务2  备用ETF: 本地读写验证")
    print("~ " * 30)

    grp = "第1组" if IS_GROUP1 else "第2组"
    print("  %s | %s | 班级%d -> %s\n" % (MYETF_NAME, MYETF_CODE, CLASS_NUMBER, grp))

    # 下载ETF数据
    raw = get_etf_data(MYETF_CODE, MYETF_NAME)

    rng_min = raw.index.min().date()
    rng_max = raw.index.max().date()
    print("  数据范围: %s ~ %s" % (rng_min, rng_max))


    price_col = raw.columns[0]
    price_min = raw[price_col].min()
    price_max = raw[price_col].max()
    print("  价格区间: [%.2f, %.2f]" % (price_min, price_max))


    flat = raw.reset_index()
    flat.columns = ['date', 'myetf']
    nrow = len(flat)
    flat.to_csv('myetf.csv', index=False, encoding='utf-8-sig')
    print("  -> 写出完毕 myetf.csv (行数=%d, index=False)" % nrow)


    back = pd.read_csv('myetf.csv', encoding='utf-8-sig')
    shp = back.shape
    print("  -> 回读 shape=%s" % str(shp))


    null_cnt = back.isnull().sum().sum()
    dup_cnt = back.duplicated().sum()
    print("  -> 质量检查: 缺失值=%d, 重复行=%d" % (null_cnt, dup_cnt))


    print("\n    -- head 6 --")
    print(back.head(6).to_string(index=False))
    print("\n    -- tail 6 --")
    print(back.tail(6).to_string(index=False))


    print("\n  idx=%s" % str(back.index))
    print("  cols=%s" % str(back.columns.tolist()))
    print("  idx_dtype=%s" % back.index.dtype)

    print("\n  任务2 完成\n")
    return raw
