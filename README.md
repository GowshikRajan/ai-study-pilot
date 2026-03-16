# AI Study Pilot

## Description
**AI Study Pilot** is a streamlined educational tool designed for students who need to transform dense academic material into actionable study aids quickly. Users can paste lecture notes or textbook excerpts into the application, and the system leverages the Gemini 3 Flash API to generate concise summaries, active-recall flashcards, and interactive quizzes.

## Features
- **Study Dashboard:** A centralized interface for inputting source text and selecting study tools.

- **Text-to-Summary (AI):** Condenses long-form notes into bulleted key takeaways using AI.

- **Flashcard Generator (AI):** Automatically extracts core concepts and transforms them into Question/Answer pairs.

- **Knowledge Check Quiz (AI):** Generates a 10-question multiple-choice quiz based strictly on the provided text.

## Tech Stack
| Layer | Chosen | Justification |
| --------------- | --------------- | --------------- |
| Backend | Python + FastAPI | Native `async` support; critical for handling AI API calls in non-blocking manner. |
| AI/LLM | Gemini 3 Flash API | Best balance of speed and reasoning for text-based summarization. |
| Database | MongoDB Atlas | Cloud-native NoSQL service that allows for flexible schema with generous free tier. |
| CI/CD | GitHub Actions | Automates the Test-Build-Deploy workflow. |
| Deployment | Render.com | Easy-to-manage environments and generous free tier. |


## Team Members & Roles
| Member | Role |
| -------------- | --------------- |
| Gowshikrajan Senthilkumar | Backend/API |
| Reham Mohsen | Frontend/UI |
| Rabiya Ishaq | DevOps/Testing |


## 3 Week Timeline
- Week 11 — Foundation 
- Week 12 — Core Development & CI Pipeline 
- Week 13 — CD Pipeline & Deployment
