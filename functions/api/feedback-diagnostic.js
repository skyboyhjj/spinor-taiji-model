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

  for (const [key, value] of formData.entries()) {
    if (typeof value === 'object' && value.size !== undefined) {
      result.files.push({
        field: key,
        name: value.name,
        type: value.type,
        size: value.size
      });
    } else {
      result.formFields[key] = value;
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
    const file = result.files[0];
    const fileObj = formData.get(file.field);
    if (fileObj) {
      try {
        const buffer = await fileObj.arrayBuffer();
        const base64 = btoa(String.fromCharCode(...new Uint8Array(buffer)));
        const testFileName = `diagnostic-test-${Date.now()}.txt`;
        const testFilePath = `feedback-images/${testFileName}`;
        const testContent = btoa('Diagnostic test file - safe to delete');

        const uploadResponse = await fetch(`https://api.github.com/repos/${githubRepo}/contents/${testFilePath}`, {
          method: 'PUT',
          headers: {
            'Authorization': `token ${env.GITHUB_TOKEN}`,
            'Content-Type': 'application/json',
            'User-Agent': 'spinor-taiji-diagnostic'
          },
          body: JSON.stringify({
            message: 'diagnostic test',
            content: testContent,
            branch: githubBranch
          })
        });

        result.fileUploadTest = {
          status: uploadResponse.status,
          success: uploadResponse.ok,
          testFile: testFilePath
        };

        if (!uploadResponse.ok) {
          result.fileUploadTest.error = await uploadResponse.text();
        }
      } catch (e) {
        result.fileUploadTest = { error: e.message };
      }
    }
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
