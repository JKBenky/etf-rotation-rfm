
# 班级序号（脱敏：原序号为个人身份信息，展示时已置空）
CLASS_NUMBER = 0
IS_ODD = (CLASS_NUMBER % 2 == 1)
IS_GROUP1 = (CLASS_NUMBER % 4 in (1, 2))

ETF_MAIN = {
    '512480': '半导体ETF',
    '515000': '科技ETF',
    '159928': '消费ETF',
}

# 备用ETF (根据班级序号分配)
MYETF_CODE = '512010'
MYETF_NAME = '医药ETF'

# 打印参数
PRINT_TARGET_CODE = '159928'
PRINT_START_ROW = 7
PRINT_END_ROW = 32


def get_etf_data(code, name):

    try:
        df = ak.fund_etf_hist_em(
            symbol=code,
            period='monthly',
            start_date='20200101',
            end_date='20260101',
            adjust='qfq'
        )
        if df is None or df.empty:
            print("  [WARN] {}({}) 无数据返回".format(name, code))
            return None

        df['date'] = pd.to_datetime(df['日期'] if '日期' in df.columns else df.index)
        df = df.set_index('date')
        df = df[['收盘']].rename(columns={'收盘': code})
        df = df.sort_index()
        df[code] = pd.to_numeric(df[code], errors='coerce')
        df = df.dropna(subset=[code])
        return df
    except Exception as e:
        print("  [ERR] {}({}): {}".format(name, code, e))
        return None


# ==================== 全局绘图设置 ====================
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
sns.set_style('whitegrid')
