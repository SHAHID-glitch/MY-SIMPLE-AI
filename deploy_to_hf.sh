#!/bin/bash
# Hugging Face Spaces Deployment Guide
# Deploy Gemini AI Assistant to HF Spaces

echo "🚀 Hugging Face Spaces Deployment Setup"
echo "========================================"
echo ""

# Step 1: Check Git
echo "Step 1: Checking Git..."
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install git first."
    exit 1
fi
echo "✅ Git is installed"
echo ""

# Step 2: Check HF Hub
echo "Step 2: Checking Hugging Face Hub..."
python3 -c "from huggingface_hub import login, create_repo, Repository; print('✅ Hugging Face Hub is ready')" 2>/dev/null || {
    echo "❌ Installing Hugging Face Hub..."
    pip install huggingface-hub -q
}
echo ""

# Step 3: Authentication
echo "Step 3: Hugging Face Authentication"
echo "======================================"
echo "You need a Hugging Face account token."
echo "Get your token from: https://huggingface.co/settings/tokens"
echo ""
echo "Choose your authentication method:"
echo "  1) Automatic (interactive login)"
echo "  2) Manual (paste token directly)"
echo ""
read -p "Enter choice (1 or 2): " auth_choice

if [ "$auth_choice" = "1" ]; then
    echo ""
    echo "Opening HF authentication..."
    python3 << 'EOF'
from huggingface_hub import login, get_token
try:
    login()
    token = get_token()
    print(f"\n✅ Successfully authenticated!")
    print(f"Token saved to ~/.cache/huggingface/token")
except Exception as e:
    print(f"❌ Authentication failed: {e}")
    exit(1)
EOF
elif [ "$auth_choice" = "2" ]; then
    read -sp "Enter your HF token: " token
    echo ""
    python3 << EOF
from huggingface_hub import login
try:
    login(token="$token", add_to_git_credential=True)
    print("✅ Successfully authenticated!")
except Exception as e:
    print(f"❌ Authentication failed: {e}")
    exit(1)
EOF
else
    echo "❌ Invalid choice"
    exit 1
fi
echo ""

# Step 4: Get user info
echo "Step 4: Getting your HF username..."
HF_USERNAME=$(python3 -c "from huggingface_hub import get_user_info; print(get_user_info().user_name)" 2>/dev/null)
if [ -z "$HF_USERNAME" ]; then
    read -p "Enter your Hugging Face username: " HF_USERNAME
fi
echo "✅ Username: $HF_USERNAME"
echo ""

# Step 5: Space name
echo "Step 5: Space Configuration"
read -p "Enter Space name (e.g., 'gemini-ai-assistant'): " SPACE_NAME
SPACE_NAME=${SPACE_NAME:-gemini-ai-assistant}
echo "✅ Space name: $SPACE_NAME"
echo ""

# Step 6: Create/get Space URL
SPACE_URL="https://huggingface.co/spaces/$HF_USERNAME/$SPACE_NAME"
echo "Step 6: Space Repository"
echo "========================="
echo "Space URL: $SPACE_URL"
echo ""

# Step 7: Initialize git repo if needed
if [ ! -d ".git" ]; then
    echo "Step 7a: Initializing Git repository..."
    git init
    git config user.name "Deployment Script"
    git config user.email "deploy@example.com"
    echo "✅ Git initialized"
    echo ""
fi

# Step 8: Create HF Space repository
echo "Step 8: Creating Space Repository..."
python3 << EOF
from huggingface_hub import create_repo

try:
    repo_url = create_repo(
        repo_id="$SPACE_NAME",
        repo_type="space",
        space_sdk="docker",
        private=False,
        exist_ok=True
    )
    print(f"✅ Space created/found: {repo_url}")
except Exception as e:
    print(f"⚠️  Note: {e}")
    print("Space may already exist or there was an issue.")
EOF
echo ""

# Step 9: Add HF remote
echo "Step 9: Adding Hugging Face Remote..."
HF_REMOTE="https://huggingface.co/spaces/$HF_USERNAME/$SPACE_NAME"
git remote remove origin 2>/dev/null
git remote add origin "$HF_REMOTE"
echo "✅ Remote added: $HF_REMOTE"
echo ""

# Step 10: Stage and push
echo "Step 10: Preparing Files for Deployment..."
echo "==========================================="
git add .
git status
echo ""

read -p "Ready to push? (y/n): " confirm
if [ "$confirm" = "y" ]; then
    echo ""
    echo "Pushing to Hugging Face Spaces..."
    git push -u origin main --force 2>&1 | head -20
    echo ""
    echo "✅ Deployment started!"
    echo ""
    echo "📊 Space URL: $SPACE_URL"
    echo ""
    echo "Next steps:"
    echo "1. Go to: $SPACE_URL/settings"
    echo "2. Add Repository Secret:"
    echo "   - Name: GEMINI_API_KEY"
    echo "   - Value: Your Google Gemini API key"
    echo "   Get it from: https://makersuite.google.com/app/apikey"
    echo ""
    echo "3. Space will rebuild automatically (5-10 minutes)"
    echo "4. Access your app at: $SPACE_URL"
else
    echo "❌ Deployment cancelled"
fi
echo ""
echo "📚 Documentation: See HF_SPACES_README.md for more info"
