export async function onRequestPost(context) {
  const { request, env } = context;

  let formData;
  try {
    formData = await request.formData();
  } catch (e) {
    return new Response(JSON.stringify({ 
      error: 'FormData 解析失败', 
      detail: e.message 
    }), {
      status: 400,
      headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' }
    });
  }

  const result = {
    formFields: {},
    files: [],
    githubTest: null,
    fileUploadTest: null
  };

  function isBlobLike(value) {
    if (!value) return false;
    if (typeof value !== 'object') return false;
    if (typeof value.arrayBuffer === 'function') return true;
    if (typeof value.stream === 'function') return true;
    if (value.size !== undefined && value.type !== undefined) return true;
    return false;
  }

  for (const [key, value] of formData.entries()) {
    if (isBlobLike(value)) {
      result.files.push({
        field: key,
        name: value.name || key,
        type: value.type || 'application/octet-stream',
        size: value.size
      });
    } else if (typeof value === 'string') {
      if (key.startsWith('files')) {
        result.formFields[key] = `[string, length=${value.length}, starts with binary=${value.charCodeAt(0) > 127}]`;
      } else {
        result.formFields[key] = value;
      }
    } else {
      result.formFields[key] = String(value);
    }
  }

  const fileKeys = [];
  for (const key of formData.keys()) {
    if (key.startsWith('files') || key === 'file') {
      fileKeys.push(key);
    }
  }
  result.fileKeys = fileKeys;

  for (const key of fileKeys) {
    try {
      const file = formData.get(key);
      if (file && isBlobLike(file)) {
        const alreadyListed = result.files.find(f => f.field === key);
        if (!alreadyListed) {
          result.files.push({
            field: key,
            name: file.name || key,
            type: file.type || 'application/octet-stream',
            size: file.size,
            fromGet: true
          });
        }
      }
    } catch (e) {
      result.formFields[`${key}_getError`] = e.message;
    }
  }

  const githubRepo = env.GITHUB_REPO || 'skyboyhjj/spinor-taiji-model';
  const githubBranch = env.GITHUB_BRANCH || 'main';

  try {
    const testResponse = await fetch(`https://api.github.com/repos/${githubRepo}`, {
      headers: {
        'Authorization': `token ${env.GITHUB_TOKEN}`,
        'User-Agent': 'spinor-taiji-diagnostic'
      }
    });
    const testData = await testResponse.json();
    result.githubTest = {
      status: testResponse.status,
      hasRepoAccess: testResponse.ok,
      repoName: testData.full_name,
      permissions: testData.permissions || null
    };
  } catch (e) {
    result.githubTest = { error: e.message };
  }

  if (result.files.length > 0) {
    try {
      const firstFile = result.files[0];
      const fileObj = formData.get(firstFile.field);
      if (fileObj) {
        const buffer = await fileObj.arrayBuffer();
        const base64 = btoa(String.fromCharCode(...new Uint8Array(buffer)));
        const testFileName = `diagnostic-test-${Date.now()}.png`;
        const testFilePath = `feedback-images/${testFileName}`;

        const uploadResponse = await fetch(`https://api.github.com/repos/${githubRepo}/contents/${testFilePath}`, {
          method: 'PUT',
          headers: {
            'Authorization': `token ${env.GITHUB_TOKEN}`,
            'Content-Type': 'application/json',
            'User-Agent': 'spinor-taiji-diagnostic'
          },
          body: JSON.stringify({
            message: 'diagnostic test image',
            content: base64,
            branch: githubBranch
          })
        });

        result.fileUploadTest = {
          status: uploadResponse.status,
          success: uploadResponse.ok,
          testFile: testFilePath,
          fileSize: buffer.byteLength,
          base64Length: base64.length
        };

        if (!uploadResponse.ok) {
          result.fileUploadTest.error = await uploadResponse.text();
        }
      }
    } catch (e) {
      result.fileUploadTest = { error: e.message, stack: e.stack };
    }
  } else if (fileKeys.length > 0) {
    result.fileUploadTest = {
      skipped: true,
      reason: 'No file objects detected (files came as strings)',
      fileKeysFound: fileKeys.length
    };
  }

  return new Response(JSON.stringify(result, null, 2), {
    status: 200,
    headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' }
  });
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
