import time
from bs4 import BeautifulSoup
from pyquery import PyQuery
from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(1, 5)
    
    def on_start(self):
        # Access the login page to get the CSRF token
        response = self.client.get("/login/")
        
        # Extract the CSRF token from the HTML response
        # soup = BeautifulSoup(response.content, "html.parser")
        # csrf_token = soup.find("input", {"name": "csrfmiddlewaretoken"})["value"]
        
        csrf_token = response.cookies['csrftoken']

        # Save the CSRF token to be used in subsequent requests
        self.client.headers.update({'X-CSRFToken': csrf_token})
        
        # Perform the login request with the extracted CSRF token
        login_data = {
            "username": "Jenny22",
            "password": "Dragon_Ball",
            "csrfmiddlewaretoken": csrf_token,
        }
        
        self.client.post("/login/", data=login_data)
        
        if response.status_code == 200:
            print("Login successful")
        else:
            print("Login failed")
    
    @task
    def home(self):
        self.client.get("/")

    @task
    def view_project(self):
        #Lista de project_ids para simular diferentes proyectos
        project_ids = [1,2, 3]

        for project_id in project_ids:
            # Acceder al project_view URL con un  project_id especifico
            response = self.client.get(f"/project/view/{project_id}")
            
            # # Extraer CSRF token
            # soup = BeautifulSoup(response.content, "html.parser")
            # csrf_token = soup.find("input", {"name": "csrfmiddlewaretoken"})["value"]

            # Incluir CSRF token en cada request
            # self.client.headers.update({"X-CSRFToken": csrf_token})

    @task(3)
    def getTasks(self):
        #Lista de project_ids para simular diferentes proyectos
        tasks_ids = [1, 2, 3]
        
        for task_id in tasks_ids:
            response = self.client.get(f"get_task_details/{task_id}/", name="Project tasks")
            
            # # Extraer CSRF token
            # soup = BeautifulSoup(response.content, "html.parser")
            # csrf_token = soup.find("input", {"name": "csrfmiddlewaretoken"})["value"]

            # # Incluir CSRF token en cada request
            # self.client.headers.update({"X-CSRFToken": csrf_token})
    
    # @task
    # def update_task(self):
    #     # Asumir un project_id y un task_id 
    #     project_id = 4  # Remplazar con el project_id a utilizar 
    #     task_id = 4     # Remplazar con el task_id a utilizar

    #     update_data = {
    #         "id": task_id,
    #         "nombre": "new_value1",
    #         "descripcion": "new_value2",
    #         "project__id": project_id,
    #         # Add other fields as needed
    #     }

    #     response= self.client.post(
    #         f"update_task_details/{project_id}/{task_id}",
    #         data=update_data,)

    #     # Get CSRF token from the response header
    #     csrf_token = response.headers.get('X-CSRFToken', '')

    #     # Include CSRF token in the headers for subsequent requests
    #     self.client.headers.update({'X-CSRFToken': csrf_token})

    #     # Check if the update was successful (you might need to adjust this based on your application's response)
    #     if response.status_code == 200:
    #         print(f"Task {task_id} updated successfully")
    #     else:
    #         print(f"Failed to update task {task_id}. Status code: {response.status_code}, Response: {response.text}")