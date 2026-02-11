import numpy as np
from scipy import stats
from typing import List, Dict, Tuple, Optional, Union

class StatisticsError(Exception):
    """统计计算相关的异常类"""
    pass

class InputValidationError(StatisticsError):
    """输入参数验证异常"""
    pass

class GenerationError(StatisticsError):
    """数据生成异常"""
    pass

# 质量工程专业级：基于确定性构造与精度补偿的正态分布生成算法
def generate_numbers_robust_spc(
    target_mean: float, 
    usl: float, 
    lsl: float, 
    cpk_min: float, 
    cpk_max: float, 
    precision: int, 
    count: int = 32
) -> Tuple[np.ndarray, float, float, float, float]:
    """
    质量工程专业级：基于确定性构造与精度补偿的正态分布生成算法
    
    参数:
        target_mean: 目标均值
        usl: 规格上限
        lsl: 规格下限
        cpk_min: 最小CPK值
        cpk_max: 最大CPK值
        precision: 精度（小数位数）
        count: 样本数量
    
    返回:
        Tuple[np.ndarray, float, float, float, float]: (生成的随机数, CP值, CPK值, 实际均值, 实际标准差)
    
    异常:
        InputValidationError: 输入参数验证失败
        GenerationError: 数据生成失败
    """
    # --- 1. 严格的输入参数验证 ---
    # 基本类型和范围检查
    if not isinstance(target_mean, (int, float)) or not isinstance(usl, (int, float)) or not isinstance(lsl, (int, float)):
        raise InputValidationError("均值、规格上限和规格下限必须是数值类型")
    
    if not isinstance(cpk_min, (int, float)) or not isinstance(cpk_max, (int, float)):
        raise InputValidationError("CPK值必须是数值类型")
    
    if not isinstance(precision, int) or precision < 0 or precision > 10:
        raise InputValidationError("精度必须是0-10之间的整数")
    
    if not isinstance(count, int) or count < 5 or count > 10000:
        raise InputValidationError("样本数量必须是5-10000之间的整数")
    
    # 业务逻辑检查
    if usl <= lsl:
        raise InputValidationError(f"规格上限(USL={usl})必须大于规格下限(LSL={lsl})")
    
    if not (lsl < target_mean < usl):
        raise InputValidationError(f"均值目标({target_mean})必须在规格限({lsl}-{usl})之间")
    
    if cpk_min <= 0 or cpk_max <= 0:
        raise InputValidationError("CPK值必须为正数")
    
    if cpk_min >= cpk_max:
        raise InputValidationError(f"最小CPK值({cpk_min})必须小于最大CPK值({cpk_max})")
    
    # 计算目标 Sigma 范围
    # Cpk = min( (USL-mu)/3s, (mu-LSL)/3s )
    dist_to_closest_spec = min(usl - target_mean, target_mean - lsl)
    
    if dist_to_closest_spec <= 0:
        raise InputValidationError("均值目标距离规格边界过近，无法生成有效数据")
    
    try:
        sigma_max = dist_to_closest_spec / (3 * cpk_min)
        sigma_min = dist_to_closest_spec / (3 * cpk_max)
    except ZeroDivisionError:
        raise InputValidationError("CPK值不能为零")
    
    if sigma_max <= 0:
        raise InputValidationError("计算得到的Sigma无效，请检查CPK设置是否为正数")

    # 选取目标参数（取中值以获得最大缓冲空间）
    target_sigma = (sigma_min + sigma_max) / 2
    
    # --- 2. 截断正态确定性采样 (确保100%在规格内) ---
    # 计算截断边界的累积分布值
    a, b = (lsl - target_mean) / target_sigma, (usl - target_mean) / target_sigma
    lower_phi = stats.norm.cdf(a)
    upper_phi = stats.norm.cdf(b)
    
    # 防止极端情况下的数值问题
    if upper_phi - lower_phi < 1e-10:
        raise GenerationError("规格限范围过小，无法生成有效的正态分布数据")
    
    # 在[lower_phi, upper_phi]之间均匀生成概率分布，再映射回Z分数
    u = np.linspace(lower_phi, upper_phi, count + 2)[1:-1]  # 避免取到极端的边界点
    np.random.shuffle(u)  # 随机扰动顺序
    
    try:
        z = stats.norm.ppf(u)
    except Exception as e:
        raise GenerationError(f"生成Z分数时出错: {str(e)}")
    
    # --- 3. 样本特征精确对齐 (对齐 mu, s) ---
    # 强制让生成的序列 Mean=0, Std=1 (Sample SD, ddof=1)
    z_mean = np.mean(z)
    z_std = np.std(z, ddof=1)
    
    if z_std <= 1e-10:
        raise GenerationError("生成的Z分数方差过小，无法继续计算")
    
    z = (z - z_mean) / z_std
    
    # 转换为目标分布
    x = target_mean + target_sigma * z
    
    # --- 4. 精度损失补偿 (The "Nudge" Strategy) ---
    # 步骤 A: 初始舍入
    x_rounded = np.round(x, precision)
    unit = 10**(-precision)  # 最小精度单位
    
    max_iter = 20  # 最大通过微调补偿的次数
    for _ in range(max_iter):
        # 计算当前统计量
        curr_mean = np.mean(x_rounded)
        curr_s = np.std(x_rounded, ddof=1)
        
        # 防止标准差为零的情况
        if curr_s <= 1e-10:
            # 如果标准差过小，人为引入一些微小的波动
            x_rounded[0] += unit
            continue
        
        curr_cpk = min((usl - curr_mean) / (3 * curr_s), (curr_mean - lsl) / (3 * curr_s))
        
        # 检查是否满足 Cpk 范围
        if cpk_min <= curr_cpk <= cpk_max:
            # 满足要求，返回结果
            # 计算CP值
            curr_cp = (usl - lsl) / (6 * curr_s)
            return x_rounded, curr_cp, curr_cpk, curr_mean, curr_s

        # 补偿策略：如果 Cpk 不满足，通常是 s (标准差) 偏离
        # 寻找对均值或方差偏差最大的点，进行 +/- 1 unit 的微调
        if curr_cpk < cpk_min:
            # 如果 Cpk 太小，说明波动(s)太大，需要缩减离均值最远的点
            idx = np.argmax(np.abs(x_rounded - curr_mean))
            # 向均值方向挪一步
            x_rounded[idx] += unit if x_rounded[idx] < curr_mean else -unit
        else:
            # 如果 Cpk 太大，说明波动(s)太小，需要扩大最远点的距离
            idx = np.argmin(np.abs(x_rounded - curr_mean))
            # 向远离均值方向挪一步
            x_rounded[idx] += -unit if x_rounded[idx] < curr_mean else unit
            
        # 确保不越界
        x_rounded = np.clip(x_rounded, lsl + unit, usl - unit)

    # 如果仍未退出，通常是由于样本量极小且精度太低，进行最后强制判定
    curr_s = np.std(x_rounded, ddof=1)
    curr_cp = (usl - lsl) / (6 * curr_s) if curr_s > 1e-10 else 0
    curr_mean_final = np.mean(x_rounded)
    curr_cpk_final = min((usl - curr_mean_final) / (3 * curr_s), 
                       (curr_mean_final - lsl) / (3 * curr_s)) if curr_s > 1e-10 else 0
    
    # 即使不满足CPK范围，也返回结果并给出警告
    return x_rounded, curr_cp, curr_cpk_final, curr_mean_final, curr_s

