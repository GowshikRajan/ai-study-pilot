# Render Deployment Configuration

This document records how the Render web service is configured for the AI Study Pilot project.

## Service Details

| Field | Value |
|---|---|
| Provider | render.com |
| Service type | Web Service (Existing Docker Image) |
| Image source | Docker Hub: `USERNAME/ai-study-pilot:latest` |
| Service name | `ai-study-pilot-STUDENT_ID` |
| Region | Oregon (US West) |
| Live URL | `https://ai-study-pilot-STUDENT_ID.onrender.com` |

## Environment Variables Set on Render

| Variable | Purpose |
|---|---|
| `GEMINI_API_KEY` | Google Gemini API key for AI features |
| `MONGO_URI` | MongoDB Atlas connection string for persistent storage |

> ⚠️ These values are NEVER committed to the repository. They live only in Render's dashboard.

## Deploy Hook

A deploy hook URL is stored as the GitHub secret `RENDER_DEPLOY_URL`.
It is called by the `deploy` job in `.github/workflows/cicd.yml` after every successful push to `main`.

## How Deployment Works

1. Developer pushes code to `main`
2. GitHub Actions runs CI (lint → test → build → smoke test)
3. GitHub Actions pushes the new image to Docker Hub (tagged `:latest` and `:<sha>`)
4. GitHub Actions calls the Render deploy hook via `curl -X POST`
5. Render pulls the new `:latest` image from Docker Hub
6. Render replaces the running container with the updated one
7. The live URL reflects the new changes within ~1–2 minutes

## Notes

- Render free-tier services spin down after 15 minutes of inactivity
- The first request after a cold start takes 30–60 seconds — this is normal
- MongoDB data persists independently of redeployments (MongoDB Atlas is cloud-hosted)