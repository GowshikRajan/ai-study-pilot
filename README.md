# AI Study Pilot

## Description
AI Study Pilot is a simple web application designed for university students who want to study faster and more efficiently. It allows users to paste lecture notes or textbook content and quickly turn them into useful study materials such as summaries, flashcards, and quizzes. The goal is to help students save time and improve understanding before exams.

## Features
- Study Dashboard: A simple interface where users can enter their study content and choose a tool
- Text-to-Summary (AI-powered): Converts long text into short, clear key points
- Flashcard Generator (AI-powered): Creates question and answer flashcards from the content
- Knowledge Check Quiz (AI-powered): Generates a multiple-choice quiz based on the text

## Tech Stack
| Layer | Chosen | Justification |
|-------|--------|--------------|
| Backend | Python + FastAPI | Simple, fast, and easy to connect with APIs |
| AI/LLM | Gemini 3 Flash API | Good performance for generating summaries and quizzes |
| Database | MongoDB Atlas | Easy to store flexible data like notes and quizzes |
| CI/CD | GitHub Actions | Automates testing and building the project |
| Deployment | Render.com | Simple deployment with free hosting |

## Team Members & Roles
| Member | Role | Ownership |
|--------|------|----------|
| Gowshikrajan Senthilkumar | Backend + AI | API routes and Gemini integration |
| Reham Mohsen | Frontend | User interface and user interaction |
| Asma Benghezal | DevOps + Testing | Docker setup, CI/CD pipeline, and deployment |

## 3 Week Timeline
- Week 11 — Foundation: Set up GitHub repository, project board, database connection, app skeleton, and Docker container  
- Week 12 — Core Development & CI Pipeline: Implement core features (summary, flashcards, quiz), connect database, and set up CI pipeline with tests  
- Week 13 — CD Pipeline & Deployment: Deploy application to cloud, complete CD pipeline, test all features, and prepare presentation  
