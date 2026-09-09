import subprocess
import os
import sys
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.settings import settings

def deploy_showcase():
    project_id = settings.gcp_project_id
    region = settings.gcp_region
    web_dir = Path("web")
    
    if not web_dir.exists():
        print(f"Error: {web_dir.absolute()} does not exist.")
        sys.exit(1)
        
    dockerfile_path = web_dir / "Dockerfile"
    nginx_conf_path = web_dir / "nginx.conf"
    cloudbuild_path = Path("cloudbuild.yaml")
    
    dockerfile_content = """FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY . /usr/share/nginx/html
RUN chmod -R a+rX /usr/share/nginx/html
EXPOSE 8080
"""
    
    nginx_conf_content = r"""server {
    listen 8080;
    server_name localhost;
    
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    
    include /etc/nginx/mime.types;
    types {
        text/markdown md;
        text/plain txt;
        video/mp4 mp4;
    }
    
    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
        try_files $uri $uri/ =404;
    }

    location ~* \.md$ {
        root /usr/share/nginx/html;
        default_type text/markdown;
        add_header Content-Type "text/markdown; charset=utf-8";
    }

    location ~* \.mp4$ {
        root /usr/share/nginx/html;
        default_type video/mp4;
        add_header Accept-Ranges bytes;
        add_header Access-Control-Allow-Origin *;
    }
}
"""

    image_tag = f"{region}-docker.pkg.dev/{project_id}/cloud-run-source-deploy/utilities-agents-portal:latest"

    cloudbuild_content = f"""steps:
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk:alpine'
    entrypoint: 'sh'
    args:
      - '-c'
      - 'mkdir -p web/demos && gsutil -m cp -r gs://utilities-agents-demos/* web/demos/'
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - 'build'
      - '-t'
      - '{image_tag}'
      - '-f'
      - 'web/Dockerfile'
      - 'web/'
images:
  - '{image_tag}'
timeout: '1200s'
"""

    try:
        with open(dockerfile_path, "w") as f:
            f.write(dockerfile_content)
        with open(nginx_conf_path, "w") as f:
            f.write(nginx_conf_content)
        with open(cloudbuild_path, "w") as f:
            f.write(cloudbuild_content)
            
        print("Generated temporary Dockerfile, nginx.conf, and cloudbuild.yaml.")
        
        print(f"Submitting Cloud Build for {image_tag}...")
        subprocess.run(
            ["gcloud", "builds", "submit", "--config", "cloudbuild.yaml", "."],
            check=True
        )
        
        print("Deploying to Cloud Run...")
        deploy_cmd = [
            "gcloud", "run", "deploy", "utilities-agents-portal",
            "--project", project_id,
            "--image", image_tag,
            "--region", region,
            "--port", "8080",
            "--memory", "1Gi",
            "--format", "value(status.url)"
        ]
        
        result = subprocess.run(deploy_cmd, check=True, capture_output=True, text=True)
        url = result.stdout.strip()
        
        print(f"\n✅ Deployment successful!")
        print(f"🌐 Live Cloud Run URL: {url}")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Deployment failed: {e}")
        if e.stderr:
            print(e.stderr)
        sys.exit(1)
    finally:
        if dockerfile_path.exists():
            dockerfile_path.unlink()
        if nginx_conf_path.exists():
            nginx_conf_path.unlink()
        if cloudbuild_path.exists():
            cloudbuild_path.unlink()
        print("Cleaned up temporary deployment files.")

if __name__ == "__main__":
    deploy_showcase()
