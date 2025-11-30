#!/usr/bin/env python3
"""
Test script for video analysis functionality
Run this to verify your video analysis system is working
"""

import sys
import os

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("🔍 Checking dependencies...\n")
    
    dependencies = {
        "Core": [
            ("opencv-python", "cv2"),
            ("numpy", "numpy"),
            ("librosa", "librosa"),
            ("textblob", "textblob"),
        ],
        "Advanced": [
            ("fer", "fer"),
            ("deepface", "deepface"),
            ("mediapipe", "mediapipe"),
        ]
    }
    
    results = {"Core": {}, "Advanced": {}}
    
    for category, deps in dependencies.items():
        print(f"📦 {category} Dependencies:")
        for package_name, import_name in deps:
            try:
                __import__(import_name)
                results[category][package_name] = True
                print(f"  ✅ {package_name}")
            except ImportError:
                results[category][package_name] = False
                print(f"  ❌ {package_name} - Install with: pip install {package_name}")
        print()
    
    return results

def check_video_analysis_module():
    """Check if video_analysis module loads correctly"""
    print("🎥 Checking video_analysis module...\n")
    
    try:
        from video_analysis import (
            VideoAnalyzer, 
            analyze_video_comprehensive,
            get_quick_feedback,
            FER_AVAILABLE,
            DEEPFACE_AVAILABLE,
            MEDIAPIPE_AVAILABLE
        )
        print("✅ video_analysis module loaded successfully")
        print(f"  - FER (Emotion Detection): {'✅ Available' if FER_AVAILABLE else '❌ Not available'}")
        print(f"  - DeepFace: {'✅ Available' if DEEPFACE_AVAILABLE else '❌ Not available'}")
        print(f"  - MediaPipe: {'✅ Available' if MEDIAPIPE_AVAILABLE else '❌ Not available'}")
        print()
        return True
    except Exception as e:
        print(f"❌ Failed to load video_analysis module: {e}")
        print()
        return False

def check_directories():
    """Check if required directories exist"""
    print("📁 Checking directories...\n")
    
    dirs = [
        "static/uploads",
        "static/audio",
        "templates"
    ]
    
    all_exist = True
    for dir_path in dirs:
        if os.path.exists(dir_path):
            print(f"  ✅ {dir_path}")
        else:
            print(f"  ❌ {dir_path} - Creating...")
            try:
                os.makedirs(dir_path, exist_ok=True)
                print(f"     ✅ Created {dir_path}")
            except Exception as e:
                print(f"     ❌ Failed to create: {e}")
                all_exist = False
    
    print()
    return all_exist

def test_basic_functionality():
    """Test basic video analysis functionality"""
    print("🧪 Testing basic functionality...\n")
    
    try:
        from video_analysis import VideoAnalyzer
        
        # Create analyzer instance
        analyzer = VideoAnalyzer()
        print("✅ VideoAnalyzer instance created")
        
        # Test sentiment analysis
        test_text = "I am very excited about this opportunity and confident in my abilities."
        sentiment = analyzer._analyze_sentiment(test_text)
        print(f"✅ Sentiment analysis working: {sentiment.get('label', 'unknown')}")
        
        # Test score calculations
        mock_emotions = {"summary": {"happy": {"average": 0.7}, "neutral": {"average": 0.2}}}
        mock_facial = {"eye_contact": 0.8, "smile_frequency": 0.5}
        mock_body = {"posture_score": 0.85, "stability": 0.9}
        
        confidence = analyzer._calculate_confidence_score(mock_emotions, mock_facial, mock_body)
        print(f"✅ Confidence calculation working: {confidence}/10")
        
        professionalism = analyzer._calculate_professionalism_score(mock_facial, mock_body)
        print(f"✅ Professionalism calculation working: {professionalism}/10")
        
        engagement = analyzer._calculate_engagement_score(mock_emotions, mock_facial, mock_body)
        print(f"✅ Engagement calculation working: {engagement}/10")
        
        # Test recommendations
        mock_results = {
            "confidence_score": confidence,
            "professionalism_score": professionalism,
            "engagement_score": engagement,
            "emotions": mock_emotions,
            "facial_analysis": mock_facial,
            "body_language": mock_body,
            "sentiment": sentiment
        }
        recommendations = analyzer._generate_recommendations(mock_results)
        print(f"✅ Recommendations generated: {len(recommendations)} items")
        
        print()
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        print()
        return False

def print_summary(dep_results, module_ok, dirs_ok, func_ok):
    """Print summary of test results"""
    print("=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    
    # Core dependencies
    core_ok = all(dep_results["Core"].values())
    print(f"\n{'✅' if core_ok else '❌'} Core Dependencies: {'All installed' if core_ok else 'Missing some'}")
    
    # Advanced dependencies
    advanced_count = sum(dep_results["Advanced"].values())
    total_advanced = len(dep_results["Advanced"])
    print(f"{'✅' if advanced_count == total_advanced else '⚠️'} Advanced Dependencies: {advanced_count}/{total_advanced} installed")
    
    # Module
    print(f"{'✅' if module_ok else '❌'} Video Analysis Module: {'Working' if module_ok else 'Failed'}")
    
    # Directories
    print(f"{'✅' if dirs_ok else '❌'} Directories: {'All present' if dirs_ok else 'Some missing'}")
    
    # Functionality
    print(f"{'✅' if func_ok else '❌'} Basic Functionality: {'Working' if func_ok else 'Failed'}")
    
    # Overall status
    all_ok = core_ok and module_ok and dirs_ok and func_ok
    print(f"\n{'🎉' if all_ok else '⚠️'} Overall Status: {'READY FOR USE' if all_ok else 'NEEDS ATTENTION'}")
    
    if not all_ok:
        print("\n💡 Recommendations:")
        if not core_ok:
            print("  - Install missing core dependencies: pip install -r requirements.txt")
        if advanced_count < total_advanced:
            print("  - Install advanced features: pip install fer deepface mediapipe")
        if not module_ok:
            print("  - Check video_analysis.py for errors")
        if not dirs_ok:
            print("  - Ensure proper file permissions")
        if not func_ok:
            print("  - Review error messages above")
    else:
        print("\n🚀 Your video interview system is ready!")
        print("   Start the server: python start.py")
        print("   Visit: http://localhost:8000/video_interview")
    
    print()

def main():
    """Main test function"""
    print("=" * 60)
    print("🎥 VIDEO INTERVIEW ANALYSIS - SYSTEM TEST")
    print("=" * 60)
    print()
    
    # Run all checks
    dep_results = check_dependencies()
    module_ok = check_video_analysis_module()
    dirs_ok = check_directories()
    func_ok = test_basic_functionality() if module_ok else False
    
    # Print summary
    print_summary(dep_results, module_ok, dirs_ok, func_ok)
    
    # Exit code
    all_ok = (all(dep_results["Core"].values()) and 
              module_ok and dirs_ok and func_ok)
    sys.exit(0 if all_ok else 1)

if __name__ == "__main__":
    main()
