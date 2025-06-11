# Care Compass

## Overview
**Name:** Care Compass  
**Contributors:** Anoushka Abroal, Arthur Huang, Katherine Ahn, Shiven Ajwaliya  
**Dialogue:** Summer 2025 Data and Software in International Government and Politics in Belgium, Northeastern University  
**Objective:**
Care Compass is a data-driven web application that helps users explore and compare global healthcare systems. By combining real-world datasets with interactive visualizations and machine learning models, Care Compass makes complex international health data intuitive, customizable, and accessible.

Every country claims its healthcare system is the best—but what if you could actually compare them all in one place? Healthcare can be overwhelming and confusing, but Care Compass makes it simple. Users choose what matters most to them—like hospital quality, emergency response, or disease prevention—and receive personalized insights based on real data.

Whether you're planning to move abroad, presenting in class, or shaping the next health reform, Care Compass empowers you with visual maps, detailed country profiles, and future projections. We help people make informed decisions, not guesses—because understanding healthcare shouldn’t be reserved for experts; it should be accessible to all.

From policymakers to students and families, Care Compass adapts to diverse needs, enabling smarter decisions through data transparency and clarity.

## Project Goals   
Care Compass is designed to serve three primary user types, each with distinct needs and workflows when engaging with global healthcare data:

### Student Researchers  
Students use Care Compass to support academic research and classroom presentations on international health systems.

**Key Goals:**  
- Compare healthcare quality and outcomes across multiple countries.
- Access key indicators such as general practitioners per capita, infant mortality rate, life expectancy, and more in one place.
- Generate visualizations for use in assignments, reports, or presentations.
- Project future trends in health outcomes using time-series forecasting tools.
- Explore detailed country profiles that include not only quantitative indicators but also articles and external resources for deeper research.

### Individuals Relocating Internationally  
People planning to move abroad use Care Compass to find countries that align with their healthcare values and expectations.

**Key Goals:**  
- Customize healthcare priorities (e.g., emergency response, prevention) to receive personalized country recommendations.
- Include their current country in the matching algorithm to blend familiarity with aspirational system qualities.
- Explore visual maps and bar charts showing alignment between priorities and country performance.
- Review country profile dashboards that include general country information, healthcare-specific context, and external resources for further research.
- Identify countries with similar healthcare systems for broader relocation options.

### Policymakers and Analysts   
Public sector professionals and analysts use Care Compass to benchmark healthcare systems and inform policy decisions.

**Key Goals:**  
- Monitor how key healthcare indicators (e.g., health expenditure, life expectancy) have changed over time for specific countries using historical regression.
- Forecast future values for selected indicators at defined time points based on historical trends and region-specific data.
- Input custom target scores for health system factors and receive an estimated timeline for when those targets may be reached under current trajectory.
- Identify which indicators are improving or stagnating and use these trends to inform policy recommendations.
- Compare indicator projections across countries to prioritize evidence-based strategies and long-term planning.

## Tech Stack  

### Frontend  
- **Framework:** Streamlit 
- **State Management:** ``st.session_state`` with RBAC (Role-Based Access Control)
- **Visualization:** Plotly, Matplotlib, Seaborn 

### Backend  
- **Framework:** Flask (Python)  
- **Database:** MySQL 
- **APIs:** RESTful API design for frontend-backend communication  
- **Authentication:** Simulated roles (Relocating Resident, Global Health Student, Policymaker)

### Machine Learning
- Personalized Recommender: Cosine similarity on normalized Global Health Security Index vectors
- Forecasting Models: Time-series regression to predict future health indicator values

## Core Functionalities

### Personalized Country Recommendations  
Users can prioritize six key healthcare factors (e.g., prevention, detection, health system) using sliders. The app uses a similarity algorithm (cosine similarity) to recommend countries that best match user preferences. Users can blend preferences with their home country's profile for more personalized results.

