# Keep only the `main` branch (local + remote)

Run these in PowerShell from your project folder:  
`c:\Users\karamtot\claims-backend\pythonProject`

---

## 1. Local branches (this machine)

You currently have only `main`. To remove any other local branch later:

```powershell
# List local branches
git branch

# Delete a branch (example: delete 'develop')
git branch -d develop
# Force delete if it has unmerged changes
git branch -D develop
```

Do **not** delete `main`; you need at least one branch.

---

## 2. Remote branches (on GitHub)

First, update your view of the remote (run this in your terminal where you’re logged into GitHub):

```powershell
git fetch origin
git branch -a
```

- `remotes/origin/...` are the branches that exist on GitHub.
- To delete a remote branch (replace `OTHER_BRANCH` with the branch name, e.g. `develop` or `feature/xyz`):

```powershell
git push origin --delete OTHER_BRANCH
```

Example: to remove a branch named `develop` from GitHub:

```powershell
git push origin --delete develop
```

Repeat for every branch you want gone; keep only `origin/main`.

---

## 3. Optional: delete stale remote-tracking refs locally

After deleting branches on the remote, clean up your local refs so they don’t still show under `remotes/origin/...`:

```powershell
git fetch origin --prune
```

---

## Summary

- **Local:** You already have only `main`. Use `git branch -d BRANCH` to delete any extra local branch.
- **Remote (GitHub):** Use `git push origin --delete BRANCH_NAME` for each branch you want removed. Then run `git fetch origin --prune`.

Deleting a folder on your PC does **not** remove branches on GitHub; you have to delete those with the commands above (or in GitHub’s “Branches” page).
