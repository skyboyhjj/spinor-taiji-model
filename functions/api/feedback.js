export async function onRequestPost(context) {
  const { request, env } = context;

  let bodyData;
  try {
    const contentType = request.headers.get('content-type') || '';
    if (contentType.includes('application/json')) {
      bodyData = await request.json();
    } else {
      const formData = await request.formData();
      bodyData = {
        type: formData.get('type'),
        source: formData.get('source'),
        content: formData.get('content'),
        contact: formData.get('contact'),
        files: []
      };
      for (const key of formData.keys()) {
        if (key.startsWith('files') || key === 'file') {
          const val = formData.get(key);
          if (val && typeof val === 'object' && val.arrayBuffer) {
            bodyData.files.push({
              name: val.name || key,
              type: val.type || 'image/png',
              size: val.size,
              _blob: val
            });
          }
        }
      }
    }
  } catch {
    return new Response(JSON.stringify({ error: '请求格式无效' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' }
    });
  }

  const type = bodyData.type;
  const source = bodyData.source;
  const content = bodyData.content;
  const contact = bodyData.contact;
  const files = bodyData.files || [];

  if (!content || content.trim().length < 5) {
    return new Response(JSON.stringify({ error: '反馈内容不能为空或过短（至少5个字符）' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' }
    });
  }

  const typeLabel = { correction: '纠错', suggestion: '建议', question: '疑问', appreciation: '赞赏' };
  const sourceLabel = { statement: '声明', glossary: '词汇表', other: '其他' };

  const issueTitle = `[反馈] ${typeLabel[type] || type} - ${sourceLabel[source] || source}`;

  const githubRepo = env.GITHUB_REPO || 'skyboyhjj/spinor-taiji-model';
  const githubBranch = env.GITHUB_BRANCH || 'main';

  const uploadedImages = [];
  const imageErrors = [];

  if (files.length > 0) {
    const timestamp = Date.now();
    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      try {
        let base64;
        if (file.base64) {
          base64 = file.base64;
        } else if (file._blob) {
          const buffer = await file._blob.arrayBuffer();
          base64 = btoa(String.fromCharCode(...new Uint8Array(buffer)));
        } else {
          continue;
        }

        const ext = (file.name || '').split('.').pop()?.toLowerCase() || 'png';
        const safeExt = ['jpg', 'jpeg', 'png', 'gif', 'webp'].includes(ext) ? ext : 'png';
        const fileName = `feedback-${timestamp}-${i + 1}.${safeExt}`;
        const filePath = `feedback-images/${fileName}`;

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

        if (uploadResponse.ok) {
          const rawUrl = `https://raw.githubusercontent.com/${githubRepo}/${githubBranch}/${filePath}`;
          uploadedImages.push({ name: fileName, url: rawUrl });
        } else {
          const errorText = await uploadResponse.text();
          console.error(`Upload failed for ${fileName}:`, errorText.substring(0, 200));
          imageErrors.push({ file: file.name || fileName, error: errorText.substring(0, 200) });
        }
      } catch (e) {
        console.error(`Image processing error:`, e.message);
        imageErrors.push({ file: file.name || `image${i+1}`, error: e.message });
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

  if (files.length > 0) {
    issueBody += `\n\n📎 **附件**: ${files.length} 张图片`;
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