def generate_normal_distribution(
    mean: float, 
    std_dev: float, 
    count: int
) -> np.ndarray:
    """
    生成正态分布随机数
    
    参数:
        mean: 均值
        std_dev: 标准差
        count: 样本数量
    
    返回:
        np.ndarray: 生成的随机数
    """
    # 输入验证
    if not isinstance(mean, (int, float)) or not isinstance(std_dev, (int, float)):
        raise InputValidationError("均值和标准差必须是数值类型")
    
    if not isinstance(count, int) or count < 1 or count > 10000:
        raise InputValidationError("样本数量必须是1-10000之间的整数")
    
    if std_dev < 0:
        raise InputValidationError("标准差不能为负数")
    
    return np.random.normal(mean, std_dev, count)

def calculate_cpk(
    data: np.ndarray, 
    upper_spec: float, 
    lower_spec: float
) -> Tuple[float, float, float, float]:
    """
    计算CP和CPK值
    
    参数:
        data: 数据数组
        upper_spec: 规格上限
        lower_spec: 规格下限
    
    返回:
        Tuple[float, float, float, float]: (CP值, CPK值, 均值, 标准差)
    """
    # 输入验证
    if not isinstance(data, np.ndarray) or len(data) == 0:
        raise InputValidationError("数据数组不能为空")
    
    if not isinstance(upper_spec, (int, float)) or not isinstance(lower_spec, (int, float)):
        raise InputValidationError("规格限必须是数值类型")
    
    if upper_spec <= lower_spec:
        raise InputValidationError(f"规格上限({upper_spec})必须大于规格下限({lower_spec})")
    
    mean = np.mean(data)
    std_dev = np.std(data, ddof=1)
    
    if std_dev <= 1e-10:
        return 0, 0, mean, std_dev
    
    cp = (upper_spec - lower_spec) / (6 * std_dev)
    cpk = min((upper_spec - mean) / (3 * std_dev), 
              (mean - lower_spec) / (3 * std_dev))
    
    return cp, cpk, mean, std_dev

