
# Cloud File Sharing Project

This project simulates a scalable and highly available cloud file sharing system with load balancing and failover detection.

## Structure
- **Servers**: Handle file uploads and downloads.
- **Load Balancer**: Routes client requests to healthy servers.
- **Client Interface**: Simple web form to upload/download files.

## Running
```bash
docker-compose up --build
```

Access:
- Load Balancer API: http://localhost:8080
- Client UI: http://localhost:8081

file not found” during download) most likely happens because the file is uploaded to one server (say server1), but then when you try to download it, the load balancer might forward the request to another server (say server2 or server3) that doesn’t have that file. Each server has its own local uploads/ 