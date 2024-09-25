import pandas as pd


def read_bom_excel(file_path):
    """
    读取BOM清单Excel文件，并返回DataFrame对象。

    参数:
        file_path (str): Excel文件的路径。

    返回:
        dict: 含有多个DataFrame的对象，包括BOM清单、用户输入界面、工艺配方指定、字典-生产设备。
    """
    # 读取Excel文件中的各个Sheet
    with pd.ExcelFile(file_path) as xls:
        dataframes = {
            'BOM': pd.read_excel(xls, sheet_name='BOM'),
            '用户输入界面': pd.read_excel(xls, sheet_name='用户输入界面'),
            '工艺配方指定': pd.read_excel(xls, sheet_name='工艺配方指定'),
            '字典-生产设备': pd.read_excel(xls, sheet_name='字典-生产设备')
        }
    return dataframes


def get_user_input(dataframes):
    """
    从Excel文件中读取用户输入的产品生产速率需求和指定的产品行号。

    参数:
        dataframes (dict): 包含多个DataFrame的对象。

    返回:
        int: 用户指定的产品行号。
        float: 用户指定的产品生产速率需求。
    """
    user_input_df = dataframes['用户输入界面']
    row_number = int(user_input_df.at[0, '指定行号'])
    production_rate_demand = float(user_input_df.at[0, '生产速率需求'])
    return row_number, production_rate_demand


def get_equipment_speed(dataframes, equipment_name):
    """
    从字典-生产设备中获取设备的速度。

    参数:
        dataframes (dict): 包含多个DataFrame的对象。
        equipment_name (str): 设备名称。

    返回:
        float: 设备的速度。
    """
    equipment_df = dataframes['字典-生产设备']
    speed = equipment_df[equipment_df['设备名称'] == equipment_name]['制造速度'].values[0]
    return speed


def calculate_production_rate(dataframes, row_number, production_rate_demand):
    """
    计算指定产品的生产速率，并递归计算所有原料的需求量。

    参数:
        dataframes (dict): 包含多个DataFrame的对象。
        row_number (int): 用户指定的产品行号。
        production_rate_demand (float): 用户指定的产品生产速率需求。

    返回:
        dict: 包含所有生产设备的数量和基础物质的生产速率。
    """
    results = {}
    bom_df = dataframes['BOM']
    recipe_df = dataframes['工艺配方指定']
    equipment_df = dataframes['字典-生产设备']

    def process_product(row_number, rate, depth=0):
        if depth > 30:
            return

        product_row = bom_df.loc[row_number]
        equipment_name = recipe_df.loc[row_number, '生产设备（选择）']
        equipment_speed = get_equipment_speed(dataframes, equipment_name)

        # 计算生产设备数量
        equipment_count = round(rate / (product_row['输出1数量'] * 60 / (product_row['制造时间'] / equipment_speed)))
        results[f"设备{equipment_name}"] = results.get(f"设备{equipment_name}", 0) + equipment_count

        # 计算副产品的生产速率
        if not pd.isna(product_row['输出2']):
            byproduct_rate = rate * product_row['输出2数量'] / product_row['输出1数量']
            results[f"副产品{product_row['输出2']}"] = results.get(f"副产品{product_row['输出2']}",
                                                                       0) + byproduct_rate

        # 计算原料的需求量
        if not pd.isna(product_row['输入1']):
            input_rate = rate * product_row['输入1数量'] / product_row['输出1数量']
            process_product(recipe_df[recipe_df['产品名'] == product_row['输入1']].index[0], input_rate,
                            depth + 1)

        # 如果还有第二个原料，递归处理
        if not pd.isna(product_row['输入2名称']):
            input_rate = rate * product_row['输入2数量'] / product_row['输出1数量']
            process_product(recipe_df[recipe_df['产品名'] == product_row['输入2名称']].index[0], input_rate,
                            depth + 1)

    process_product(row_number, production_rate_demand)
    return results


def generate_report(results):
    """
    生成报告，包括每次迭代的结果和汇总结果。

    参数:
        results (dict): 包含所有生产设备的数量和基础物质的生产速率。
    """
    for key, value in results.items():
        print(f"{key}: {value}")

    # 假设所有基础物质的生产速率可以直接从results中提取
    base_materials = {k: v for k, v in results.items() if '基础物质' in k}
    print("\n基础物质的生产速率:")
    for material, rate in base_materials.items():
        print(f"{material}: {rate}")


def main():
    """
    主函数，用于执行整个流水线订单的计算过程。
    """
    # 文件路径
    file_path = 'C:/Factory/BOM清单V1.1(20240825).xlsx'

    # 读取BOM清单和其他相关数据
    dataframes = read_bom_excel(file_path)

    # 获取用户输入
    row_number, production_rate_demand = get_user_input(dataframes)

    # 计算生产速率
    results = calculate_production_rate(dataframes, row_number, production_rate_demand)

    # 生成报告
    generate_report(results)


if __name__ == '__main__':
    main()