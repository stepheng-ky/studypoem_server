// 初始化省份和城市数据
const provinces = ["北京", "天津", "河北", "山西", "内蒙古", "辽宁", "吉林", "黑龙江", "上海"
    , "江苏", "浙江", "安徽", "福建", "江西", "山东", "河南", "湖北", "湖南", "广东", "广西", "海南"
    , "重庆", "四川", "贵州", "云南", "西藏", "陕西", "甘肃", "青海", "宁夏", "新疆"];

// 页面加载时初始化地图状态
window.onload = function () {
    const provinceSelect = document.getElementById('province');

    // 加载省份选项（保持不变）
    provinces.forEach(province => {
        const option = document.createElement('option');
        option.value = province;
        option.textContent = province;
        provinceSelect.appendChild(option);
    });

    // 加载已点亮的省份状态（修正：遍历对象数组）
    loadSavedProvinces();

    // 初始化默认省份颜色为灰色（保持不变）
    const allProvinceElements = document.querySelectorAll('#china-map path'); // 明确选择 svg 内的 path
    allProvinceElements.forEach(provinceElement => {
        provinceElement.style.fill = 'gray';
    });

    // 弹窗逻辑（保持不变）
    document.getElementById('点亮足迹').addEventListener('click', function () {
        document.getElementById('modal').classList.remove('hidden');
    });

    document.getElementById('close-modal').addEventListener('click', function () {
        document.getElementById('modal').classList.add('hidden');
    });

    // 仅保留修改后的提交逻辑（移除原重复绑定）
    document.getElementById('footprint-form').addEventListener('submit', function (event) {
        event.preventDefault();
        const province = document.getElementById('province').value;
        const date = document.getElementById('date').value; // 确保获取到正确的日期值
        updateMapProvince(province);
        saveProvince(province, date); // 传递省份和时间
        this.reset();
        document.getElementById('modal').classList.add('hidden');
        alert(`已点亮 ${province} 的足迹，时间为 ${date}`);
    });

    // 新增：创建提示框元素
    const tooltip = document.createElement('div');
    tooltip.id = 'province-tooltip';
    tooltip.style.position = 'fixed';
    tooltip.style.display = 'none';
    tooltip.style.backgroundColor = 'rgba(0,0,0,0.8)';
    tooltip.style.color = 'white';
    tooltip.style.padding = '8px 12px';
    tooltip.style.borderRadius = '4px';
    tooltip.style.fontSize = '14px';
    tooltip.style.zIndex = '1000'; // 确保在最上层
    document.body.appendChild(tooltip);

    // 新增：为所有省份路径元素添加事件监听
    const provinceElements = document.querySelectorAll('#china-map path');
    provinceElements.forEach(provinceElement => {
        provinceElement.style.pointerEvents = 'auto'; // 允许鼠标事件

        // 鼠标悬停时
        provinceElement.addEventListener('mouseover', function (e) {
            const province = this.id; // 获取省份名称（与 path 的 id 一致）
            const savedProvinces = JSON.parse(localStorage.getItem('litProvinces')) || [];
            const provinceData = savedProvinces.find(item => item.province === province);
            const timeText = provinceData ? `点亮时间：${provinceData.date}` : '未点亮'; // 关键：读取 date 字段

            // 设置提示框内容和位置
            tooltip.innerHTML = `省份：${province}<br>${timeText}`;
            tooltip.style.left = `${e.clientX + 10}px`;
            tooltip.style.top = `${e.clientY + 10}px`;
            tooltip.style.display = 'block';
        });

        // 鼠标离开时
        provinceElement.addEventListener('mouseout', function () {
            tooltip.style.display = 'none';
        });
    });
};

// 保存已点亮的省份（修正：正确接收 date 参数）
function saveProvince(province, date) {
    let savedProvinces = JSON.parse(localStorage.getItem('litProvinces')) || [];
    const isExisted = savedProvinces.some(item => item.province === province);
    if (!isExisted) {
        savedProvinces.push({ province, date }); // 存储包含 date 的对象
        localStorage.setItem('litProvinces', JSON.stringify(savedProvinces));
    }
}

// 加载已点亮的省份（修正：遍历对象数组）
function loadSavedProvinces() {
    const savedProvinces = JSON.parse(localStorage.getItem('litProvinces')) || [];
    savedProvinces.forEach(item => {
        updateMapProvince(item.province); // 提取对象中的省份名称
    });
}

// 更新地图颜色（保持不变）
function updateMapProvince(province) {
    const provinceElement = document.querySelector(`#china-map [id="${province}"]`); // 明确选择 svg 内的 path
    if (provinceElement) {
        provinceElement.style.fill = 'green';
    }
}
