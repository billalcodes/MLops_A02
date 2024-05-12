# Automated Data Extraction and Transformation with Apache Airflow

This repository contains code and documentation for automating data extraction, transformation, and version-controlled storage using Apache Airflow. The project focuses on extracting data from two sources, dawn.com and BBC.com, transforming it, and storing it in a version-controlled manner.

## Project Structure

- **data_extraction.py**: Python script for extracting links from dawn.com and BBC.com and saving them in CSV files (`dawn_links.csv` and `bbc_links.csv`).
- **data_transformation.py**: Python script for extracting titles and descriptions from links, applying retry strategies, and saving transformed data in new CSV files (`dawn_links_transformed.csv` and `bbc_links_transformed.csv`).
- **data_extraction_transformation_dag.py**: Apache Airflow DAG for automating data extraction and transformation tasks, ensuring task dependencies and error handling.

## Usage

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/username/data-extraction-transformation.git
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the data extraction and transformation scripts:

   ```bash
   python data_extraction.py
   python data_transformation.py
   ```

4. Start Apache Airflow webserver:

   ```bash
   airflow webserver
   ```

5. Access the Airflow UI in your browser (`http://localhost:8080`) to view and trigger the DAG (`data_extraction_transformation_dag`).

## Dependencies

- Python 3.x
- Apache Airflow
- requests
- BeautifulSoup

## Additional Notes

- Ensure proper configuration of Apache Airflow, including database setup and DAG configuration.
- Customize retry strategies, timeouts, and error handling as per project requirements.
- Update paths and filenames in scripts and DAG according to your environment.
