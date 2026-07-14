# Upload this project to GitHub

Recommended repository name:

```text
ti6al4v-force-ellipsoids
```

Create an empty public repository on GitHub. Do not initialize it with an
additional README, `.gitignore`, or license because those files already exist here.

From the extracted project folder:

```bash
git init
git add .
git commit -m "Initial reproducible release"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/ti6al4v-force-ellipsoids.git
git push -u origin main
```

Then:

1. Replace `SEU-USUARIO` in `CITATION.cff`.
2. Add the repository URL to the manuscript.
3. Ask each coauthor to review the public files.
4. Create a release only after tests pass.
5. Archive the release in Zenodo to obtain a DOI.
