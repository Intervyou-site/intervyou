# IntervYou Project Cleanup Script
# This script removes unnecessary files and prepares the project for production

Write-Host "Starting IntervYou Project Cleanup..." -ForegroundColor Cyan
Write-Host ""

# Documentation files to remove (keeping only README.md and DEPLOYMENT_GUIDE.md)
$docsToRemove = @(
    "ABUSE_PROTECTION_GUIDE.md", "ABUSE_PROTECTION_QUICK_START.md", "ABUSE_PROTECTION_SUMMARY.md",
    "ACHIEVEMENTS_FIX.md", "ADMIN_COMPLETE_GUIDE.md", "ADMIN_DELIVERY_SUMMARY.md",
    "ADMIN_FINAL_STATUS.md", "ADMIN_IMPLEMENTATION_SUMMARY.md", "ADMIN_QUICK_REFERENCE.md",
    "ADMIN_QUICK_SETUP.md", "ADMIN_REDESIGN_SUMMARY.md", "ADMIN_ROUTER_COMPLETE.md",
    "ADMIN_SYSTEM_README.md", "AI_FEEDBACK_ENHANCEMENTS.md", "AI_FEEDBACK_IMPLEMENTATION_SUMMARY.md",
    "AI_FEEDBACK_TESTING_GUIDE.md", "AI_FEEDBACK_VISUAL_GUIDE.md", "APTITUDE_QUESTIONS_ADDED_SUMMARY.md",
    "APTITUDE_QUESTIONS_EXPANSION.md", "ARCHITECTURE.md", "AUTH_ROUTER_COMPLETE.md",
    "BEHAVIORAL_QUESTIONS_DEBUG.md", "BROWSER_CACHE_FIX.md", "BUG_FIX_DIFFICULTY_MISMATCH.md",
    "CACHE_BUSTING_FIX.md", "CAMERA_FIX_COMPLETE.md", "CAMERA_FIX_GUIDE.md",
    "CAMERA_FIXED_SUMMARY.md", "CAMERA_NUCLEAR_FIX.md", "CATEGORY_MISMATCH_FIX.md",
    "COMPLETE_APP_DOCUMENTATION.md", "COMPLETE_FIX_SUMMARY.md", "COMPLETE_TEST.md",
    "CONTEXT_TRANSFER_UPDATED.md", "DEBUG_IDE_INPUT.md", "DOCKER_SETUP.md",
    "FINAL_FIX_COMPANY_QUESTIONS.md", "FINAL_FIX_SUMMARY.md", "FINAL_PUSH_STEPS.md",
    "FIX_COMPANY_QUESTIONS.md", "HTTPS_CAMERA_READY.md", "IDE_CHALLENGE_LOADING_FIX.md",
    "IDE_CODE_QUALITY_IMPROVEMENT.md", "IDE_RATE_LIMIT_FIX.md", "IDE_RATE_LIMIT_FLOW.md",
    "IDE_RATE_LIMIT_QUICK_FIX.md", "IDE_STDIN_FIX.md", "IDE_TIMEOUT_FIX.md",
    "IMMEDIATE_ACTION_PLAN.md", "MANUAL_TESTING_GUIDE.md", "MASS_RECRUITMENT_COMPANY_BRANDING_COMPLETE.md",
    "MASS_RECRUITMENT_COMPANY_SPECIFIC_QUESTIONS_COMPLETE.md", "MASS_RECRUITMENT_QUICK_START.md",
    "PRACTICE_PAGE_COMPLETE_FIX.md", "PRODUCTION_SECURITY_GUIDE.md", "PROFILE_STATS_FIX.md",
    "PROFILE_USERNAME_FIX.md", "PROOF_SERVER_WORKS.md", "PUSH_INSTRUCTIONS.md",
    "QUESTION_BANK_ADDED.md", "QUESTION_BANK_EXPANSION_PLAN.md", "QUESTION_BANK_SUMMARY.md",
    "QUICK_FIX_NOW.md", "QUICK_REFERENCE.md", "RAPID_FIRE_IMPLEMENTATION.md",
    "README_SECURITY_UPDATE.md", "REMOVED_CATEGORIES_SUMMARY.md", "RESUME_BUILDER_ENHANCEMENT_PLAN.md",
    "RESUME_ENHANCEMENT_STATUS.md", "RESUME_TEMPLATE_IMPROVEMENTS.md", "REVERT_COMPLETE.md",
    "ROTATE_SECRETS_NOW.txt", "SECRET_ROTATION_CHECKLIST.md", "SECRET_ROTATION_COMPLETE.md",
    "SECRETS_REMEDIATION_GUIDE.md", "SECURITY_AUDIT_IDOR.md", "SECURITY_AUDIT_REPORT.md",
    "SECURITY_AUDIT_SUMMARY.md", "SECURITY_BEST_PRACTICES.md", "SECURITY_CHECKLIST.md",
    "SECURITY_CHECKLIST.txt", "SECURITY_COMPLETE.md", "SECURITY_COMPLETION_CHECKLIST.md",
    "SECURITY_DEPLOYMENT_SUMMARY.md", "SECURITY_FINAL_STATUS.md", "SECURITY_IMPLEMENTATION_SUMMARY.md",
    "SECURITY_IMPLEMENTATION.md", "SECURITY_QUICK_START.md", "SECURITY_README.md",
    "SECURITY_SCAN_COMPLETE.md", "SECURITY_SECRETS_AUDIT_REPORT.md", "SECURITY_STATUS_FINAL.md",
    "SECURITY_TEST_REPORT.md", "SECURITY_VERIFICATION_REPORT.md", "SECURITY_VISUAL_SUMMARY.md",
    "SECURITY.md", "SERVER_STATUS_REPORT.md", "START_HERE.md", "TASK_10_COMPLETE.md",
    "TESTING_COMPLETE.md", "DEPLOYMENT_CHECKLIST.txt"
)

