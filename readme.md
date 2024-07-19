# 产能分析 - GZH

## 描述

* 目的: 拉满所有机器
* 每颗物料可在不同产线上作业,并且在每个产线上的单件工时不同
* 已知条件 : 所有物料的未来需求数量和它们相应的产线上的表现(单件工时)

### 如何运行

```python
pip install -r requirement.txt
python main.py
```

##### 核心逻辑代码

```python
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



```
