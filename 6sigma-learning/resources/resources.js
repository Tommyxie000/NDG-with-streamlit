// 资源中心页面交互功能

document.addEventListener('DOMContentLoaded', function() {
    // 页面元素
    const categoryCards = document.querySelectorAll('.category-card');
    const sections = {
        templates: document.getElementById('templates-section'),
        books: document.getElementById('books-section'),
        tools: document.getElementById('tools-section')
    };
    const downloadBtns = document.querySelectorAll('.btn-download');
    const faqItems = document.querySelectorAll('.faq-item');
    const glossarySearch = document.getElementById('glossary-search');
    const glossaryItems = document.querySelectorAll('.glossary-item');
    
    // 初始化页面
    initializePage();
    
    // 类别卡片点击事件
    categoryCards.forEach(card => {
        card.addEventListener('click', function() {
            const category = this.dataset.category;
            showCategory(category);
        });
    });
    
    // 下载按钮事件
    downloadBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const template = this.dataset.template;
            downloadTemplate(template);
        });
    });
    
    // FAQ展开/折叠事件
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        question.addEventListener('click', function() {
            toggleFaqItem(item);
        });
    });
    
    // 术语搜索事件
    if (glossarySearch) {
        glossarySearch.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            searchGlossary(searchTerm);
        });
    }
    
    // 页面初始化
    function initializePage() {
        // 默认显示模板部分
        showCategory('templates');
        
        // 添加一些演示数据
        addDemoDownloads();
    }
    
    // 显示类别内容
    function showCategory(category) {
        // 移除所有活动状态
        categoryCards.forEach(card => {
            card.classList.remove('active');
        });
        
        // 隐藏所有部分
        Object.values(sections).forEach(section => {
            if (section) section.style.display = 'none';
        });
        
        // 显示选中的类别
        const targetCard = document.querySelector(`[data-category="${category}"]`);
        if (targetCard) {
            targetCard.classList.add('active');
        }
        
        if (sections[category]) {
            sections[category].style.display = 'block';
        }
    }
    
    // 下载模板功能
    function downloadTemplate(template) {
        // 模拟下载过程
        const templateData = getTemplateData(template);
        if (!templateData) {
            showNotification('模板不存在！', 'error');
            return;
        }
        
        // 显示下载进度
        showDownloadProgress(templateData);
        
        // 记录下载统计
        trackDownload(template);
    }
    
    // 获取模板数据
    function getTemplateData(template) {
        const templates = {
            'charter': {
                name: '项目章程模板',
                content: `6 Sigma项目章程

项目名称: ________________
项目负责人: ______________
开始日期: ______________
目标描述: ______________
成功标准: ______________
约束条件: ______________

项目范围:
- 包括: _______________
- 不包括: _____________

风险评估:
- 高风险: _____________
- 中风险: _____________
- 低风险: _____________

资源需求:
- 人员: _______________
- 设备: _______________
- 预算: _______________

项目计划:
- 阶段1: _____________
- 阶段2: _____________
- 阶段3: _____________
- 阶段4: _____________
- 阶段5: _____________`
            },
            'msa': {
                name: 'MSA数据收集表',
                content: `测量系统分析数据收集表

操作员: ________________
测量日期: ______________
零件编号: ______________
测量项目: ______________

量具信息:
- 量具名称: _____________
- 量具编号: _____________
- 精度等级: _____________

数据收集:
零件 | 操作员A | 操作员B | 操作员C
1    |        |        |
2    |        |        |
3    |        |        |
4    |        |        |
5    |        |        |
6    |        |        |
7    |        |        |
8    |        |        |
9    |        |        |
10   |        |        |

备注: ___________________`
            },
            'capability': {
                name: '过程能力分析表',
                content: `过程能力分析表

过程名称: _______________
测量日期: _______________
样本数量: _______________

基本统计:
- 平均值: ______________
- 标准差: ______________
- 最小值: ______________
- 最大值: ______________

规格要求:
- 上规格限: ____________
- 下规格限: ____________
- 目标值: ______________

能力指数:
- Cp: __________________
- Cpk: _________________
- Pp: __________________
- Ppk: _________________

结论: ___________________
改进建议: _______________`
            },
            'fmea': {
                name: 'FMEA分析表',
                content: `失效模式与影响分析表

过程步骤: _______________
分析日期: _______________

失效模式分析:
1. 失效模式: ___________
   严重度(1-10): _______
   发生度(1-10): _______
   探测度(1-10): _______
   RPN: ________________

2. 失效模式: ___________
   严重度(1-10): _______
   发生度(1-10): _______
   探测度(1-10): _______
   RPN: ________________

3. 失效模式: ___________
   严重度(1-10): _______
   发生度(1-10): _______
   探测度(1-10): _______
   RPN: ________________

推荐措施: _______________
负责人: _________________
完成日期: _______________`
            },
            'doe': {
                name: 'DOE实验设计表',
                content: `实验设计表

实验目的: _______________
因子数量: _______________
水平数: _________________

实验计划:
因子A: 水平1(____) 水平2(____)
因子B: 水平1(____) 水平2(____)
因子C: 水平1(____) 水平2(____)

实验序号 | 因子A | 因子B | 因子C | 响应值
1       |      |      |      |
2       |      |      |      |
3       |      |      |      |
4       |      |      |      |
5       |      |      |      |
6       |      |      |      |
7       |      |      |      |
8       |      |      |      |

实验条件:
环境温度: _______________
环境湿度: _______________
操作员: _________________
测试日期: _______________`
            },
            'control-plan': {
                name: '控制计划表',
                content: `过程控制计划表

过程名称: _______________
编制日期: _______________

控制方法:
1. 检验项目: ___________
   控制标准: ____________
   检验方法: ____________
   检验频次: ____________
   负责人: ______________

2. 检验项目: ___________
   控制标准: ____________
   检验方法: ____________
   检验频次: ____________
   负责人: ______________

3. 检验项目: ___________
   控制标准: ____________
   检验方法: ____________
   检验频次: ____________
   负责人: ______________

异常处理:
- 轻微异常: ____________
- 严重异常: ____________
- 紧急情况: ____________

审批:
编制: _________________
审核: _________________
批准: _________________`
            },
            'sipoc': {
                name: 'SIPOC分析表',
                content: `SIPOC分析表

项目名称: _______________
分析日期: _______________

供应商(Suppliers):
1. _____________________
2. _____________________
3. _____________________
4. _____________________
5. _____________________

输入(Inputs):
1. _____________________
2. _____________________
3. _____________________
4. _____________________
5. _____________________

过程(Process):
1. _____________________
   关键输出: ___________
   
2. _____________________
   关键输出: ___________
   
3. _____________________
   关键输出: ___________
   
4. _____________________
   关键输出: ___________
   
5. _____________________
   关键输出: ___________

输出(Outputs):
1. _____________________
2. _____________________
3. _____________________
4. _____________________
5. _____________________

客户(Customers):
1. _____________________
2. _____________________
3. _____________________
4. _____________________
5. _____________________`
            },
            'spc': {
                name: 'SPC控制图模板',
                content: `SPC控制图数据表

过程名称: _______________
测量项目: _______________
样本大小: _______________
采样频次: _______________

数据记录:
子组 | 测量值1 | 测量值2 | 测量值3 | 平均值 | 极差
1    |         |         |         |        |
2    |         |         |         |        |
3    |         |         |         |        |
4    |         |         |         |        |
5    |         |         |         |        |
6    |         |         |         |        |
7    |         |         |         |        |
8    |         |         |         |        |
9    |         |         |         |        |
10   |         |         |         |        |
11   |         |         |         |        |
12   |         |         |         |        |
13   |         |         |         |        |
14   |         |         |         |        |
15   |         |         |         |        |
16   |         |         |         |        |
17   |         |         |         |        |
18   |         |         |         |        |
19   |         |         |         |        |
20   |         |         |         |        |

控制限计算:
- 平均值上限(UCL): ______
- 平均值下限(LCL): ______
- 极差上限(UCLR): ______
- 极差下限(LCLR): ______

分析结论: _______________
改进措施: _______________`
            }
        };
        
        return templates[template] || null;
    }
    
    // 显示下载进度
    function showDownloadProgress(templateData) {
        const progressBar = document.createElement('div');
        progressBar.className = 'download-progress';
        progressBar.innerHTML = `
            <div class="progress-content">
                <h4>正在准备 ${templateData.name}</h4>
                <div class="progress-bar">
                    <div class="progress-fill"></div>
                </div>
                <p class="progress-text">准备下载中...</p>
            </div>
        `;
        
        // 添加进度条样式
        const style = document.createElement('style');
        style.textContent = `
            .download-progress {
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
            .progress-content {
                background: white;
                border-radius: 10px;
                padding: 30px;
                text-align: center;
                max-width: 400px;
                width: 90%;
            }
            .progress-bar {
                background: #f0f0f0;
                border-radius: 10px;
                height: 20px;
                margin: 20px 0;
                overflow: hidden;
            }
            .progress-fill {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                height: 100%;
                width: 0%;
                transition: width 0.3s ease;
            }
            .progress-text {
                color: #666;
                margin: 0;
            }
        `;
        
        document.head.appendChild(style);
        document.body.appendChild(progressBar);
        
        // 模拟下载进度
        const progressFill = progressBar.querySelector('.progress-fill');
        const progressText = progressBar.querySelector('.progress-text');
        let progress = 0;
        
        const interval = setInterval(() => {
            progress += Math.random() * 30;
            if (progress > 100) progress = 100;
            
            progressFill.style.width = `${progress}%`;
            progressText.textContent = `下载中... ${Math.round(progress)}%`;
            
            if (progress >= 100) {
                clearInterval(interval);
                setTimeout(() => {
                    if (document.body.contains(progressBar)) {
                        document.body.removeChild(progressBar);
                    }
                    if (document.head.contains(style)) {
                        document.head.removeChild(style);
                    }
                    
                    // 实际下载文件
                    downloadFile(templateData);
                    showNotification(`${templateData.name} 下载完成！`, 'success');
                }, 500);
            }
        }, 200);
    }
    
    // 实际下载文件
    function downloadFile(templateData) {
        const blob = new Blob([templateData.content], { type: 'text/plain;charset=utf-8' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${templateData.name}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    }
    
    // 跟踪下载统计
    function trackDownload(template) {
        const downloads = JSON.parse(localStorage.getItem('template_downloads') || '{}');
        downloads[template] = (downloads[template] || 0) + 1;
        localStorage.setItem('template_downloads', JSON.stringify(downloads));
        
        // 更新显示统计
        updateDownloadStats();
    }
    
    // 更新下载统计
    function updateDownloadStats() {
        const downloads = JSON.parse(localStorage.getItem('template_downloads') || '{}');
        const total = Object.values(downloads).reduce((sum, count) => sum + count, 0);
        
        // 可以在这里更新页面上的下载统计显示
        console.log(`总下载次数: ${total}`);
    }
    
    // 添加演示下载数据
    function addDemoDownloads() {
        if (!localStorage.getItem('template_downloads')) {
            const demoDownloads = {
                'charter': 15,
                'msa': 8,
                'capability': 12,
                'fmea': 6
            };
            localStorage.setItem('template_downloads', JSON.stringify(demoDownloads));
        }
    }
    
    // 切换FAQ项目
    function toggleFaqItem(item) {
        const isActive = item.classList.contains('active');
        
        // 关闭所有FAQ项目
        faqItems.forEach(faqItem => {
            faqItem.classList.remove('active');
        });
        
        // 如果当前项目不是活动状态，则打开它
        if (!isActive) {
            item.classList.add('active');
        }
    }
    
    // 搜索术语表
    function searchGlossary(searchTerm) {
        glossaryItems.forEach(item => {
            const term = item.querySelector('h4').textContent.toLowerCase();
            const definition = item.querySelector('p').textContent.toLowerCase();
            
            if (term.includes(searchTerm) || definition.includes(searchTerm)) {
                item.classList.remove('hidden');
            } else {
                item.classList.add('hidden');
            }
        });
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
    
    // 页面加载完成后的初始化
    updateDownloadStats();
});