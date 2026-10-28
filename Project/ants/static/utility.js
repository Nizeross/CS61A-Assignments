function formatAntButtons(antTypes) {
    // 为每种蚂蚁创建按钮

    let antSection = document.querySelector('.ants-section');
    for (i = 0; i < antTypes.length; i++) {
        let antButton = document.createElement('button');
        antButton.setAttribute('class', `ant-btn`);
        antButton.setAttribute('id', antTypes[i]);
        antButton.style.backgroundImage = `url('../static/assets/ants/${antTypes[i]}.gif')`;
        antSection.appendChild(antButton);
        selectedAntsTable[antTypes[i]] = false; // 向表中添加键值对（键为蚂蚁名称，值表示是否被选中）
    }
    addListenerToAnts(); // 为蚂蚁按钮添加事件监听器
}


function formatGameGrid(rows, cols, wetPlaces) {
    let gameSectionStyle = document.querySelector(".game-section").style;
    let maxWidth = 12; // 隧道最大长度为 12

    if (0 < cols <= maxWidth) {
        // 根据列数确定网格与蜂巢各自占据的空间
        gameSectionStyle.gridTemplateColumns = `${cols / maxWidth}fr ${(maxWidth - cols) / maxWidth}fr`;
    } else {
        console.log("===== ERROR: number of columns not supported =====");
    }

    addRowsToGrid(rows); // 向网格添加行
    for (i = 0; i < rows; i++) {
        createButtonsForRow(cols, i, wetPlaces); // 向行中添加按钮
    }
    formatHive();
    addListenerToTile(); // 为地块添加事件监听器
}


function addRowsToGrid(rows) {
    /* 向游戏网格添加行 */

    let s = '';
    let tunnelGrid = document.querySelector(".tunnel-grid");

    for (i = 0; i < rows; i++){
        if (i === rows - 1) {
            s += `1fr`;
        } else {
            s += `1fr `;
        }
        let row = document.createElement('div');
        row.setAttribute('class', `tunnel-row-${i}`);
        row.style.display = 'flex'; // 使每一行使用 Flex 布局
        row.style.justifyContent = 'space-between';
        tunnelGrid.appendChild(row);
    }

    tunnelGrid.style.gridTemplateRows = s; // 将 tunnelGrid 设置为 CSS 网格，并设置正确数量的 fr 轨道
}


function createButtonsForRow(buttonCount, row, wetPlaces) {
    // 为给定行添加按钮（地块）

    for (let i = 0; i < buttonCount; i ++) {
        let button = document.createElement('button');
        button.setAttribute('class', `tile-btn`);
        button.setAttribute('id', `${row}-${i}`);
        let image = document.createElement('img');
        image.setAttribute('src', `../static/assets/tiles/${i % 3}.png`);

        for (let j = 0; j < wetPlaces.length; j++) { // 检查每个水域地点是否为当前地点
            if (wetPlaces[j][0] === row && wetPlaces[j][1] === i) {
                image.setAttribute('src', `../static/assets/tiles/wet.png`); // 将 src 设置为水域地块图像
                break;
            }
        }

        image.setAttribute('class', `tile-img`);
        button.appendChild(image);
        document.querySelector(`.tunnel-row-${row}`).appendChild(button);
    }
}


function formatHive() {
    // 设置蜂巢并添加图像
    hive = document.querySelector(".beehive");
    hive.style.position = 'relative';
    hive.style.overflow = 'hideen';
    image = document.createElement('img');
    image.setAttribute('src', `../static/assets/fog.jpg`);
    image.style.width = '100%';
    image.style.height = '100%';
    image.style.objectFit = 'cover';
    image.style.opacity = '85%';
    hive.appendChild(image);
}


