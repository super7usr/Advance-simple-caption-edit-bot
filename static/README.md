# Telegram Caption Bot - Web Interface

This folder contains a static web interface for the Telegram Caption Bot. These files are specifically designed to be deployed on Cloudflare Pages, providing a publicly accessible interface for the bot.

## Deployment Instructions

### Deploying to Cloudflare Pages

1. **Sign in to Cloudflare**
   - Go to the Cloudflare dashboard and sign in to your account.

2. **Access Pages**
   - Navigate to the "Pages" section from the dashboard.

3. **Create a New Project**
   - Click "Create a new project".
   - Choose "Connect to Git" and select your repository.

4. **Configure Build Settings**
   - Set your production branch (usually `main` or `master`).
   - **Build command**: Leave empty, as this is a static site.
   - **Build output directory**: `static` (or the directory where these files are located).

5. **Save and Deploy**
   - Click "Save and Deploy" to start the deployment process.

6. **Access Your Site**
   - Once deployed, your site will be available at `[project-name].pages.dev`.

### Updating the Site

To update the site:
1. Make changes to the HTML files in this directory.
2. Push your changes to the connected Git repository.
3. Cloudflare Pages will automatically deploy the updated site.

## Files Overview

- `index.html` - The main landing page
- `status.html` - Server status information
- `commands.html` - Bot commands reference
- `_redirects` - Cloudflare Pages redirect rules
- `_headers` - Security headers for Cloudflare Pages

## Contact

For any issues or questions, contact the bot administrator via Telegram at @Elizabeth_Olsen_robot.