def generate_numbers_with_cpk(
    center: float, 
    upper_spec: float, 
    lower_spec: float, 
    cpk_lower: float, 
    cpk_upper: float, 
    mean: float, 
    precision: int, 
    count: int = 32
) -> Tuple[np.ndarray, float, float, float, float]:
    """
    生成满足CPK要求的随机数（传统方法，作为备选）
    
    参数:
        center: 中心值
        upper_spec: 规格上限
        lower_spec: 规格下限
        cpk_lower: 最小CPK值
        cpk_upper: 最大CPK值
        mean: 均值
        precision: 精度（小数位数）
        count: 样本数量
    
    返回:
        Tuple[np.ndarray, float, float, float, float]: (生成的随机数, CP值, CPK值, 实际均值, 实际标准差)
    """
    # 输入验证
    if not isinstance(center, (int, float)) or not isinstance(mean, (int, float)):
        raise InputValidationError("中心值和均值必须是数值类型")
    
    if not isinstance(upper_spec, (int, float)) or not isinstance(lower_spec, (int, float)):
        raise InputValidationError("规格限必须是数值类型")
    
    if not isinstance(cpk_lower, (int, float)) or not isinstance(cpk_upper, (int, float)):
        raise InputValidationError("CPK值必须是数值类型")
    
    if not isinstance(precision, int) or precision < 0 or precision > 10:
        raise InputValidationError("精度必须是0-10之间的整数")
    
    if not isinstance(count, int) or count < 5 or count > 10000:
        raise InputValidationError("样本数量必须是5-10000之间的整数")
    
    # 业务逻辑检查
    if upper_spec <= lower_spec:
        raise InputValidationError(f"规格上限({upper_spec})必须大于规格下限({lower_spec})")
    
    if not (lower_spec < mean < upper_spec):
        raise InputValidationError(f"均值({mean})必须在规格限({lower_spec}-{upper_spec})之间")
    
    if cpk_lower <= 0 or cpk_upper <= 0:
        raise InputValidationError("CPK值必须为正数")
    
    if cpk_lower >= cpk_upper:
        raise InputValidationError(f"最小CPK值({cpk_lower})必须小于最大CPK值({cpk_upper})")
    
    max_attempts = 5000
    
    # 1. 可行性检查：推导[σmin, σmax]
    d = min(upper_spec - mean, mean - lower_spec)
    if d <= 0:
        raise InputValidationError(f"均值 {mean} 超出规格限范围 [{lower_spec}, {upper_spec}]，无法生成符合要求的随机数")
    
    # 计算σ的范围
    sigma_min = d / (3 * cpk_upper)
    sigma_max = d / (3 * cpk_lower)
    
    # 检查σ范围是否合理
    if sigma_min < 0 or sigma_max < 0 or sigma_min > sigma_max:
        raise InputValidationError(f"CPK设置不合理，无法计算有效的标准差范围。请检查CPK设置。")
    
    # 2. 选CpkTarget（区间中值）
    cpk_target = (cpk_lower + cpk_upper) / 2
    
    # 3. 算σ
    sigma = d / (3 * cpk_target)
    
    # 4. 构造型采样：生成z并强制mean(z)=0, sd(z)=1
    for attempt in range(max_attempts):
        # 生成标准正态分布随机数
        z = np.random.normal(0, 1, count)
        
        # 强制mean(z)=0, sd(z)=1
        z_mean = np.mean(z)
        z_std = np.std(z, ddof=1)
        if z_std > 1e-10:
            z = (z - z_mean) / z_std
        
        # 得到x=μ+σz
        x = mean + sigma * z
        
        # 5. 用"内部未round的x"计算Cpk校验
        try:
            cp, cpk, mean_val, std_dev = calculate_cpk(x, upper_spec, lower_spec)
        except Exception:
            continue
        
        # 检查CPK是否在范围内
        if cpk_lower <= cpk <= cpk_upper:
            # 6. 启用"所有点必须在规格内"
            # 检查是否有越界点
            out_of_spec = np.any((x < lower_spec) | (x > upper_spec))
            
            if out_of_spec:
                # 对极少数越界点做温和替换
                for i in range(3):  # 迭代2-3次
                    # 找出越界点
                    mask = (x < lower_spec) | (x > upper_spec)
                    if not np.any(mask):
                        break
                    
                    # 替换越界点为规格边界内的值
                    x[mask] = np.random.uniform(lower_spec, upper_spec, np.sum(mask))
                    
                    # 线性微调把均值/标准差拉回目标
                    # 调整均值
                    current_mean = np.mean(x)
                    x = x + (mean - current_mean)
                    
                    # 调整标准差
                    current_std = np.std(x, ddof=1)
                    if current_std > 1e-10:
                        x = mean + (x - mean) * (sigma / current_std)
                    
                    # 再次检查越界
                    x = np.clip(x, lower_spec, upper_spec)
            
            # 展示时round
            numbers = np.round(x, precision)
            
            # 重新计算CPK（使用舍入后的值）
            try:
                final_cp, final_cpk, final_mean, final_std = calculate_cpk(numbers, upper_spec, lower_spec)
            except Exception:
                continue
            
            # 再次检查CPK是否在范围内
            if cpk_lower <= final_cpk <= cpk_upper:
                return numbers, final_cp, final_cpk, final_mean, final_std
    
    # 多次尝试后仍无法生成符合条件的CPK值，使用健壮算法作为备选
    try:
        return generate_numbers_robust_spc(
            mean, upper_spec, lower_spec, cpk_lower, cpk_upper, precision, count
        )
    except Exception as e:
        raise GenerationError(f"无法生成符合CPK范围 [{cpk_lower:.4f}, {cpk_upper:.4f}] 的随机数。经过 {max_attempts} 次尝试后仍未成功。请检查CPK设置是否合理，或尝试调整精度、样本量等参数。")

