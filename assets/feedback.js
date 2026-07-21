document.addEventListener('DOMContentLoaded', function() {
    const feedbackFloat = document.getElementById('feedbackFloat');
    const feedbackOverlay = document.getElementById('feedbackOverlay');
    const feedbackClose = document.getElementById('feedbackClose');
    const feedbackForm = document.getElementById('feedbackForm');
    const feedbackSuccess = document.getElementById('feedbackSuccess');
    const fbSubmit = document.getElementById('fbSubmit');
    const fileUploadArea = document.getElementById('fileUploadArea');
    const fbFile = document.getElementById('fbFile');
    const filePreviewContainer = document.getElementById('filePreviewContainer');
    const fbContent = document.getElementById('fbContent');
    const fbCount = document.getElementById('fbCount');
    const fbError = document.getElementById('fbError');
    
    const uploadedFiles = [];
    let isContentValid = false;
    
    const feedbackSource = feedbackFloat ? feedbackFloat.dataset.source || 'unknown' : 'unknown';

    function validateContent() {
        if (!fbContent || !fbCount || !fbError) return;
        
        const content = fbContent.value.trim();
        const chineseCount = (content.match(/[\u4e00-\u9fa5]/g) || []).length;
        const totalCount = content.length;
        const hasChinese = chineseCount > 0;
        
        const isValid = hasChinese ? chineseCount >= 5 : totalCount >= 10;
        
        fbCount.textContent = hasChinese 
            ? totalCount + ' / 2000 字（至少5个汉字）'
            : totalCount + ' / 2000 chars (at least 10 characters)';
        
        if (isValid) {
            fbContent.classList.remove('error');
            fbError.classList.remove('show');
            fbCount.classList.remove('error');
            fbCount.classList.add('success');
            isContentValid = true;
        } else {
            fbContent.classList.add('error');
            fbError.classList.add('show');
            fbCount.classList.remove('success');
            fbCount.classList.add('error');
            isContentValid = false;
        }
    }

    window.openFeedback = function() {
        if (!feedbackOverlay) return;
        feedbackOverlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    };

    function closeFeedback() {
        if (!feedbackOverlay || !feedbackForm || !feedbackSuccess) return;
        
        feedbackOverlay.classList.remove('active');
        document.body.style.overflow = '';
        feedbackForm.style.display = '';
        feedbackSuccess.classList.remove('show');
        
        if (fbContent) {
            fbContent.value = '';
            fbContent.classList.remove('error');
        }
        if (document.getElementById('fbContact')) {
            document.getElementById('fbContact').value = '';
        }
        if (document.getElementById('fbType')) {
            document.getElementById('fbType').value = 'suggestion';
        }
        if (fbError) {
            fbError.classList.remove('show');
        }
        if (fbCount) {
            fbCount.classList.remove('error', 'success');
            fbCount.textContent = '0 / 2000 字（至少5个汉字）';
        }
        
        isContentValid = false;
        uploadedFiles.length = 0;
        if (filePreviewContainer) {
            filePreviewContainer.innerHTML = '';
        }
    }

    function handleFiles(files) {
        for (let i = 0; i < files.length; i++) {
            const file = files[i];
            if (uploadedFiles.length >= 3) {
                alert('最多只能上传3张图片');
                break;
            }
            if (!file.type.startsWith('image/')) {
                alert('请上传图片文件');
                continue;
            }
            if (file.size > 5 * 1024 * 1024) {
                alert('单张图片不能超过5MB');
                continue;
            }
            uploadedFiles.push(file);
            showFilePreview(file, uploadedFiles.length - 1);
        }
    }

    function showFilePreview(file, index) {
        if (!filePreviewContainer) return;
        
        const reader = new FileReader();
        reader.onload = function(e) {
            const previewItem = document.createElement('div');
            previewItem.className = 'file-preview-item';
            previewItem.innerHTML = '<img src="' + e.target.result + '" alt="图片预览"><div class="file-preview-remove" onclick="window.removeFeedbackFile(' + index + ')">×</div>';
            filePreviewContainer.appendChild(previewItem);
        };
        reader.readAsDataURL(file);
    }

    window.removeFeedbackFile = function(index) {
        uploadedFiles.splice(index, 1);
        if (filePreviewContainer) {
            filePreviewContainer.innerHTML = '';
            uploadedFiles.forEach((file, i) => showFilePreview(file, i));
        }
    };

    async function fetchWithRetry(url, options, retries, timeoutMs) {
        retries = (retries !== undefined) ? retries : 2;
        timeoutMs = (timeoutMs !== undefined) ? timeoutMs : 15000;
        for (var attempt = 0; attempt <= retries; attempt++) {
            var controller = new AbortController();
            var timer = setTimeout(function() { controller.abort(); }, timeoutMs);
            try {
                var resp = await fetch(url, Object.assign({}, options, { signal: controller.signal }));
                clearTimeout(timer);
                return resp;
            } catch (e) {
                clearTimeout(timer);
                if (attempt === retries) throw e;
                // 递增延迟：1s, 2s，等待网络恢复
                await new Promise(function(r) { setTimeout(r, 1000 * (attempt + 1)); });
            }
        }
    }

    function submitFeedback() {
        if (!fbSubmit) return;
        
        validateContent();
        if (!isContentValid) {
            return;
        }
        
        fbSubmit.disabled = true;
        fbSubmit.textContent = '提交中…';
        
        (async function() {
            try {
                var fileDataList = [];
                for (var i = 0; i < uploadedFiles.length; i++) {
                    var file = uploadedFiles[i];
                    var reader = new FileReader();
                    var dataUrl = await new Promise(function(resolve, reject) {
                        reader.onload = function() { resolve(reader.result); };
                        reader.onerror = reject;
                        reader.readAsDataURL(file);
                    });
                    var base64 = dataUrl.split(',')[1];
                    var mime = dataUrl.split(',')[0].split(':')[1].split(';')[0];
                    fileDataList.push({
                        name: file.name,
                        type: file.type || mime,
                        size: file.size,
                        base64: base64
                    });
                }
                
                var content = document.getElementById('fbContent') ? document.getElementById('fbContent').value.trim() : '';
                var payload = {
                    type: document.getElementById('fbType') ? document.getElementById('fbType').value : 'suggestion',
                    source: feedbackSource,
                    content: content,
                    contact: document.getElementById('fbContact') ? document.getElementById('fbContact').value.trim() : '',
                    files: fileDataList
                };
                
                var resp = await fetchWithRetry('/api/feedback', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                var data = await resp.json();
                
                if (data.success) {
                    if (feedbackForm) feedbackForm.style.display = 'none';
                    if (feedbackSuccess) feedbackSuccess.classList.add('show');
                    
                    if (data.imagesUploaded !== undefined && feedbackSuccess) {
                        var successMsgEl = feedbackSuccess.querySelector('p');
                        if (successMsgEl) {
                            successMsgEl.textContent = '🎉 感谢你的反馈！\\n图片上传: ' + data.imagesUploaded + '/' + uploadedFiles.length;
                            successMsgEl.style.whiteSpace = 'pre-line';
                        }
                    }
                } else {
                    throw new Error(data.error || 'API返回错误');
                }
            } catch (e) {
                var errMsg = e.message || '';
                if (e.name === 'AbortError') {
                    alert('请求超时，网络可能不稳定，请稍后重试。\n\n您也可以通过以下方式联系我们：\n📧 微信公众号：TS爱心联盟');
                } else if (errMsg === 'Failed to fetch' || e.name === 'TypeError') {
                    alert('网络连接失败，请检查网络后重试。\n\n如果问题持续出现，您也可以通过以下方式联系我们：\n📧 微信公众号：TS爱心联盟');
                } else {
                    alert('反馈服务暂时不可用，请稍后再试。\n\n您也可以通过以下方式联系我们：\n📧 微信公众号：TS爱心联盟');
                }
            } finally {
                if (fbSubmit) {
                    fbSubmit.disabled = false;
                    fbSubmit.textContent = '提交反馈';
                }
            }
        })();
    }

    if (fbContent) {
        fbContent.addEventListener('input', validateContent);
        fbContent.addEventListener('blur', validateContent);
    }

    if (feedbackFloat) {
        feedbackFloat.addEventListener('click', openFeedback);
    }

    if (feedbackClose) {
        feedbackClose.addEventListener('click', closeFeedback);
    }

    if (feedbackOverlay) {
        feedbackOverlay.addEventListener('click', function(e) {
            if (e.target === feedbackOverlay) closeFeedback();
        });
    }

    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && feedbackOverlay && feedbackOverlay.classList.contains('active')) {
            closeFeedback();
        }
    });

    if (fileUploadArea && fbFile) {
        fileUploadArea.addEventListener('click', function() {
            fbFile.click();
        });

        fileUploadArea.addEventListener('dragover', function(e) {
            e.preventDefault();
            this.classList.add('dragover');
        });

        fileUploadArea.addEventListener('dragleave', function() {
            this.classList.remove('dragover');
        });

        fileUploadArea.addEventListener('drop', function(e) {
            e.preventDefault();
            this.classList.remove('dragover');
            handleFiles(e.dataTransfer.files);
        });

        fbFile.addEventListener('change', function(e) {
            handleFiles(e.target.files);
        });
    }

    if (fbSubmit) {
        fbSubmit.addEventListener('click', submitFeedback);
    }
});
