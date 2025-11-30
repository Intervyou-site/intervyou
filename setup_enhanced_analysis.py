#!/usr/bin/env python3
"""
Setup script for Enhanced Video Analysis features
Tests all dependencies and provides installation guidance
"""

import sys
import subprocess
from typing import Dict, List, Tuple

def check_package(package_name: str, import_name: str = None) -> Tuple[bool, str]:
    """Check if a package is installed and working"""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        return True, f"✅ {package_name} is installed"
    except ImportError:
        return False, f"❌ {package_name} is NOT installed"
    except Exception as e:
        return False, f"⚠️  {package_name} installed but has issues: {str(e)}"

def check_all_dependencies() -> Dict[str, bool]:
    """Check all required dependencies"""
    print("=" * 60)
    print("Enhanced Video Analysis - Dependency Check")
    print("=" * 60)
    print()
    
    dependencies = {
        "Core": [
            ("opencv-python", "cv2"),
            ("numpy", "numpy"),
            ("scipy", "scipy"),
        ],
        "Video Analysis": [
            ("fer", "fer"),
            ("deepface", "deepface"),
            ("mediapipe", "mediapipe"),
        ],
        "Audio Analysis": [
            ("librosa", "librosa"),
            ("SpeechRecognition", "speech_recognition"),
            ("soundfile", "soundfile"),
        ],
        "ML/AI": [
            ("transformers", "transformers"),
            ("torch", "torch"),
            ("textblob", "textblob"),
        ],
        "Web": [
            ("fastapi", "fastapi"),
            ("websockets", "websockets"),
        ]
    }
    
    results = {}
    missing_packages = []
    
    for category, packages in dependencies.items():
        print(f"\n{category}:")
        print("-" * 40)
        
        for package_name, import_name in packages:
            success, message = check_package(package_name, import_name)
            print(f"  {message}")
            results[package_name] = success
            
            if not success:
                missing_packages.append(package_name)
    
    print("\n" + "=" * 60)
    
    if missing_packages:
        print(f"\n⚠️  Missing {len(missing_packages)} package(s):")
        for pkg in missing_packages:
            print(f"  - {pkg}")
        print("\nTo install missing packages, run:")
        print(f"  pip install {' '.join(missing_packages)}")
        print("\nOr install all at once:")
        print("  pip install -r requirements.txt")
    else:
        print("\n✅ All dependencies are installed!")
    
    return results

def test_video_analysis():
    """Test video analysis functionality"""
    print("\n" + "=" * 60)
    print("Testing Video Analysis Modules")
    print("=" * 60)
    
    try:
        from video_analysis import VideoAnalyzer
        analyzer = VideoAnalyzer()
        print("✅ VideoAnalyzer initialized successfully")
        
        # Check which features are available
        features = []
        if analyzer.emotion_detector:
            features.append("Emotion Detection (FER)")
        if analyzer.face_mesh:
            features.append("Face Mesh (MediaPipe)")
        if analyzer.pose:
            features.append("Pose Detection (MediaPipe)")
        
        if features:
            print(f"✅ Available features: {', '.join(features)}")
        else:
            print("⚠️  No advanced features available (install fer, mediapipe)")
        
        return True
    except Exception as e:
        print(f"❌ VideoAnalyzer test failed: {e}")
        return False

def test_realtime_analysis():
    """Test real-time analysis functionality"""
    print("\n" + "=" * 60)
    print("Testing Real-Time Analysis")
    print("=" * 60)
    
    try:
        from realtime_analysis import RealtimeAnalyzer
        analyzer = RealtimeAnalyzer()
        print("✅ RealtimeAnalyzer initialized successfully")
        
        # Test with a dummy frame
        import numpy as np
        dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        result = analyzer.analyze_frame(dummy_frame)
        
        if result and "metrics" in result:
            print("✅ Frame analysis working")
        else:
            print("⚠️  Frame analysis returned unexpected result")
        
        return True
    except Exception as e:
        print(f"❌ RealtimeAnalyzer test failed: {e}")
        return False

def test_audio_extraction():
    """Test audio extraction capability"""
    print("\n" + "=" * 60)
    print("Testing Audio Extraction")
    print("=" * 60)
    
    try:
        import moviepy.editor as mp
        print("✅ MoviePy is available for audio extraction")
        return True
    except Exception as e:
        print(f"⚠️  MoviePy not available: {e}")
        print("   Audio extraction may not work")
        return False

def print_feature_summary():
    """Print summary of available features"""
    print("\n" + "=" * 60)
    print("Feature Availability Summary")
    print("=" * 60)
    
    features = {
        "✅ Basic Video Analysis": True,
        "👁️ Advanced Eye Tracking": False,
        "😊 Emotion Detection": False,
        "🎤 Voice Analysis": False,
        "🔍 Micro-expressions": False,
        "⚡ Real-time Feedback": False,
    }
    
    try:
        import mediapipe
        features["👁️ Advanced Eye Tracking"] = True
    except:
        pass
    
    try:
        import fer
        features["😊 Emotion Detection"] = True
    except:
        pass
    
    try:
        import librosa
        features["🎤 Voice Analysis"] = True
    except:
        pass
    
    try:
        import deepface
        features["🔍 Micro-expressions"] = True
    except:
        pass
    
    try:
        import websockets
        features["⚡ Real-time Feedback"] = True
    except:
        pass
    
    print()
    for feature, available in features.items():
        status = "Available" if available else "Not Available"
        print(f"  {feature}: {status}")
    
    print()

def main():
    """Main setup and test function"""
    print("\n🚀 Enhanced Video Analysis Setup\n")
    
    # Check dependencies
    results = check_all_dependencies()
    
    # Test modules
    video_ok = test_video_analysis()
    realtime_ok = test_realtime_analysis()
    audio_ok = test_audio_extraction()
    
    # Print feature summary
    print_feature_summary()
    
    # Final recommendations
    print("=" * 60)
    print("Recommendations")
    print("=" * 60)
    print()
    
    if all(results.values()):
        print("✅ All systems ready! You can use all enhanced features.")
        print("\nTo start the server:")
        print("  python start.py")
        print("\nThen visit:")
        print("  http://localhost:8000/video_interview")
    else:
        print("⚠️  Some features are not available.")
        print("\nFor full functionality, install missing packages:")
        print("  pip install -r requirements.txt")
        print("\nCritical packages for enhanced features:")
        print("  pip install fer deepface mediapipe SpeechRecognition")
    
    print("\n📚 Documentation:")
    print("  See ENHANCED_VIDEO_ANALYSIS.md for detailed information")
    print()

if __name__ == "__main__":
    main()
