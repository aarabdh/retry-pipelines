# Retry Pipelines
Simple python tool with no dependencies that can be used to retry failing pipelines in your gitlab build. Useful for flakey tests that are preventing your merge request.

### Usage:
#### First-time setup:
1. Download the run.py file (or the whole project, either works).
2. Open run.py in a text editor (any will do).
3. Use [this tutorial](https://www.merge.dev/blog/gitlab-access-token) to get your Personal Access Token for Gitlab. Make sure to use the scope "api", otherwise the retry functionality won't work.
4. Delete "PASTE_ACCESS_TOKEN_HERE" in run.py and paste your access token inside double quotes.
5. Use [this method](https://docs.gitlab.com/ee/user/project/working_with_projects.html#access-a-project-by-using-the-project-id) to get the project ID for your project.
6. Replace "PASTE_PROJECT_ID_HERE" with your project ID in run.py.
7. Replace "PASTE_URL_HERE" with your gitlab URL (this is the website you visit to access your repository).
8. Now save run.py. Your first time setup is done.

#### Retrying a pipeline:
1. Get the Pipeline ID from the Gitlab UI or URL. It is a # followed by some number. This is the pipeline that will be retried.
2. Open command prompt or powershell in the folder where run.py is saved.
3. Run `python retry_pipeline.py <pipeline_id>` after replacing `<pipeline_id>` with your Pipeline ID.
4. Now sit back and watch the magic happen. Helpful failure messages have been provided in case something is misconfigured.
