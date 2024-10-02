// 初始化计数器为0
let count = 0;

// 获取页面中ID为'counter'的元素，用于显示计数值
const counterElement = document.getElementById('counter');

// 获取页面中ID为'increase'的按钮元素，用于增加计数
const increaseButton = document.getElementById('increase');

// 获取页面中ID为'decrease'的按钮元素，用于减少计数
const decreaseButton = document.getElementById('decrease');

// 获取页面中ID为'reset'的按钮元素，用于重置计数
const resetButton = document.getElementById('reset');

// 定义一个函数，用于更新显示计数值
function updateCounter() {
    // 将当前计数值显示在counterElement中
    counterElement.textContent = count;
}

// 为增加按钮添加点击事件监听器
increaseButton.addEventListener('click', function() {
    // 增加计数值
    count++;
    // 更新显示
    updateCounter();
});

// 为减少按钮添加点击事件监听器
decreaseButton.addEventListener('click', function() {
    // 减少计数值
    count--;
    // 更新显示
    updateCounter();
});

// 为重置按钮添加点击事件监听器
resetButton.addEventListener('click', function() {
    // 重置计数值为0
    count = 0;
    // 更新显示
    updateCounter();
});

// 初始化时更新显示
updateCounter();
