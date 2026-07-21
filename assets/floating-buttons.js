/**
 * 浮动按钮系统 - 统一管理返回顶部、返回首页、反馈建议
 * 
 * 使用方式：
 *   1. 引入 floating-buttons.css 和 floating-buttons.js
 *   2. 在 HTML 中放置以下按钮元素：
 *      <button class="back-to-top" id="backToTopBtn" title="返回顶部" aria-label="返回顶部">↑</button>
 *      <button class="back-to-home" id="backToHomeBtn" title="返回首页" data-home-url="https://example.com" aria-label="返回首页">🏠</button>
 *      <button class="feedback-float" id="feedbackFloat" title="反馈建议" data-source="page_id">📝 反馈建议</button>
 * 
 * 配置属性：
 *   data-home-url     - 首页链接（默认 "/"）
 *   data-show-threshold - 显示阈值 px（默认 300）
 *   data-source       - 反馈来源标识（默认 "unknown"）
 */
(function() {
  'use strict';

  document.addEventListener('DOMContentLoaded', function() {
    var backToTop = document.getElementById('backToTopBtn');
    var backToHome = document.getElementById('backToHomeBtn');
    var feedbackFloat = document.getElementById('feedbackFloat');

    if (!backToTop && !backToHome && !feedbackFloat) return;

    var threshold = parseInt(backToTop ? backToTop.getAttribute('data-show-threshold') : '300') || 300;
    if (backToHome && !threshold) {
      threshold = parseInt(backToHome.getAttribute('data-show-threshold') || '300') || 300;
    }

    // 滚动控制：显示/隐藏按钮
    var ticking = false;
    window.addEventListener('scroll', function() {
      if (!ticking) {
        requestAnimationFrame(function() {
          var resultPanel = document.getElementById('result');
          var isResultOpen = resultPanel && resultPanel.classList.contains('open');
          var feedbackOverlay = document.getElementById('feedbackOverlay');
          var isFeedbackOpen = feedbackOverlay && feedbackOverlay.classList.contains('active');
          var show = !isResultOpen && !isFeedbackOpen && window.scrollY > threshold;
          if (backToTop) backToTop.classList.toggle('show', show);
          if (backToHome) backToHome.classList.toggle('show', show);
          if (feedbackFloat) feedbackFloat.classList.toggle('show', show);
          ticking = false;
        });
        ticking = true;
      }
    }, { passive: true });

    // 返回顶部
    if (backToTop) {
      backToTop.addEventListener('click', function() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      });
    }

    // 返回首页
    if (backToHome) {
      backToHome.addEventListener('click', function() {
        var homeUrl = backToHome.getAttribute('data-home-url') || '/';
        window.location.href = homeUrl;
      });
    }
  });
})();