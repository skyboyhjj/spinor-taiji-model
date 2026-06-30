export async function onRequestPost(context) {
  const { request, env } = context;

  let formData;
  try {
    formData = await request.formData();
  } catch {
    return new Response(JSON.stringify({ error: '请求格式无效' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' }
    });
  }

  const type = formData.get('type');
  const source = formData.get('source');
  const content = formData.get('content');
  const contact = formData.get('contact');

  if (!content || content.trim().length < 5) {
    return new Response(JSON.stringify({ error: '反馈内容不能为空或过短（至少5个字符）' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' }
    });
  }

  const typeLabel = { correction: '纠错', suggestion: '建议', question: '疑问', appreciation: '赞赏' };
  const sourceLabel = { statement: '声明', glossary: '词汇表', other: '其他' };

  const issueTitle = `[反馈] ${typeLabel[type] || type} - ${sourceLabel[source] || source}`;
  
  function isBlobLike(value) {
    if (!value) return false;
    if (typeof value !== 'object') return false;
    if (typeof value.arrayBuffer === 'function') return true;
    if (typeof value.stream === 'function') return true;
    if (value.size !== undefined && value.type !== undefined) return true;
    return false;
  }

  const allFiles = [];
  const fileKeys = [];
  for (const key of formData.keys()) {
    if (key.startsWith('files') || key === 'file') {
      fileKeys.push(key);
    }
  }

  for (const key of fileKeys) {
    try {
      const file = formData.get(key);
      if (file && isBlobLike(file) && file.size > 0) {
        allFiles.push({ key, file });
      }
    } catch (e) {
      console.error(`Error getting file ${key}:`, e.message);
    }
  }

  console.log(`File keys found: ${fileKeys.length}, files detected: ${allFiles.length}`);

  const githubRepo = env.GITHUB_REPO || 'skyboyhjj/spinor-taiji-model';
  const githubBranch = env.GITHUB_BRANCH || 'main';

  const uploadedImages = [];
  const imageErrors = [];

  if (allFiles.length > 0) {
    const timestamp = Date.now();
    for (let i = 0; i < allFiles.length; i++) {
      const { key, file } = allFiles[i];
      try {
        const buffer = await file.arrayBuffer();
        console.log(`File ${i} buffer size: ${buffer.byteLength}`);
        
        const base64 = btoa(String.fromCharCode(...new Uint8Array(buffer)));
        console.log(`File ${i} base64 length: ${base64.length}`);
        
        const ext = file.name?.split('.').pop() || 'png';
        const safeExt = ['jpg', 'jpeg', 'png', 'gif', 'webp'].includes(ext.toLowerCase()) ? ext.toLowerCase() : 'png';
        const fileName = `feedback-${timestamp}-${i + 1}.${safeExt}`;
        const filePath = `feedback-images/${fileName}`;

        console.log(`Uploading to: ${filePath}`);

        const uploadResponse = await fetch(`https://api.github.com/repos/${githubRepo}/contents/${filePath}`, {
          method: 'PUT',
          headers: {
            'Authorization': `token ${env.GITHUB_TOKEN}`,
            'Content-Type': 'application/json',
            'User-Agent': 'spinor-taiji-feedback'
          },
          body: JSON.stringify({
            message: `feedback: ${fileName}`,
            content: base64,
            branch: githubBranch
          })
        });

        console.log(`Upload response status: ${uploadResponse.status}`);

        if (uploadResponse.ok) {
          const uploadResult = await uploadResponse.json();
          console.log(`Upload success: ${uploadResult.content?.download_url}`);
          const rawUrl = `https://raw.githubusercontent.com/${githubRepo}/${githubBranch}/${filePath}`;
          uploadedImages.push({ name: fileName, url: rawUrl });
        } else {
          const errorText = await uploadResponse.text();
          console.error(`Upload failed: ${errorText}`);
          imageErrors.push({ file: file.name, error: errorText });
        }
      } catch (e) {
        console.error(`Image processing error: ${e.message}`);
        imageErrors.push({ file: file.name, error: e.message });
      }
    }
  }

  let issueBody = [
    '## 反馈详情',
    '',
    `- **类型**: ${typeLabel[type] || type}`,
    `- **来源**: ${sourceLabel[source] || source}`,
    '',
    content,
    '',
    contact ? `- **联系方式**: ${contact}` : '',
  ].join('\n');

  if (allFiles.length > 0) {
    issueBody += `\n\n📎 **附件**: ${allFiles.length} 张图片`;
  }

  if (uploadedImages.length > 0) {
    issueBody += '\n\n---\n\n### 📷 附件图片\n';
    uploadedImages.forEach((img, i) => {
      issueBody += `\n![图片${i + 1} - ${img.name}](${img.url})\n`;
    });
  }

  if (imageErrors.length > 0) {
    issueBody += '\n\n⚠️ **部分图片上传失败**:\n';
    imageErrors.forEach(err => {
      issueBody += `- ${err.file}: ${err.error.substring(0, 200)}\n`;
    });
  }

  issueBody += [
    '',
    '---',
    `> 标签: \`status:triage\` \`source:${source}\` \`type:${type}\``,
    '',
    '*此 Issue 由用户通过页面反馈表单自动提交*'
  ].join('\n');

  try {
    const feedbackLabel = env.FEEDBACK_LABEL || 'feedback';
    const labels = [feedbackLabel, `source:${source}`, `type:${type}`];

    const githubResponse = await fetch(`https://api.github.com/repos/${githubRepo}/issues`, {
      method: 'POST',
      headers: {
        'Authorization': `token ${env.GITHUB_TOKEN}`,
        'Content-Type': 'application/json',
        'User-Agent': 'spinor-taiji-feedback'
      },
      body: JSON.stringify({
        title: issueTitle,
        body: issueBody,
        labels: labels
      })
    });

    if (!githubResponse.ok) {
      const errorText = await githubResponse.text();
      return new Response(JSON.stringify({ 
        error: '提交失败（GitHub API 错误）', 
        detail: errorText,
        imagesUploaded: uploadedImages.length,
        imageErrors: imageErrors
      }), {
        status: 502,
        headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' }
      });
    }

    const issue = await githubResponse.json();

    return new Response(JSON.stringify({ 
      success: true, 
      url: issue.html_url,
      imagesUploaded: uploadedImages.length,
      imageErrors: imageErrors
    }), {
      headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' }
    });

  } catch (e) {
    return new Response(JSON.stringify({ 
      error: '提交失败，请稍后重试', 
      detail: e.message,
      imagesUploaded: uploadedImages.length,
      imageErrors: imageErrors
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' }
    });
  }
}

export async function onRequestOptions() {
  return new Response(null, {
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type'
    }
  });
}
