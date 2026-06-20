@echo off
chcp 65001 >nul
title 《道德经》公众号推送脚本

:: ================================================
:: 《道德经》"无死地"旋量太极读解 - 公众号推送一键脚本
:: ================================================

echo.
echo ================================================
echo 📤 《道德经》公众号推送一键脚本
echo ================================================
echo.

:: 步骤1: 验证配置文件
echo 【步骤1/3】验证配置文件
echo --------------------------------
if not exist ".env" (
    echo ❌ 错误: 未找到配置文件 .env
    pause
    exit /b 1
)
echo ✅ 配置文件存在

:: 步骤2: 生成配图（可选）
echo.
echo 【步骤2/3】是否重新生成配图？
echo --------------------------------
echo 1. 是（重新生成所有配图）
echo 2. 否（使用已生成的配图）
set /p regenerate=请选择 [1/2]: 

if "%regenerate%"=="1" (
    echo 🔄 正在重新生成配图...
    python "E:\Trac Project\04-伦理即道体\generate_daodejing_images.py"
    
    if %errorlevel% neq 0 (
        echo ❌ 配图生成失败!
        pause
        exit /b 1
    )
    echo ✅ 配图生成完成
) else (
    echo ⏭️ 跳过配图生成，使用已有的配图
)
echo.

:: 步骤3: 推送文章到草稿箱
echo 【步骤3/3】推送文章到公众号草稿箱
echo --------------------------------
echo 正在推送文章...
python "E:\Trac Project\04-伦理即道体\push_daodejing_draft.py"

if %errorlevel% neq 0 (
    echo ❌ 推送失败!
    pause
    exit /b 1
)
echo ✅ 推送完成
echo.

:: 完成提示
echo ================================================
echo 🎉 恭喜！文章已成功推送到公众号草稿箱
echo ================================================
echo.
echo 📌 下一步操作:
echo    1. 登录微信公众号后台
echo    2. 进入「素材管理」-「草稿箱」
echo    3. 查看并编辑已推送的文章
echo    4. 确认无误后即可发布
echo.
echo 📁 相关文件:
echo    - 更新后的文章: 《道德经》无死地_旋量太极读解_公众号版_with_new_images.html
echo    - 生成的配图: images/taiji_life.png, images/six_levels.png, images/cover.png
echo    - 草稿列表: draft_list_daodejing.json
echo    - 配置文件: .env
echo.
pause