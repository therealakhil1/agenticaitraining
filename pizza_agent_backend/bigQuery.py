from google.cloud import bigquery
from typing import List, Dict, Any
# import os
from dotenv import load_dotenv

load_dotenv()

class BigQueryInterface:
    def __init__(self, project_id, dataset_id, table_id):
        """Initialize BigQuery client and set project details"""
        self.client = bigquery.Client()
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.table_id = table_id

    def get_pizza_menu(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Fetch pizza menu data from BigQuery
        Returns a dictionary with pizza menu items
        """
        try:
            query = f"""
            SELECT 
                id,
                name,
                description,
                price,
                ARRAY_AGG(size) as sizes
            FROM `{self.project_id}.{self.dataset_id}.{self.table_id}`
            GROUP BY id, name, description, price
            ORDER BY id
            """
            
            query_job = self.client.query(query)
            results = query_job.result()

            # Transform results into the expected format
            pizzas = []
            for row in results:
                pizza = {
                    "id": row.id,
                    "name": row.name,
                    "description": row.description,
                    "price": float(row.price),
                    "size": row.sizes
                }
                pizzas.append(pizza)

            return {"pizzas": pizzas}

        except Exception as e:
            print(f"Error fetching pizza menu: {str(e)}")
            raise

    def add_pizza(self, pizza_data: Dict[str, Any]) -> None:
        """
        Add a new pizza to the menu
        Args:
            pizza_data: Dictionary containing pizza details
        """
        try:
            table_ref = f"{self.project_id}.{self.dataset_id}.{self.table_id}"
            rows_to_insert = [pizza_data]
            
            errors = self.client.insert_rows_json(table_ref, rows_to_insert)
            if errors:
                raise Exception(f"Errors inserting rows: {errors}")

        except Exception as e:
            print(f"Error adding pizza: {str(e)}")
            raise

    def update_pizza(self, pizza_id: int, pizza_data: Dict[str, Any]) -> None:
        """
        Update an existing pizza in the menu
        Args:
            pizza_id: ID of the pizza to update
            pizza_data: Dictionary containing updated pizza details
        """
        try:
            query = f"""
            UPDATE `{self.project_id}.{self.dataset_id}.{self.table_id}`
            SET 
                name = @name,
                description = @description,
                price = @price,
                size = @size
            WHERE id = @id
            """
            
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("id", "INTEGER", pizza_id),
                    bigquery.ScalarQueryParameter("name", "STRING", pizza_data["name"]),
                    bigquery.ScalarQueryParameter("description", "STRING", pizza_data["description"]),
                    bigquery.ScalarQueryParameter("price", "FLOAT64", pizza_data["price"]),
                    bigquery.ArrayQueryParameter("size", "STRING", pizza_data["size"])
                ]
            )
            
            query_job = self.client.query(query, job_config=job_config)
            query_job.result()

        except Exception as e:
            print(f"Error updating pizza: {str(e)}")
            raise

    def delete_pizza(self, pizza_id: int) -> None:
        """
        Delete a pizza from the menu
        Args:
            pizza_id: ID of the pizza to delete
        """
        try:
            query = f"""
            DELETE FROM `{self.project_id}.{self.dataset_id}.{self.table_id}`
            WHERE id = @id
            """
            
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("id", "INTEGER", pizza_id)
                ]
            )
            
            query_job = self.client.query(query, job_config=job_config)
            query_job.result()

        except Exception as e:
            print(f"Error deleting pizza: {str(e)}")
            raise 