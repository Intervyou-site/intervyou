#!/usr/bin/env python3
"""
Fix all TemplateResponse calls to use the new Starlette syntax
"""

import re

# Read the file
with open('fastapi_app_cleaned.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern 1: templates.TemplateResponse("template.html", {"request": request})
# Replace with: templates.TemplateResponse(request=request, name="template.html")
pattern1 = r'templates\.TemplateResponse\("([^"]+)",\s*\{"request":\s*request\}\)'
replacement1 = r'templates.TemplateResponse(request=request, name="\1")'
content = re.sub(pattern1, replacement1, content)

# Pattern 2: templates.TemplateResponse("template.html", {"request": request, "key": value})
# Replace with: templates.TemplateResponse(request=request, name="template.html", context={"key": value})
pattern2 = r'templates\.TemplateResponse\("([^"]+)",\s*\{("request":\s*request,\s*.+?)\}\)'
def replace_pattern2(match):
    template_name = match.group(1)
    context_content = match.group(2)
    # Remove "request": request, from context
    context_content = re.sub(r'"request":\s*request,\s*', '', context_content)
    if context_content.strip():
        return f'templates.TemplateResponse(request=request, name="{template_name}", context={{{context_content}}})'
    else:
        return f'templates.TemplateResponse(request=request, name="{template_name}")'

content = re.sub(pattern2, replace_pattern2, content)

# Pattern 3: response = templates.TemplateResponse("template.html", {"request": request})
# Already handled by pattern 1 and 2

# Write the fixed content
with open('fastapi_app_cleaned.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed all TemplateResponse calls!")
print("   Updated fastapi_app_cleaned.py")
