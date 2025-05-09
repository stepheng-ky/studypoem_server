
const provinces = ["北京", "天津", "河北", "山西", "内蒙古", "辽宁", "吉林", "黑龙江", "上海", "江苏", "浙江", "安徽", "福建", "江西"
    , "山东", "河南", "湖北", "湖南", "广东", "广西", "海南", "重庆", "四川", "贵州", "云南", "西藏", "陕西", "甘肃", "青海", "宁夏"
    , "新疆", "台湾", "香港", "澳门"];

let savedProvinces = []; // 用于存储从服务器获取的数据

// 页面加载时初始化地图状态
window.onload = function () {
    const provinceSelect = document.getElementById('province');

    // 加载省份选项
    provinces.forEach(province => {
        const option = document.createElement('option');
        option.value = province;
        option.textContent = province;
        provinceSelect.appendChild(option);
    });

    // 初始化默认省份颜色为灰色
    const allProvinceElements = document.querySelectorAll('#china-map path'); // 明确选择 svg 内的 path
    allProvinceElements.forEach(provinceElement => {
        provinceElement.style.fill = 'gray';
    });

    // 加载已点亮的省份状态
    loadSavedProvincesFromServer();

    // 添加省份名称到地图
    addProvinceNamesToMap();

    document.getElementById('点亮足迹').addEventListener('click', function () {
        updateProvinceDropdown(); // 每次打开模态框前更新下拉框
        document.getElementById('modal').classList.remove('hidden');
    });

    document.getElementById('close-modal').addEventListener('click', function () {
        document.getElementById('modal').classList.add('hidden');
    });

    document.getElementById('footprint-form').addEventListener('submit', function (event) {
        event.preventDefault();
        const province = document.getElementById('province').value;
        const date = document.getElementById('date').value;
        const imageInput = document.getElementById('image');
        const form = document.getElementById('footprint-form'); // 获取表单对象

        if (imageInput.files.length > 0) {
            const file = imageInput.files[0];
            updateMapProvince(province, date, URL.createObjectURL(file));
            saveProvinceToServer(province, date, file)
                .then(() => {
                    // 更新 savedProvinces 后重新加载地图状态
                    loadSavedProvincesFromServer().then(() => {
                        form.reset();
                        document.getElementById('modal').classList.add('hidden');
                        alert(`已点亮 ${province} 的足迹，时间为 ${date}`);
                    });
                })
            .catch(err => console.error("保存足迹失败:", err));
        } else {
            alert("请选择一张留念照片~");
        }
    });

    // 创建提示框元素
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

    // 为所有省份路径元素添加事件监听
    const provinceElements = document.querySelectorAll('#china-map path');
    provinceElements.forEach(provinceElement => {
        provinceElement.style.pointerEvents = 'auto'; // 允许鼠标事件

        // 鼠标悬停时
        provinceElement.addEventListener('mouseover', function (e) {
            const province = this.id; // 获取省份名称（与 path 的 id 一致）
            const provinceData = savedProvinces.find(item => item.province === province);
            const timeText = provinceData ? `点亮时间：${provinceData.light_up_time}` : '未点亮';

            // 设置提示框内容和位置
            tooltip.innerHTML = `${province}<br>${timeText}`;
            if (provinceData && provinceData.light_up_img) {
                // 使用接口动态生成图片URL
                const [imgPath, imgName] = provinceData.light_up_img.split('/');
                const imgUrl = `/studypoem/get_png/${imgPath}/${imgName}`;
                tooltip.innerHTML += `<br><img src="${imgUrl}" style="max-width:100px; max-height:100px;">`;
            }
            tooltip.style.left = `${e.clientX + 10}px`;
            tooltip.style.top = `${e.clientY + 10}px`;
            tooltip.style.display = 'block';
        });

        // 鼠标离开时
        provinceElement.addEventListener('mouseout', function () {
            tooltip.style.display = 'none';
        });
    });
    // ===== 地图缩放与拖拽功能开始 =====
    const svg = document.getElementById('china-map');
    let scale = 1;
    let offsetX = 0;
    let offsetY = 0;
    let isDragging = false;
    let lastMouseX = 0;
    let lastMouseY = 0;

    // 鼠标按下事件 - 开始拖拽
    svg.addEventListener('mousedown', function(e) {
        if (e.button === 0) { // 左键
            isDragging = true;
            lastMouseX = e.clientX;
            lastMouseY = e.clientY;
            svg.style.cursor = 'grabbing';
        }
    });

    // 鼠标松开事件 - 停止拖拽
    window.addEventListener('mouseup', function() {
        isDragging = false;
        svg.style.cursor = 'grab';
    });

    // 鼠标移动事件 - 拖拽地图
    window.addEventListener('mousemove', function(e) {
        if (isDragging) {
            const dx = e.clientX - lastMouseX;
            const dy = e.clientY - lastMouseY;

            offsetX += dx / scale;
            offsetY += dy / scale;

            updateTransform();

            lastMouseX = e.clientX;
            lastMouseY = e.clientY;
        }
    });

    // 滚轮事件 - 缩放
    svg.addEventListener('wheel', function(e) {
        e.preventDefault();

        const zoomFactor = 0.1;
        const mouseX = e.offsetX;
        const mouseY = e.offsetY;

        // 获取当前 viewBox
        const vb = svg.viewBox.baseVal;
        const zoomPointX = (mouseX / svg.clientWidth) * vb.width + vb.x;
        const zoomPointY = (mouseY / svg.clientHeight) * vb.height + vb.y;

        if (e.deltaY < 0) {
            console.log("鼠标滚轮向上:", e.deltaY);
            scale *= (1 + zoomFactor);
        } else {
            console.log("鼠标滚轮向下:", e.deltaY);
            scale /= (1 + zoomFactor);
        }

        // 限制缩放范围
        scale = Math.max(0.5, Math.min(scale, 5));

        // 更新 viewBox，以鼠标为中心缩放
        const newWidth = vb.width / scale;
        const newHeight = vb.height / scale;

        vb.x = zoomPointX - (mouseX / svg.clientWidth) * newWidth;
        vb.y = zoomPointY - (mouseY / svg.clientHeight) * newHeight;
        vb.width = newWidth;
        vb.height = newHeight;

    }, { passive: false });

    // 更新 transform（仅用于调试或附加效果）
    function updateTransform() {
        svg.style.transform = `translate(${offsetX}px, ${offsetY}px) scale(${scale})`;
    }

    // ===== 地图缩放与拖拽功能结束 =====

};

