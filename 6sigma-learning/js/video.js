// 视频教程页面JavaScript

// 搜索和过滤功能
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('video-search');
    const filterTags = document.querySelectorAll('.filter-tag');
    const videoCards = document.querySelectorAll('.video-card');
    const categorySections = document.querySelectorAll('.category-section');

    // 搜索功能
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        filterVideos(searchTerm, getActiveCategory());
    });

    // 过滤标签点击事件
    filterTags.forEach(tag => {
        tag.addEventListener('click', function() {
            // 移除所有标签的active类
            filterTags.forEach(t => t.classList.remove('active'));
            // 为当前标签添加active类
            this.classList.add('active');
            
            const category = this.dataset.category;
            filterVideos(searchInput.value.toLowerCase(), category);
        });
    });

    // 获取当前激活的分类
    function getActiveCategory() {
        const activeTag = document.querySelector('.filter-tag.active');
        return activeTag ? activeTag.dataset.category : 'all';
    }

    // 过滤视频
    function filterVideos(searchTerm, category) {
        categorySections.forEach(section => {
            let hasVisibleVideos = false;
            
            const videosInSection = section.querySelectorAll('.video-card');
            videosInSection.forEach(video => {
                const videoCategory = video.dataset.category;
                const videoText = video.textContent.toLowerCase();
                
                const matchesCategory = category === 'all' || videoCategory === category;
                const matchesSearch = videoText.includes(searchTerm);
                
                if (matchesCategory && matchesSearch) {
                    video.style.display = 'block';
                    hasVisibleVideos = true;
                } else {
                    video.style.display = 'none';
                }
            });
            
            // 显示/隐藏分类标题
            if (category === 'all') {
                section.style.display = hasVisibleVideos ? 'block' : 'none';
            } else {
                // 如果选择了特定分类，只显示该分类的section
                if (section.querySelector(`[data-category="${category}"]`)) {
                    section.style.display = hasVisibleVideos ? 'block' : 'none';
                } else {
                    section.style.display = 'none';
                }
            }
        });
    }

    // 初始化页面
    filterVideos('', 'all');
});
