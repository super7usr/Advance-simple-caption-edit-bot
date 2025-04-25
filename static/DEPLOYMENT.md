# Deploying Telegram Caption Bot UI to Cloudflare Pages

This guide provides step-by-step instructions for deploying the static web interface of the Telegram Caption Bot to Cloudflare Pages.

## Prerequisites

1. A Cloudflare account (free tier is sufficient)
2. A Git repository containing the static files (optional, but recommended)

## Deployment Options

### Option 1: Direct Upload (Easiest)

1. **Log in to Cloudflare Dashboard**
   - Go to [Cloudflare Dashboard](https://dash.cloudflare.com)
   - Sign in with your account

2. **Navigate to Pages**
   - Click on "Pages" in the left sidebar

3. **Create a New Project**
   - Click "Create a project"
   - Select "Upload assets"

4. **Upload Files**
   - Enter a project name (e.g., "telegram-caption-bot")
   - Drag and drop the contents of the `static` directory from this repository
   - Click "Deploy site"

5. **Access Your Site**
   - Once deployment is complete, your site will be available at:
   - `https://[your-project-name].pages.dev`

### Option 2: GitHub Integration (Recommended for Ongoing Updates)

1. **Prepare Your Repository**
   - Create a new GitHub repository
   - Push the contents of the `static` directory to this repository
   - Make sure all files are in the root of the repository (not inside a subdirectory)

2. **Log in to Cloudflare Dashboard**
   - Go to [Cloudflare Dashboard](https://dash.cloudflare.com)
   - Sign in with your account

3. **Navigate to Pages**
   - Click on "Pages" in the left sidebar

4. **Create a New Project**
   - Click "Create a project"
   - Select "Connect to Git"

5. **Connect to GitHub**
   - Follow the prompts to connect to your GitHub account
   - Select the repository containing your static files

6. **Configure Build Settings**
   - Set your production branch (usually `main` or `master`)
   - **Build command**: Leave empty, as this is a static site
   - **Build output directory**: Leave empty (or `.` if required)
   - Click "Save and Deploy"

7. **Access Your Site**
   - Once deployment is complete, your site will be available at:
   - `https://[your-project-name].pages.dev`

## Custom Domain (Optional)

1. **Add a Custom Domain**
   - In your project's dashboard, click on "Custom domains"
   - Click "Set up a custom domain"
   - Enter your domain name and follow the verification process

2. **Update DNS Settings**
   - Follow Cloudflare's instructions to update your DNS settings
   - This typically involves adding CNAME records

## Updating Your Site

### For Direct Upload
- Go to your Pages project
- Click "Manage deployment"
- Upload new files as needed

### For GitHub Integration
- Push changes to your connected GitHub repository
- Cloudflare will automatically deploy the changes

## Important Files

The static site includes several important configuration files:

- `_redirects`: Defines URL redirect rules
- `_headers`: Sets security headers for the site
- `robots.txt`: Provides instructions for search engine crawlers
- `sitemap.xml`: Helps search engines discover your pages

## Troubleshooting

If you encounter issues with your deployment:

1. **Check Build Logs**
   - In your project dashboard, examine the build logs for errors

2. **Verify File Structure**
   - Make sure all HTML files are in the correct location
   - Confirm that paths to assets (CSS, images) are correct

3. **Test Locally**
   - Before deploying, test the site by opening the HTML files locally in a browser

4. **Contact Support**
   - If issues persist, contact Cloudflare support or refer to their documentation

## Maintenance

For optimal performance:

- Periodically update content to reflect any changes in the bot functionality
- Test all links and features regularly
- Keep your GitHub repository (if used) synced with local changes