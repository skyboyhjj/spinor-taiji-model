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
                const fileDataList = [];
                for (const file of uploadedFiles) {
                    const reader = new FileReader();
                    const dataUrl = await new Promise((resolve, reject) => {
                        reader.onload = () => resolve(reader.result);
                        reader.onerror = reject;
                        reader.readAsDataURL(file);
                    });
                    const base64 = dataUrl.split(',')[1];
                    const mime = dataUrl.split(',')[0].split(':')[1].split(';')[0];
                    fileDataList.push({
                        name: file.name,
                        type: file.type || mime,
                        size: file.size,
                        base64: base64
                    });
                }
                
                const content = document.getElementById('fbContent') ? document.getElementById('fbContent').value.trim() : '';
                const payload = {
                    type: document.getElementById('fbType') ? document.getElementById('fbType').value : 'suggestion',
                    source: feedbackSource,
                    content: content,
                    contact: document.getElementById('fbContact') ? document.getElementById('fbContact').value.trim() : '',
                    files: fileDataList
                };
                
                const resp = await fetch('/api/feedback', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await resp.json();
                
                if (data.success) {
                    if (feedbackForm) feedbackForm.style.display = 'none';
                    if (feedbackSuccess) feedbackSuccess.classList.add('show');
                    
                    if (data.imagesUploaded !== undefined && feedbackSuccess) {
                        const successMsgEl = feedbackSuccess.querySelector('p');
                        if (successMsgEl) {
                            successMsgEl.textContent = '🎉 感谢你的反馈！\\n图片上传: ' + data.imagesUploaded + '/' + uploadedFiles.length;
                            successMsgEl.style.whiteSpace = 'pre-line';
                        }
                    }
                } else {
                    throw new Error(data.error || 'API返回错误');
                }
            } catch (e) {
                alert('反馈服务暂时不可用，请稍后再试。\\n\\n您可以通过以下方式联系我们：\\n📧 微信公众号：TS爱心联盟');
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

    function updateFloatButtons() {
        const isVisible = window.scrollY > 300;
        feedbackFloat?.classList.toggle('show', isVisible);
    }

    if (feedbackFloat) {
        updateFloatButtons();
        window.addEventListener('scroll', updateFloatButtons);
    }
});
