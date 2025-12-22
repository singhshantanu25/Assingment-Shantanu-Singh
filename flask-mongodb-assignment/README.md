# Flask MongoDB Kubernetes Deployment Assignment

## Deployment Successful!

### Application Status
- Flask Application: 2 replicas (Running)
- MongoDB: 1 replica with authentication (Running)
- Horizontal Pod Autoscaler: Configured (min:2, max:5, CPU:70%)
- Services: Flask (NodePort), MongoDB (ClusterIP)
- Persistent Storage: Configured for MongoDB

### Test Results
1. Root Endpoint (GET /): WORKING
   Response: Welcome to the Flask app! The current time is: 2025-12-22 15:58:29.323662

2. Data Insertion (POST /data): WORKING
   Response: {"status":"Data inserted"}

3. Data Retrieval (GET /data): WORKING
   Response: [{"assignment":"Kubernetes","status":"completed"}]

4. HPA Status: WORKING
   Current CPU: 2%/70%

### Files Structure
flask-mongodb-assignment/
├── README.md
├── flask-app/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .dockerignore
└── kubernetes-manifests/
    ├── 01-namespace.yaml
    ├── 02-secrets.yaml
    ├── 03-pv-pvc.yaml
    ├── 04-mongo-statefulset.yaml
    ├── 05-mongo-service.yaml
    ├── 06-flask-deployment.yaml
    ├── 06-flask-deployment-fixed.yaml
    ├── 07-flask-service.yaml
    └── 08-hpa.yaml

### DNS Resolution
Services communicate using DNS names:
- Format: service-name.namespace.svc.cluster.local
- Flask connects to MongoDB: mongodb://mongo.flask-mongo-ns.svc.cluster.local:27017/
- Kubernetes CoreDNS automatically resolves these names

### Resource Management
Configured resource requests and limits:
- Requests: memory: 256Mi, cpu: 200m
- Limits: memory: 512Mi, cpu: 500m

Requests: Guaranteed resources for scheduling
Limits: Maximum resources to prevent starvation

### Design Choices
1. StatefulSet for MongoDB: Maintains stable network identity
2. ClusterIP for MongoDB: Internal access only
3. NodePort for Flask: External access for testing
4. imagePullPolicy: Never: Uses local Minikube image
5. Readiness/Liveness Probes: Health checks for Flask app

### Testing Scenarios
1. Application Functionality: All endpoints tested ✓
2. MongoDB Authentication: Credentials from Secrets ✓
3. Data Persistence: POST/GET operations working ✓
4. HPA Monitoring: CPU metrics collected ✓
5. Service Discovery: Flask to MongoDB connection working ✓

### Deployment Commands
# Build Docker image
docker build -t flask-mongo-app:latest ./flask-app

# Load into Minikube
minikube image load flask-mongo-app:latest

# Deploy Kubernetes resources
kubectl apply -f kubernetes-manifests/

### Access the Application
# Method 1: Port-forward
kubectl port-forward -n flask-mongo-ns service/flask-service 5000:5000
curl http://localhost:5000/

# Method 2: Minikube service
minikube service flask-service -n flask-mongo-ns --url

### Screenshots
1. All pods running: kubectl get all -n flask-mongo-ns
2. HPA status: kubectl get hpa -n flask-mongo-ns
3. Test results: curl outputs shown above