# Test/Debug/Utility scripts to remove
$scriptsToRemove = @(
    "add_aptitude_questions.py", "azure-setup.ps1", "azure-setup.sh",
    "check_server_status.py", "create_admin.py", "fix_all_user_dicts.py",
    "fix_database.py", "fix_integration.py", "fix_user_dict.py",
    "free_ai_models.py", "generate_cert.py", "huggingface_utils.py",
    "integrate_questions.py", "integrate_security_logging.py", "oauth_config.py",
    "password_reset_service.py", "promote_to_admin.py", "question_generator.py",
    "realtime_analysis.py", "resume_pdf_generator.py", "resume_templates.py",
    "rotate_secrets.sh", "run_app.py", "schemas.py", "security_setup.py",
    "setup_enhanced_analysis.py", "setup_intervyou_db.sql", "test_aptitude_questions.py",
    "test_companies_endpoint.py", "test_live_server.py", "test.cpp",
    "unblock_ip.py", "vector_store.py", "verify_fix.py", "verify_question_bank.py",
    "wsgi.py", "program", "email_service.py", "email_verification.py"
)

# Certificate files (should be generated per environment)
$certsToRemove = @("cert.pem", "key.pem")

# Unused templates
$templatesToRemove = @(
    "templates/camera_diagnostic.html",
    "templates/camera_test.html",
    "templates/simple_camera_test.html",
    "templates/ide_test.html",
    "templates/practice_enhanced.html"
)

# Old service files
$oldServicesToRemove = @(
    "services/resume_templates_old.py"
)

# Folders to remove
$foldersToRemove = @(
    "notebooks",
    "entrypoint",
    "src",
    "node_modules",
    "swark-output",
    "mobile",
    "utils",
    "data",
    "config",
    "alembic"
)

# Count total items
$totalItems = $docsToRemove.Count + $scriptsToRemove.Count + $certsToRemove.Count + 
              $templatesToRemove.Count + $oldServicesToRemove.Count + $foldersToRemove.Count

Write-Host "Cleanup Summary:" -ForegroundColor Yellow
Write-Host "  - Documentation files: $($docsToRemove.Count)"
Write-Host "  - Script files: $($scriptsToRemove.Count)"
Write-Host "  - Certificate files: $($certsToRemove.Count)"
Write-Host "  - Template files: $($templatesToRemove.Count)"
Write-Host "  - Old service files: $($oldServicesToRemove.Count)"
Write-Host "  - Folders: $($foldersToRemove.Count)"
Write-Host "  - Total items: $totalItems"
Write-Host ""

$confirmation = Read-Host "Do you want to proceed with cleanup? (yes/no)"
if ($confirmation -ne "yes") {
    Write-Host "Cleanup cancelled." -ForegroundColor Red
    exit
}

Write-Host ""
Write-Host "Removing files..." -ForegroundColor Cyan

# Remove documentation files
$removed = 0
foreach ($file in $docsToRemove) {
    if (Test-Path $file) {
        Remove-Item $file -Force
        $removed++
    }
}
Write-Host "[OK] Removed $removed documentation files" -ForegroundColor Green

# Remove script files
$removed = 0
foreach ($file in $scriptsToRemove) {
    if (Test-Path $file) {
        Remove-Item $file -Force
        $removed++
    }
}
Write-Host "[OK] Removed $removed script files" -ForegroundColor Green

# Remove certificate files
$removed = 0
foreach ($file in $certsToRemove) {
    if (Test-Path $file) {
        Remove-Item $file -Force
        $removed++
    }
}
Write-Host "[OK] Removed $removed certificate files" -ForegroundColor Green

# Remove unused templates
$removed = 0
foreach ($file in $templatesToRemove) {
    if (Test-Path $file) {
        Remove-Item $file -Force
        $removed++
    }
}
Write-Host "[OK] Removed $removed unused templates" -ForegroundColor Green

# Remove old service files
$removed = 0
foreach ($file in $oldServicesToRemove) {
    if (Test-Path $file) {
        Remove-Item $file -Force
        $removed++
    }
}
Write-Host "[OK] Removed $removed old service files" -ForegroundColor Green

# Remove folders
$removed = 0
foreach ($folder in $foldersToRemove) {
    if (Test-Path $folder) {
        Remove-Item $folder -Recurse -Force
        $removed++
    }
}
Write-Host "[OK] Removed $removed folders" -ForegroundColor Green

# Clean up __pycache__ directories
Write-Host ""
Write-Host "Cleaning Python cache..." -ForegroundColor Cyan
Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
Write-Host "[OK] Python cache cleaned" -ForegroundColor Green

# Clean up .pyc files
Get-ChildItem -Path . -Recurse -Filter "*.pyc" | Remove-Item -Force
Write-Host "[OK] .pyc files removed" -ForegroundColor Green

Write-Host ""
Write-Host "Cleanup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Project structure is now production-ready!" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Review .env file and update production values"
Write-Host "  2. Generate SSL certificates for HTTPS (if needed)"
Write-Host "  3. Run: python start.py (for development)"
Write-Host "  4. Or use Docker: docker-compose up -d (for production)"
Write-Host ""