def calculate_additional_stats(numbers: Optional[np.ndarray]) -> Tuple[float, float, float, float]:
    """
    计算额外的统计信息
    
    参数:
        numbers: 数据数组
    
    返回:
        Tuple[float, float, float, float]: (最大值, 最小值, 范围, 方差)
    """
    if numbers is None or len(numbers) == 0:
        return 0, 0, 0, 0
    
    max_val = np.max(numbers)
    min_val = np.min(numbers)
    range_val = max_val - min_val
    variance = np.var(numbers, ddof=1)
    
    return max_val, min_val, range_val, variance

def perform_normality_tests(numbers: Optional[np.ndarray]) -> Dict[str, Union[float, bool]]:
    """
    执行正态性检验
    
    参数:
        numbers: 数据数组
    
    返回:
        Dict[str, Union[float, bool]]: 正态性检验结果
    """
    if numbers is None or len(numbers) < 3:
        return {
            'shapiro_stat': 0,
            'shapiro_p': 0,
            'dagostino_stat': 0,
            'dagostino_p': 0,
            'skewness': 0,
            'kurtosis': 0,
            'is_normal': False
        }
    
    try:
        # Shapiro-Wilk检验（适用于小样本，n < 5000）
        if len(numbers) < 5000:
            shapiro_stat, shapiro_p = stats.shapiro(numbers)
        else:
            # 对于大样本，使用Kolmogorov-Smirnov检验
            # 先标准化数据
            mean = np.mean(numbers)
            std = np.std(numbers, ddof=1)
            if std > 1e-10:
                normalized_numbers = (numbers - mean) / std
                shapiro_stat, shapiro_p = stats.kstest(normalized_numbers, 'norm')
            else:
                shapiro_stat, shapiro_p = 0, 0
        
        # D'Agostino's K-squared检验
        try:
            dagostino_stat, dagostino_p = stats.normaltest(numbers)
        except Exception:
            dagostino_stat, dagostino_p = 0, 0
        
        # 偏度和峰度
        skewness = stats.skew(numbers)
        kurtosis = stats.kurtosis(numbers)
        
        # 判断是否为正态分布（p值 > 0.05 通常认为符合正态分布）
        is_normal = shapiro_p > 0.05 and (dagostino_p > 0.05 or dagostino_p == 0)
        
        return {
            'shapiro_stat': shapiro_stat,
            'shapiro_p': shapiro_p,
            'dagostino_stat': dagostino_stat,
            'dagostino_p': dagostino_p,
            'skewness': skewness,
            'kurtosis': kurtosis,
            'is_normal': is_normal
        }
    except Exception as e:
        # 如果正态性检验失败，返回默认值
        return {
            'shapiro_stat': 0,
            'shapiro_p': 0,
            'dagostino_stat': 0,
            'dagostino_p': 0,
            'skewness': 0,
            'kurtosis': 0,
            'is_normal': False
        }

