# Git Commands to Add odooKr Repository

## ⚠️ STATUS: Repository is Empty
The odooKr repository (https://github.com/krasiklalitadmin/odooKr.git) currently contains no content.

## Current Options:

### Option 1: Add as Submodule (for future content)
```bash
# Add empty repository as submodule - will track future updates
git submodule add https://github.com/krasiklalitadmin/odooKr.git odooKr
git commit -m "Add odooKr submodule (empty)"
git push origin master
```

### Option 2: Wait and Add Later
```bash
# Check if repository has content later
git ls-remote https://github.com/krasiklalitadmin/odooKr.git

# When it has content, then use:
git subtree add --prefix=odooKr https://github.com/krasiklalitadmin/odooKr.git main --squash
```

## Method 2: Add as Git Submodule
This will reference the odooKr repository as a separate module:

```bash
# Navigate to your project root
cd d:\sagar

# Add as submodule
git submodule add https://github.com/krasiklalitadmin/odooKr.git odooKr

# Initialize and update submodule
git submodule init
git submodule update
```

## Method 3: Clone and Copy (Simple approach)
This will download and copy the content directly:

```bash
# Navigate to your project root
cd d:\sagar

# Clone the repository temporarily
git clone https://github.com/krasiklalitadmin/odooKr.git temp_odooKr

# Copy the content to your project
cp -r temp_odooKr/* ./odooKr/

# Remove the temporary clone
rm -rf temp_odooKr

# Add to your git
git add odooKr/
git commit -m "Add odooKr repository content"
```

## Method 4: Add as Remote and Merge
This will add it as a remote repository and merge:

```bash
# Navigate to your project root
cd d:\sagar

# Add as remote
git remote add odooKr https://github.com/krasiklalitadmin/odooKr.git

# Fetch the remote content
git fetch odooKr

# Create a new branch for the merge
git checkout -b integrate-odooKr

# Merge with allow-unrelated-histories
git merge odooKr/main --allow-unrelated-histories --no-edit

# If main doesn't exist, try master
git merge odooKr/master --allow-unrelated-histories --no-edit

# Checkout back to main and merge
git checkout main
git merge integrate-odooKr
```

## Recommended: Use Method 1 (Git Subtree)
Run this command from your project root:

```bash
cd d:\sagar
git subtree add --prefix=odooKr https://github.com/krasiklalitadmin/odooKr.git main --squash
```

## After Adding, Update Your Deployment
Once you've added the odooKr repository, you may want to update your deployment configuration to include any additional Odoo modules from that repository.

## Push Changes
After adding the repository using any method:

```bash
git add .
git commit -m "Integrate odooKr repository"
git push origin main
```