### Country Comparison Table  
Users can select multiple countries and view a side-by-side comparison of indicators such as:
- General Practitioners per 10,000 population
- Total Health Expenditure per capita
- Impoverished Households due to out-of-pocket costs
- Infant Mortality Rate
- Life Expectancy
- Live Births per 1,000 population

### Country Profiles with Contextual Resources  
Each country page includes the national flag, a general overview of the country, healthcare-specific information, and curated external resources to support deeper research. Users also see a list of countries with similar overall healthcare scores, making it easier to explore alternatives or draw comparisons.

### Feature Trend Analysis  
Users can view how a specific indicator (e.g., life expectancy, health spending) has changed over time for a given country. This helps students and analysts evaluate historical shifts, policy effects, or crises.

### Forecasting with Regression Models  
The app supports forecasting key indicators into the future using regression models. Users can select a factor and view projected values for upcoming years.

### Target Score Simulation  
Users can enter target values for healthcare factors and receive an estimate of how long it will take a country to reach those targets based on current trends. This supports strategic planning and policy evaluation.

### Role-Based Views  
Different functionality is emphasized for different user types:
- **Students** focus on comparison tables and feature trends for academic analysis.
- **Future residents** use sliders and country profiles to explore where to move.
- **Policymakers** rely on forecasting and target-setting tools to guide reforms.


## Structure of the Repo

- The repo is organized into five main directories:
  - `./app` - the Streamlit app
  - `./api` - the Flask REST API
  - `./database-files` - SQL scripts to initialize the MySQL database
  - `./datasets` - folder for storing datasets
  - `./ml-src` - folder for storing ML models
- The repo also contains a `docker-compose.yaml` file that is used to set up the Docker containers for the front end app, the REST API, and MySQL database. This file is used to run the app and API in Docker containers.

## Prerequisites
- A GitHub Account
- A terminal-based git client or GUI Git client such as GitHub Desktop or the Git plugin for VSCode.
- VSCode with the Python Plugin
- A distribution of Python running on your laptop. The distribution supported by the course is Anaconda or Miniconda.


## Run Instructions

Anyone should be able to get Care Compass running by following these simple steps — **no code editing or ML expertise required.**

### 1. Clone the Repository
In a terminal:
```
git clone https://github.com/remainingdelta/care-compass.git
cd care-compass
```

### 2. Set Up the Environment
Inside the ``/api`` folder, copy the environment template:
```
cp .env.template .env
```

Update the ``.env`` file to look like this:
```
SECRET_KEY=someCrazyS3cR3T!Key.!
DB_USER=root
DB_HOST=db
DB_PORT=3306
DB_NAME=cc_database
MYSQL_ROOT_PASSWORD=<your-secure-password>
```
- ``DB_NAME`` should be set to ``cc_database`` (not ``northwind``)  
- Replace ``<your-secure-password>`` with a strong password of your choice

### 3. Build the Docker Containers
Next, run:
```
docker compose build
```
This ensures all services (database, API, frontend) are built correctly.

### 4. Start the App
Run the app in the background:
```
docker compose up -d
```

This will:
- Start the MySQL database
- Launch the Flask REST API
- Run the Streamlit frontend

Visit http://localhost:8501 in your browser to start using the app.


## Future Plans

- Integrate quality-of-life datasets (e.g., safety, cost of living, education) to enhance recommendations by identifying countries that align not only in healthcare but in overall living conditions relative to a user's country of origin.
- Expand and enrich country profile pages with information sourced from organizations like WHO, World Bank, and OECD to provide deeper context beyond raw metrics.
- Improve the similarity scoring algorithm by refining the cosine similarity logic
- Add authentication and saved sessions so users can bookmark comparisons, track forecast scenarios, and revisit their priority sliders over time.
- Support downloadable reports and visualizations to help users present or share findings in academic or policy settings.
- Build interactive dashboards for instructors or facilitators to use the platform in classroom simulations or group workshops.
- Introduce clustering and classification models to identify country “health system types” and allow users to explore these clusters instead of only ranked lists.