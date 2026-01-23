// 学习路径页面交互功能

document.addEventListener('DOMContentLoaded', function() {
    // 页面元素
    const levelCards = document.querySelectorAll('.level-card');
    const learningPaths = document.querySelectorAll('.learning-path');
    const currentLevelSelect = document.getElementById('current-level');
    const completedModulesInput = document.getElementById('completed-modules');
    const updateProgressBtn = document.getElementById('update-progress');
    
    // 初始化页面
    initializePage();
    
    // 级别卡片点击事件
    levelCards.forEach(card => {
        card.addEventListener('click', function() {
            const level = this.dataset.level;
            showLearningPath(level);
            updateProgressDisplay(level);
        });
    });
    
    // 开始学习按钮事件
    const startModuleBtns = document.querySelectorAll('.start-module');
    startModuleBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const moduleNum = this.dataset.module;
            startModule(moduleNum);
        });
    });
    
    // 更新进度按钮事件
    updateProgressBtn.addEventListener('click', updateProgress);
    
    // 页面初始化
    function initializePage() {
        // 检查本地存储中的学习进度
        const savedProgress = localStorage.getItem('sixsigma_learning_progress');
        if (savedProgress) {
            const progress = JSON.parse(savedProgress);
            if (progress.currentLevel) {
                currentLevelSelect.value = progress.currentLevel;
            }
            if (progress.completedModules) {
                completedModulesInput.value = progress.completedModules;
            }
            updateProgressDisplay(progress.currentLevel);
        }
        
        // 默认显示黄带路径
        showLearningPath('yellow');
    }
    
    // 显示学习路径
    function showLearningPath(level) {
        // 隐藏所有路径
        learningPaths.forEach(path => {
            path.style.display = 'none';
        });
        
        // 显示选中的路径
        const targetPath = document.getElementById(`${level}-belt-path`);
        if (targetPath) {
            targetPath.style.display = 'block';
        }
        
        // 更新级别选择
        currentLevelSelect.value = level;
    }
    
    // 更新进度显示
    function updateProgressDisplay(level) {
        if (!level) return;
        
        // 获取当前级别的进度
        const progress = getLearningProgress();
        const completedModules = progress.completedModules || 0;
        
        // 计算进度百分比
        const totalModules = getTotalModulesForLevel(level);
        const progressPercent = (completedModules / totalModules) * 100;
        
        // 更新进度条
        const levelCard = document.querySelector(`[data-level="${level}"]`);
        if (levelCard) {
            const progressFill = levelCard.querySelector('.progress-fill');
            const progressText = levelCard.querySelector('.progress-text');
            
            if (progressFill && progressText) {
                progressFill.style.width = `${progressPercent}%`;
                progressText.textContent = `${Math.round(progressPercent)}% 完成`;
            }
        }
        
        // 更新时间线项目状态
        updateTimelineItems(level, completedModules);
        
        // 更新成就状态
        updateAchievements(level, progressPercent);
    }
    
    // 获取级别总模块数
    function getTotalModulesForLevel(level) {
        const moduleCounts = {
            'yellow': 4,
            'green': 5,
            'black': 4
        };
        return moduleCounts[level] || 0;
    }
    
    // 更新时间线项目状态
    function updateTimelineItems(level, completedModules) {
        const pathElement = document.getElementById(`${level}-belt-path`);
        if (!pathElement) return;
        
        const timelineItems = pathElement.querySelectorAll('.timeline-item');
        timelineItems.forEach((item, index) => {
            const moduleNum = parseInt(item.dataset.module);
            if (moduleNum <= completedModules) {
                item.classList.add('completed');
                const btn = item.querySelector('.start-module');
                if (btn) {
                    btn.textContent = '已完成';
                    btn.disabled = true;
                    btn.style.background = '#4CAF50';
                }
            } else {
                item.classList.remove('completed');
                const btn = item.querySelector('.start-module');
                if (btn) {
                    btn.textContent = '开始学习';
                    btn.disabled = false;
                    btn.style.background = '';
                }
            }
        });
    }
    
    // 更新成就状态
    function updateAchievements(level, progressPercent) {
        // 重置所有成就
        const achievements = document.querySelectorAll('.achievement');
        achievements.forEach(achievement => {
            achievement.classList.remove('achieved');
        });
        
        // 第一个模块完成
        if (progressPercent > 0) {
            document.getElementById('first-step').classList.add('achieved');
        }
        
        // 50%进度完成
        if (progressPercent >= 50) {
            document.getElementById('half-way').classList.add('achieved');
        }
        
        // 当前级别完成
        if (progressPercent >= 100) {
            document.getElementById('completion').classList.add('achieved');
            
            // 如果是黄带完成，可以推荐绿带
            if (level === 'yellow') {
                setTimeout(() => {
                    if (confirm('恭喜完成黄带学习！是否开始绿带学习？')) {
                        showLearningPath('green');
                        currentLevelSelect.value = 'green';
                    }
                }, 1000);
            }
        }
    }
    
    // 开始模块学习
    function startModule(moduleNum) {
        const currentLevel = currentLevelSelect.value;
        if (!currentLevel) {
            alert('请先选择学习级别！');
            return;
        }
        
        // 这里可以添加跳转到具体学习内容的逻辑
        const moduleInfo = getModuleInfo(currentLevel, moduleNum);
        if (moduleInfo) {
            // 显示模块学习对话框
            showModuleDialog(moduleInfo);
        }
    }
    
    // 获取模块信息
    function getModuleInfo(level, moduleNum) {
        const modules = {
            'yellow': {
                1: { title: '基础概念', topics: ['6 Sigma概述', 'DMAIC流程', '项目选择'] },
                2: { title: '团队协作', topics: ['团队角色', '沟通技巧', '会议管理'] },
                3: { title: '基础工具', topics: ['流程图', '检查表', '帕累托图', '因果图'] },
                4: { title: '项目实践', topics: ['案例分析', '项目报告', '成果展示'] }
            },
            'green': {
                1: { title: '定义阶段', topics: ['SIPOC分析', 'CTQ树', 'VOC收集', '项目章程'] },
                2: { title: '测量阶段', topics: ['MSA分析', '过程能力分析', '数据收集计划', '统计基础'] },
                3: { title: '分析阶段', topics: ['假设检验', '回归分析', 'ANOVA', 'FMEA'] },
                4: { title: '改进阶段', topics: ['DOE实验设计', '精益工具', '解决方案评估', '实施计划'] },
                5: { title: '控制阶段', topics: ['SPC控制图', '控制计划', '标准化', '项目移交'] }
            },
            'black': {
                1: { title: '高级统计方法', topics: ['多元回归', 'Logistic回归', '时间序列分析', '生存分析'] },
                2: { title: '领导力和变革管理', topics: ['变革管理', '教练技术', '项目管理', '财务分析'] },
                3: { title: '培训和指导', topics: ['培训设计', '成人教育', '演讲技巧', '指导方法'] },
                4: { title: '高级项目实践', topics: ['大型项目', '跨职能项目', '持续改进文化', '成果评估'] }
            }
        };
        
        return modules[level] && modules[level][moduleNum] ? modules[level][moduleNum] : null;
    }
    
    // 显示模块学习对话框
    function showModuleDialog(moduleInfo) {
        const dialog = document.createElement('div');
        dialog.className = 'module-dialog';
        dialog.innerHTML = `
            <div class="dialog-content">
                <div class="dialog-header">
                    <h3>${moduleInfo.title}</h3>
                    <button class="close-dialog">&times;</button>
                </div>
                <div class="dialog-body">
                    <h4>学习内容：</h4>
                    <ul>
                        ${moduleInfo.topics.map(topic => `<li>${topic}</li>`).join('')}
                    </ul>
                    <div class="learning-tips">
                        <h4>学习建议：</h4>
                        <p>建议结合实际案例进行学习，并使用相关工具进行实践操作。</p>
                    </div>
                </div>
                <div class="dialog-footer">
                    <button class="btn btn-primary start-learning">开始学习</button>
                    <button class="btn btn-secondary mark-complete">标记为已完成</button>
                </div>
            </div>
        `;
        
        document.body.appendChild(dialog);
        
        // 添加对话框样式
        const style = document.createElement('style');
        style.textContent = `
            .module-dialog {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.5);
                display: flex;
                justify-content: center;
                align-items: center;
                z-index: 1000;
            }
            .dialog-content {
                background: white;
                border-radius: 10px;
                max-width: 500px;
                width: 90%;
                max-height: 80vh;
                overflow-y: auto;
            }
            .dialog-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 20px;
                border-bottom: 1px solid #eee;
            }
            .dialog-body {
                padding: 20px;
            }
            .dialog-footer {
                padding: 20px;
                border-top: 1px solid #eee;
                display: flex;
                gap: 10px;
                justify-content: flex-end;
            }
            .close-dialog {
                background: none;
                border: none;
                font-size: 24px;
                cursor: pointer;
            }
        `;
        document.head.appendChild(style);
        
        // 关闭对话框
        dialog.querySelector('.close-dialog').addEventListener('click', () => {
            document.body.removeChild(dialog);
            document.head.removeChild(style);
        });
        
        // 开始学习按钮
        dialog.querySelector('.start-learning').addEventListener('click', () => {
            alert('开始学习功能将在后续版本中实现！');
            document.body.removeChild(dialog);
            document.head.removeChild(style);
        });
        
        // 标记完成按钮
        dialog.querySelector('.mark-complete').addEventListener('click', () => {
            const currentLevel = currentLevelSelect.value;
            const currentProgress = getLearningProgress();
            const completedModules = parseInt(completedModulesInput.value) || 0;
            const newCompletedModules = Math.max(completedModules, parseInt(dialog.querySelector('.timeline-item').dataset.module));
            
            updateProgressWithModules(currentLevel, newCompletedModules);
            document.body.removeChild(dialog);
            document.head.removeChild(style);
        });
    }
    
    // 更新学习进度
    function updateProgress() {
        const currentLevel = currentLevelSelect.value;
        const completedModules = parseInt(completedModulesInput.value) || 0;
        
        if (!currentLevel) {
            alert('请选择当前学习级别！');
            return;
        }
        
        if (completedModules < 0 || completedModules > getTotalModulesForLevel(currentLevel)) {
            alert(`请输入0到${getTotalModulesForLevel(currentLevel)}之间的数字！`);
            return;
        }
        
        updateProgressWithModules(currentLevel, completedModules);
    }
    
    // 更新进度（具体实现）
    function updateProgressWithModules(level, completedModules) {
        // 保存到本地存储
        const progress = {
            currentLevel: level,
            completedModules: completedModules,
            lastUpdated: new Date().toISOString()
        };
        localStorage.setItem('sixsigma_learning_progress', JSON.stringify(progress));
        
        // 更新界面显示
        updateProgressDisplay(level);
        
        // 显示成功消息
        showNotification('学习进度已更新！', 'success');
    }
    
    // 获取学习进度
    function getLearningProgress() {
        const saved = localStorage.getItem('sixsigma_learning_progress');
        return saved ? JSON.parse(saved) : { currentLevel: '', completedModules: 0 };
    }
    
    // 显示通知
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        
        // 添加通知样式
        const style = document.createElement('style');
        style.textContent = `
            .notification {
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 15px 20px;
                border-radius: 5px;
                color: white;
                font-weight: 500;
                z-index: 1000;
                animation: slideIn 0.3s ease;
            }
            .notification.success {
                background: #4CAF50;
            }
            .notification.error {
                background: #f44336;
            }
            .notification.info {
                background: #2196F3;
            }
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
        `;
        document.head.appendChild(style);
        
        document.body.appendChild(notification);
        
        // 3秒后自动移除
        setTimeout(() => {
            if (document.body.contains(notification)) {
                document.body.removeChild(notification);
            }
            if (document.head.contains(style)) {
                document.head.removeChild(style);
            }
        }, 3000);
    }
    
    // 添加一些演示数据
    function addDemoData() {
        // 可以添加一些演示学习进度
        const demoProgress = {
            currentLevel: 'green',
            completedModules: 2,
            lastUpdated: new Date().toISOString()
        };
        
        // 只在没有保存的进度时才添加演示数据
        if (!localStorage.getItem('sixsigma_learning_progress')) {
            localStorage.setItem('sixsigma_learning_progress', JSON.stringify(demoProgress));
        }
    }
    
    // 页面加载完成后添加演示数据
    setTimeout(addDemoData, 1000);
});