# AI-Powered Group Travel Planner 🌍✈️

An intelligent travel planning system that helps groups plan trips efficiently by considering budget, interests, schedules, preferred destinations, weather, transport, and accommodation preferences.

## 🎯 Project Overview

This project aims to reduce conflicts in group decisions and automatically generate optimized itineraries using AI algorithms. It combines recommendation systems, NLP, optimization algorithms, and clustering techniques to create personalized travel experiences for groups.

### Key Problems Solved
- **Group Preference Conflicts**: AI matches diverse preferences and finds optimal solutions
- **Budget Optimization**: Smart allocation of resources across accommodation, transport, and activities
- **Time Management**: Efficient scheduling considering weather, traffic, and attraction hours
- **Personalization**: Tailored recommendations based on individual traveler profiles

## ✨ Features

### Core Features
- 🤖 **AI-Generated Personalized Itineraries**: Machine learning-based trip planning
- 👥 **Group Preference Matching**: Consensus-based decision making
- 💰 **Budget Optimization**: Smart cost allocation and expense splitting
- 🎯 **Smart Destination Recommendations**: Content and collaborative filtering
- 🌤️ **Weather-Aware Planning**: Real-time weather integration
- 🏨 **Hotel & Transport Suggestions**: Price comparison and ranking
- 💸 **Expense Splitting**: Fair cost distribution among group members
- 💬 **Chatbot-Based Travel Assistant**: NLP-powered conversational interface
- 🗺️ **Interactive Map Integration**: Visual trip planning

## 🏗️ Project Architecture

```
┌────────────────────────────────────────────────────────┐
│          React.js Frontend                            │
│  (Dashboard, Itinerary, Chat Interface)               │
└────────────────────────────────┬──────────────────────┘
                     │
        ┌────────────────────────────┬──────────────┐
        │                            │              │
┌───────▼────────────┐  ┌──────────▼────────┐  ┌──▼──────────────┐
│   REST API         │  │  WebSocket        │  │  External APIs  │
│   (FastAPI)        │  │  (Real-time)      │  │  (Google Maps)  │
└───────┬────────────┘  └──────────┬────────┘  └──┬──────────────┘
        │                         │             │
├───────┴─────────────────────────┴─────────────┤
│    Core Backend Services                      │
├──────────────────────────────────────────────┤
│ • Recommendation Engine                      │
│ • Itinerary Optimizer                        │
│ • Budget Calculator                          │
│ • NLP Chatbot                                │
│ • Group Consensus Algorithm                  │
└───────┬──────────────┬────────────┬──────────┘
        │              │            │
┌───────▼────┐ ┌──────▼─────┐ ┌───▼──────────┐
│ Database   │ │ ML Models  │ │ External     │
│(MongoDB/   │ │(TensorFlow)│ │ APIs         │
│ MySQL)     │ │            │ │ (Google Maps)│
└────────────┘ └────────────┘ └──────────────┘
```

## 📁 Project Structure

```
AI-Group-Travel-Planner/
├── backend/
│   ├── app.py                    # Main FastAPI application
│   ├── requirements.txt          # Python dependencies
│   ├── config.py                 # Configuration settings
│   ├── .env.example              # Environment variables template
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py               # User authentication
│   │   ├── trips.py              # Trip management
│   │   ├── recommendations.py    # Recommendation engine
│   │   ├── itinerary.py          # Itinerary generation
│   │   ├── chatbot.py            # Chatbot endpoints
│   │   └── budget.py             # Budget management
│   ├── models/
│   │   ├── __init__.py
│   │   ├── db_models.py          # SQLAlchemy/Mongoose models
│   │   ├── schemas.py            # Pydantic schemas
│   │   └── recommendation_model.py # ML model classes
│   ├── services/
│   │   ├── __init__.py
│   │   ├── recommendation_service.py
│   │   ├── itinerary_service.py
│   │   ├── budget_service.py
│   │   ├── nlp_service.py
│   │   ├── api_service.py        # External API calls
│   │   └── group_consensus_service.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── auth_utils.py
│   │   ├── validation.py
│   │   ├── constants.py
│   │   └── helpers.py
│   └── database/
│       ├── __init__.py
│       └── connection.py
├── ml_training/
│   ├── notebooks/
│   │   ├── 01_data_exploration.ipynb
│   │   ├── 02_data_preprocessing.ipynb
│   │   ├── 03_recommendation_model.ipynb
│   │   ├── 04_nlp_training.ipynb
│   │   ├── 05_clustering.ipynb
│   │   └── 06_model_evaluation.ipynb
│   ├── data/
│   │   ├── raw/
│   │   ├── processed/
│   │   └── datasets.md
│   └── scripts/
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── styles/
│   │   └── App.js
│   ├── package.json
│   └── .env.example
├── docker/
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   └── docker-compose.yml
├── .github/
│   └── workflows/
│       ├── python-tests.yml
│       └── deploy.yml
├── tests/
│   ├── unit/
│   ├── integration/
│   └── conftest.py
├── docs/
│   ├── API_DOCUMENTATION.md
│   ├── ML_MODEL_DETAILS.md
│   ├── DEPLOYMENT.md
│   ├── ARCHITECTURE.md
│   └── SETUP_GUIDE.md
├── .gitignore
├── .env.example
├── docker-compose.yml
├── LICENSE
└── CONTRIBUTING.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 14+
- MongoDB or MySQL
- Git

### Backend Setup

```bash
# Clone the repository
git clone https://github.com/PuskarDas/AI-Group-Travel-Planner.git
cd AI-Group-Travel-Planner/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Update .env with your API keys

