# PC Parts Optimization Platform

A budget-conscious PC build recommendation engine that optimizes GPU and CPU pairings based on specific user requirements, real-world benchmarks, and current market pricing.

## 🛠 Tech Stack

- **Frontend**: [React](https://react.dev/) (v18), [Vite](https://vitejs.dev/), [Tailwind CSS](https://tailwindcss.com/)
- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) (Python), [SQLAlchemy](https://www.sqlalchemy.org/) (ORM), [Pydantic](https://docs.pydantic.dev/)
- **Database**: PostgreSQL (managed via SQLAlchemy)
- **Data Processing**: Pandas (for data ingestion and cleaning)
- **Styling**: Modern dark-mode UI with glassmorphism and Material Symbols

## 📂 Project Structure

- `Backend/`: The core API service.
  - `main.py`: Application entry point and API routing.
  - `models.py` & `schemas.py`: Database models and Pydantic validation schemas.
  - `services/recommender.py`: The heuristic engine that scores hardware combinations.
  - `data_loader_*.py`: Specialized scripts for ingesting CPU/GPU price and performance data.
- `Frontend/`: The interactive user interface.
  - `app.jsx`: Main dashboard logic and state management.
  - `components/`: Modular UI components (Forms, Selectors, Result Cards).
- `testing.ipynb`: Jupyter notebook for data analysis and prototyping recommendation logic.

## ⚙️ How it Works

The platform utilizes a **rule-based heuristic engine** to find the optimal hardware balance:
1. **Parameter Input**: Users define a total budget, a specific use case (e.g., 4K Gaming, ML Compute), and an optional GPU/CPU budget split.
2. **Heuristic Scoring**: The backend applies weighted scoring to hardware specs based on the use case. For example, 4K gaming prioritizes GPU VRAM and shaders, while ML Compute emphasizes raw compute scores.
3. **Normalization**: Raw hardware metrics (PassMark scores, clock speeds, etc.) are normalized using min-max scaling to ensure fair comparison across different generations.
4. **Optimization**: The engine iterates through valid pairings, applies budget filters, and adds bonuses for "under-budget" headroom to deliver the top 3 best-value combinations.

## 🚀 Setup & Installation

### Backend
1. Navigate to the `Backend` directory.
2. Create a virtual environment: `python -m venv venv`
3. Install dependencies: `pip install -r requirements.txt`
4. Configure environment: Create a `.env` file based on `.env.example` with your `DATABASE_URL`.
5. Run the server: `uvicorn main:app --reload`

### Frontend
1. Navigate to the `Frontend` directory.
2. Install dependencies: `npm install`
3. Start the development server: `npm run dev`
4. Access the dashboard at `http://localhost:5173`.

## ✨ Features

- **Budget-Aware Recommendations**: Automatically filters hardware to fit within user-defined price limits.
- **Use-Case Optimization**: Specialized scoring for 1080p/1440p/4K Gaming, ML Workloads, and General Use.
- **Dynamic Budget Splitting**: Fine-tune the percentage of budget allocated to the GPU vs. CPU.
- **Detailed Reasoning**: Each recommendation includes a clear explanation of why that specific pairing was chosen.
- **Telemetry Dashboard**: High-tech, futuristic UI providing detailed hardware specs and performance metrics.

