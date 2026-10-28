const socket = io.connect(); // 连接到 WebSocket
var selectedAntsTable = {}; // 以各蚂蚁类型的名称为键，以表示该类型是否被选中的布尔值为值
const moveBeeAnimationDuration = 1.2; // 秒
const throwLeafAnimationDuration = 0.75; // 秒
const insectDieAnimationDuration = 0.6; // 秒
const insectsHurtAnimationDuration = 0.2; // 秒
const insectsActionInterval = 4; // 昆虫按 insectsActionInterval 指定的秒数间隔行动


function inLobby(data) {
    /* 玩家连接服务器后由后端触发。玩家处于大厅，等待开始游戏。 */

    let main = document.querySelector(".main-window");
    main.style.opacity = '0'; // 隐藏主窗口，以显示大厅背景图
    let startButton = document.querySelector('.start-button');
    startButton.addEventListener('click', startGame); // 为开始按钮添加事件监听器
}


function startGame() {
    /* 玩家点击开始按钮时触发。从服务器获取初始数据，并设置游戏网格。 */

    console.log("===== Game Started! =====");

    fetch('/initialize_game', { // 向后端发送 initialize_game 信号
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({}), // 发送空数据
    })
    .then(response => response.json())
    .then(data => { // 处理服务器传来的数据

        let main = document.querySelector(".main-window");
        main.style.opacity = '1'; // 显示主窗口

        let body = document.getElementsByTagName("BODY")[0];
        body.style.backgroundImage = 'none'; // 移除大厅背景图
        let startButton = document.querySelector('.start-button');
        startButton.remove(); // 移除开始按钮

        formatAntButtons(data.ant_types); // 根据可用的蚂蚁类型设置蚂蚁按钮
        formatGameGrid(data.dimensions_x, data.dimensions_y, data.wet_places); // 设置游戏网格
        playMusic();

        // 设置两个函数的调用间隔，分别为 4 秒和 50 毫秒。
        setInterval(insectsTakeActions, insectsActionInterval * 1000);
        setInterval(updateStats, 50);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}


function moveBee(data) {
    /* 由后端触发。移动一只蜜蜂 */

    let animationDelay = 50;

    setTimeout(() => { // 必须使用延迟调用才能启用动画
        let destination = document.getElementById(`${data.destination[0]}-${data.destination[1]}`);
        let currentTile = document.getElementById(`${data.current_pos[0]}-${data.current_pos[1]}`);
        let distance = destination.getBoundingClientRect().right - currentTile.getBoundingClientRect().right; // 计算距离
        let beeImg = document.getElementById(`${data.bee_id}`);

        beeImg.style.transition = `transform ${moveBeeAnimationDuration}s ease-in-out`; // 在 moveBeeAnimationDuration 指定的时长内平移蜜蜂
        beeImg.style.transform = `translateX(${distance}px)`;
        beeImg.style.top = `${(destination.offsetHeight - beeImg.offsetHeight) / 2}px`; // 使精灵图位于隧道中间

        // 从当前地块移除，并添加到目标地点
        setTimeout(() => {
            beeImg.remove();
            destination.appendChild(beeImg);
            beeImg.style.transform = `translateX(0px)`;
            beeImg.style.top = `${(destination.offsetHeight - beeImg.offsetHeight) / 2}px`;
        }, moveBeeAnimationDuration * 1000 + animationDelay);

    }, animationDelay * 2);
}


function moveBeeFromHive(data) {
    // 由后端触发。将蜜蜂移出蜂巢。

    let animationDelay = 75; // 毫秒

    setTimeout(() => {
        let beeImg = document.createElement('img');
        let destination = document.getElementById(`${data.destination[0]}-${data.destination[1]}`);
        destination.appendChild(beeImg);
        beeImg.setAttribute('class', 'insect-on-tile-img');
        beeImg.setAttribute('id', data.bee_id);
        beeImg.setAttribute('src', `../static/assets/bees/${data.bee_name}.gif`)
        beeImg.style.zIndex = '5'; // 将蜜蜂图像置于地块图像上方

        let offset = destination.getBoundingClientRect().right - beeImg.getBoundingClientRect().right;
        beeImg.style.transition = `transform ${moveBeeAnimationDuration}s ease-in-out`;
        beeImg.style.top = `${(destination.offsetHeight - beeImg.offsetHeight) / 2}px`;

        setTimeout(() => {
            beeImg.style.transform = `translateX(${offset}px)`;
            beeImg.style.top = `${(destination.offsetHeight - beeImg.offsetHeight) / 2}px`;
        }, animationDelay);


        setTimeout(() => { // 添加到新的父元素，并重置平移
            beeImg.style.transition = '';
            beeImg.style.transform = `translateX(0px)`;
            beeImg.style.left = `0px`;
        }, moveBeeAnimationDuration * 1000 + animationDelay * 2);

    }, animationDelay * 2);
}


function removeInsect(data) {
    // 由后端触发。从图形界面移除昆虫。但与昆虫受伤变红的效果配合时，这里仍有一些问题

    setTimeout(() => {
        let insect = document.getElementById(data.insect_id);
        let animationDelay = 50; // 毫秒
        insect.style.transition = `opacity ${insectDieAnimationDuration}s ease-out`;
        insect.style.opacity = '0';
        setTimeout(() => {
            insect.remove(); // 移除 HTML 元素
        }, insectDieAnimationDuration * 1000 + animationDelay)
    }, throwLeafAnimationDuration * 1000 + insectsHurtAnimationDuration * 1000)
}


function endGame(data) {
    // 由后端触发。结束游戏。

    showEndGameAlert(data.antsWon)
    let mainWindow = document.querySelector('.main-window');
    mainWindow.style.transition = 'filter 2s ease-in-out';
    mainWindow.style.filter = 'brightness(35%)'; // 降低游戏画面的亮度
}


function insectsTakeActions() {
    /* 定时调用。让昆虫执行行动 */

    const timeDelay = 100; // 毫秒

    fetch('/ants_take_actions') // 向后端请求蚂蚁行动
    .then(response => response.json())
    .then(data => { // 处理后端数据
    })
    .catch(error => {
        console.error('Error:', error);
    });

    setTimeout(() => { // 在蚂蚁和蜜蜂行动之间留出时间播放动画（树叶击中蜜蜂以及蜜蜂变红）
        fetch('/bees_take_actions') // 向后端请求蜜蜂行动
        .then(response => response.json())
        .then(data => {
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }, throwLeafAnimationDuration * 1000 + insectsHurtAnimationDuration * 1000 + timeDelay);
}


function updateStats() {
    /* 定时调用。向服务器查询食物量和回合数 */

    fetch('/update_stats') // 触发服务器中的 update_stats 信号
    .then(response => response.json())
    .then(data => { // 处理服务器数据

        setTimeout(() => { // 使用延迟调用以避免崩溃
            let food = data.food;
            let turn = data.turn;
            food_display = document.querySelector('.display-food-div');
            food_display.innerText = `Food: ${food}`;
            food_display = document.querySelector('.display-turn-div');
            food_display.innerText = `Turn: ${turn}`;
            adjustAntButtons(data.available_ants); // 在图形界面中更新可用蚂蚁的信息
        }, 50);
    })

    .catch(error => {
        console.error('Error:', error);
    });
}


function reduceHealth(data) {
    /* 由后端触发。播放昆虫受伤后变红的动画 */

    const animationDelay = 100; // 毫秒

    setTimeout(() => {
        let insectImg = document.getElementById(data.insect_id);
        setTimeout(() => {
            insectImg.style.transition = '';
            insectImg.style.filter = "invert(67%) sepia(89%) saturate(7492%) hue-rotate(346deg) brightness(84%) contrast(146%)";
        }, animationDelay)
        setTimeout(() => {
            insectImg.style.transition = '';
            insectImg.style.filter = 'none';
        }, animationDelay + 1000 * insectsHurtAnimationDuration)
    }, throwLeafAnimationDuration * 1000)
}


function throwAt(data) {
    // 由后端触发。播放蚂蚁向蜜蜂投掷树叶的动画

    let target = document.getElementById(`${data.target_pos[0]}-${data.target_pos[1]}`);
    let thrower = document.getElementById(`${data.thrower_pos[0]}-${data.thrower_pos[1]}`);
    let distance = target.getBoundingClientRect().left - thrower.getBoundingClientRect().right;
    let offset = thrower.getBoundingClientRect().left - thrower.getBoundingClientRect().right;
    let leafImg = document.createElement('img');
    let animationDelay = 25 // 毫秒

    thrower.appendChild(leafImg);
    leafImg.setAttribute('src', '../static/assets/testLeaf.png');
    leafImg.setAttribute('class', 'leaf-on-tile-img');

    leafImg.style.transform = `translateX(${offset}px)`;
    leafImg.style.transition = `transform ${throwLeafAnimationDuration}s ease-in`;
    leafImg.style.top = `${(target.offsetHeight - leafImg.offsetHeight) / 2}px`;
    setTimeout(() => {
        leafImg.style.transform = `translateX(${distance}px)`;
        leafImg.style.top = `${(target.offsetHeight - leafImg.offsetHeight) / 2}px`;
    }, animationDelay);

    setTimeout(() => {
        leafImg.remove();
    }, animationDelay * 2 + throwLeafAnimationDuration * 1000);

}


// 处理来自服务器的信号。这些函数由后端触发。
socket.on('loadLobby', inLobby);
socket.on('moveBee', moveBee);
socket.on('moveBeeFromHive', moveBeeFromHive);
socket.on('onInsectDeath', removeInsect);
socket.on('endGame', endGame);
socket.on('throwAt', throwAt);
socket.on('reduceHealth', reduceHealth);

