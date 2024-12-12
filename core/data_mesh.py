import pandas as pd
import json

class DataDomain:
    def __init__(self, name):
        self.name = name
        self.data_products = {}

    def add_data_product(self, name, data):
        if name in self.data_products:
            raise ValueError(f"Data product '{name}' already exists in domain '{self.name}'.")
        self.data_products[name] = DataProduct(name, data)

    def get_data_product(self, name):
        if name not in self.data_products:
            raise ValueError(f"Data product '{name}' not found in domain '{self.name}'.")
        return self.data_products[name]

class DataProduct:
    def __init__(self, name, data):
        self.name = name
        self.data = data  # Assuming data is a Pandas DataFrame

    def query(self, filters=None):
        if not filters:
            return self.data
        filtered_data = self.data
        for column, value in filters.items():
            filtered_data = filtered_data[filtered_data[column] == value]
        return filtered_data

    def to_json(self):
        return self.data.to_json()

class UnityCatalog:
    def __init__(self):
        self.catalog = {}

    def register_product(self, domain_name, product_name, metadata):
        key = f"{domain_name}.{product_name}"
        if key in self.catalog:
            raise ValueError(f"Product '{key}' is already registered in the catalog.")
        self.catalog[key] = metadata

    def get_product_metadata(self, domain_name, product_name):
        key = f"{domain_name}.{product_name}"
        if key not in self.catalog:
            raise ValueError(f"Product '{key}' is not found in the catalog.")
        return self.catalog[key]

    def list_products(self):
        return self.catalog

class DataPlatform:
    def __init__(self):
        self.domains = {}

    def add_domain(self, domain):
        if domain.name in self.domains:
            raise ValueError(f"Domain '{domain.name}' already exists.")
        self.domains[domain.name] = domain

    def get_domain(self, name):
        if name not in self.domains:
            raise ValueError(f"Domain '{name}' not found.")
        return self.domains[name]

class FederatedGovernance:
    def __init__(self):
        self.policies = {}

    def add_policy(self, domain_name, policy):
        if domain_name not in self.policies:
            self.policies[domain_name] = []
        self.policies[domain_name].append(policy)

    def enforce_policies(self, domain_name, data):
        if domain_name not in self.policies:
            return data
        for policy in self.policies[domain_name]:
            data = policy(data)
        return data

# Library API
class PyDataMesh:
    def __init__(self):
        self.platform = DataPlatform()
        self.governance = FederatedGovernance()
        self.catalog = UnityCatalog()

    def create_domain(self, domain_name):
        domain = DataDomain(domain_name)
        self.platform.add_domain(domain)

    def add_data_product(self, domain_name, product_name, data, metadata=None):
        domain = self.platform.get_domain(domain_name)
        domain.add_data_product(product_name, data)
        if metadata:
            self.catalog.register_product(domain_name, product_name, metadata)

    def query_data_product(self, domain_name, product_name, filters=None):
        domain = self.platform.get_domain(domain_name)
        data_product = domain.get_data_product(product_name)
        return data_product.query(filters)

    def add_governance_policy(self, domain_name, policy):
        self.governance.add_policy(domain_name, policy)

    def get_data_with_policies(self, domain_name, product_name):
        domain = self.platform.get_domain(domain_name)
        data_product = domain.get_data_product(product_name)
        return self.governance.enforce_policies(domain_name, data_product.data)

    def get_product_metadata(self, domain_name, product_name):
        return self.catalog.get_product_metadata(domain_name, product_name)

    def list_registered_products(self):
        return self.catalog.list_products()