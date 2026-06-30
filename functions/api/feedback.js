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
  
  let issueBody = [
    '## 反馈详情',
    '',
    `- **类型**: ${typeLabel[type] || type}`,
    `- **来源**: ${sourceLabel[source] || source}`,
    '',
    content,
    '',
    contact ? `- **联系方式**: ${contact}` : '',
    '',
    '---',
    `> 标签: \`status:triage\` \`source:${source}\` \`type:${type}\``,
    '',
    '*此 Issue 由用户通过页面反馈表单自动提交*'
  ].join('\n');

  try {
    const githubRepo = env.GITHUB_REPO || 'skyboyhjj/spinor-taiji-model';
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
      return new Response(JSON.stringify({ error: '提交失败（GitHub API 错误）', detail: errorText }), {
        status: 502,
        headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' }
      });
    }

    const issue = await githubResponse.json();
    const issueNumber = issue.number;

    const files = formData.getAll('files');
    if (files.length > 0 && files[0] !== '') {
      for (const file of files) {
        if (!file || file.size === 0) continue;
        
        const uploadResponse = await fetch(`https://uploads.github.com/repos/${githubRepo}/issues/${issueNumber}/uploads`, {
          method: 'POST',
          headers: {
            'Authorization': `token ${env.GITHUB_TOKEN}`,
            'Content-Type': file.type || 'application/octet-stream',
            'User-Agent': 'spinor-taiji-feedback',
            'Accept': 'application/vnd.github.v3+json'
          },
          body: file
        });

        if (uploadResponse.ok) {
          const uploadResult = await uploadResponse.json();
          issueBody += `\n\n![${uploadResult.name}](${uploadResult.url})`;
        }
      }

      if (issueBody !== issue.body) {
        await fetch(`https://api.github.com/repos/${githubRepo}/issues/${issueNumber}`, {
          method: 'PATCH',
          headers: {
            'Authorization': `token ${env.GITHUB_TOKEN}`,
            'Content-Type': 'application/json',
            'User-Agent': 'spinor-taiji-feedback'
          },
          body: JSON.stringify({ body: issueBody })
        });
      }
    }

    return new Response(JSON.stringify({ success: true, url: issue.html_url }), {
      headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' }
    });

  } catch (e) {
    return new Response(JSON.stringify({ error: '提交失败，请稍后重试', detail: e.message }), {
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