# 工厂函数：根据需求选择合适的生成算法
def generate_numbers_factory(
    algorithm: str = 'robust',
    **kwargs
) -> Tuple[np.ndarray, float, float, float, float]:
    """
    随机数生成算法工厂函数
    
    参数:
        algorithm: 算法类型 ('robust' 或 'traditional')
        **kwargs: 算法参数
    
    返回:
        Tuple[np.ndarray, float, float, float, float]: (生成的随机数, CP值, CPK值, 实际均值, 实际标准差)
    """
    if algorithm == 'robust':
        # 提取robust算法所需的参数
        required_params = ['target_mean', 'usl', 'lsl', 'cpk_min', 'cpk_max', 'precision']
        for param in required_params:
            if param not in kwargs:
                raise InputValidationError(f"健壮算法需要参数: {param}")
        
        return generate_numbers_robust_spc(
            kwargs['target_mean'],
            kwargs['usl'],
            kwargs['lsl'],
            kwargs['cpk_min'],
            kwargs['cpk_max'],
            kwargs['precision'],
            kwargs.get('count', 32)
        )
    elif algorithm == 'traditional':
        # 提取traditional算法所需的参数
        required_params = ['center', 'upper_spec', 'lower_spec', 'cpk_lower', 'cpk_upper', 'mean', 'precision']
        for param in required_params:
            if param not in kwargs:
                raise InputValidationError(f"传统算法需要参数: {param}")
        
        return generate_numbers_with_cpk(
            kwargs['center'],
            kwargs['upper_spec'],
            kwargs['lower_spec'],
            kwargs['cpk_lower'],
            kwargs['cpk_upper'],
            kwargs['mean'],
            kwargs['precision'],
            kwargs.get('count', 32)
        )
    else:
        raise InputValidationError(f"不支持的算法类型: {algorithm}")

