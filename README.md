# template-mkdocs
MkDocs template for `sponsor-*` and `event-*` documentation repositories

## Start the Development Server
```bash
docker build -t mkdocs-dev -f Dockerfile.dev .
docker run --rm -it -v $(pwd):/opt/mkdocs -p 8000:8000 mkdocs-dev
```