function makeAntSelector(antName) {
    /* 返回按下按钮时调用的 antSelector 函数 */

    function antSelector() {
        for (let ant in selectedAntsTable) {
            /* 遍历所有蚂蚁类型。若某类型被选中，则在表中记录并更改边框颜色；重置其他所有类型的表项和颜色 */
            let antButton = document.getElementById(ant);
            if (ant === antName) {
                selectedAntsTable[ant] = true;
                antButton.style.borderWidth = '5px';
                antButton.style.borderColor = 'rgba(50, 20, 200, 0.8)';

            } else {
                selectedAntsTable[ant] = false;
                antButton.style.borderWidth = '2px';
                antButton.style.borderColor = 'rgba(54, 57, 235, 0.2)';
            }
        }
    }

    return antSelector;
}


function addListenerToAnts() {
    /* 为每个蚂蚁按钮添加事件监听器 */

    let buttons = document.getElementsByClassName('ant-btn');
    for (i = 0; i < buttons.length; i++) {
        buttons[i].addEventListener('click', makeAntSelector(buttons[i].id));
    }
}


function getSelectedAnt() {
    // 从表中返回选中的蚂蚁；若未选中任何蚂蚁，则返回 undefined
    for (let ant in selectedAntsTable){
        if (selectedAntsTable[ant]){
            return ant;
        }
    }
}


function makeOnClickTile(buttonID) {
    /* 返回点击地块按钮时调用的函数 */

    function onClickTile() {

        // 检查是否选中了蚂蚁
        selectedAnt = getSelectedAnt();
        if (selectedAnt == undefined){
            return;
        }

        // 准备发送给服务器的数据（哪个按钮以及哪种蚂蚁）
        const data = {
            pos: buttonID,
            ant: selectedAnt
        };

        fetch('/deploy_ants', { // 通过 deploy_ants 向 Flask 服务器发送 AJAX 请求
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => { // 处理服务器传来的数据
            deployed = data.deployed;
            if (deployed){ // 部署成功
                placeAnt(selectedAnt, buttonID, data.insect_id);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });

    }

    return onClickTile;
}


function addListenerToTile() {
    // 为每个地块按钮添加事件监听器
    let buttons = document.getElementsByClassName('tile-btn');
    for (i = 0; i < buttons.length; i++) {
        buttons[i].addEventListener('click', makeOnClickTile(buttons[i].id));
    }
}


function placeAnt(antName, place, ant_id) {
    // 在图形界面中放置蚂蚁
    let image = document.createElement('img');
    let button = document.getElementById(place);

    image.setAttribute('class', 'insect-on-tile-img');
    image.setAttribute('src', `../static/assets/ants/${antName}.gif`);
    image.setAttribute('id', ant_id);
    button.appendChild(image);

    // 将蚂蚁置于按钮中央
    image.style.top = `50%`;
    image.style.left = `50%`;
    image.style.transform = 'translate(-50%, -50%)';
}


function adjustAntButtons(availableAnts) {
    // 提高可用蚂蚁（食物足够部署）的亮度，降低不可用蚂蚁的亮度
    let antButtons = document.getElementsByClassName('ant-btn');
    for (i = 0; i < antButtons.length; i++) {
        let button = antButtons[i];
        if (availableAnts.includes(button.id)) {
            button.style.filter = 'brightness(100%)';
        } else {
            button.style.filter = 'brightness(35%)';
        }
    }
}


function showEndGameAlert(result) {
    // 显示提示消息。游戏结束时调用。
    let body = document.body;
    let alert = document.createElement('alert');
    alert.style.opacity = '0'; // 将初始不透明度设置为 0
    body.appendChild(alert);
    alert.setAttribute('class', 'alert');
    let text = document.createElement('p');
    alert.appendChild(text);

    if (result) { // 蚂蚁获胜
        text.innerText = 'You Won!';
        alert.style.backgroundColor = 'rgba(30, 200, 50, 1)';
    } else {
        text.innerText = 'You Lost!';
        alert.style.backgroundColor = 'rgba(190, 40, 50, 1)';
    }

    alert.style.transition = 'opacity 2s ease-in-out';
    setTimeout(() => { // 动画需要延迟调用
        alert.style.opacity = '0.9'; // 在 2 秒内将提示框的不透明度变为 90%
    }, 50);
}


function playMusic() {
    // 播放音乐
    let audio = document.getElementById('backgroundmusic');
    audio.play();
}


