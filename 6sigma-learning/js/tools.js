// 工具库页面JavaScript

// 搜索和过滤功能
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const filterTags = document.querySelectorAll('.filter-tag');
    const toolItems = document.querySelectorAll('.tool-item');
    const phaseSections = document.querySelectorAll('.phase-section');

    // 搜索功能
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        filterTools(searchTerm, getActivePhase());
    });

    // 过滤标签点击事件
    filterTags.forEach(tag => {
        tag.addEventListener('click', function() {
            // 移除所有标签的active类
            filterTags.forEach(t => t.classList.remove('active'));
            // 为当前标签添加active类
            this.classList.add('active');
            
            const phase = this.dataset.phase;
            filterTools(searchInput.value.toLowerCase(), phase);
        });
    });

    // 获取当前激活的阶段
    function getActivePhase() {
        const activeTag = document.querySelector('.filter-tag.active');
        return activeTag ? activeTag.dataset.phase : 'all';
    }

    // 过滤工具
    function filterTools(searchTerm, phase) {
        phaseSections.forEach(section => {
            let hasVisibleTools = false;
            
            const toolsInSection = section.querySelectorAll('.tool-item');
            toolsInSection.forEach(tool => {
                const toolPhase = tool.dataset.phase;
                const toolText = tool.textContent.toLowerCase();
                
                const matchesPhase = phase === 'all' || toolPhase === phase;
                const matchesSearch = toolText.includes(searchTerm);
                
                if (matchesPhase && matchesSearch) {
                    tool.style.display = 'flex';
                    hasVisibleTools = true;
                } else {
                    tool.style.display = 'none';
                }
            });
            
            // 显示/隐藏阶段标题
            if (phase === 'all') {
                section.style.display = hasVisibleTools ? 'block' : 'none';
            } else {
                // 如果选择了特定阶段，只显示该阶段的section
                if (section.querySelector(`[data-phase="${phase}"]`)) {
                    section.style.display = hasVisibleTools ? 'block' : 'none';
                } else {
                    section.style.display = 'none';
                }
            }
        });
    }

    // 初始化页面
    filterTools('', 'all');
});
