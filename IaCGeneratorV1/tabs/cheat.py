import customtkinter as ctk


def create_cheat_tab(parent_tab):

    # Scrollable frame (kept for overall page scrolling)
    scrollable_frame = ctk.CTkScrollableFrame(parent_tab)
    scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Make columns expand evenly
    scrollable_frame.grid_columnconfigure(0, weight=1)
    scrollable_frame.grid_columnconfigure(1, weight=1)
    scrollable_frame.grid_columnconfigure(2, weight=1)

    # Table header
    headers = ["Field", "Valid Example", "Invalid Example"]

    for col, text in enumerate(headers):
        lbl = ctk.CTkLabel(
            scrollable_frame,
            text=text,
            font=("Arial", 12, "bold")
        )
        lbl.grid(row=0, column=col, padx=10, pady=8, sticky="nsew")

    # Input data fields
    fields = [
        {
            "name": "Azure Subscription ID",
            "valid": "11111111-2222-3333-4444-555555555555",
            "invalid": "11111-abc-333"
        },
        {
            "name": "Resource Group Name",
            "valid": "myResourceGroup-01",
            "invalid": "My Resource Group!"
        },
        {
            "name": "Prefix Name",
            "valid": "myapp01",
            "invalid": "My App 01!"
        },
        {
            "name": "Azure Region",
            "valid": "westeurope",
            "invalid": "West Europe"
        },

        # AWS
        {
            "name": "AWS Access Key ID",
            "valid": "AKIAIOSFODNN7EXAMPLE",
            "invalid": "123-abc-key"
        },
        {
            "name": "AWS Secret Access Key",
            "valid": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
            "invalid": "secret123"
        },
        {
            "name": "S3 Bucket Name",
            "valid": "aws-cloudtrail-logs-123456789",
            "invalid": "My Bucket!"
        },
        {
            "name": "AWS Region",
            "valid": "eu-west-1",
            "invalid": "EU West 1"
        }
    ]

    # Table rows
    for row, field in enumerate(fields, start=1):
        for col, key in enumerate(["name", "valid", "invalid"]):

            cell_frame = ctk.CTkFrame(
                scrollable_frame,
                corner_radius=6
            )
            cell_frame.grid(
                row=row,
                column=col,
                padx=8,
                pady=4,
                sticky="nsew"
            )

            label = ctk.CTkLabel(
                cell_frame,
                text=field[key],
                justify="left",
                anchor="w",
                wraplength=220,
                font=("Arial", 12)
            )
            label.pack(fill="both", expand=True, padx=8, pady=6)
