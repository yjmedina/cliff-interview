# License Classification API

This project implements a FastAPI-based service that classifies software licenses into different categories using Open API.

## Technical Approach

The solution uses a combination of FastAPI for the web service and Open AI API for license classification. The system:

1. The license descriptions are classified using GPT from OpenAI. We use prompting to tell the model to return a valid category and a 150 character explanation. This process is executed individually by each license, so we will do $n$ requests where $n$ is the number of licenses. 
3. Stores results in an csv file, this could be improve into a real database with more time.
4. Provides RESTful API endpoints for querying and managing classifications

## Setup and Installation

1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with:
```
input_licenses_csv=data/licenses.csv
output_licenses_csv=data/processed_licenses.csv
open_api_key=...
```


4. Classifiy licenses:

```bash
python api/usecases.py
```

This will write the processed liceses into `output_licenses_csv`, which was set on the .env file

5. Run the application:
```bash
uvicorn api.main:app --reload
```

6. Run tests:
```bash
pytest tests -v
```

## API Endpoints

- `GET /licenses`: Get all classified licenses
- `GET /summary`: Get aggregated metrics by category
- `PUT /licenses/{id}`: Update a license classification

Since we use a .csv file as database, updating is expensive and takes $O(n)$ time.

## Future Improvements
I had problems using GROQ API due to an invalid API Key, so I changed to open AI since it was the fastest change available.

If given more time, I would:

- Change to GROQ API
- We dont need an LLM + prompting to classify, we could use zero shot classification model for free, which can be downloaded from hugginface and ran locally. Use an smaller LLM to create an explanation.
- Implement rate limiting and API key authentication
- Implement batch processing
- Create a docker image to deploy the API
- Create async endpoints, right now they are totally sync


## Scaling Strategy

1. We can improve the process of classifying licenses using message queues. And this will become available in the API once they are processed. Adding a endpoint to the API is another valid options, but we may overload the API if we reach to many requests. 
2. Use a proper database instead of csv files so adding, updating and deleting are efficient.

## Embeddings Strategy

To use embeddings instead of direct prompting:

1. Generate embeddings for all license descriptions
2. Create category embeddings for each typology
3. Use vector similarity to classify licenses
4. Implement a hybrid approach combining embeddings with LLM for explanations
5. Cache embeddings for frequently seen licenses

## Versioning Strategy

The service would be versioned using:

1. Semantic versioning for API endpoints
4. A/B testing
5. Proper documentation of breaking changes 