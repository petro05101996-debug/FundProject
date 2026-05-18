# Timeweb App Platform deployment notes

Use these settings for deploying the Streamlit app to Timeweb App Platform:

- Protocol: HTTP
- Port: 8501
- Healthcheck path: `/_stcore/health`
- Initial delay / start period: 120 seconds
- Timeout: 10 seconds
- Retries: 10-12

The Dockerfile intentionally does not include a Docker `HEALTHCHECK` directive for the first deployment attempt. If Timeweb still fails health checks and the platform UI cannot be configured to use `/_stcore/health`, add a Dockerfile health check in a separate commit:

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=5 CMD curl -f http://localhost:8501/_stcore/health || exit 1
```
