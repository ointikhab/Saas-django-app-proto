# Saas-Django-App-Proto

A **SaaS-based Django application prototype** designed for scalability and ease of deployment using Docker.

## 🚀 Getting Started

### **Prerequisites**
Make sure you have the following installed:
for now i have pushed env keys as well. which can be replace later with env keys
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### **Installation & Setup**
Clone the repository:
```sh
git clone https://github.com/YOUR-USERNAME/Saas-django-app-proto.git
cd Saas-django-app-proto
```

### **Build and Run the Application**
#### 1️⃣ Build the Docker containers:
```sh
docker-compose build
```
#### 2️⃣ Start the application in detached mode:
```sh
docker-compose up -d
```

### **Managing Specific Containers**
To start or stop a specific container, use:
```sh
docker-compose up <container_name>
docker-compose down <container_name>
```

### **Running Migrations**
To apply migrations, first access the Django container:
```sh
docker-compose exec django_project bash
```
Then run:
```sh
python manage.py migrate
```

### **Stopping the Application**
To stop all running containers:
```sh
docker-compose down
```

## 📌 Notes
- Ensure the environment variables are properly configured in `.env` before starting the application.
- Logs can be checked using:
  ```sh
  docker-compose logs -f
  ```
- If facing any issues, try rebuilding the containers:
  ```sh
  docker-compose build --no-cache
  ```

## 📜 License
This project is open-source and available under the [MIT License](LICENSE).

## 💡 Contributing
Contributions are welcome! Feel free to submit a pull request.

---
Happy coding! 🚀

