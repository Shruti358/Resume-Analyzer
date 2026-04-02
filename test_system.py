"""
Test Script for Resume Analyzer
Validates the system is working correctly
"""

import sys
import json
from pathlib import Path


def test_imports():
    """Test if all required modules can be imported"""
    print("=" * 60)
    print("TESTING MODULE IMPORTS")
    print("=" * 60)
    
    modules_to_test = [
        ("streamlit", "Streamlit"),
        ("pandas", "Pandas"),
        ("plotly", "Plotly"),
        ("PyPDF2", "PyPDF2"),
        ("docx", "python-docx"),
    ]
    
    failed = []
    
    for module, name in modules_to_test:
        try:
            __import__(module)
            print(f"✅ {name:<20} - OK")
        except ImportError as e:
            print(f"❌ {name:<20} - FAILED: {str(e)}")
            failed.append(name)
    
    print()
    
    if failed:
        print(f"⚠️  Missing modules: {', '.join(failed)}")
        print("\nInstall missing modules with:")
        print(f"pip install -r requirements_modern.txt")
        return False
    
    print("✅ All dependencies installed!")
    return True


def test_custom_modules():
    """Test if custom modules can be imported"""
    print("=" * 60)
    print("TESTING CUSTOM MODULES")
    print("=" * 60)
    
    try:
        from resume_parser import ResumeParser
        print("✅ resume_parser.py      - OK")
    except Exception as e:
        print(f"❌ resume_parser.py      - FAILED: {str(e)}")
        return False
    
    try:
        from skill_analyzer import SkillAnalyzer, ResumeAnalyzer
        print("✅ skill_analyzer.py     - OK")
    except Exception as e:
        print(f"❌ skill_analyzer.py     - FAILED: {str(e)}")
        return False
    
    try:
        from resume_api import ResumeAnalysisAPI
        print("✅ resume_api.py         - OK")
    except Exception as e:
        print(f"❌ resume_api.py         - FAILED: {str(e)}")
        return False
    
    try:
        import app
        print("✅ app.py                - OK")
    except Exception as e:
        print(f"❌ app.py                - FAILED: {str(e)}")
        # This is expected if dependencies aren't installed
        return False
    
    print()
    print("✅ All custom modules loaded successfully!")
    return True


def test_skill_analyzer():
    """Test skill analyzer functionality"""
    print("=" * 60)
    print("TESTING SKILL ANALYZER")
    print("=" * 60)
    
    try:
        from skill_analyzer import SkillAnalyzer
        
        # Test skill extraction from text
        job_text = "We need a Python developer with React, AWS, and Docker experience"
        skills = SkillAnalyzer.extract_skills_from_text(job_text)
        
        print(f"Job description: {job_text}")
        print(f"Detected skills: {skills}")
        
        if "python" in [s.lower() for s in skills]:
            print("✅ Skill detection working")
        else:
            print("⚠️  Skill detection might need improvement")
        
        # Test learning resources
        resource = SkillAnalyzer.get_learning_resources("Python")
        if resource and "youtube" in resource:
            print("✅ Learning resources available")
        else:
            print("❌ Learning resources not found")
            return False
        
        print()
        print("✅ Skill analyzer tests passed!")
        return True
    
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False


def test_resume_parser():
    """Test resume parser initialization"""
    print("=" * 60)
    print("TESTING RESUME PARSER")
    print("=" * 60)
    
    try:
        from resume_parser import ResumeParser
        
        parser = ResumeParser()
        
        # Test skill database
        if len(parser.ALL_SKILLS) > 0:
            print(f"✅ Skill database loaded: {len(parser.ALL_SKILLS)} skills")
        else:
            print("❌ Skill database empty")
            return False
        
        # Show sample skills
        print(f"\nSample skills: {parser.ALL_SKILLS[:10]}")
        
        print()
        print("✅ Resume parser tests passed!")
        return True
    
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False


def test_file_structure():
    """Test if all required files exist"""
    print("=" * 60)
    print("TESTING FILE STRUCTURE")
    print("=" * 60)
    
    required_files = [
        "app.py",
        "resume_parser.py",
        "skill_analyzer.py",
        "resume_api.py",
        "config.json",
        "requirements_modern.txt",
    ]
    
    all_exist = True
    
    for filename in required_files:
        filepath = Path(filename)
        if filepath.exists():
            size = filepath.stat().st_size
            print(f"✅ {filename:<30} - OK ({size:,} bytes)")
        else:
            print(f"❌ {filename:<30} - NOT FOUND")
            all_exist = False
    
    # Check directories
    dirs_to_check = [
        ("Uploaded_Resumes", "Resume upload directory"),
    ]
    
    print()
    
    for dirname, description in dirs_to_check:
        dirpath = Path(dirname)
        if dirpath.exists():
            print(f"✅ {dirname:<30} - OK ({description})")
        else:
            print(f"⚠️  {dirname:<30} - NOT FOUND (will be created on upload)")
    
    print()
    
    if all_exist:
        print("✅ All required files present!")
    else:
        print("❌ Some files are missing")
    
    return all_exist


def test_example_analysis():
    """Test analysis with sample data"""
    print("=" * 60)
    print("TESTING SAMPLE ANALYSIS")
    print("=" * 60)
    
    try:
        from resume_parser import ResumeParser
        from skill_analyzer import ResumeAnalyzer, SkillAnalyzer
        
        print("Testing skill matching...")
        
        resume_skills = ["Python", "JavaScript", "React"]
        job_skills = ["Python", "TypeScript", "React", "Node.js"]
        
        matched, missing, extra, percentage = SkillAnalyzer.match_skills(
            resume_skills, job_skills
        )
        
        print(f"Resume skills: {resume_skills}")
        print(f"Job skills: {job_skills}")
        print(f"\nMatched: {matched}")
        print(f"Missing: {missing}")
        print(f"Extra: {extra}")
        print(f"Match %: {percentage}%")
        
        if matched and missing and percentage > 0:
            print("\n✅ Analysis test passed!")
            return True
        else:
            print("\n❌ Analysis test failed!")
            return False
    
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n")
    print("🔍 RESUME ANALYZER - SYSTEM TEST SUITE")
    print("=" * 60)
    print()
    
    results = []
    
    # Run tests
    results.append(("File Structure", test_file_structure()))
    results.append(("Module Imports", test_imports()))
    
    # Only continue with more tests if basic imports passed
    if results[-1][1]:
        results.append(("Custom Modules", test_custom_modules()))
        results.append(("Resume Parser", test_resume_parser()))
        results.append(("Skill Analyzer", test_skill_analyzer()))
        results.append(("Sample Analysis", test_example_analysis()))
    
    # Summary
    print()
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{name:<25} {status}")
    
    print()
    print(f"Total: {passed}/{total} tests passed")
    
    print()
    
    if passed == total:
        print("🎉 All tests passed! Ready to run:")
        print("   streamlit run app.py")
        return 0
    else:
        print("⚠️  Some tests failed. Please fix issues and try again.")
        print("\nTo install dependencies:")
        print("   pip install -r requirements_modern.txt")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
