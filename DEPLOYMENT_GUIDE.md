# Streamlit Cloud Deployment Guide

## For Streamlit Cloud Deployment

When deploying to Streamlit Cloud, you need to:

1. **Create a requirements.txt file** in your repository root with these exact contents:
```
streamlit>=1.28.0
numpy>=1.24.0
pandas>=2.0.0
plotly>=5.15.0
scipy>=1.10.0
```

2. **File Structure** - Ensure your repository has this structure:
```
your-repo/
├── app.py
├── requirements.txt
├── models/
│   ├── pricing.py
│   ├── advertising.py
│   ├── scheduling.py
│   ├── profit.py
│   └── seasonality.py
└── utils/
    └── visualizations.py
```

3. **Deploy Steps**:
   - Push your code to GitHub
   - Go to https://share.streamlit.io/
   - Connect your GitHub repository
   - Select app.py as the main file
   - Streamlit Cloud will automatically install dependencies from requirements.txt

## Quick Fix for Your Current Error

The plotly import error you're seeing is because Streamlit Cloud needs a requirements.txt file. Here's what to do:

1. **Copy the contents of `deployment_requirements.txt`** (in this repository) 
2. **Create a new file called `requirements.txt`** in your GitHub repository root
3. **Paste the requirements** into that file
4. **Push to GitHub** and redeploy

## Alternative: Copy deployment_requirements.txt

If you can't create requirements.txt, rename `deployment_requirements.txt` to `requirements.txt` in your deployment repository.

## Error Handling Features

The app now includes:
- ✅ Better error messages for missing dependencies
- ✅ Graceful handling of import failures
- ✅ Clear instructions for fixing issues
- ✅ Robust fallback mechanisms

## Common Issues:

- **Module not found errors**: Make sure requirements.txt is in the root directory
- **Import errors**: Ensure all model files are in the correct directory structure
- **Version conflicts**: Use the exact versions specified above
- **Path issues**: Ensure your GitHub repo has the same folder structure as shown above

## Local Testing

Before deploying, test locally with:
```bash
streamlit run app.py
```

## Support

If you continue to have issues:
1. Check that requirements.txt is in your GitHub repository root
2. Verify all model files are present in the correct directories
3. Ensure you're using the latest version of your code on GitHub