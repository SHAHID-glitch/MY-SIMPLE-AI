#!/usr/bin/env python3
"""
Hugging Face Spaces Deployment Script
Deploy Gemini AI Assistant to HF Spaces - Cross-platform (Windows/Mac/Linux)
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def run_command(cmd, shell=False):
    """Run a shell command and return output"""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, shell=shell)
        return result.stdout.strip(), result.returncode
    except Exception as e:
        print(f"❌ Error running command: {e}")
        return "", 1

def check_git():
    """Check if Git is installed"""
    output, code = run_command("git --version")
    if code == 0:
        print("✅ Git is installed")
        return True
    else:
        print("❌ Git is not installed. Please install Git first.")
        return False

def check_hf_hub():
    """Check if HF Hub is installed"""
    try:
        from huggingface_hub import login, get_user_info
        print("✅ Hugging Face Hub is installed")
        return True
    except ImportError:
        print("❌ Installing Hugging Face Hub...")
        run_command([sys.executable, "-m", "pip", "install", "huggingface-hub", "-q"])
        print("✅ Hugging Face Hub installed")
        return True

def authenticate_hf():
    """Authenticate with Hugging Face"""
    print("\n🔐 Hugging Face Authentication")
    print("=" * 50)
    print("Get your token: https://huggingface.co/settings/tokens")
    print()
    
    try:
        from huggingface_hub import login, get_user_info
        
        print("Choose authentication method:")
        print("  1) Interactive login (opens browser)")
        print("  2) Paste token directly")
        print("  3) Use existing token from cache")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            print("\nOpening HF authentication...")
            login(add_to_git_credential=True)
            print("✅ Successfully authenticated!")
        elif choice == "2":
            token = input("Paste your HF token: ").strip()
            login(token=token, add_to_git_credential=True)
            print("✅ Successfully authenticated!")
        elif choice == "3":
            user_info = get_user_info()
            print(f"✅ Using existing token for: {user_info.user_name}")
            return user_info.user_name
        else:
            print("❌ Invalid choice")
            return None
        
        user_info = get_user_info()
        print(f"✅ Logged in as: {user_info.user_name}")
        return user_info.user_name
        
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return None

def create_space(username, space_name):
    """Create a new HF Space"""
    print(f"\n📦 Creating Space '{space_name}'...")
    
    try:
        from huggingface_hub import create_repo
        
        repo_url = create_repo(
            repo_id=space_name,
            repo_type="space",
            space_sdk="docker",
            private=False,
            exist_ok=True
        )
        print(f"✅ Space ready: {repo_url}")
        return repo_url
    except Exception as e:
        print(f"⚠️  Note: {e}")
        return f"https://huggingface.co/spaces/{username}/{space_name}"

def setup_git_repo(username, space_name):
    """Setup git repository for HF Spaces"""
    print(f"\n🔗 Setting up Git Repository...")
    
    # Initialize git if needed
    if not Path(".git").exists():
        print("  Initializing git repository...")
        run_command("git init", shell=True)
        run_command("git config user.name Deployment", shell=True)
        run_command("git config user.email deploy@example.com", shell=True)
    
    # Add HF remote
    hf_remote = f"https://huggingface.co/spaces/{username}/{space_name}"
    run_command(f"git remote remove origin", shell=True)
    run_command(f'git remote add origin "{hf_remote}"', shell=True)
    print(f"✅ Remote configured: {hf_remote}")
    return hf_remote

def prepare_deployment():
    """Prepare files for deployment"""
    print("\n📁 Preparing Files for Deployment...")
    
    # Stage all files
    run_command("git add .", shell=True)
    
    # Show status
    status, _ = run_command("git status --short", shell=True)
    if status:
        lines = status.split("\n")[:10]
        for line in lines:
            print(f"  {line}")
        if len(status.split("\n")) > 10:
            print(f"  ... and {len(status.split(chr(10))) - 10} more files")
    
    return True

def push_to_hf():
    """Push code to HF Spaces"""
    print("\n📤 Pushing to Hugging Face Spaces...")
    print("  This may take a minute...")
    
    # First pull if branch exists
    run_command("git pull origin main --allow-unrelated-histories", shell=True)
    
    # Push code
    output, code = run_command("git push -u origin main --force", shell=True)
    
    if code == 0:
        print("✅ Code pushed successfully!")
        return True
    else:
        print(f"⚠️  Push result: {output}")
        return code == 0

def main():
    """Main deployment flow"""
    os.chdir(Path(__file__).parent)
    
    print("\n" + "=" * 60)
    print("🚀 GEMINI AI ASSISTANT - HUGGING FACE SPACES DEPLOYMENT")
    print("=" * 60)
    
    # Step 1: Check prerequisites
    print("\n📋 Checking Prerequisites...")
    if not check_git():
        return False
    
    if not check_hf_hub():
        return False
    
    # Step 2: Authenticate
    username = authenticate_hf()
    if not username:
        return False
    
    # Step 3: Configure Space
    print("\n⚙️  Space Configuration")
    print("=" * 50)
    space_name = input("Enter Space name (e.g., 'gemini-ai-assistant'): ").strip()
    space_name = space_name or "gemini-ai-assistant"
    print(f"✅ Space name: {space_name}")
    
    # Step 4: Create Space
    space_url = create_space(username, space_name)
    
    # Step 5: Setup Git
    setup_git_repo(username, space_name)
    
    # Step 6: Prepare files
    prepare_deployment()
    
    # Step 7: Confirm and push
    print("\n" + "=" * 50)
    print("📊 Deployment Summary:")
    print("=" * 50)
    print(f"  Username: {username}")
    print(f"  Space Name: {space_name}")
    print(f"  Space URL: https://huggingface.co/spaces/{username}/{space_name}")
    print()
    
    confirm = input("Ready to push? (y/n): ").strip().lower()
    if confirm != "y":
        print("❌ Deployment cancelled")
        return False
    
    # Push
    if not push_to_hf():
        return False
    
    # Step 8: Post-deployment instructions
    print("\n" + "=" * 50)
    print("✅ DEPLOYMENT SUCCESSFUL!")
    print("=" * 50)
    print(f"\n🌐 Your Space URL:")
    print(f"   https://huggingface.co/spaces/{username}/{space_name}")
    
    print("\n📝 NEXT STEPS - Add Gemini API Key:")
    print("=" * 50)
    print(f"1. Open: https://huggingface.co/spaces/{username}/{space_name}/settings")
    print("2. Click 'Repository secrets'")
    print("3. Add a new secret:")
    print("   - Name: GEMINI_API_KEY")
    print("   - Value: Your Google Gemini API key")
    print("4. Get your free key: https://makersuite.google.com/app/apikey")
    
    print("\n⏳ Build Status:")
    print("   The Space will build automatically (5-10 minutes)")
    print(f"   Monitor here: https://huggingface.co/spaces/{username}/{space_name}/logs")
    
    print("\n📚 Documentation:")
    print("   See HF_SPACES_README.md for more information")
    print()
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Deployment cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