# Run the server
uvicorn app:app --reload
```

The API will be available at `http://localhost:8000`

### Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env
# Update with your API endpoint

# Start development server
npm start
```

The frontend will be available at `http://localhost:3000`

### Using Docker

```bash
# From project root
docker-compose up --build
```

## 📊 Models & Algorithms

### 1. **Recommendation Engine**
- **Approach**: Hybrid recommendation (Content-based + Collaborative Filtering)
- **Algorithm**: Matrix Factorization (SVD) with TensorFlow
- **Input**: User preferences, travel history, budget, interests
- **Output**: Ranked destination and activity suggestions

### 2. **Itinerary Optimization**
- **Approach**: Constraint Satisfaction Problem (CSP) + Genetic Algorithm
- **Constraints**: Time windows, weather, budget, group preferences
- **Output**: Optimized day-by-day itinerary

### 3. **NLP Chatbot**
- **Model**: Fine-tuned BERT for travel domain
- **Framework**: Hugging Face Transformers
- **Capabilities**: User preference understanding, Q&A, recommendations

### 4. **Group Consensus**
- **Algorithm**: Preference Aggregation (Borda Count + Weighted Scoring)
- **Goal**: Maximize group satisfaction while respecting individual preferences

### 5. **Budget Optimizer**
- **Approach**: Linear Programming (scipy.optimize.linprog)
- **Goal**: Optimal cost allocation across trip components

## 🔧 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout

### Trips
- `GET /api/trips` - Get user's trips
- `POST /api/trips` - Create new trip
- `GET /api/trips/{trip_id}` - Get trip details
- `PUT /api/trips/{trip_id}` - Update trip
- `DELETE /api/trips/{trip_id}` - Delete trip
- `POST /api/trips/{trip_id}/members` - Add group member

### Recommendations
- `POST /api/recommendations/destinations` - Get destination recommendations
- `POST /api/recommendations/activities` - Get activity recommendations
- `POST /api/recommendations/accommodations` - Get hotel recommendations

### Itinerary
- `POST /api/itinerary/generate` - Generate AI itinerary
- `GET /api/itinerary/{trip_id}` - Get itinerary
- `PUT /api/itinerary/{trip_id}` - Update itinerary

### Budget
- `GET /api/budget/{trip_id}` - Get budget details
- `POST /api/budget/{trip_id}/split` - Calculate expense split
- `POST /api/budget/{trip_id}/add-expense` - Add expense

### Chatbot
- `POST /api/chat/message` - Send message to chatbot
- `GET /api/chat/history/{trip_id}` - Get chat history

## 🤖 ML Model Details

See [ML_MODEL_DETAILS.md](docs/ML_MODEL_DETAILS.md) for comprehensive information about:
- Model architectures
- Training procedures
- Performance metrics
- Hyperparameter tuning

## 📚 Documentation

- [API Documentation](docs/API_DOCUMENTATION.md)
- [Architecture Design](docs/ARCHITECTURE.md)
- [Setup Guide](docs/SETUP_GUIDE.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [ML Model Details](docs/ML_MODEL_DETAILS.md)

## 🧪 Testing

```bash
# Run unit tests
pytest tests/unit -v

# Run integration tests
pytest tests/integration -v

# Run all tests with coverage
pytest --cov=backend tests/
```

## 📈 Performance Metrics

- **Recommendation Accuracy**: RMSE, MAE, Hit Rate
- **Itinerary Optimization**: Constraint satisfaction rate, user satisfaction
- **API Response Time**: <200ms for most endpoints
- **Model Inference Time**: <100ms for real-time recommendations

## 🔐 Security Features

- JWT-based authentication
- Input validation and sanitization
- Rate limiting
- CORS configuration
- Environment variable management
- SQL injection prevention
- XSS protection

## 🌐 External APIs Used

1. **Google Maps API**
   - Distance Matrix
   - Directions
   - Places
   - Maps Embedding

2. **OpenWeather API**
   - Current weather
   - 5-day forecast
   - Historical data

3. **OpenTripMap API**
   - Points of interest
   - Attraction details
   - Ratings and reviews

4. **Skyscanner/Flight APIs**
   - Flight search
   - Price comparison

5. **Hotel APIs**
   - Room availability
   - Price comparison
   - Booking integration

## 🚀 Deployment

The project can be deployed on:
- AWS (EC2, ECS, Lambda)
- Google Cloud Platform
- Azure
- Heroku
- DigitalOcean

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed instructions.

## 📊 Dataset Information

Datasets used in this project:
- Kaggle Travel Datasets: [Link](https://www.kaggle.com/datasets)
- OpenTripMap API: [Link](https://opentripmap.com/)
- Public hotel reviews datasets
- Flight price datasets

See [datasets.md](ml_training/data/datasets.md) for detailed information.

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💼 Author

**Puskar Das**
- GitHub: [@PuskarDas](https://github.com/PuskarDas)
- Email: puskar@example.com

## 🙏 Acknowledgments

- TensorFlow and PyTorch communities
- FastAPI documentation
- React.js ecosystem
- Open source contributors

## 📞 Support

For issues, questions, or suggestions:
1. Open an issue on GitHub
2. Check existing documentation
3. Contact the author

---

**⭐ If you find this project helpful, please consider giving it a star!**
