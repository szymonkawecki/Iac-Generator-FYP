# tabs/home.py
import tkinter as tk
import customtkinter as ctk
import os
import shutil
import re
from additional.tooltip import ToolTip

# Validation regex
SUBSCRIPTION_REGEX = re.compile(
    r'^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})$'
)
RESOURCE_GROUP_REGEX = re.compile(r'^[a-zA-Z0-9_\-]+$')  # allows letters, digits, hyphen, underscore
PREFIX_REGEX = re.compile(r'^[a-z0-9]{1,12}$')  # lowercase, max 12 chars

def create_home_tab(parent_tab):
    # Scrollable frame
    main_frame = ctk.CTkScrollableFrame(parent_tab)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Frame for base inputs
    base_frame = ctk.CTkFrame(main_frame)
    base_frame.pack(fill="x", padx=10, pady=(0,10))

    info_fields = {
        "Azure Subscription ID": "Your Azure Subscription ID (GUID format 8-4-4-4-12).",
        "Desired Azure Region": "Select the Azure region to deploy resources.",
        "Existing Resource Group Name": "Alphanumeric + hyphens, no spaces.",
        "Prefix Name": "Lowercase alphanumeric, max 12 chars."
    }

    info_vars = {}
    entries = {}

    # Mesh labels with tooltips + more
    for key, tooltip_text in info_fields.items():
        var = tk.StringVar()
        label = ctk.CTkLabel(base_frame, text=key)
        label.pack(anchor="w", padx=5, pady=(5,0))
        if key == "Desired Azure Region":
            # Dropdown for regions
            regions = [
                "eastus", "eastus2", "westus", "westus2", "centralus", "northcentralus", "southcentralus",
                "northeurope", "westeurope", "francecentral", "francesouth", "uksouth", "ukwest",
                "germanynorth", "germanywestcentral", "switzerlandnorth", "switzerlandwest",
                "norwayeast", "norwaywest", "japaneast", "japanwest", "koreacentral", "koreasouth",
                "australiaeast", "australiasoutheast", "australiasouth", "australiacentral", "australiacentral2",
                "southeastasia", "eastasia", "brazilsouth", "centralindia", "southindia", "westindia",
                "canadacentral", "canadaeast", "uaecentral", "uaenorth", "southafricanorth", "southafricawest"
            ]
            entry = ctk.CTkOptionMenu(base_frame, variable=var, values=regions)
            var.set("westeurope")
        else:
            entry = ctk.CTkEntry(base_frame, textvariable=var)
        entry.pack(fill="x", padx=5, pady=(0,5))
        entries[key] = entry
        info_vars[key] = var
        ToolTip(entry, tooltip_text)

    # Modules frame
    modules_frame = ctk.CTkFrame(main_frame)
    modules_frame.pack(fill="x", padx=10, pady=(0,10))

    # Base SIEM architecture checkbox (always included but shown separately)
    base_siem_var = tk.BooleanVar(value=True)
    base_siem_cb = ctk.CTkCheckBox(modules_frame, text="Base SIEM Architecture", variable=base_siem_var)
    base_siem_cb.pack(anchor="w", pady=(5,2))
    ToolTip(base_siem_cb, "This is the core SIEM setup, always included.")

    # Optional log collectors
    log_frame = ctk.CTkFrame(modules_frame)
    log_frame.pack(fill="x", pady=(5,2))
    ctk.CTkLabel(log_frame, text="Optional Modules:").pack(anchor="w")
    aws_cloudtrail_var = tk.BooleanVar(value=False)
    aws_cb = ctk.CTkCheckBox(log_frame, text="AWS CloudTrail", variable=aws_cloudtrail_var)
    aws_cb.pack(anchor="w", padx=10)
    ToolTip(aws_cb, "Optional log collector via AWS CloudTrail.")

    # AWS CloudTrail module input frame
    aws_frame = ctk.CTkFrame(main_frame)
    aws_frame.pack(fill="x", padx=10, pady=(0,10))
    aws_frame.pack_forget()  # hide initially

    aws_fields = {
        "AWS Access Key": "Access key for the AWS account.",
        "AWS Secret Key": "Secret key for the AWS account.",
        "S3 Bucket Name": "S3 bucket where logs will be stored.",
        "AWS Region": "Region where CloudTrail logs will be sent."
    }
    aws_vars = {}
    for key, tooltip_text in aws_fields.items():
        var = tk.StringVar()
        label = ctk.CTkLabel(aws_frame, text=key)
        label.pack(anchor="w", padx=5, pady=(5,0))
        entry = ctk.CTkEntry(aws_frame, textvariable=var)
        entry.pack(fill="x", padx=5, pady=(0,5))
        aws_vars[key] = var
        ToolTip(entry, tooltip_text)

    # Show/hide AWS inputs based on checkbox
    def toggle_aws_inputs():
        if aws_cloudtrail_var.get():
            aws_frame.pack(fill="x", padx=10, pady=(0,10))
        else:
            aws_frame.pack_forget()

    aws_cloudtrail_var.trace_add("write", lambda *args: toggle_aws_inputs())

    # Validation function
    def validate_all(*args):
        # subscription ID
        entries["Azure Subscription ID"].configure(
            fg_color="white" if SUBSCRIPTION_REGEX.match(info_vars["Azure Subscription ID"].get()) else "#ffcccc"
        )
        # resource group
        entries["Existing Resource Group Name"].configure(
            fg_color="white" if RESOURCE_GROUP_REGEX.match(info_vars["Existing Resource Group Name"].get()) else "#ffcccc"
        )
        # prefix
        entries["Prefix Name"].configure(
            fg_color="white" if PREFIX_REGEX.match(info_vars["Prefix Name"].get()) else "#ffcccc"
        )
        # enable submit if all valid
        all_valid = (
            SUBSCRIPTION_REGEX.match(info_vars["Azure Subscription ID"].get()) and
            RESOURCE_GROUP_REGEX.match(info_vars["Existing Resource Group Name"].get()) and
            PREFIX_REGEX.match(info_vars["Prefix Name"].get())
        )
        submit_button.configure(state="normal" if all_valid else "disabled")

    for var in info_vars.values():
        var.trace_add("write", validate_all)

    # Terraform 'generate' button
    submit_button = ctk.CTkButton(main_frame, text="Generate Terraform", state="disabled")
    submit_button.pack(pady=(10,10))

    # Function to generate code - built on .tftemplates
    def generate_code():
        code_dir = os.path.join(os.getcwd(), "code")
        if os.path.exists(code_dir):
            shutil.rmtree(code_dir)
        os.makedirs(code_dir)

        # Copy main template
        shutil.copy(os.path.join("templates", "main.tf.template"), os.path.join(code_dir, "main.tf"))

        # Copy AWS CloudTrail template if selected
        if aws_cloudtrail_var.get():
            shutil.copy(
                os.path.join("templates", "aws_cloudtrail.tf.template"),
                os.path.join(code_dir, "aws_cloudtrail.tf")
            )

            # Copy function_app.zip from templates/packages/
            packages_dir = os.path.join(code_dir, "packages")
            os.makedirs(packages_dir, exist_ok=True)
            shutil.copy(
                os.path.join("templates", "packages", "function_app.zip"),
                os.path.join(packages_dir, "function_app.zip")
            )
            
        # Copy variables template
        shutil.copy(os.path.join("templates", "variables.tf.template"), os.path.join(code_dir, "variables.tf"))

        # Write terraform.tfvars
        with open(os.path.join(code_dir, "terraform.tfvars"), "w") as f:
            f.write(f'subscription_id = "{info_vars["Azure Subscription ID"].get()}"\n')
            f.write(f'resource_group_name = "{info_vars["Existing Resource Group Name"].get()}"\n')
            f.write(f'location = "{info_vars["Desired Azure Region"].get()}"\n')
            f.write(f'resource_name = "{info_vars["Prefix Name"].get()}"\n')

            # Optional AWS CloudTrail variables
            if aws_cloudtrail_var.get():
                f.write(f'aws_access_key = "{aws_vars["AWS Access Key"].get()}"\n')
                f.write(f'aws_secret_key = "{aws_vars["AWS Secret Key"].get()}"\n')
                f.write(f's3_bucket = "{aws_vars["S3 Bucket Name"].get()}"\n')
                f.write(f'aws_region = "{aws_vars["AWS Region"].get()}"\n')
        
        print("[SUCCESS] Terraform code generation complete!")
        print("Please review the ./code directory for your IaC.")

    submit_button.configure(command=generate_code)
