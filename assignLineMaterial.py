# 为每条产线找到最优解
import random
from model import ProductionLine, Material, MaterialLine, AssignState,MonthProduction
from utils import generate_random_string
import pandas as pd
from typing import Tuple


def assignMain():
    for month in range(1, 13):
        materials, production_lines = getMonthMaterialsAndProductionLines(month)
        # 分配算法
        for material in materials:
            best_line, need_usage = getBestLineAndNeedUsageByMaterial(material)
            if best_line is not None:
                best_line.produce_material.append(material)
                best_line.usage += need_usage
        monthProduction = MonthProduction(month=month,production_lines=production_lines)
        print(monthProduction.getMonthLineData())
        

def getMonthMaterialsAndProductionLines(month):
    # TODO:获取指定月份的物料和产线数据,产线是需要重新实例化的,因为每月产线都从0开始运作
    # 生成 10 个产线数据
    production_lines = [ProductionLine(
        name=generate_random_string(10),
        code=f"PL-{random.randint(100, 999)}",
        line_type=random.choice(["lineTypeA", "lineTypeB", "lineTypeC"]),
        line_desc=generate_random_string(20),
        init_life=random.randint(180000, 200000)
    ) for _ in range(10)]

    # 生成 1000 个物料数据
    materials = [Material(
        name=generate_random_string(8),
        code=f"M-{random.randint(1000, 9999)}",
        material_type=random.choice(["materialTypeA", "materialTypeB", "materialTypeC"]),
        material_desc=generate_random_string(15),
        req=random.randint(50, 500),
        production_lines=[MaterialLine(line=random.choice(production_lines), ct=random.randint(10, 50)) for _ in range(random.randint(1, 5))]
    ) for _ in range(1000)] # production_lines 只能从当月生成的产线中选择
    return materials, production_lines

def getBestLineAndNeedUsageByMaterial(material: Material) -> Tuple[ProductionLine, int]:
    """获取最优产线,不对产线作修改,只获取最优产线

    Args:
        material (Material): _description_

    Returns:
        ProductionLine: _description_
    """
    lineUsage = []
    for materialLine in material.production_lines:
        if materialLine.line.assign_state == AssignState.FINISHED:
            # 加完之前发现该线已达标了
            continue
        materialLine: MaterialLine = materialLine
        need_usage = materialLine.ct * material.req
        origin_usage = materialLine.line.usage
        materialLine.line.usage = origin_usage + need_usage
        if materialLine.line.assign_state == AssignState.FINISHED:
            # 加完之后发现超目标了
            materialLine.line.usage = origin_usage
            continue
        lineUsage.append({
            "line": materialLine.line,
            "usage_rate": materialLine.line.usage_rate,
            "need_usage": need_usage,
        })
        # 恢复原有usage
        materialLine.line.usage = origin_usage
    if len(lineUsage) == 0:
        return None, 0
    df = pd.DataFrame(lineUsage)
    df = df.sort_values(by="usage_rate", ascending=False)
    best_line: ProductionLine = df.iloc[0]["line"]  # 取出第一行（最小的）对应的 line
    need_usage = df.iloc[0]["need_usage"]  # 取出第一行（最小的）对应的 line
    return best_line, need_usage
