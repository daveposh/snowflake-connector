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
   git clone https://github.com/daveposh/snowflake-connector.git
   cd snowflake-connector
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create initial `.env` file with AWS credentials:
   ```bash
   # AWS KMS Configuration
   AWS_REGION=us-east-1
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

## AWS Cost Considerations

1. **AWS KMS Costs**
   - **Regional Pricing (as of 2024)**
     - US East (N. Virginia): $0.03 per 10,000 API requests
     - US West (Oregon): $0.03 per 10,000 API requests
     - EU (Ireland): €0.025 per 10,000 API requests
     - Asia Pacific (Tokyo): ¥3.30 per 10,000 API requests
     - Monthly key cost varies by region
     - Data transfer costs between regions
   
   - **Cost Components**
     - Key storage: $1.00 per month per key
     - API requests: $0.03 per 10,000 requests
     - Data transfer: Varies by region and volume
     - CloudWatch metrics: Included in KMS costs
     - KMS key rotation: No additional cost

2. **Cost Optimization Strategies**
   - **Request Optimization**
     - Implement request batching for multiple operations
     - Cache frequently used keys
     - Use key aliases to reduce key count
     - Optimize API call frequency
     - Implement exponential backoff for retries
   
   - **Resource Management**
     - Clean up unused keys regularly
     - Use key aliases for better organization
     - Implement key lifecycle policies
     - Monitor key usage patterns
     - Archive inactive keys
   
   - **Performance Optimization**
     - Use regional endpoints for reduced latency
     - Implement connection pooling
     - Cache key material when possible
     - Use appropriate key types for workload
     - Monitor and optimize request patterns

3. **Cost Comparison with Alternatives**
   - **AWS KMS vs. Self-Managed**
     - Self-managed: Higher operational costs
     - Self-managed: Requires dedicated infrastructure
     - Self-managed: Higher security risks
     - Self-managed: More complex maintenance
   
   - **AWS KMS vs. Other Cloud Providers**
     - Azure Key Vault: Similar pricing model
     - Google Cloud KMS: Competitive pricing
     - HashiCorp Vault: Self-hosted option
     - Comparison of features and limitations
   
   - **Total Cost of Ownership**
     - Infrastructure costs
     - Operational costs
     - Security costs
     - Compliance costs
     - Maintenance costs

4. **Budget Planning**
   - **Cost Estimation**
     - Calculate expected API calls
     - Estimate key count
     - Factor in data transfer
     - Consider growth projections
     - Account for regional costs
   
   - **Budget Controls**
     - Set up AWS Budgets
     - Configure CloudWatch alarms
     - Implement cost allocation tags
     - Regular cost reviews
     - Automated cost optimization
   
   - **Reserved Capacity**
     - Evaluate commitment options
     - Calculate potential savings
     - Consider usage patterns
     - Plan for capacity changes
     - Monitor utilization

5. **Cost Monitoring and Allocation**
   - **Monitoring Tools**
     - AWS Cost Explorer
     - CloudWatch metrics
     - Cost and Usage Report
     - Budget alerts
     - Custom dashboards
   
   - **Cost Allocation**
     - Resource tagging strategy
     - Cost center mapping
     - Project-based allocation
     - Environment-based tracking
     - Department chargeback
   
   - **Reporting and Analysis**
     - Monthly cost reports
     - Usage pattern analysis
     - Cost trend analysis
     - Optimization recommendations
     - ROI calculations
   
   - **Chargeback Strategy**
     - Define cost allocation rules
     - Set up billing reports
     - Implement showback/chargeback
     - Track resource ownership
     - Monitor cost distribution

6. **Deployment Cost Scenarios**
   - **Development Environment**
     - Estimated monthly cost: $5-10
     - 1 KMS key
     - ~1,000 API calls/day
     - Minimal data transfer
     - Cost optimization: Use shared keys
   
   - **Staging Environment**
     - Estimated monthly cost: $15-25
     - 2 KMS keys
     - ~5,000 API calls/day
     - Moderate data transfer
     - Cost optimization: Implement caching
   
   - **Production Environment**
     - Estimated monthly cost: $50-100
     - 3-5 KMS keys
     - ~20,000 API calls/day
     - High data transfer
     - Cost optimization: Reserved capacity
   
   - **Multi-Region Deployment**
     - Estimated monthly cost: $150-300
     - 5-10 KMS keys
     - ~50,000 API calls/day
     - Cross-region data transfer
     - Cost optimization: Regional endpoints

7. **Cost Optimization Case Studies**
   - **Case Study 1: High-Frequency API Calls**
     - Initial cost: $200/month
     - Problem: Excessive API calls
     - Solution: Implemented request batching
     - Result: 60% cost reduction
     - Implementation:
       ```yaml
       cache:
         enabled: true
         ttl: 300
         max_size: 1000
         batch_size: 10
       ```
   
   - **Case Study 2: Multi-Environment Setup**
     - Initial cost: $500/month
     - Problem: Redundant key usage
     - Solution: Key sharing and aliases
     - Result: 40% cost reduction
     - Implementation:
       ```yaml
       kms:
         key_aliases:
           - name: "shared-key"
             environments: ["dev", "staging"]
           - name: "prod-key"
             environments: ["prod"]
       ```
   
   - **Case Study 3: Cross-Region Deployment**
     - Initial cost: $800/month
     - Problem: High data transfer costs
     - Solution: Regional endpoints and caching
     - Result: 45% cost reduction
     - Implementation:
       ```yaml
       endpoints:
         primary: "kms.us-east-1.amazonaws.com"
         secondary: "kms.eu-west-2.amazonaws.com"
       cache:
         cross_region: true
         replication: "async"
       ```

8. **Detailed Chargeback Implementation**
   - **Resource Tagging Strategy**
     ```yaml
     tags:
       - key: "Environment"
         values: ["dev", "staging", "prod"]
       - key: "Department"
         values: ["engineering", "finance", "operations"]
       - key: "Project"
         values: ["snowflake-connector", "data-pipeline"]
       - key: "CostCenter"
         values: ["CC001", "CC002", "CC003"]
     ```
   
   - **Cost Allocation Rules**
     ```yaml
     allocation:
       rules:
         - name: "Environment Split"
           type: "percentage"
           values:
             dev: 10%
             staging: 20%
             prod: 70%
         - name: "Department Split"
           type: "usage"
           metrics:
             - api_calls
             - data_transfer
             - storage
     ```
   
   - **Billing Report Configuration**
     ```yaml
     billing:
       report:
         format: "csv"
         frequency: "monthly"
         include:
           - resource_ids
           - usage_types
           - cost_centers
           - tags
         exclude:
           - internal_services
           - shared_resources
     ```
   
   - **Showback Dashboard**
     ```yaml
     dashboard:
       metrics:
         - name: "Monthly Cost"
           type: "line"
           aggregation: "sum"
         - name: "API Usage"
           type: "bar"
           aggregation: "count"
         - name: "Cost by Department"
           type: "pie"
           dimension: "Department"
       alerts:
         - threshold: 1000
           metric: "daily_cost"
           action: "notify"
     ```

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