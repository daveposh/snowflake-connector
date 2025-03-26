# Snowflake Database Connector Agent with AWS KMS Integration

This project provides a secure way to connect to Snowflake using the Snowflake Database Connector Agent with AWS KMS encryption for credential management.

## Prerequisites

- Docker and Docker Compose installed
- Python 3.7 or higher
- AWS Account with KMS service enabled
- Snowflake account and credentials
- AWS IAM user with KMS permissions

## AWS Setup

1. Create a KMS key in your AWS account:
   ```bash
   aws kms create-key --description "Snowflake Connector Encryption Key"
   ```

2. Create an IAM user with the following permissions:
   ```json
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Effect": "Allow",
               "Action": [
                   "kms:Encrypt",
                   "kms:Decrypt"
               ],
               "Resource": "arn:aws:kms:region:account:key/key-id"
           }
       ]
   }
   ```

3. Generate AWS access keys for the IAM user

## Project Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd snowflake-connector
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create initial `.env` file with AWS credentials:
   ```bash
   # AWS KMS Configuration
   AWS_REGION=us-west-2
   AWS_KMS_KEY_ID=your-kms-key-id
   AWS_ACCESS_KEY_ID=your-aws-access-key
   AWS_SECRET_ACCESS_KEY=your-aws-secret-key

   # KMS Encrypted Snowflake Credentials
   KMS_ENCRYPTED_ACCOUNT=
   KMS_ENCRYPTED_USER=
   KMS_ENCRYPTED_PASSWORD=
   KMS_ENCRYPTED_ROLE=
   KMS_ENCRYPTED_WAREHOUSE=
   KMS_ENCRYPTED_DATABASE=
   KMS_ENCRYPTED_SCHEMA=
   ```

4. Set proper file permissions:
   ```bash
   chmod 600 .env
   chmod 600 config/config.yaml
   ```

## Development Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-cov black isort mypy
   ```

3. Set up pre-commit hooks:
   ```bash
   pre-commit install
   ```

4. Run tests:
   ```bash
   pytest
   ```

## Encrypting Credentials

1. Run the encryption script:
   ```bash
   python encrypt_credentials.py
   ```

2. Enter your Snowflake credentials when prompted. The script will:
   - Encrypt each credential using AWS KMS
   - Update the `.env` file with encrypted values
   - Preserve existing AWS configuration

## Running the Connector

1. Start the Snowflake Connector Agent:
   ```bash
   docker-compose up -d
   ```

2. Check the logs:
   ```bash
   docker-compose logs -f
   ```

3. Verify the connection:
   ```bash
   curl http://localhost:8080/health
   ```

## Deployment Scenarios

### Local Development
```bash
docker-compose -f docker-compose.yaml -f docker-compose.dev.yaml up -d
```

### Production Deployment
```bash
docker-compose -f docker-compose.yaml -f docker-compose.prod.yaml up -d
```

### Kubernetes Deployment
1. Create Kubernetes secrets:
   ```bash
   kubectl create secret generic snowflake-credentials \
     --from-file=.env \
     --from-file=config/config.yaml
   ```

2. Apply Kubernetes manifests:
   ```bash
   kubectl apply -f k8s/
   ```

## Configuration Files

### config.yaml
The main configuration file for the Snowflake Connector Agent. Contains:
- Global settings
- AWS KMS configuration
- Connector settings
- Query settings
- Cache settings
- Security settings
- Performance settings
- Monitoring settings

### docker-compose.yaml
Docker Compose configuration that:
- Sets up the Snowflake Connector Agent container
- Maps configuration files
- Sets up networking
- Configures environment variables

### Advanced Configuration Options

#### Query Optimization
```yaml
query:
  timeout: 300
  max_rows: 10000
  fetch_size: 1000
  retry_count: 3
  retry_delay: 5
```

#### Cache Configuration
```yaml
cache:
  enabled: true
  ttl: 300
  max_size: 1000
  eviction_policy: "LRU"
```

#### Performance Tuning
```yaml
performance:
  parallel_queries: 4
  connection_pool_size: 10
  idle_timeout: 300
  max_connections: 20
```

## Security Considerations

1. File Permissions:
   - `.env` file should have 600 permissions
   - `config.yaml` should have 600 permissions
   - Keep encryption script secure

2. AWS Security:
   - Use IAM roles instead of access keys when running in AWS
   - Regularly rotate AWS credentials
   - Use the principle of least privilege for IAM permissions
   - Enable AWS CloudTrail for audit logging
   - Use AWS Secrets Manager for additional security

3. Docker Security:
   - Run container as non-root user
   - Use read-only volumes where possible
   - Keep Docker images updated
   - Scan images for vulnerabilities
   - Use Docker secrets for sensitive data

4. Network Security:
   - Use VPC endpoints for AWS services
   - Implement network policies
   - Use TLS 1.2 or higher
   - Configure firewall rules

## Monitoring

The connector provides several monitoring endpoints:
- Health check: `http://localhost:8080/health`
- Metrics: `http://localhost:8080/metrics`
- Prometheus metrics: `http://localhost:8080/prometheus`

### Monitoring Tools Integration
- Prometheus configuration
- Grafana dashboards
- CloudWatch metrics
- AlertManager setup

## Troubleshooting

1. Check container logs:
   ```bash
   docker-compose logs -f
   ```

2. Verify AWS credentials:
   ```bash
   aws sts get-caller-identity
   ```

3. Test KMS access:
   ```bash
   aws kms list-keys
   ```

4. Common Issues:
   - Connection timeouts
   - KMS decryption failures
   - Permission issues
   - Network connectivity problems

## Support

For issues related to:
- Snowflake Connector Agent: [Snowflake Documentation](https://docs.snowflake.com/)
- AWS KMS: [AWS KMS Documentation](https://docs.aws.amazon.com/kms/)
- Docker: [Docker Documentation](https://docs.docker.com/)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 