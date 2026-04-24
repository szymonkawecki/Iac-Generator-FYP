import customtkinter as ctk

# Function to create dropdown
def create_dropdown(parent, title, content_text):

    container = ctk.CTkFrame(parent, fg_color="transparent")
    container.pack(fill="x", padx=20, pady=(10, 0))

    def toggle():
        if content_frame.winfo_ismapped():
            content_frame.pack_forget()
            button.configure(text=f"▶ {title}")
        else:
            content_frame.pack(fill="x", pady=(5, 0))
            button.configure(text=f"▼ {title}")

    # Header button
    button = ctk.CTkButton(
        container,
        text=f"▶ {title}",
        anchor="w",
        command=toggle
    )
    button.pack(fill="x")

    # Content frame
    content_frame = ctk.CTkFrame(container)

    # NORMAL (non-bold) dropdown text
    label = ctk.CTkLabel(
        content_frame,
        text=content_text,
        wraplength=640,
        justify="left",
        anchor="w",
        font=("Arial", 13, "normal")  # explicitly non-bold
    )
    label.pack(fill="x", padx=10, pady=10)


def create_information_tab(frame):

    # Header welcome information
    welcome_label = ctk.CTkLabel(
        frame,
        text=(
            "Hi. Welcome to IaC Generator v1 developed by Szymon Kawecki.\n"
            "Please read through the below information to best guide your configuration "
            "throughout."
        ),
        font=("Arial", 15),
        justify="left",
        anchor="w"
    )
    welcome_label.pack(fill="x", padx=20, pady=(20, 10))

    # Scrollable area definition
    top_frame = ctk.CTkScrollableFrame(frame)
    top_frame.pack(fill="both", expand=True)

    # Each create_dropdown() represents a dropdown
    create_dropdown(
        top_frame,
        "General Instructions",
        "This section covers general instructions for the initial input fields at the top of the Main tab."

        "\n\n1. How to retrieve your Azure Subscription ID:"
        "\n\tGo to: https://portal.azure.com"
        "\n\tIn the search bar, type Subscriptions"
        "\n\tClick Subscriptions"
        "\n\tSelect your subscription"
        "\n\tOn the overview page, you will see:"
        "\n\tSubscription ID ← this is what you need"

        "\n\n2. Desired Azure Region"
        "\nGeographic location within Microsoft’s global cloud infrastructure where Azure resources are physically deployed and operated. Designed to support data residency, compliance, disaster recovery and latency requirements."
        "\n\tTo learn more, please search 'Azure regions list'"

        "\n\n3. Existing Resource Group Name"
        "\n⚠️ Note: This can be left blank to create a whole new resource group. Otherwise, it will be automatically imported."
        "\n\tSimply input the name of your existing or desired Azure Resource Group."

        "\n\n4. Prefix Name"
        "\nMerely used as a naming convention whereby resources created will have a unique name."
        "\n\tE.g. 'showcase'"
        "\n\tThis will result in resources such as: kv-showcase (KV standing for Key Vault)"
    )

    create_dropdown(
        top_frame,
        "Base SIEM Architecture",
        "A Security Information and Event Management (SIEM) system collects logs from multiple sources, "
        "correlates events, and detects threats using rule-based and behavioural analysis. It includes ingestion, storage, "
        "correlation engine, and visual dashboards."

        "\n\nThis deploys a complete Azure-based SIEM and secure networking architecture using Infrastructure as Code (Terraform)."
        "\n"
        "\nNetworking Components:"
        "\n\t- Virtual Network (VNet) with segmented address space"
        "\n\t- Multiple Subnets (Application and Data tiers)"
        "\n\t- Network Security Group (NSG) with inbound security rules"
        "\n\t- Load Balancer with public IP and backend pool"
        "\n"
        "\nPrivate Connectivity:"
        "\n\t- Private Endpoints for secure access to services"
        "\n\t- Integration with Storage, Key Vault, Event Hub, and ADX"
        "\n\t- Private DNS Zones for internal name resolution"
        "\n\t- VNet links to enable private service communication"
        "\n"
        "\nSecurity and Access Control:"
        "\n\t- Azure Key Vault for secrets management"
        "\n\t- Role-Based Access Control (RBAC) assignments"
        "\n\t- Secure service-to-service communication"
        "\n"
        "\nLogging and SIEM:"
        "\n\t- Log Analytics Workspace for centralised logging"
        "\n\t- Microsoft Sentinel (SecurityInsights) integration"
        "\n\t- Event ingestion and monitoring pipeline"
        "\n"
        "\nData and Analytics:"
        "\n\t- Azure Data Explorer (ADX) cluster and database"
        "\n\t- Event Hub Namespace for streaming data ingestion"
        "\n"
        "\nInfrastructure Management:"
        "\n\t- Resource Group creation and management"
        "\n\t- Terraform provider configuration (AzureRM and AzAPI)"
        "\n\t- Modular and scalable infrastructure design"
        "\n"
        "\nThis architecture is designed to be secure, scalable, and suitable for enterprise-level monitoring and threat detection."
    )

    create_dropdown(
        top_frame,
        "AWS CloudTrail",
        "AWS CloudTrail records API activity and user actions across AWS accounts. "
        "It supports auditing, compliance, and security monitoring by logging all API calls and changes."

        "\n\nThis component extends the architecture by integrating AWS CloudTrail logs into Azure for centralised monitoring and analysis."
        "\n"
        "\nAWS Credential Management:"
        "\n\t- Secure storage of AWS Access Key and Secret Key in Azure Key Vault"
        "\n\t- Secrets are referenced dynamically by applications (no hardcoding)"
        "\n"
        "\nServerless Processing (Azure Function):"
        "\n\t- Linux-based Azure Function App running Python"
        "\n\t- Retrieves CloudTrail logs from AWS S3 bucket"
        "\n\t- Uses environment variables for AWS region and bucket configuration"
        "\n\t- Securely accesses credentials via Key Vault references"
        "\n"
        "\nStorage and Hosting:"
        "\n\t- Azure Storage Account for function runtime and state"
        "\n\t- Serverless consumption plan for cost-efficient execution"
        "\n\t- Application Insights for monitoring and diagnostics"
        "\n"
        "\nEvent Streaming:"
        "\n\t- Azure Event Hub used for ingesting AWS CloudTrail events"
        "\n\t- Consumer group configured for SIEM integration"
        "\n\t- Enables scalable, real-time event processing"
        "\n"
        "\nData Ingestion and Analytics:"
        "\n\t- Azure Data Explorer (ADX) table for CloudTrail logs"
        "\n\t- JSON ingestion mapping for structured data parsing"
        "\n\t- Event Hub connected directly to ADX for streaming ingestion"
        "\n"
        "\nSecurity and Access Control:"
        "\n\t- Managed Identity assigned to the Function App"
        "\n\t- Role-based access to Key Vault, Storage, and Event Hub"
        "\n\t- No credentials stored in code or configuration files"
        "\n"
        "\nNetwork and Access Rules:"
        "\n\t- Network Security Group rules allow controlled inbound AWS traffic"
        "\n\t- Load Balancer routes HTTPS traffic securely"
        "\n"
        "\nOverall Functionality:"
        "\n\t- Collects AWS CloudTrail logs"
        "\n\t- Processes and forwards them to Azure Event Hub"
        "\n\t- Streams data into ADX for querying and analysis"
        "\n\t- Enables cross-cloud security monitoring within a single SIEM solution"

        "\n\nTo set up AWS CloudTrail logging:"
        "\n\n1. Create a CloudTrail trail"
        "\n\tGo to: https://console.aws.amazon.com/cloudtrail/"
        "\n\tClick: Create trail"
        "\n\tConfigure:"
        "\n\t\t- Trail name: e.g. org-trail"
        "\n\t\t- Apply trail to all regions: ✔ (recommended)"
        "\n\t\t- Management events: Read/Write events ✔"
        "\n\tStorage configuration:"
        "\n\t\t- S3 bucket (required)"
        "\n\t\t  - Click \"Create new S3 bucket\""
        "\n\t\t  - OR select existing bucket"
        "\n\tExample bucket name: aws-cloudtrail-logs-123456789"
        "\n\tClick: Next"
        "\n\tClick: Create trail"
        "\n------------------------------------------------------------"
        "\n2. Where CloudTrail logs are stored"
        "\n\tCloudTrail logs are stored in Amazon S3."
        "\n\tDefault structure: s3://<bucket-name>/AWSLogs/<account-id>/CloudTrail/<region>/"
        "\n\tExample: s3://aws-cloudtrail-logs-123456789/AWSLogs/123456789012/CloudTrail/eu-west-1/"
        "\n\tHow to find your bucket:"
        "\n\t\tOption A (S3 Console)"
        "\n\t\t\t- Go to S3 service"
        "\n\t\t\t- Find bucket created during CloudTrail setup"
        "\n\t\t\t- Open bucket and follow folder structure"
        "\n\t\tOption B (CloudTrail Console)"
        "\n\t\t\t- Open CloudTrail"
        "\n\t\t\t- Select your trail"
        "\n\t\t\t- View \"S3 bucket name\""
        "\n------------------------------------------------------------"
        "\n3. Create Access Key + Secret Access Key"
        "\n\t⚠ Important: Use IAM user (NOT root user)"
        "\n\tSteps:"
        "\n\t\t- Go to: https://console.aws.amazon.com/iam/"
        "\n\t\t- Click Users"
        "\n\t\t- Select or create a user"
        "\n\t\t- Open Security credentials tab"
        "\n\t\t- Under Access keys, click: Create access key"
        "\n\tSelect use case:"
        "\n\t\t- CLI / application access ✔"
        "\n\tYou will receive:"
        "\n\t\t- Access Key ID"
        "\n\t\t- Secret Access Key ⚠ (shown only once)"
        "\n\t\tIMPORTANT: Save it immediately"
        "\n\t\tExample:"
        "\n\t\tAccess Key ID:     AKIAxxxxxxxxxxxx"
        "\n\t\tSecret Access Key:  xxxxxxxxxxxxxxxxxxxxx"
        "\n------------------------------------------------------------"
        "\n4. Find CloudTrail region"
        "\n\tCloudTrail can operate in:"
        "\n\t\t- Region-specific mode (e.g. eu-west-1, us-east-1)"
        "\n\t\t- Multi-region mode (recommended) → logs all regions"
        "\nHow to check region:"
        "\n\tOption A (Console)"
        "\n\t\t- Open CloudTrail"
        "\n\t\t- Select trail"
        "\n\t\t- Check \"Region\" field"
        "\n\tOption B (AWS CLI)"
        "\n\t\taws cloudtrail describe-trails"
        "\n\t\tLook for:"
        "\n\t\t'HomeRegion': 'eu-west-1'"
    )


    create_dropdown(
        top_frame,
        "Code generation and deployment",
        "After supplying all required input fields and pressing 'Generate Terraform' code will be generated within the */code directory.    "

        "\n\nTo deploy the code, navigate to the above directory and login to Microsoft using Azure CLI."
        "\n\taz login --use-device-code"

        "\n\nInitiate the Terraform directory"
        "\n\tterraform init"

        "\n\nPrepare for code deployment"
        "\n\tterraform apply"

        "\n\nThis is when Terraform will print an output in your terminal that will showcase a preview of each and every resource that it will create."
        "\n⚠️ Please read through this carefully and replace 'yes' if the resources satisfy your requirements."
        "\n⚠️ Note: If you are an importing a resource group, please make sure it says 'importing' not 'adding' or 'replacing'."
    )

    create_dropdown(
        top_frame,
        "Licensing (GPL)",
        "The GNU General Public License (GPL) is a free software license that ensures users have the freedom to use, study, modify, and distribute this software."

        "\n\nUnder the GPL:"
        "\n\t- You are free to run this program for any purpose"
        "\n\t- You may modify the source code"
        "\n\t- You may share the software with others"
        "\n\t- If you distribute modified versions, you must also release them under the GPL license"

        "\n\nThis ensures that the software and all improvements remain open and freely available to the community."

        "\n\nThis project is licensed under GPL-3.0"
    )

    # Author section
    author_frame = ctk.CTkFrame(frame, corner_radius=12)
    author_frame.pack(fill="x", padx=20, pady=20)

    author_title = ctk.CTkLabel(
        author_frame,
        text="Author Information",
        font=("Arial", 16, "bold")
    )
    author_title.pack(anchor="w", padx=15, pady=(10, 5))

    divider = ctk.CTkFrame(author_frame, height=2)
    divider.pack(fill="x", padx=15, pady=5)

    author_label = ctk.CTkLabel(
        author_frame,
        text=(
            "Szymon Kawecki\n"
            "C00286043\n"
            "South East Technological University"
        ),
        justify="left",
        anchor="w",
        font=("Arial", 13, "normal")
    )
    author_label.pack(anchor="w", padx=15, pady=(5, 15))
