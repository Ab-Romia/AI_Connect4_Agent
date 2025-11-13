# 🚀 Hugging Face Deployment Guide

This guide will help you deploy the Connect 4 AI game to Hugging Face Spaces.

## 📋 Prerequisites

- A Hugging Face account (free at https://huggingface.co)
- Git installed on your local machine
- This repository cloned locally

## 🎯 Quick Deployment (Recommended)

### Option 1: Upload via Hugging Face Web Interface

1. **Create a New Space**
   - Go to https://huggingface.co/spaces
   - Click "Create new Space"
   - Choose a name (e.g., "connect4-ai")
   - Select **Gradio** as the SDK
   - Choose your license (MIT recommended)
   - Click "Create Space"

2. **Upload Files**
   - Click on "Files and versions" tab
   - Upload these files from your local repository:
     - `app.py` (main application file)
     - `Board.py` (game logic)
     - `MiniMax.py` (AI engine)
     - `requirements.txt` (dependencies)
     - `README_HF.md` (rename to `README.md` when uploading)

3. **Wait for Build**
   - Hugging Face will automatically build your Space
   - This usually takes 2-5 minutes
   - Once complete, your app will be live!

### Option 2: Deploy via Git (Advanced)

1. **Create a New Space on Hugging Face**
   - Go to https://huggingface.co/spaces
   - Click "Create new Space"
   - Choose a name and select **Gradio** SDK
   - Clone the Space repository:
   ```bash
   git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
   cd YOUR_SPACE_NAME
   ```

2. **Copy Files**
   ```bash
   # Copy necessary files from this repository
   cp /path/to/AI_Connect4_Agent/app.py .
   cp /path/to/AI_Connect4_Agent/Board.py .
   cp /path/to/AI_Connect4_Agent/MiniMax.py .
   cp /path/to/AI_Connect4_Agent/requirements.txt .
   cp /path/to/AI_Connect4_Agent/README_HF.md ./README.md
   ```

3. **Commit and Push**
   ```bash
   git add .
   git commit -m "Deploy Connect 4 AI to Hugging Face"
   git push
   ```

4. **Wait for Deployment**
   - Hugging Face will automatically build and deploy your Space
   - Visit your Space URL to see it live!

## 📁 Required Files for Deployment

Make sure these files are included:

- ✅ `app.py` - Main Gradio application
- ✅ `Board.py` - Game board logic with bitboard implementation
- ✅ `MiniMax.py` - AI engine with minimax algorithm
- ✅ `requirements.txt` - Python dependencies (gradio, pillow, numpy)
- ✅ `README.md` - Space description (use README_HF.md)

## 🔧 Configuration

### README.md Front Matter

Your README.md should start with this YAML front matter:

```yaml
---
title: Connect 4 AI - Minimax Algorithm
emoji: 🎮
colorFrom: blue
colorTo: red
sdk: gradio
sdk_version: 4.0.0
app_file: app.py
pinned: false
license: mit
---
```

### requirements.txt

Ensure your requirements.txt contains:

```txt
gradio>=4.0.0
Pillow>=9.0.0
numpy>=1.21.0
```

## 🧪 Testing Locally Before Deployment

Before deploying, test the app locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Visit `http://localhost:7860` to test the interface.

## 🎨 Customization Options

### Change App Title and Appearance
Edit the metadata in `README.md`:
- `title`: Your Space's display name
- `emoji`: Icon shown next to title
- `colorFrom` and `colorTo`: Gradient colors for the Space card

### Adjust AI Performance
In `app.py`, modify the difficulty settings:
```python
difficulty_map = {
    "Easy": 2,
    "Medium": 4,
    "Hard": 6,
    # Add more levels...
}
```

### Customize Colors
In `app.py`, edit the `COLORS` dictionary:
```python
COLORS = {
    'board': (0, 116, 217),      # Blue
    'player1': (255, 65, 54),    # Red
    'player2': (255, 220, 0),    # Yellow
    # etc...
}
```

## 🐛 Troubleshooting

### Build Fails
- **Check requirements.txt**: Ensure all dependencies are specified
- **Python version**: Hugging Face uses Python 3.10+ by default
- **File names**: Make sure `app.py` is exactly named (case-sensitive)

### App Loads but Crashes
- **Check imports**: Ensure all local imports (Board, MiniMax) are present
- **Test locally first**: Run `python app.py` to catch errors
- **Check logs**: View build logs in the "Logs" tab of your Space

### Slow Performance
- **Default to Medium difficulty**: Higher difficulties (Expert, Insane) are slow
- **Optimize evaluation**: Consider reducing search depth for web deployment
- **Add loading messages**: Inform users that AI is thinking

### UI Issues
- **Browser compatibility**: Test in Chrome, Firefox, and Safari
- **Mobile responsiveness**: Gradio handles this automatically
- **Image display**: Ensure PIL images are created correctly

## 📊 Space Configuration

### Making Your Space Public
- By default, Spaces are public
- You can make it private in Space settings
- Free tier allows unlimited public Spaces

### Hardware Options
- **Free**: CPU-only, sufficient for this app
- **Upgraded**: GPU available for paid accounts (not needed for this app)
- Medium difficulty works well on free tier

### Analytics
- Hugging Face provides built-in analytics
- View visitor count and usage statistics
- Available in Space settings

## 🌟 Sharing Your Space

Once deployed, share your Space:
- **Direct URL**: `https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME`
- **Embed**: Use the embed code for your website
- **Social Media**: Share the link on Twitter, LinkedIn, etc.

## 🔄 Updating Your Space

To update your deployed app:

1. **Via Web Interface**:
   - Go to "Files and versions"
   - Upload updated files
   - Space rebuilds automatically

2. **Via Git**:
   ```bash
   git pull  # Get latest changes
   # Make your modifications
   git add .
   git commit -m "Update: description of changes"
   git push
   ```

## 📝 Best Practices

1. **Test Locally First**: Always test changes before pushing
2. **Use Meaningful Commit Messages**: Help track changes over time
3. **Monitor Performance**: Check Space logs for errors
4. **Document Changes**: Update README with new features
5. **Set Reasonable Defaults**: Start with Medium difficulty
6. **Provide Clear Instructions**: Help users understand the game

## 🎓 Learn More

- **Gradio Documentation**: https://gradio.app/docs
- **Hugging Face Spaces**: https://huggingface.co/docs/hub/spaces
- **Space Examples**: https://huggingface.co/spaces

## 💡 Pro Tips

1. **Add Examples**: Gradio allows pre-filled examples for users
2. **Enable Queueing**: For high traffic, enable queue in `demo.launch()`
3. **Add Analytics**: Track game statistics and display them
4. **Create Variants**: Make different Spaces with different themes
5. **Collect Feedback**: Add a feedback form for users

## 📞 Support

If you encounter issues:
1. Check Hugging Face Spaces documentation
2. Visit the Gradio Discord community
3. Open an issue on GitHub
4. Contact Hugging Face support

---

## ✅ Deployment Checklist

Before deploying, ensure:
- [ ] All required files are present
- [ ] requirements.txt is correct
- [ ] README.md has proper front matter
- [ ] App works locally (`python app.py`)
- [ ] No hardcoded paths or secrets
- [ ] Default settings are user-friendly
- [ ] Instructions are clear
- [ ] License is specified

---

<div align="center">

**Ready to deploy? Let's make Connect 4 AI available to the world! 🚀**

Good luck with your deployment! 🎮🤖

</div>
