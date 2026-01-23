// 培训案例页面JavaScript

// 案例过滤功能
document.addEventListener('DOMContentLoaded', function() {
    const filterTags = document.querySelectorAll('.filter-tag');
    const caseCards = document.querySelectorAll('.case-card');

    // 过滤标签点击事件
    filterTags.forEach(tag => {
        tag.addEventListener('click', function() {
            // 移除所有标签的active类
            filterTags.forEach(t => t.classList.remove('active'));
            // 为当前标签添加active类
            this.classList.add('active');
            
            const industry = this.dataset.industry;
            filterCases(industry);
        });
    });

    // 过滤案例
    function filterCases(industry) {
        caseCards.forEach(card => {
            const cardIndustry = card.dataset.industry;
            
            if (industry === 'all' || cardIndustry === industry) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    }

    // 初始化页面
    filterCases('all');
});