// 点亮足迹下拉框的省份更新
function updateProvinceDropdown() {
    const provinceSelect = document.getElementById('province');
    const selectedProvince = provinceSelect.value;

    // 清空现有选项
    provinceSelect.innerHTML = '';

    // 获取所有已点亮的省份名称
    const lightedProvinces = savedProvinces.map(p => p.province);

    // 筛选出未被点亮的省份
    const availableProvinces = provinces.filter(province => !lightedProvinces.includes(province));

    if (availableProvinces.length === 0) {
        const option = document.createElement('option');
        option.value = '';
        option.textContent = '无可点亮的省份';
        option.disabled = true;
        provinceSelect.appendChild(option);
    } else {
        availableProvinces.forEach(province => {
            const option = document.createElement('option');
            option.value = province;
            option.textContent = province;
            provinceSelect.appendChild(option);
        });

        // 可选：恢复上次选择（如果有）
        if (availableProvinces.includes(selectedProvince)) {
            provinceSelect.value = selectedProvince;
        }
    }
}

// 更新地图颜色并刷新全局变量
function updateMapProvince(province, date, image) {
    const provinceElement = document.querySelector(`#china-map [id="${province}"]`);
    if (provinceElement) {
        provinceElement.style.fill = 'green';
    }

    // 更新全局变量 savedProvinces
    const index = savedProvinces.findIndex(item => item.province === province);
    if (index === -1) {
        savedProvinces.push({ province, light_up_time: date, light_up_img: image });
    } else {
        savedProvinces[index] = { province, light_up_time: date, light_up_img: image };
    }
}

// 点亮足迹保存数据到服务器
async function saveProvinceToServer(province, date, imageFile) {
    const formData = new FormData();
    formData.append("province", province);
    formData.append("light_up_time", date);
    formData.append("light_up_img", imageFile);

    const response = await fetch("/studypoem/light_footprint", {
        method: "POST",
        body: formData
    });

    if (!response.ok) {
        throw new Error("上传失败");
    }

    return await response.json();
}

// 加载已点亮的省份（从服务器获取）
function loadSavedProvincesFromServer() {
    return fetch('/studypoem/all_footprints')
        .then(response => {
            if (!response.ok) {
                throw new Error("网络响应失败");
            }
            return response.json();
        })
        .then(data => {
            savedProvinces = data; // 更新全局变量
            data.forEach(item => {
                updateMapProvince(item.province, item.light_up_time, item.light_up_img); // 更新地图颜色
            });
        })
        .catch(err => {
            console.error("加载足迹失败:", err);
        });
}

/**
 * 在地图上添加省份名称
 */
function addProvinceNamesToMap() {
    // 手动配置特殊省份的文本位置
    const customPositions = {
        "辽宁": { xRatio: 0.58, yRatio: 0.50 },
        "河北": { xRatio: 0.35, yRatio: 0.65 },
        "内蒙古": { xRatio: 0.45, yRatio: 0.80 },
        "江苏": { xRatio: 0.60, yRatio: 0.50 },
        "陕西": { xRatio: 0.70, yRatio: 0.50 },
        "甘肃": { xRatio: 0.72, yRatio: 0.70 },
        "新疆": { xRatio: 0.60, yRatio: 0.50 },
        "云南": { xRatio: 0.45, yRatio: 0.60 },
        "台湾": { xRatio: 0.30, yRatio: 0.50 },
        "广西": { xRatio: 0.60, yRatio: 0.50 },
        "广东": { xRatio: 0.50, yRatio: 0.40 },
        "海南": { xRatio: 0.12, yRatio: 0.07 },
        "黑龙江": { xRatio: 0.50, yRatio: 0.70 }
    };

    const provinceElements = document.querySelectorAll('#china-map path');
    provinceElements.forEach(provinceElement => {
        const provinceName = provinceElement.id; // 确保每个 path 都有 id 属性表示省份名称

        // 如果是自定义位置的省份，则使用手动设置
        if (customPositions[provinceName]) {
            const pos = customPositions[provinceName];
            xRatio = pos.xRatio;
            yRatio = pos.yRatio;
        }else{
            xRatio = 0.5;
            yRatio = 0.5;
        }

        try {
            const bbox = provinceElement.getBBox();
            const x = bbox.x + bbox.width *  xRatio;
            const y = bbox.y + bbox.height *  yRatio;

            const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
            text.setAttribute("x", x);
            text.setAttribute("y", y);
            text.setAttribute("text-anchor", "middle");
            text.setAttribute("dominant-baseline", "central");
            text.textContent = provinceName;
            text.style.fill = 'black';
            text.style.fontSize = '12px';
            text.style.pointerEvents = 'none';

            provinceElement.closest('svg').appendChild(text);
        } catch (err) {
            console.warn(`无法添加省份名称：${provinceName}`, err);
        }
    });
}