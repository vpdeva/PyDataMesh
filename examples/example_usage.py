import pandas as pd
from core.data_mesh import PyDataMesh

if __name__ == "__main__":
    data_mesh = PyDataMesh()

    # Create domains
    data_mesh.create_domain("Sales")
    data_mesh.create_domain("HR")

    # Add data products
    sales_data = pd.DataFrame({"order_id": [1, 2, 3], "amount": [100, 200, 300]})
    hr_data = pd.DataFrame({"employee_id": [1, 2], "name": ["Alice", "Bob"]})

    data_mesh.add_data_product("Sales", "SalesData", sales_data, metadata={"owner": "Sales Team", "description": "Sales transaction data."})
    data_mesh.add_data_product("HR", "EmployeeData", hr_data, metadata={"owner": "HR Team", "description": "Employee information."})

    # Query data products
    print(data_mesh.query_data_product("Sales", "SalesData", {"amount": 200}))

    # Add governance policy
    def mask_amount(data):
        data["amount"] = data["amount"].apply(lambda x: "MASKED" if x > 150 else x)
        return data

    data_mesh.add_governance_policy("Sales", mask_amount)

    # Get data with policies
    print(data_mesh.get_data_with_policies("Sales", "SalesData"))

    # Retrieve metadata
    print(data_mesh.get_product_metadata("Sales", "SalesData"))

    # List all registered products
    print(data_mesh.list_registered_products())