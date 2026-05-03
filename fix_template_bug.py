#!/usr/bin/env python3
"""
Emergency fix for TemplateResponse TypeError
The error occurs when passing a dict as the first argument instead of using named parameters
"""

import re

# Read the file
with open('fastapi_app_cleaned.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern: templates.TemplateResponse({...})
# This is WRONG and causes "TypeError: unhashable type: 'dict'"
# Should be: templates.TemplateResponse(request=request, name="template.html", context={...})

# Find any TemplateResponse calls that start with a dict
pattern = r'templates\.TemplateResponse\(\s*\{'
matches = re.findall(pattern, content)

if matches:
    print(f"❌ Found {len(matches)} problematic TemplateResponse calls!")
    print("These need to be fixed manually.")
else:
    print("✅ No problematic TemplateResponse calls found.")

# Also check for TemplateResponse without 'request=' parameter
pattern2 = r'templates\.TemplateResponse\([^r]'
matches2 = re.findall(pattern2, content)

if matches2:
    print(f"⚠️  Found {len(matches2)} TemplateResponse calls that might be incorrect")

print("\nDone!")
